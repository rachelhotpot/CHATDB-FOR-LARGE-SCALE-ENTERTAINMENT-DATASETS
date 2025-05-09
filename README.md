# CHATDB-FOR-LARGE-SCALE-ENTERTAINMENT-DATASETS
CHATDB FOR LARGE-SCALE ENTERTAINMENT DATASETS

# To access our full dataset, please visit this Drive [Link](https://drive.google.com/drive/folders/1z1rtXkZ8yUWFPUhPlxfFKT2U-K7_RcWU?usp=drive_link)

# to install MySQL
brew install mysql

# to start MySQL Service
brew services start mysql

# to install Streamlit
pip install streamlit

# to install langchain
pip install langchain, langchain_community, langchain_openai

# to install pymysql
pip install pymysql


# Upload to MySQL
1. login to MySQL
  mysql -u root -p
2. Enter password
3. create database
   CREATE DATABASE project551;
4. Use created database
   USE project551;
5. Upload dataset
   source dataset.sql

# Upload to PostGreSQL
1. login to PostGreSQL
  psql -U postgres
2. create database
   CREATE DATABASE project551;
3. connect to created database
   \c project551
4. Upload dataset
5. \i dataset_psql.sql

# Start streamlit
streamlit run app.py
streamlit run mongo_db.py


