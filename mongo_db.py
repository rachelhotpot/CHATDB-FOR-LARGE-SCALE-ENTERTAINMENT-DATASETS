from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import streamlit as st

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import csv
import json 
from typing import Dict, Any
import certifi
import re
from bson import ObjectId

OPENAI_API_KEY = "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"


# resources: https://cloud.mongodb.com/v2/67ce728a207f1176e92d7d77#/connect/dsci-551-project?automateSecurity=true
def init_database(user: str, password: str, appName: str):
    db_uri = f"mongodb+srv://{user}:{password}@{appName}.gaj6t5p.mongodb.net/?retryWrites=true&w=majority&appName={appName}"
#     db_uri = f"mongodb+srv://{user}:{password}@{appName}.gaj6t5p.mongodb.net/?appName={appName}"
    # Send a ping to confirm a successful connection
    client = MongoClient(db_uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client['551-project']  
    except Exception as e:
        print(e)
        

# resources: https://www.oneschema.co/blog/import-csv-mongodb
def upload_data_to_mongo(client):
    db = client['551-project']
    collection = db['rating-new']

    # CSV file path
    with open("dataset/json/rating.json", "r") as f:
        data = json.load(f)  # Use json.loads(line) in a loop for newline-delimited files

    # Insert the documents
    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
            
            
# db_uri = "mongodb+srv://riyaberr:cjdOzwkTHXqihuHK@dsci-551-project.gaj6t5p.mongodb.net/?retryWrites=true&w=majority&appName=dsci-551-project"
# client = MongoClient(db_uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
# upload_data_to_mongo(client)

# resources: https://stackoverflow.com/questions/73191050/how-can-i-get-a-mongo-databases-schema-through-python-code  
# def get_mongo_chain(db):
#     template = """
#     You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
#     Based on the table schema below, write a MongoDB query that would answer the user's question. Take the conversation history 
#     into account. You may use any of the available collections: ratings, links. 
    
#     Table schema: {schema}
    
#     Conversation History: {chat_history}
    
#     Write only the MongoDB query and nothing else. Do not wrap the MongoDB query in any other text.
    
#     For example:
#     Question: How many ratings are in the database?
#     MongoDB Query: db.ratings.count()
#     Question: Find top 5 movies with the highest average rating. 
    
#     MongoDB Query: db.ratings.aggregate([
#         {{ "$group": {{
#             "_id": "$movieId",
#             "avg_rating": {{ "$avg": "$rating" }}
#         }} }},
#         {{ "$sort": {{ "avg_rating": -1 }} }},
#         {{ "$limit": 5 }}
#     ])

#     Your turn:
    
#     Question: {question}
#     MongoDB:
#     """
    
#     prompt = ChatPromptTemplate.from_template(template)
    
#     llm = ChatOpenAI(model="gpt-3.5-turbo", api_key = OPENAI_API_KEY)
    
#     def get_schema(_):
#         return db['rating'].find_one()
    
#     return(
#         RunnablePassthrough.assign(schema=get_schema)
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

# "query": [List of valid MongoDB aggregation stages, where each stage is a dictionary with **only one key**]
def get_mongo_chain(db):
    template = """
    You are a data analyst. You are interacting with a user who is asking you questions about the company's database. 
    
    Based on the database schema and user question, generate the appropriate MongoDB query that would answer the user's question 
    and indicate the collection name. Take the conversation history into account. 
    
    Available collections: rating, link, tag, genome_tags, genome_scores, movie.
    
    Respond in this JSON format:
    {{
      "collection": "<collection_name>",
      "operation": "find" | "aggregate" | "insert" | "update" | "delete" | "list_collections" | "get_fields" | "sample_documents",
      "query": <MongoDB query or payload as a Python dict or list>
    }}
    
    ---
    
    General Rules:
    - Use "find" for read-only queries (aggregation or find).
    - Use "aggregate" for grouped analysis, sorting, joining, or metrics (avg, count, sum, top-N).
    - Use "insert" with a single document or "documents" for bulk inserts.
    - Use "update" with {{ filter, update, many }}.
    - Use "delete" with {{ filter, many }}.
    - Do NOT use $insert, $update, or $delete operators in aggregation.
    
    - If the user asks for the list of collections, return:
    {{
      "operation": "list_collections"
    }}
    
    (Do not include a collection key in this case.)

    - If the user wants to see examples from a collection, return:
    {{
      "collection": "<collection_name>",
      "operation": "sample_documents"
    }}
    
    - If the user asks what fields are in a collection, return:
    {{
      "operation": "get_fields",
      "collection": "<collection_name>"
    }}

    ---

    Aggregation guidance:
    - Each pipeline stage must be a **single-key dictionary**. If multiple conditions are required, use multiple stages.
    
    Correct Example: 
    [
      {{ "$match": {{ "genre": "Comedy" }} }},
      {{ "$group": {{ ... }} }},
      {{ "$limit": 5 }}
    ]
    
    INCORRECT example:
    [
      {{ "$match": {{ "genre": "Comedy" }}, "$limit": 5 }} ← DO NOT DO THIS
    ]
    
    - If the query involves filtering or aggregation on a large collection (like rating), include: {{ "$limit": 1000 }}
    early in the pipeline — before $lookup or $group
    - Use $lookup to join across collections. 
    IMPORTANT: Use $lookup only when the user asks for fields that exist in a different collection (e.g., a title from the movie 
    collection). Always place $lookup **after** any $match, $group, or $limit stages to avoid joining unnecessary documents.
    - Use $limit for top-N queries.
    - If userId or movieId filtering is required, include a $match stage early.

    ---

    Schema: {schema}

    Conversation History: {chat_history}
    Question: {question}
    """
    
#     change db.rating.movieId to int instead of string
#     db["rating"].update_many({}, [
#         { "$set": { "movieId": { "$toInt": "$movieId" } } }
#     ])
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

    def get_schema(_):
        return {
            "rating": db["rating"].find_one(),
            "link": db["link"].find_one(),
            "genome_scores": db["genome_scores"].find_one(),
            "tag": db["tag"].find_one(),
            "genome_tags": db["genome_tags"].find_one(),
            "movie": db["movie"].find_one()
        }
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
        | (lambda x: json.loads(x))
    )
    
