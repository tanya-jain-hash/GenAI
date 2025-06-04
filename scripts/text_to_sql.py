import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine

from langchain_experimental.sql import SQLDatabaseChain
from langgraph.graph import MessagesState
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

db_engine = create_engine("sqlite:///logistics.db")
load_dotenv()

path = ""

def csv_to_sqlite_pandas(csv_file, db_file, table_name):
    conn = sqlite3.connect(db_file)
    df = pd.read_csv(csv_file)
    df.dropna(inplace=True)
    print(df.head())
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

# for file in os.listdir(path):
#     try:
#         csv_to_sqlite_pandas(os.path.join(path,file), "logistics.db",str(file).replace(".csv",""))
#     except:
#         pass


openai_key = os.getenv("OPENAI_API_KEY")

# llm = OpenAI(model="gpt-4o-mini", api_key=openai_key)
llm = ChatOllama(
    model="BahaSlama/llama3.1-finetuned:latest",
    temperature=0)

prompt_template = """
ROLE: Expert Database Manager
You are an expert database manager who is skilled in generating SQLlite queries to query a database logistics.db.

Database:
The database logistics.db contains 4 tables:
1. Customer:
This table contains information about the customer. It contains the following attributes:
- C_ID: customer_id
- C_NAME: customer name
- C_EMAIL_ID: customer email id
- C_TYPE: customer type (Wholesale, retail, internal goods)
- C_ADDR: customer address
- C_CONT_NO: customer container number
- M_ID: memebership id

2. Payment_Details:
This table contains information about the payment of the shipment of each customer. It contains the following attributes:
- Payment_ID: payment id
- AMOUNT: amount paid by the customer C_ID for the shipment SH_ID
- Payment_Status: Paid or not paid
- Payment_Mode: COD or Card payment
- Payment_date: Date the payment was made
- SH_ID: shipment_id
- C_ID: customer id

3. Shipment_Details:
This table contains information the shipment deatils. It contains the following attributes:
- SH_ID: shipment_id
- SH_CONTENT: shipment content (home furninshing, luggage, healthcare and more)
- SH_DOMAIN: one of domestic or international
- SER_TYPE: Express or regular
- SH_WEIGHT: shipment weight
- SH_CHARGES: shipment charges
- SH_ADDR: shipment address
- DS_ADDR: shipment destination address
- C_ID: customer id for the shipment id

4. Status:
This table contains the status of the shipment. It contains the following attributes:
- SH_ID: shipment_id
- Current_status: status of the shipment (delivered or not delivered)
- Sent_date: date the shipment was sent 
- Delivery_date: date the shipment reached the destination

GOAL:
Your task is to generate a sql query based on the user's need to query the database and get the relevant data.

example 1:
user query: Provide the status of the shipment_id 123
SQL query: SELECT status from status where SH_ID is 123

example 2:
user 

User_query:
{query}

SQL Query:
"""

prompt = PromptTemplate.from_template("prompt_template")

chain = prompt | llm | StrOutputParser()
print(chain.invoke({"query":"return top 5 rows of the customer table"}))


# sql_chain = SQLDatabaseChain.from_llm(llm, db=SQLDatabase(db_engine),  return_sql=True, return_direct=True)
# response = sql_chain.invoke("return top 5 customers")





