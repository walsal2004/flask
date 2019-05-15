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

layout_doctor = html.Div(

    children=[
        html.Div(
            className="container",
            style={
                "display": "grid"
            },
            children=[
                html.Button(
                    children=[html.A('prediction', href='/success')],
                    n_clicks=0,
                    type='button',
                    style={
                        "margin-top":"10px"
                    }
                ),
                html.Button(
                    children=[html.A('search', href='/search')],
                    n_clicks=0,
                    type='button',
                    style={
                        "margin-top":"10px"
                    }
                )
            ])
    ]
)

# Create success layout
layout = html.Div(children=[
dcc.Location(id='url_login_success', refresh=True),
    html.Label("phone"),
    dcc.Input(placeholder='Enter your PHONE  NUMBER',
               type='text',
                id='SEARCH-PHONE',
              style={
                  "width":"50%"
              }),
    html.Button(
        children='search',
        n_clicks=0,
        type='submit',
        id='search-btn'
    ),
    dcc.Graph(id='my_graph_s'),
    html.Div(id='display-value_s')
])

pre_style = {
    'whiteSpace': 'pre-wrap',
    'wordBreak': 'break-all',
    'whiteSpace': 'normal'
}

@app.callback(Output('my_graph_s', 'figure'),
              [Input('search-btn', 'n_clicks')],
              [State('SEARCH-PHONE', 'value')])
def search(n_clicks, search_text):

    conn = sqlite3.connect("patient.db")
    c = conn.cursor()
    c.execute(
        f"""select result, name from Presults where phone = '{search_text}';"""
    )
    rr = c.fetchall()
    conn.close()
    try:
        values = json.loads(rr[0][0])
        Figure1 = go.Figure(
            data=[go.Pie(labels=['Yes', 'No'],
                         values=values)],
            layout=go.Layout(
                title=f'Diagnosis for mr/ms {rr[0][1]}')
        )
    except IndexError:
        Figure1 = go.Figure(
            data=[go.Pie(
                         values=[0])],
            layout=go.Layout(
                title='no search found')
        )
    return Figure1


@app.callback(Output('display-value_s', 'children'),
              [Input('search-btn', 'n_clicks')],
              [State('SEARCH-PHONE', 'value')])
def display_value_s(n_clicks, search_text):

    conn = sqlite3.connect("patient.db")
    c = conn.cursor()
    c.execute(
        f"""select predresult from Presults where phone = '{search_text}';"""
    )
    rr = c.fetchall()
    conn.close()
    try:
        predresult = (rr[0][0])
        print(predresult)
        if predresult == 0:
            showResult = "The analysis shows that the patient is not infected with breast cancer."
        if predresult == 1:
            showResult = "The analysis shows that the patient has breast cancer, please see your doctor as soon as possible."
        print(showResult)
        return showResult
    except IndexError:
        return ""

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
