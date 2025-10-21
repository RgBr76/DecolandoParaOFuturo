from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import graficos_aviacao, formulario_aviacao, analises_avancadas

# Configuração da navegação com base na AZUL airlines 
navegacao = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/graficos", className="nav-link-custom")),
        dbc.NavItem(dbc.NavLink("Previsão de Falhas", href="/formulario", className="nav-link-custom")),
        dbc.NavItem(dbc.NavLink("Análises", href="/analises", className="nav-link-custom")),
    ],
    brand="Sistema de Gestão de Aviação",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4",
    style={"boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}
)

# Página inicial
pagina_inicial = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Bem-vindo ao Sistema de Gestão de Aviação", 
                    className="display-4 text-center mb-4 text-dark"),
                html.P("Sistema completo para análise e previsão de falhas em aeronaves",
                    className="lead text-center text-muted mb-5"),
                
                dbc.CardGroup([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("📊", className="text-center mb-3"),
                            html.H4("Dashboard Analítico", className="card-title text-center"),
                            html.P("Visualize estatísticas, tendências e insights sobre a frota de aeronaves", 
                                className="card-text"),
                            dbc.Button("Acessar Dashboard", href="/graficos", color="primary", 
                                    className="mt-3 w-100")
                        ])
                    ], className="m-2"),
                    
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("🛠️", className="text-center mb-3"),
                            html.H4("Previsão de Falhas", className="card-title text-center"),
                            html.P("Preveja riscos de falha baseado nas características da aeronave", 
                                className="card-text"),
                            dbc.Button("Fazer Previsão", href="/formulario", color="danger", 
                                    className="mt-3 w-100")
                        ])
                    ], className="m-2"),
                    
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("📈", className="text-center mb-3"),
                            html.H4("Relatórios Avançados", className="card-title text-center"),
                            html.P("Análises detalhadas e relatórios técnicos da operação", 
                                className="card-text"),
                            dbc.Button("Ver Análises", href="/analises", color="info", 
                                    className="mt-3 w-100")
                        ])
                    ], className="m-2"),
                ], className="mb-5"),
                
                html.Hr(className="my-5"),
                
                # Estatísticas rápidas
                html.H3("Visão Geral do Sistema", className="text-center mb-4"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("2.000+", className="text-primary"),
                                html.P("Aeronaves Monitoradas", className="text-muted")
                            ])
                        ], className="text-center border-0 shadow-sm")
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("24.2%", className="text-warning"),
                                html.P("Taxa de Falha Média", className="text-muted")
                            ])
                        ], className="text-center border-0 shadow-sm")
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("88.7%", className="text-success"),
                                html.P("Precisão do Modelo", className="text-muted")
                            ])
                        ], className="text-center border-0 shadow-sm")
                    ], md=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("8", className="text-info"),
                                html.P("Modelos de Aeronaves", className="text-muted")
                            ])
                        ], className="text-center border-0 shadow-sm")
                    ], md=3),
                ]),
                
                # Informações técnicas sobre os dados a serem mostrados
                html.Div([
                    html.H4("Sobre o Sistema", className="mt-5 mb-3"),
                    html.P("""
                        Este sistema utiliza machine learning para prever falhas críticas em aeronaves 
                        baseado em dados históricos de operação, manutenção e características técnicas. 
                        O modelo foi treinado com dados de 2.000 aeronaves e alcança 88.7% de precisão 
                        na previsão de falhas.
                    """, className="text-justify"),
                    
                    html.H5("Funcionalidades Principais:", className="mt-4"),
                    html.Ul([
                        html.Li("Análise exploratória completa da frota"),
                        html.Li("Previsão de risco de falha em tempo real"),
                        html.Li("Comparação entre modelos e companhias"),
                        html.Li("Monitoramento de indicadores de manutenção"),
                        html.Li("Relatórios técnicos detalhados")
                    ]),
                    
                    html.H5("Variáveis Analisadas:", className="mt-4"),
                    html.Ul([
                        html.Li("Idade da aeronave e horas de voo"),
                        html.Li("Tipo de motor e modelo da aeronave"),
                        html.Li("Histórico de manutenção"),
                        html.Li("Ciclos de pouso e decolagem"),
                        html.Li("Condições operacionais (temperatura)")
                    ])
                ], className="mt-5 p-4 bg-light rounded")
                
            ])
        ])
    ])
], fluid=True)

# Página de análises (pode ser expandida posteriormente)
pagina_analises = dbc.Container([
    html.H1("Análises Avançadas", className="text-center my-4"),
    html.P("Página em desenvolvimento - Em breve mais análises detalhadas", 
        className="text-center text-muted lead"),
    dbc.Alert(
        "Esta seção está em desenvolvimento e incluirá relatórios técnicos avançados, "
        "tendências temporais e análises preditivas detalhadas.",
        color="info",
        className="text-center"
    )
])

# Layout principal da aplicação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navegacao,
    html.Div(id='page-content', style={'minHeight': '80vh'})
])

# Callback para roteamento de páginas
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/formulario':
        return formulario_aviacao.layout
    elif pathname == '/graficos':
        return graficos_aviacao.layout
    elif pathname == '/analises':
        return analises_avancadas.layout
    else:
        return pagina_inicial

# CSS personalizado
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Sistema de Gestão de Aviação</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link-custom {
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .nav-link-custom:hover {
                transform: translateY(-2px);
            }
            .card {
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                border: none;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }
            .display-4 {
                background: linear-gradient(45deg, #3498db, #2c3e50);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    print("     Iniciando Sistema de Gestão de Aviação...")
    print("     URLs disponíveis:")
    print("   - http://localhost:8050/ (Página Inicial)")
    print("   - http://localhost:8050/graficos (Dashboard)")
    print("   - http://localhost:8050/formulario (Previsão de Falhas)")
    print("   - http://localhost:8050/analises (Análises Avançadas)")
    print("\n   Estatísticas do sistema:")
    print("   - 2.000 aeronaves no dataset")
    print("   - Modelo com 88.7% de precisão")
    print("   - 8 tipos de aeronaves diferentes")
    print("   - 3 tipos de motor analisados")
    
    app.run(debug=True, host='0.0.0.0', port=8050)