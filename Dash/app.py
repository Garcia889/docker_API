import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import io
import base64
import plotly.graph_objects as go
from sklearn import metrics
import plotly.express as px
import kds
import os
import seaborn as sns
from scipy.stats import ks_2samp
import dash_bootstrap_components as dbc

import os
app = dash.Dash(__name__)
datadir="data/"




 

app.layout = html.Div(
    [   html.H4("Result ROC and PR curves in deferents population"),
    html.P("Select population:"),
    dcc.Dropdown(
        id='dropdown',
        options=["Train", "Test","NewObservation"],
        value='Train',
        clearable=False
    ),
    dcc.Graph(id="graph_roc"),
    dcc.Graph(id="graph_ks"),
        html.H4("EDA Train"),
        html.Div(id="call base"),
        html.Button("Get eda Sql base", id="sql"),
        html.Div(id="output-data-upload"),
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
    Output("graph_ks", "figure"), 
    Input('dropdown', "value"))
def train_and_display(pop_name):
    response = requests.get('http://api:8000/clients')
    data = response.json()
    df = pd.read_json(data, orient='records')
    df.columns=['ID','SEX',
        'PAY_2',
        'PAY_4',
        'PAY_5',
        'PAY_6',
        'BILL_AMT1',
        'PAY_AMT2',
        'PAY_AMT4',
        'PAY_AMT5','TARGET_DEFAULT','TYPE_POP','pred1','pred2'] 
    df=df[df['TYPE_POP']==pop_name]

    new_row = pd.DataFrame({'decile':0, 'prob_min':0, 'prob_max':0, 'prob_avg': 0,
                            'cnt_cust':0, 'cnt_resp':0, 'cnt_non_resp':0, 'cnt_resp_rndm':0,
                            'cnt_resp_wiz':0, 'resp_rate':0, 'cum_cust':0, 'cum_resp':0,
                            'cum_resp_wiz':0, 'cum_non_resp':0, 'cum_cust_pct':0,
                            'cum_resp_pct':0, 'cum_resp_pct_wiz':0, 'cum_non_resp_pct':0,
                            'KS':0, 'lift':0}, index =[0]) 

    df_deciles = kds.metrics.report(df.TARGET_DEFAULT.to_numpy(), df.pred2.to_numpy(), labels=False)
    df_deciles = pd.concat([new_row, df_deciles]).reset_index(drop = True)
    
    ks_metric = df_deciles["KS"].max()

    SIZE_MARKER = 7

    fig = go.Figure()

    fig.add_trace(go.Scatter(x = round(df_deciles.decile, 0),
                             y = round(df_deciles.cum_resp_pct, 1),
                             line = dict(color = ('darkorange'), width = 3),
                             showlegend=True,
                             mode='lines+markers',
                             marker=dict(color='darkorange', size=SIZE_MARKER, symbol="circle"),
                             name='Goods'
                             )
                )

    fig.add_trace(go.Scatter(x = round(df_deciles.decile, 0),
                             y = round(df_deciles.cum_non_resp_pct, 1),
                             line = dict(color = ('red'), width = 3),
                             showlegend=True,
                             mode='lines+markers',
                             marker=dict(color='red', size=SIZE_MARKER, symbol="circle"),
                             name='Bads'
                             )
                )
    
    decile_ks = int(df_deciles.loc[df_deciles.KS.idxmax(), ['decile']][0])
    good_ks = float(df_deciles.loc[df_deciles.KS.idxmax(), ['cum_resp_pct']][0])
    bad_ks = float(df_deciles.loc[df_deciles.KS.idxmax(), ['cum_non_resp_pct']][0])    
    
    fig.add_annotation(x=decile_ks, y=good_ks+1.0,
                       text="Máxima distancia",
                       showarrow=True,
                       arrowhead=1,
                       font=dict(color="black", size=15))           
    
    fig.add_trace(go.Scatter(x = [decile_ks, decile_ks],
                             y  = [bad_ks, good_ks],
                             mode='lines',
                             line = dict(color = ('purple'), width = 3, dash = 'dot'),
                             showlegend=False))    
    
    fig.add_trace(go.Scatter(x = [0,10], y  = [0,100],
                             line = dict(color = ('green'), width = 3, dash = 'dot'),
                             showlegend=False))

    fig.update_layout(
        title=f'Goods vs Bads Distance (KS={ks_metric:.4f})',
        xaxis_title='Deciles',
        yaxis_title='Response',
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99, font=dict(size= 11)),
        margin=dict(l=1, r=20, t=30, b=20),
        paper_bgcolor="White"
    )

    return fig

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

        url = 'http://api:8000/check'
        file_post = {'file': open('test.csv', 'rb')}

        response = requests.post(url=url,files=file_post)
        data_graph=df.groupby('SEX').count()['ID'].reset_index()
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            response = requests.get('http://api:8000/download')
            data = response.json()
            
            df1 = pd.read_json(data, orient='records')
            df1.columns=['ID','SEX',
            'PAY_2',
            'PAY_4',
            'PAY_5',
            'PAY_6',
            'BILL_AMT1',
            'PAY_AMT2',
            'PAY_AMT4',
            'PAY_AMT5','pred1','pred2'] 
            df1.loc[df['SEX']==1,'SEX']='Male'
            df1.loc[ df['SEX']==2,'SEX']='Female'

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
                    ,
                    layout=go.Layout(
                    title=go.layout.Title(text="Number of observations per gender Uploaded csv data"))
                )
            ),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Box(
                            x=df1["SEX"],
                            y=df1["pred1"],
                        ),
                    ] ,
                    layout=go.Layout(
                    title=go.layout.Title(text="Box plot predicteds per gender Uploaded csv data"))
                )
            ),
        ]
    )
        


