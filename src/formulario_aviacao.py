from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import numpy as np
from app import app

# Carregar modelo e metadados
try:
    modelo = joblib.load("../models/modelo_aviacao.pkl")
    label_encoders = joblib.load("../models/label_encoders.pkl")
    features_modelo = joblib.load("../models/features_modelo.pkl")
    mapeamento_categorias = joblib.load("../models/mapeamento_categorias.pkl")
    print("Modelo e metadados carregados com sucesso!")
except Exception as e:
    print(f"Erro ao carregar modelo: {e}")
    modelo = None

# Opções para os dropdowns (SEM companhia aérea)
opcoes_modelo = [
    {'label': 'Boeing 737', 'value': 'Boeing 737'},
    {'label': 'Airbus A320', 'value': 'Airbus A320'},
    {'label': 'Boeing 787', 'value': 'Boeing 787'},
    {'label': 'Airbus A330', 'value': 'Airbus A330'},
    {'label': 'Embraer E190', 'value': 'Embraer E190'},
    {'label': 'Boeing 777', 'value': 'Boeing 777'},
    {'label': 'Airbus A350', 'value': 'Airbus A350'},
    {'label': 'Bombardier CRJ', 'value': 'Bombardier CRJ'}
]

opcoes_motor = [
    {'label': 'Turbojato', 'value': 'Turbojato'},
    {'label': 'Turbofan', 'value': 'Turbofan'},
    {'label': 'Turboprop', 'value': 'Turboprop'}
]

# Layout do formulário (SEM companhia aérea)
formulario = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Previsão de Falhas em Aeronaves", 
                className="text-center mb-4 text-primary"),
            
            dbc.Card([
                dbc.CardHeader("Dados da Aeronave", className="bg-primary text-white"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Modelo da Aeronave *", className="fw-bold"),
                            dbc.Select(
                                id="modelo_aeronave",
                                options=opcoes_modelo,
                                placeholder="Selecione o modelo..."
                            )
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Tipo de Motor *", className="fw-bold"),
                            dbc.Select(
                                id="tipo_motor",
                                options=opcoes_motor,
                                placeholder="Selecione o tipo de motor..."
                            )
                        ], md=6)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Idade da Aeronave (anos) *", className="fw-bold"),
                            dbc.Input(
                                id="idade_aeronave",
                                type="number",
                                min=1,
                                max=30,
                                placeholder="Ex: 5"
                            )
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Horas Totais de Voo *", className="fw-bold"),
                            dbc.Input(
                                id="horas_voo",
                                type="number",
                                min=500,
                                max=50000,
                                placeholder="Ex: 15000"
                            )
                        ], md=6)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Última Manutenção (meses) *", className="fw-bold"),
                            dbc.Input(
                                id="ultima_manutencao",
                                type="number",
                                min=1,
                                max=24,
                                placeholder="Ex: 6"
                            )
                        ], md=6),
                        dbc.Col([
                            dbc.Label("Ciclos de Pouso/Decolagem *", className="fw-bold"),
                            dbc.Input(
                                id="ciclos_pouso",
                                type="number",
                                min=50,
                                max=5000,
                                placeholder="Ex: 1500"
                            )
                        ], md=6)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Temperatura Média de Operação (°C) *", className="fw-bold"),
                            dbc.Input(
                                id="temperatura_media",
                                type="number",
                                min=-40,
                                max=45,
                                step=0.1,
                                placeholder="Ex: 25.5"
                            )
                        ], md=12)
                    ], className="mb-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Prever Risco de Falha",
                                id="botao-prever",
                                color="danger",
                                size="lg",
                                className="w-100"
                            )
                        ], md=8, className="mx-auto")
                    ])
                ])
            ])
        ])
    ])
])

# Layout principal da página
layout = html.Div([
    html.Div([
        html.H1("Sistema de Previsão de Falhas em Aeronaves", 
            className="text-center mt-4 mb-4 text-dark"),
        html.P("Preveja o risco de falha crítica baseado nas características da aeronave",
            className="text-center text-muted mb-5"),
        formulario,
        html.Div(id="previsao-aviacao", className="mt-4")
    ], className="container")
])

