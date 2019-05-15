from __future__ import unicode_literals, print_function
from pydna import readers
from pydna.assembly import Assembly
from pydna.dseqrecord import Dseqrecord
import warnings
import plotly.graph_objs as go
import sqlite3
from sqlite3 import Error
from flask import request
# Dash configuration
from flask_login import current_user

from server import app

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# function to convert sequence strings into k-mer words, default size = 8 (hexamer words)
def getKmers(sequence, size=4):
    return [sequence[x:x + size].lower() for x in range(len(sequence) - size + 1)]


import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# =============================
# import plac
import random
from pathlib import Path
# import spacy
# from tqdm import tqdm # loading bar
import requests
import bs4
# from spacy import displacy
# output_dir='UntitledFolder'
# nlp2 = spacy.load(output_dir)
import requests
import bs4

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import base64
import json
import plotly
import io
import dash

from datetime import datetime

import flask

import warnings

warnings.filterwarnings('ignore')

# ==================================


warnings.filterwarnings("ignore")

# Create success layout
layout = html.Div(children=[
    dcc.Location(id='url_login_success', refresh=True),
    html.Div(
        className="container",
        children=[
            html.Div(children='', id='validation_p', style={"color": "red"}),
            html.Div(
                className="row",
                children=[
                    html.Div(
                        className="ten columns",
                        children=[
                            html.Br(),
                            html.Div(''),
                        ]
                    ),
                    dcc.Input(
                        className="ten columns",
                        placeholder='Enter patient name',
                        type='text',
                        id='p_name'
                    ),
                ]), html.Div(
                className="row",
                children=[
                    html.Div(
                        className="ten columns",
                        children=[
                            html.Br(),
                            html.Div(''),
                        ]
                    ),
                    dcc.Input(
                        className="ten columns",
                        placeholder='Enter patient phone',
                        type='text',
                        id='phone'
                    ),
                ]),
            html.Div(
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="ten columns",
                            children=[
                                html.Br(),
                                html.Div(''),
                            ]
                        ),
                        html.Div
                            ([
                            html.Div(id='waitfor'),
                            dcc.Upload(
                                id='upload',
                                accept=".fasta",
                                children=html.Div([
                                    html.A('''
                                 Select a DNA '''),
                                    # 'Drag and Drop or'
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                }

                            ),
                            html.Div(id=''),
                            html.Div(children='''
                            A web application framework for detect breast cancer by analyzing the DNA data.
                        '''),

                        ])

                    ]
                )
            )
        ]
    ),
    dcc.Graph(id='my_graph'),

    html.Div(id='display-value')

])


pre_style = {
    'whiteSpace': 'pre-wrap',
    'wordBreak': 'break-all',
    'whiteSpace': 'normal'
}


@app.callback(Output('my_graph', 'figure'),
              [Input('upload', 'filename'),
               Input('upload', 'last_modified'),
               Input('upload', 'contents')
               ], [State('p_name', 'value'),
                   State('phone', 'value')])
