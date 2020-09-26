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

##########################
# OUTPUT FOR QUESTION 2 #
##########################
csv_file = pd.read_csv('dataset.csv')
print(csv_file)


#########################
# FUNCTION DECLARATIONS #
#########################

def ArrestCount(csv):
    court_df = pd.DataFrame(csv)
    court_df = court_df.groupby('State Identifier')['Case Number'].nunique().reset_index()
    court_df = court_df.rename(columns={"Case Number": "Number of Arrests", "State Identifier": "State ID"})
    court_df.to_csv(r'C:/Users/zalexander/Desktop/answer3a_csv.csv', index=False)
    print('Generated csv for Answer 3A')

def AppearanceDateFilter(csv):
    df_filtered = csv.loc[csv['Court Appearance Status'] == 'Attended']

    for index, row in df_filtered.iterrows():
        if((row['Court Appearance Status'] == 'Attended') and (pd.isnull(row['Court Appearance Attended Date']))):
            row['Court Appearance Attended Date'] = row['Court Appearance Date']
        else:
            pass

    df_filtered.to_csv(r'C:/Users/zalexander/Desktop/answer3b_csv.csv', index=False)
    print('Generated csv for Answer 3B!')

##########################
# OUTPUT FOR QUESTION 3A #
##########################

ArrestCount(csv_file)


##########################
# OUTPUT FOR QUESTION 3B #
##########################

AppearanceDateFilter(csv_file)


############################
# EXTENDING BOTH QUESTIONS #
############################


# READING IN DATA FROM POSTGRESQL DATABASE AND SAVING OUTPUT

# SYNTAX FOR QUESTION 3A
data_df = pd.read_sql_query('SELECT * FROM "Fulldata"', con=conn)
answer3a = pd.DataFrame(data_df.groupby('StateID')['CaseNumber'].nunique()).reset_index()
answer3a = answer3a.rename(columns={"CaseNumber": "Number of Arrests", "StateID": "State ID"})
answer3a.to_csv(r'C:/Users/zalexander/Desktop/answer3a.csv', index=False)
print('Generated csv for Answer 3A - from database!')

# SYNTAX FOR QUESTION 3B
df_filtered = data_df.loc[data_df['CourtAppearanceStatus'] == 'Attended']

for index, row in df_filtered.iterrows():
    if((row['CourtAppearanceStatus'] == 'Attended') and (row['CourtAppearanceAttendedDate'] == None)):
        row['CourtAppearanceAttendedDate'] = row['CourtAppearanceDate']
    else:
        pass

df_filtered.to_csv(r'C:/Users/zalexander/Desktop/answer3b.csv', index=False)
print('Generated csv for Answer 3B - from database!')

################################
# Building routes for the site #
################################

app = Flask(__name__)
# Home page
@app.route('/')
def hello_world():
    return 'Hello, World!'