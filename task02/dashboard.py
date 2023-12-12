import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np


# Inicializar a aplicação Dash
app = dash.Dash(__name__)

def dados_redis():
    redis_client = redis.Redis(host="192.168.121.66", port=6379, db=0)
    data = redis_client.get("2021031599-proj3-output").decode('utf-8')
    return json.loads(data)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Dashboard de Recursos do Sistema"),
    
    dcc.Graph(id='graph-rede-egresso'),
    dcc.Graph(id='graph-cache-memoria'),
    
    *[
        dcc.Graph(id=f'graph-cpu-{i}') for i in range(16)
    ]
])

# Atualiza os gráficos com os dados da função handler
@app.callback(
    Output('graph-rede-egresso', 'figure'),
    Output('graph-cache-memoria', 'figure'),
    *[
        Output(f'graph-cpu-{i}', 'figure') for i in range(16)
    ],
    Input('interval-component', 'n_intervals')  # Adicione um componente de intervalo para atualizações periódicas
)
def update_graphs(n_intervals):
    # Call your data retrieval function
    dados = dados_redis()

    # Logic to create figures based on data
    figure_rede_egresso = {
        'data': [
            {'x': ['Percent Egress'], 'y': [dados.get('porcentagem-rede-egresso', 0)], 'type': 'bar', 'name': 'Percent Egress'},
        ],
        'layout': {
            'title': 'Porcentagem de Egresso de Rede'
        }
    }

    figure_cache_memoria = {
        'data': [
            {'x': ['Percent Memory Cache'], 'y': [dados.get('porcentagem-cache-memoria', 0)], 'type': 'bar', 'name': 'Percent Memory Cache'},
        ],
        'layout': {
            'title': 'Porcentagem de Cache de Memória'
        }
    }

    figures_cpu = [
        {
            'data': [
                {'x': [f'Média Móvel CPU {i}'], 'y': [dados.get(f'media-movel-cpu{i}', 0)], 'type': 'bar', 'name': f'Média Móvel CPU {i}'},
            ],
            'layout': {
                'title': f'Média Móvel CPU {i}'
            }
        } for i in range(16)
    ]

    return figure_rede_egresso, figure_cache_memoria, *figures_cpu


# Adicione um componente de intervalo para atualizações periódicas
app.layout.children.append(dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0))

# Executa a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