@app.callback( Output("call base", "children"), [Input("sql", "n_clicks")])
def update_output(n_nlicks):

    
        response = requests.get('http://api:8000/clients')
        data = response.json()
        df = pd.read_json(data, orient='records')
        df.columns=['ID','SEX',
        'PAY_2',
        'PAY_4',
        'PAY_5',
        'PAY_6',
        'BILL_AMT1',
        'PAY_AMT2',
        'PAY_AMT4',
        'PAY_AMT5','TARGET_DEFAULT','TYPE_POP','pred1','pred2']
        df.loc[df['SEX']==1,'SEX']='Male'
        df.loc[ df['SEX']==2,'SEX']='Female'

        data_graph=df.groupby('SEX').count()['ID'].reset_index()
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:

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
                    ],
                    layout=go.Layout(
                    title=go.layout.Title(text="Number of observations per gender train data")
                  )
                )
            ),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Box(
                            x=df["SEX"],
                            y=df["pred1"],
                        ),
                    ],
                    layout=go.Layout(
                    title=go.layout.Title(text="Box plot predicteds per gender train data"))
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
    #df1 = pd.read_csv("../API/data/test_pred.csv")
    response = requests.get('http://api:8000/download')
    data = response.json()
    df1 = pd.read_json(data, orient='records')
    df1.columns=['ID','SEX',
        'PAY_2',
        'PAY_4',
        'PAY_5',
        'PAY_6',
        'BILL_AMT1',
        'PAY_AMT2',
        'PAY_AMT4',
        'PAY_AMT5','pred1','pred2']

   
    return dcc.send_data_frame(df1.to_csv, filename="predicted_test.csv")


@app.callback(
    Output("graph_roc", "figure"), 
    Input('dropdown', "value"))
def train_and_display(pop_name):
    response = requests.get('http://api:8000/clients')
    data = response.json()
    df = pd.read_json(data, orient='records')
    df.columns=['ID','SEX',
        'PAY_2',
        'PAY_4',
        'PAY_5',
        'PAY_6',
        'BILL_AMT1',
        'PAY_AMT2',
        'PAY_AMT4',
        'PAY_AMT5','TARGET_DEFAULT','TYPE_POP','pred1','pred2'] 
    df=df[df['TYPE_POP']==pop_name]



    fpr, tpr, thresholds = metrics.roc_curve(df['TARGET_DEFAULT'], df['pred2'])
    score = metrics.auc(fpr, tpr)

    fig = px.area(
        x=fpr, y=tpr,
        title=f'ROC Curve (AUC={score:.4f})',
        labels=dict(
            x='False Positive Rate', 
            y='True Positive Rate'))
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1)

    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port=8050) # configurar host host='0.0.0.0', port=8050

 