def fix_pipeline(pipeline):
    fixed = []
    for stage in pipeline:
        if isinstance(stage, dict):
            # If it's a multi-key stage (illegal), split into separate single-key stages
            if len(stage) > 1:
                for k, v in stage.items():
                    fixed.append({k: v})
            else:
                key = list(stage.keys())[0]
                # If it's not a stage operator like $match, $group, $sort — wrap in $match
                if not key.startswith("$"):
                    fixed.append({"$match": stage})
                else:
                    fixed.append(stage)
        else:
            fixed.append(stage)
    return fixed


def get_response(user_query: str, db: MongoClient, chat_history: list):
    mongo_chain = get_mongo_chain(db)

    llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

    response_template = """
    You are a helpful MongoDB assistant at a company. You are interacting with a user who is asking you questions about the 
    company's database.
    
    Based on the schema, question, MongoDB query, and MongoDB response, write a natural language answer for the user.

    <SCHEMA>{schema}</SCHEMA>
    Conversation History: {chat_history}
    MongoDB Query: <MongoDB>{query}</MongoDB>
    User Question: {question}
    MongoDB Response: {response}
    """

    prompt = ChatPromptTemplate.from_template(response_template)
    
    if "schema" not in st.session_state:
        st.warning("Please connect to the database first.")
        st.stop()

    # 1. Get Mongo query + collection name
    mongo_output = mongo_chain.invoke({
        "question": user_query,
        "chat_history": chat_history
    })

    collection_name = mongo_output.get("collection")
    operation = mongo_output.get("operation", "find")
    query = mongo_output.get("query", {})
    

    # 2. Execute MongoDB query
    if operation == "insert":
        result = db[collection_name].insert_one(query)
        mongo_response = { "inserted_id": str(result.inserted_id) }
        
    elif operation == "update":
        filter_ = query["filter"]
        update_ = query["update"]
        result = db[collection_name].update_many(filter_, update_)
        mongo_response = {
            "matched": result.matched_count,
            "modified": result.modified_count
        }
        
    elif operation == "delete":
        result = db[collection_name].delete_many(query)
        mongo_response = { "deleted": result.deleted_count }
    elif operation == "list_collections":
        mongo_response = db.list_collection_names()
    elif operation == "sample_documents":
        mongo_response = list(db[collection_name].find().limit(5))
    elif operation == "get_fields":
        sample = db[collection_name].find_one()
        mongo_response = list(sample.keys()) if sample else []
    else: 
        print("Generated pipeline (before fix):", query)
        pipeline = query if isinstance(query, list) else [query]
        pipeline = fix_pipeline(pipeline)
        print("Fixed pipeline:", pipeline)
        mongo_response = list(db[collection_name].aggregate(pipeline, maxTimeMS=300000))

    # 3. Natural language generation
    chain = (
        RunnablePassthrough.assign(
            schema=lambda _: {
                "rating": db["rating"].find_one(),
                "link": db["link"].find_one(),
                "genome_scores": db["genome_scores"].find_one(),
                "tag": db["tag"].find_one(),
                "genome_tags": db["genome_tags"].find_one(),
                "movie": db["movie"].find_one()
            },
            query=lambda _: query,
            response=lambda _: mongo_response
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history
    })


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm an AI Assistant, Ask me anything about your database."),
    ]
    
if "schema" not in st.session_state:
    st.session_state.schema = None 

load_dotenv()

st.set_page_config(page_title="Chat with our ChatDB", page_icon=":speech_balloon")
st.title("Chat with our ChatDB")

with st.sidebar:
    st.subheader("Settings")
    st.write("Connect with MongoDB. Connect to the database and start chatting")
    
    st.text_input("User", value="riyaberr", key="User")
    st.text_input("Password", type="password", value="cjdOzwkTHXqihuHK", key="Password")
    st.text_input("AppName", value="dsci-551-project", key="AppName")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["AppName"]
            )
            
#             # ✅ Store schema ONCE
#             st.session_state.schema = {
#                 "rating": db["rating"].find_one(),
#                 "link": db["link"].find_one(),
#                 "genome_scores": db["genome_scores"].find_one(),
#                 "tag": db["tag"].find_one(),
#                 "genome_tags": db["genome_tags"].find_one(),
#                 "movie": db["movie"].find_one()
#             }


            st.session_state.db = db
            st.success("Connected to database!")
    

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        response =  get_response(user_query, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)
        
    st.session_state.chat_history.append(AIMessage(content=response))