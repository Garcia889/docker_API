#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 11:40:25 2023

@author: delia.cardenas
"""

import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import joblib
from dash import dcc
from dash import html

import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
import pandas as pd

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

# https://stackoverflow.com/questions/50867470/print-output-based-on-user-input-in-dash-or-shiny
# https://stackoverflow.com/questions/62097062/uploading-a-csv-to-plotly-dash-and-rendering-a-bar-plot-based-on-a-pandas-datafr
app = dash.Dash()


app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "30%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-data-upload"),
        html.Button("Download csv", id="btn"),
        dcc.Download(id="download"),
    ]
)


def get_predicted(data):
    ##loading the model from the saved file

    model = joblib.load("estimator_hyper_xgb.joblib")
    pred = model.predict_proba(
        data
    )  # aqui le pueden poner una muestra de la base de kaggle
    return pred


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

            df[["predicted_0", "predicted_0"]] = get_predicted(df)
            df.to_csv("predicted.csv")
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return html.Div(
        [
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=pd.unique(df["SEX"]),
                            y=df["BILL_AMT2"],
                            textposition="auto",
                        ),
                    ]
                )
            ),
        ]
    )


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("upload-data", "last_modified")],
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def generate_csv(n_nlicks):
    df1 = pd.read_csv("predicted.csv")
    return dcc.send_data_frame(df1.to_csv, filename="predicciones.csv")


if __name__ == "__main__":
    app.run_server(debug=True, port=3004)
