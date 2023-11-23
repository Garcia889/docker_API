import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import requests

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la interfaz gráfica
app.layout = html.Div(
    style={'textAlign': 'center', 'marginTop': '20%'},
    children=[
        html.Label('Ingrese su nombre:'),
        dcc.Input(id='input-box', type='text', value='', style={'marginBottom': '10px'}),
        html.Button('Saludar', id='button', n_clicks=0, style={'marginBottom': '10px'}),
        html.Div(id='output-container', children=[]),
    ]
)

# Definir la función de callback
@app.callback(
    Output('output-container', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_output(n_clicks, input_value):
    if n_clicks > 0:
        # Hacer la solicitud HTTP
        url = f'http://localhost:8000/todos/{input_value}'
        response = requests.get(url)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            return f'Respuesta del servidor: {response.text}'
        else:
            return f'Error en la solicitud al servidor (código {response.status_code})'

    return ''


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
