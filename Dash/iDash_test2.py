import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import io
import base64
import plotly.graph_objects as go

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

datadir="data/"

import os
dir="../API/data"
## If folder doesn't exists, create it ##
if not os.path.isdir(dir):
    os.mkdir(dir)

# Diseño de la interfaz gráfica
#app.layout = html.Div(
#    style={'textAlign': 'center', 'marginTop': '20%'},
#    children=[
#        html.Label('Ingrese su nombre:'),
#        dcc.Input(id='input-box', type='text', value='', style={'marginBottom': '10px'}),
#        html.Button('Saludar', id='button', n_clicks=0, style={'marginBottom': '10px'}),
#        html.Div(id='output-container', children=[]),
#    ]
#)


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

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

            
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])
    return df

# Definir la función de callback



@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("upload-data", "last_modified")],
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        eventlog_data = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]

        df =eventlog_data[0]
        df.to_csv('test.csv')

        url = 'http://127.0.0.1:8000/check'
        file_post = {'file': open('test.csv', 'rb')}

        response = requests.post(url=url,files=file_post)
        data_graph=df.groupby('SEX').count()['ID'].reset_index()
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            df1 = pd.read_csv("../API/data/test_pred.csv")

            return html.Div(
        [
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=data_graph["SEX"],
                            y=data_graph["ID"],
                            textposition="auto",
                        ),
                    ]
                )
            ),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Box(
                            x=df1["SEX"],
                            y=df1["pred1"],
                        ),
                    ]
                )
            ),
        ]
    )
        


    


        #f'Respuesta del servidor: {response.text}'
                   
        


        else:
            return f'Error en la solicitud al servidor (código {response.status_code})'
        return file


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def generate_csv(n_nlicks):
    df1 = pd.read_csv("../API/data/test_pred.csv")

   
    return dcc.send_data_frame(df1.to_csv, filename="predicted_test.csv")


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