@app.callback(
    Output("previsao-aviacao", "children"),
    Input("botao-prever", "n_clicks"),
    [State("modelo_aeronave", "value"),
    State("tipo_motor", "value"),
    State("idade_aeronave", "value"),
    State("horas_voo", "value"),
    State("ultima_manutencao", "value"),
    State("ciclos_pouso", "value"),
    State("temperatura_media", "value")],
    prevent_initial_call=True
)
def prever_falha_aviacao(n_clicks, modelo_aeronave, tipo_motor, idade_aeronave, 
                        horas_voo, ultima_manutencao, ciclos_pouso, temperatura_media):
    
    if n_clicks == 0:
        return ""
    
    # Validar entradas (SEM companhia aérea)
    campos_obrigatorios = [modelo_aeronave, tipo_motor, idade_aeronave, 
                        horas_voo, ultima_manutencao, ciclos_pouso, temperatura_media]
    
    if any(campo is None for campo in campos_obrigatorios):
        return dbc.Alert("Por favor, preencha todos os campos obrigatórios!", 
                        color="warning", className="text-center")
    
    if modelo is None:
        return dbc.Alert("Modelo não carregado. Execute o script de treinamento primeiro.", 
                        color="danger", className="text-center")
    
    try:
        # Preparar dados para predição (SEM companhia_aerea)
        entradas_usuario = pd.DataFrame({
            'idade_aeronave_anos': [idade_aeronave],
            'horas_voo_total': [horas_voo],
            'ultima_manutencao_meses': [ultima_manutencao],
            'ciclos_pouso_decolagem': [ciclos_pouso],
            'temperatura_media_operacao': [temperatura_media],
            'modelo_aeronave_encoded': [label_encoders['modelo_aeronave'].transform([modelo_aeronave])[0]],
            'tipo_motor_encoded': [label_encoders['tipo_motor'].transform([tipo_motor])[0]]
        })
        
        # Garantir ordem correta das features
        entradas_usuario = entradas_usuario[features_modelo]
        
        # Fazer a previsão
        previsao = modelo.predict(entradas_usuario)[0]
        probabilidade = modelo.predict_proba(entradas_usuario)[0]
        
        # Calcular risco percentual
        risco_percentual = probabilidade[1] * 100
        
        # Criar resultado
        if previsao == 1:
            if risco_percentual > 80:
                cor_alerta = "danger"
                icone = "🚨"
                recomendacao = "Recomendação: Manutenção imediata necessária!"
            elif risco_percentual > 60:
                cor_alerta = "warning"
                icone = "⚠️"
                recomendacao = "Recomendação: Agendar manutenção preventiva."
            else:
                cor_alerta = "info"
                icone = "🔍"
                recomendacao = "Recomendação: Monitorar condições."
                
            mensagem = f"{icone} RISCO ALTO DE FALHA: {risco_percentual:.1f}%"
            
        else:
            cor_alerta = "success"
            icone = "✅"
            mensagem = f"{icone} RISCO BAIXO DE FALHA: {risco_percentual:.1f}%"
            recomendacao = "Aeronave em condições operacionais adequadas."
        
        # Card de resultado
        resultado = dbc.Card([
            dbc.CardHeader("Resultado da Análise", className="bg-light"),
            dbc.CardBody([
                html.H4(mensagem, className=f"text-{cor_alerta}"),
                html.P(recomendacao, className="mt-2"),
                html.Hr(),
                html.H5("Detalhes da Probabilidade:"),
                dbc.Progress([
                    dbc.Progress(value=risco_percentual, color=cor_alerta, bar=True),
                ], style={"height": "25px"}, className="mb-2"),
                html.P(f"Probabilidade de falha: {risco_percentual:.1f}%"),
                html.P(f"Probabilidade de operação segura: {100-risco_percentual:.1f}%"),
                html.Hr(),
                html.H5("Resumo dos Dados:"),
                html.Ul([
                    html.Li(f"Modelo: {modelo_aeronave}"),
                    html.Li(f"Motor: {tipo_motor}"),
                    html.Li(f"Idade: {idade_aeronave} anos"),
                    html.Li(f"Horas de voo: {horas_voo:,}h"),
                    html.Li(f"Última manutenção: {ultima_manutencao} meses atrás"),
                    html.Li(f"Ciclos: {ciclos_pouso} pousos/decolagens"),
                    html.Li(f"Temperatura média: {temperatura_media}°C")
                ])
            ])
        ], color=cor_alerta, outline=True, className="mt-3")
        
        return resultado
        
    except Exception as e:
        return dbc.Alert(f"Erro na previsão: {str(e)}", 
                        color="danger", className="text-center")

# Callback para validação em tempo real (SEM companhia aérea)
@app.callback(
    Output("botao-prever", "disabled"),
    [Input("modelo_aeronave", "value"),
    Input("tipo_motor", "value"),
    Input("idade_aeronave", "value"),
    Input("horas_voo", "value"),
    Input("ultima_manutencao", "value"),
    Input("ciclos_pouso", "value"),
    Input("temperatura_media", "value")]
)
def validar_formulario(modelo_aeronave, tipo_motor, idade_aeronave, 
                    horas_voo, ultima_manutencao, ciclos_pouso, temperatura_media):
    campos_obrigatorios = [modelo_aeronave, tipo_motor, idade_aeronave, 
                        horas_voo, ultima_manutencao, ciclos_pouso, temperatura_media]
    return any(campo is None for campo in campos_obrigatorios)