def display_content(filename, last_modified, contents, p_name, phone):
    content_type, content_string = contents.split('base64,')
    x = filename
    if not p_name or not phone:
        return "you should enter name and phone"
    ##tt = type(contents)
    ##ttt = str(tt)
    # ttt = tt.
    decoded = base64.b64decode(content_string)
    fastafile = decoded.decode('utf-8')
    sequences = []
    count = 0
    lines = fastafile.split('\n')
    for line in lines:
        count += 1
        if count % 2 == 0:
            seq = line
            sequences.append(seq)

    class1_1 = ''.join(sequences)
    dnadata = [{'sequence': class1_1, 'class': 2}]
    df = pd.DataFrame(dnadata)
    df['words'] = df.apply(lambda x: getKmers(x['sequence']), axis=1)

    df = df.drop('sequence', axis=1)
    df_texts = list(df['words'])
    for item in range(len(df_texts)):
        df_texts[item] = ' '.join(df_texts[item])
    y_h = df.iloc[:, 0].values
    pickled_model, cv = pickle.load(open("tuple_model.pkl", 'rb'))
    X_test = cv.transform(df_texts)
    pred = pickled_model.predict(X_test)
    predresult = pred[0]  ##
    prob1 = pickled_model.predict_log_proba(X_test)
    prob2 = prob1[0]
    values_res = []
    if predresult == 0:
        prob3 = prob2[1]

        prob4 = str(prob3).replace('-', '')
        prob5 = str(prob4).replace('.', '')
        prob6 = '0.' + prob5

        prob7 = float(prob6)
        prob8 = 1 - prob7
        Figure1 = go.Figure(
            data=[go.Pie(labels=['Yes', 'No'],
                         values=[prob8, prob7])],
            layout=go.Layout(
                title='Diagnosis')
        )
        values_res = [prob8, prob7]

    if predresult == 1:
        prob3 = prob2[0]

        prob4 = str(prob3).replace('-', '')
        prob5 = str(prob4).replace('.', '')
        prob6 = '0.' + prob5

        prob7 = float(prob6)
        prob8 = 1 - prob7
        Figure1 = go.Figure(
            data=[go.Pie(labels=['Yes', 'No'],
                         values=[prob7, prob8])],
            layout=go.Layout(
                title='Diagnosis')
        )
        values_res = [prob7, prob8]

    # prob4 = str(prob3).replace('-', '')
    # prob5 = str(prob4).replace('.', '')
    # prob6 = '0.'+prob5

    # prob7 = float(prob6)
    # prob8 = 1-prob7

    # if predresult == 0:
    #    showResult = "Congratulations, our analysis shows that you are not infected with breast cancer."
    # if predresult == 1:
    #    showResult = "Unfortunately our analysis shows that you have breast cancer, please see your doctor as soon as possible."

    # Figure1=  go.Figure(
    #                                         data=[go.Pie(labels=['Yes', 'No'],
    #                                                    values=[prob7, prob8])],
    #                                       layout=go.Layout(
    #                                           title='Diagnosis')
    #
    #                                   )
    conn = sqlite3.connect("patient.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS Presults (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name text NOT NULL,
                                        phone text NOT NULL,
                                        user integer NOT NULL,
                                        predresult integer NOT NULL,
                                        result text NOT NULL
                                    );
              """)

    c.execute(
        f"""INSERT INTO Presults (name,phone ,user,result,predresult)
              VALUES('{p_name}','{phone}',{current_user.id},'{json.dumps(values_res)}',{predresult});"""
          )
    conn.commit()
    conn.close()
    return Figure1


@app.callback(Output('validation_p', 'children'),
              [Input('upload', 'filename'),
               ], [State('p_name', 'value'),
                   State('phone', 'value')])
def validation_p(filename, p_name, phone):
    if (not p_name or not phone) and filename:
        return "you should enter name and phone"
    else:
        return ""


@app.callback(Output('display-value', 'children'),
              [Input('upload', 'filename'),
               Input('upload', 'last_modified'),
               Input('upload', 'contents')])
def display_value(filename, last_modified, contents):
    if contents:
        content_type, content_string = contents.split('base64,')
    else:
        return
    x = filename
    ##tt = type(contents)
    ##ttt = str(tt)
    # ttt = tt.
    decoded = base64.b64decode(content_string)
    fastafile = decoded.decode('utf-8')
    sequences = []
    count = 0
    lines = fastafile.split('\n')
    for line in lines:
        count += 1
        if count % 2 == 0:
            seq = line
            sequences.append(seq)

    class1_1 = ''.join(sequences)
    dnadata = [{'sequence': class1_1, 'class': 2}]
    df = pd.DataFrame(dnadata)
    df['words'] = df.apply(lambda x: getKmers(x['sequence']), axis=1)

    df = df.drop('sequence', axis=1)
    df_texts = list(df['words'])
    for item in range(len(df_texts)):
        df_texts[item] = ' '.join(df_texts[item])
    y_h = df.iloc[:, 0].values

    pickled_model, cv = pickle.load(open("tuple_model.pkl", 'rb'))
    X_test = cv.transform(df_texts)
    pred = pickled_model.predict(X_test)
    predresult = pred[0]  ##
    prob1 = pickled_model.predict_log_proba(X_test)
    prob2 = prob1[0]
    if predresult == 0:
        prob3 = prob2[1]
    if predresult == 1:
        prob3 = prob2[0]

    # prob4 = str(prob3)
    prob4 = str(prob3).replace('-', '')
    prob5 = str(prob4).replace('.', '')
    prob6 = '0.' + prob5

    if predresult == 0:
        showResult = "The analysis shows that the patient has breast cancer, please see your doctor as soon as possible."
    if predresult == 1:
        showResult = "The analysis shows that the patient is not infected with breast cancer."
    return showResult


# Create callbacks
@app.callback(Output('url_login_success', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
