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

db_uri = "mongodb+srv://riyaberr:cjdOzwkTHXqihuHK@dsci-551-project.gaj6t5p.mongodb.net/?appName=dsci-551-project"
client = MongoClient(db_uri, server_api=ServerApi('1'))

schema = '''
"Title": "String",
  "Premiere": "String",
  "Watchtime": "String",
  "is_tv_show": "String",
  "Genres": [
    "Genre_Action": "String",
    "Genre_Adventure": "String",
    "Genre_Animation": "String",
    "Genre_Biography": "String",
    ...
    "Genre_Western": "String"
  ]
'''

# resources: https://cloud.mongodb.com/v2/67ce728a207f1176e92d7d77#/connect/dsci-551-project?automateSecurity=true
def init_database():
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        

# resources: https://www.oneschema.co/blog/import-csv-mongodb
def upload_data_to_mongo(client):
    db = client['551-project']
    collection = db['most-watched-tv-shows']

    # CSV file path
    csv_file_path = 'dataset/most_watched_movies_tv_cleaned.csv'
    with open(csv_file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            collection.insert_one(row)

            
# resources: https://stackoverflow.com/questions/73191050/how-can-i-get-a-mongo-databases-schema-through-python-code  
def get_mongo_chain(db, collection):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    Table schema: """ +  schema """
    
    Conversation History: {chat_history}
    
    Write only the MongoDB query and nothing else. Do not wrap the MongoDB query in any other text.
    
    For example:
    Question: How many users are in the database?
    MongoDB Query: db.users.count()
    Question: Find Users with the family name Smith
    SQL Query: db.users.find({"name.family": "Smith"})
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    return(
        RunnablePassthrough.assign(schema=schema)
        | prompt
        | llm
        | StrOutputParser()
    )
    
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    mongo_chain = get_mongo_chain(db, collection)
    
    template ="""
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, MongoDB query, and MongoDB response, write a natural language response.
        <SCHEMA>{schema}</SCHEMA>
        
        Conversation History: {chat_history}
        MongoDB Query: <MongoDB>{query}</MongoDB>
        User Question: {question}
        MongoDB Response: {response}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = [
#         AIMessage(content="Hello! I'm an AI Assistant, Ask me anything about your database."),
#     ]

# load_dotenv()

# st.set_page_config(page_title="Chat with our ChatDB", page_icon=":speech_balloon")

# st.title("Chat with our ChatDB")

# with st.sidebar:
#     st.subheader("Settings")
#     st.write("Connect with MySQL. Connect to the database and start chatting")
    
#     st.text_input("Host", value="localhost", key="Host")
#     st.text_input("Port", value="3306", key="Port")
#     st.text_input("User", value="root", key="User")
#     st.text_input("Password", type="password", value="Dsci-551-Group-62", key="Password")
#     st.text_input("Database", value="world", key="Database")
    
#     if st.button("Connect"):
#         with st.spinner("Connecting to database..."):
#             db = init_database(
#                 st.session_state["User"],
#                 st.session_state["Password"],
#                 st.session_state["Host"],
#                 st.session_state["Port"],
#                 st.session_state["Database"]
#             )
#             st.session_state.db = db
#             st.success("Connected to database!")
    

# for message in st.session_state.chat_history:
#     if isinstance(message, AIMessage):
#         with st.chat_message("AI"):
#             st.markdown(message.content)
#     elif isinstance(message, HumanMessage):
#         with st.chat_message("Human"):
#             st.markdown(message.content)

# user_query = st.chat_input("Type a message...")
# if user_query is not None and user_query.strip() != "":
#     st.session_state.chat_history.append(HumanMessage(content=user_query))
    
#     with st.chat_message("Human"):
#         st.markdown(user_query)
        
#     with st.chat_message("AI"):
#         response =  get_response(user_query, st.session_state.db, st.session_state.chat_history)
#         st.markdown(response)
        
#     st.session_state.chat_history.append(AIMessage(content=response))