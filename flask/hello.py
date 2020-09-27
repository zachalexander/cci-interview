from flask import Flask, jsonify, make_response, render_template, request, flash, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


LOCAL_DB_URL = os.getenv("LOCAL_DB_URL")
result = urlparse(LOCAL_DB_URL)

user = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

load_dotenv()
app = Flask(__name__)

ENV = 'dev'

conn = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=hostname,
    port=5432
)


# Setting database configs
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB_URL

db = SQLAlchemy(app)

# Building ratings model
class Client(db.Model):
    __tablename__ = 'Client'
    ClientID = db.Column(db.Integer, primary_key=True)
    StateID = db.Column(db.String(200))
    FirstName = db.Column(db.String(200))
    LastName = db.Column(db.String(200))
    DateOfBirth = db.Column(db.Date)

    def __init__(self, StateID, FirstName, LastName, DateOfBirth):
        self.StateID = StateID
        self.FirstName = FirstName
        self.LastName = LastName
        self.DateOfBirth = DateOfBirth


class Case(db.Model):
    __tablename__ = 'Case'
    CaseID = db.Column(db.Integer, primary_key=True)
    CaseNumber = db.Column(db.String(200))
    ClientID = db.Column(db.Integer)
    ArrestDate = db.Column(db.Date)
    ChargeID = db.Column(db.Integer)
    ArraignmentDate = db.Column(db.Date)

    
    def __init__(self, CaseNumber, ClientID, ArrestDate, ChargeID, ArraignmentDate):
        self.CaseNumber = CaseNumber
        self.ClientID = ClientID
        self.ArrestDate = ArrestDate
        self.ChargeID = ChargeID
        self.ArraignmentDate = ArraignmentDate

class Charge(db.Model):
    __tablename__ = 'Charge'
    ChargeID = db.Column(db.Integer, primary_key=True)
    ChargeCode = db.Column(db.String(200))

    def __init__(self, ChargeCode):
        self.ChargeCode = ChargeCode

class Judge(db.Model):
    __tablename__ = 'Judge'
    JudgeID = db.Column(db.Integer, primary_key=True)
    JudgeName = db.Column(db.String(200))

    def __init__(self, JudgeName):
        self.JudgeName = JudgeName

class Appearance(db.Model):
    __tablename__ = 'Appearance'
    AppearanceID = db.Column(db.Integer, primary_key=True)
    AppearanceDate = db.Column(db.Date)
    JudgeID = db.Column(db.Integer)
    AttendanceStatusID = db.Column(db.Integer)
    CaseID = db.Column(db.Integer)
    AppearanceAttendedDate = db.Column(db.Date)

    def __init__(self, AppearanceDate, JudgeID, AttendanceStatusID, CaseID, AppearanceAttendedDate):
        self.AppearanceDate = AppearanceDate
        self.JudgeID = JudgeID
        self.AttendanceStatusID = AttendanceStatusID
        self.CaseID = CaseID
        self.AppearanceAttendedDate = AppearanceAttendedDate

class AttendanceStatus(db.Model):
    __tablename__ = 'AttendanceStatus'
    AttendanceStatusID = db.Column(db.Integer, primary_key=True)
    AttendanceStatusType = db.Column(db.String(200))

    def __init__(self, AttendanceStatusType):
        self.AttendanceStatusType = AttendanceStatusType


# Home page
@app.route('/',  methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        courtdata = db.session.query(Client, Case, Appearance).filter(Client.ClientID == Case.ClientID,).filter(Case.CaseID == Appearance.CaseID,).all()
        return render_template('homepage.html', data=courtdata)
    else: 
        return render_template('homepage.html')


@app.route("/get3acsv")
def get3aCSV():
    data_df = pd.read_sql_query('SELECT * FROM "Fulldata"', con=conn)
    answer3a = pd.DataFrame(data_df.groupby('StateID')['CaseNumber'].nunique()).reset_index()
    answer3a = answer3a.rename(columns={"CaseNumber": "Number of Arrests", "StateID": "State ID"})
    return Response(
        answer3a.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=answer3a.csv"})

@app.route("/get3bcsv")
def get3bCSV():
    data_df = pd.read_sql_query('SELECT * FROM "Fulldata"', con=conn)
    df_filtered = data_df.loc[data_df['CourtAppearanceStatus'] == 'Attended']

    for index, row in df_filtered.iterrows():
        if((row['CourtAppearanceStatus'] == 'Attended') and (row['CourtAppearanceAttendedDate'] == None)):
            row['CourtAppearanceAttendedDate'] = row['CourtAppearanceDate']
        else:
            pass

    return Response(
        df_filtered.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=answer3b.csv"})

@app.route("/getscript")
def getScript():
    sqlscript = open("courtdata.txt")
    return Response(
        sqlscript,
        mimetype="text",
        headers={"Content-disposition": "attachment; filename=sqlscript.txt"})

if __name__ == '__main__':
    app.run()