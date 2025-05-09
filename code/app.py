from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import streamlit as st
db = SQLDatabase.from_uri("mysql+pymysql://root:@localhost/chatdb")
import os


# Dynamic database initialization
def init_database(db_type: str, user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    if db_type == "MySQL":
        db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    elif db_type == "PostgreSQL":
        db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError("Unsupported database type selected.")
    return SQLDatabase.from_uri(db_uri)

# SQL chain for query generation
def get_sql_chain(db, db_type):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a {db_type} SQL query that would answer the user's question. Take the conversation history into account.
    
    Always qualify columns with the table name when using JOINs to avoid ambiguity. For example, use 'movie.movieId' instead of just 'movieId'.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

    Your turn:

    Question: {question}
    SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-3.5-turbo",
                api_key="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"     )
    
    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema, db_type=lambda _: db_type)
        | prompt
        | llm
        | StrOutputParser()
    )


# Query → SQL → Run → Natural Language response
def get_response(user_query: str, db: SQLDatabase, chat_history: list, db_type: str):
    sql_chain = get_sql_chain(db, db_type)
    
    template ="""
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, sql query, and sql response, write a natural language response.
        <SCHEMA>{schema}</SCHEMA>
        
        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        User Question: {question}
        SQL Response: {response}
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

# Initial Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm an AI Assistant, Ask me anything about your database."),
    ]

load_dotenv()

st.set_page_config(page_title="Chat with our ChatDB", page_icon=":speech_balloon")
st.title("Chat with our ChatDB")

# Sidebar Settings
with st.sidebar:
    st.subheader("Settings")
    st.write("Choose your database and connect to start chatting.")
    
    db_type = st.selectbox("Database Type", ["MySQL", "PostgreSQL"])
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306" if db_type == "MySQL" else "5432", key="Port")
    st.text_input("User", value="root" if db_type == "MySQL" else "kevinbui", key="User")
    st.text_input("Password", type="password", value="Dsci-551-Group-62" if db_type == "MySQL" else "", key="Password")
    st.text_input("Database", value="551Project" if db_type == "MySQL" else "project551", key="Database")
    
    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            try:
                db = init_database(
                    db_type,
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")
            except Exception as e:
                st.error(f"Failed to connect: {e}")

# Chat Interface
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
        response = get_response(user_query, st.session_state.db, st.session_state.chat_history, db_type)
        st.markdown(response)
        
    st.session_state.chat_history.append(AIMessage(content=response))
