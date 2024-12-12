# pip install mysql-connector-python
# pip install streamlit

import mysql.connector
import pandas as pd
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import google.generativeai as genai

# ********************** CONEXÃO COM O BANCO DE DADOS **********************

app = Flask("registro")    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:525748@127.0.0.1/bd_medidor' #senai%40134

mybd = SQLAlchemy(app)    

def conexao(query):
    conn = mysql.connector.connect(
        host ='127.0.0.1',
        port='3306',
        user='root',
        password='525748', #senai@134
        db='bd_medidor'
              
    )
    
    dataframe = pd.read_sql(query, conn)
    
    conn.close()
    
    return dataframe