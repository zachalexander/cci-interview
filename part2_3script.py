# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import psycopg2
import pandas as pd


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
    court_df.to_csv(r'answer3a_csv.csv', index=False)
    print('Generated csv for Answer 3A')

def AppearanceDateFilter(csv):
    df_filtered = csv.loc[csv['Court Appearance Status'] == 'Attended']

    for index, row in df_filtered.iterrows():
        if((row['Court Appearance Status'] == 'Attended') and (pd.isnull(row['Court Appearance Attended Date']))):
            row['Court Appearance Attended Date'] = row['Court Appearance Date']
        else:
            pass

    df_filtered.to_csv(r'answer3b_csv.csv', index=False)
    print('Generated csv for Answer 3B!')

##########################
# OUTPUT FOR QUESTION 3A #
##########################

ArrestCount(csv_file)


##########################
# OUTPUT FOR QUESTION 3B #
##########################

AppearanceDateFilter(csv_file)


