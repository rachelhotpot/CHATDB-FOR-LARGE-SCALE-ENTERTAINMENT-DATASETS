# CHATDB-FOR-LARGE-SCALE-ENTERTAINMENT-DATASETS
CHATDB FOR LARGE-SCALE ENTERTAINMENT DATASETS

# To access our full dataset, please visit this Drive [Link](https://drive.google.com/drive/folders/1z1rtXkZ8yUWFPUhPlxfFKT2U-K7_RcWU?usp=drive_link). The original dataset can be found on [Kaggle](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset/data?select=genome_scores.csv)

# To install all required libraries and packages
`pip install -r requirements.txt`

# to install MySQL
`brew install mysql`

# to start MySQL Service
`brew services start mysql`

# to install Streamlit
`pip install streamlit`

# to install langchain
`pip install langchain, langchain_community, langchain_openai`

# to install pymysql
`pip install pymysql`


# Upload to MySQL
1. login to MySQL

`mysql -u root -p`

2. Enter password
3. create database

`CREATE DATABASE project551;`

4. Use created database

`USE project551;`

5. Upload dataset

`source dataset.sql`

# Upload to PostGreSQL
1. login to PostGreSQL

`psql -U postgres`

2. create database

`CREATE DATABASE project551;`
   
3. connect to created database

`\c project551`
   
4. Upload dataset

`\i dataset_psql.sql`

# Upload to MongoDB
1. Place your JSON file
Save the JSON file you want to upload to MongoDB in our `CHATDB-FOR-LARGE-SCALE-ENTERTAINMENT-DATASETS` folder
   
2. Edit the script with your MongoDB credentials 
In the `mongo_db.py` file, find the `init_database` function and call it with your MongoDB username, password, and appName

3. Update the file path
In `upload_data_to_mongo` function, update the file path to match the location of your JSON file

4. Run the Upload
Call the `upload_data_to_mongo` function to upload collections to the MongoDB database 

# Start streamlit to interact with our NLI real-time 
`streamlit run app.py`

`streamlit run mongo_db.py`

# Repository Structure 
|--requirements.txt  

|--README.md 

|--code/  

	|--app.py # Used to create NLI and generate queries for MySQL/PostgreSQL
  	|--mongo_db.py  # Used to create NLI and generate queries for MongoDB
	|--dataset.sql   # Used to upload data to MySQL
  	|--dataset_psql.sql  # Used to upload data to PostgreSQL
  
|--reports/

	|--Draft- Group Proposal.pdf 
	|--Mid Progress Report.pdf
	|--551_ Group Proposal Final.pdf
 	|--CHATDB_Final_Report.pdf


# OpenAI API Keys
For privacy and security reasons, we have not attached the API keys used in the Github. 
# However, we have added comments in the code indicating when to use your personal API key to replace the variable OPENAI_API_KEY.
