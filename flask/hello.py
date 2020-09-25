from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import pandas as pd

conn = psycopg2.connect(
    database="courtdata",
    user="postgres",
    password="Biology512",
    host="localhost",
    port=5432
)

# Reading in local csv file of court data
csv_file = pd.read_csv('dataset.csv')

#########################
# FUNCTION DECLARATIONS #
#########################

def ArrestCount(csv):
    court_df = pd.DataFrame(csv)
    court_df = court_df.groupby('State Identifier')['Case Number'].nunique().reset_index()
    court_df = court_df.rename(columns={"Case Number": "Number of Arrests", "State Identifier": "State ID"})
    court_df.to_csv(r'C:/Users/zalexander/Desktop/answer3a_csv.csv', index=False)

def AppearanceDateFilter(csv):
    df_filtered = csv.loc[csv['Court Appearance Status'] == 'Attended']

    for index, row in df_filtered.iterrows():
        if((row['Court Appearance Status'] == 'Attended') and (pd.isnull(row['Court Appearance Attended Date']))):
            row['Court Appearance Attended Date'] = row['Court Appearance Date']
        else:
            pass

    df_filtered.to_csv(r'C:/Users/zalexander/Desktop/answer3b_csv.csv', index=False)


# SYNTAX FOR QUESTION 3A

data_df = pd.read_sql_query('SELECT * FROM "Fulldata"', con=conn)
answer3a = pd.DataFrame(data_df.groupby('StateID')['CaseNumber'].nunique()).reset_index()
answer3a = answer3a.rename(columns={"CaseNumber": "Number of Arrests", "StateID": "State ID"})
print(answer3a)
answer3a.to_csv(r'C:/Users/zalexander/Desktop/answer3a.csv', index=False)

# SYNTAX FOR QUESTION 3B
df_filtered = data_df.loc[data_df['CourtAppearanceStatus'] == 'Attended']

for index, row in df_filtered.iterrows():
    if((row['CourtAppearanceStatus'] == 'Attended') and (row['CourtAppearanceAttendedDate'] == None)):
        row['CourtAppearanceAttendedDate'] = row['CourtAppearanceDate']
    else:
        pass

# print(df_filtered)

df_filtered.to_csv(r'C:/Users/zalexander/Desktop/answer3b.csv', index=False)



# CSV File work
ArrestCount(csv_file)
AppearanceDateFilter(csv_file)

# , jsonify, make_response, render_template, request, flash, redirect, session, url_for, Response;
# from flask_cors import CORS, cross_origin;
# import requests;
# from markupsafe import escape;
# from sqlalchemy import event, create_engine, inspect, DDL
# from random import seed, random
# import uuid
# from uuid import uuid1
# import xmltodict
# import urllib.request as urllib2
# from urllib.parse import quote
# import json
# import os
# from dotenv import load_dotenv

# load_dotenv()


# CORS(app)
# ENV = 'prod'

# LOCAL_DB_URL = os.getenv("LOCAL_DB_URL")
# REMOTE_DB_URL = os.getenv("REMOTE_DB_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")

# # Setting database configs
# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB_URL
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = REMOTE_DB_URL

# app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SECRET_KEY'] = SECRET_KEY

# db = SQLAlchemy(app)



################################
# Building routes for the site #
################################

app = Flask(__name__)
# Home page
@app.route('/')
def hello_world():
    return 'Hello, World!'