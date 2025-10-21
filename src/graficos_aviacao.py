import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
import numpy as np

# Carregando o Dataset de Aviação
try:
    dados = pd.read_csv("aviacao_falhas.csv")
    print("Dados carregados para gráficos")
except:
    print("Erro ao carregar dados")
    dados = pd.DataFrame()

# Configuração global para gráficos
CONFIG_GRAFICO = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'responsive': True
}

#  GRÁFICO 1: Distribuição de Idade das Aeronaves 
if not dados.empty:
    histograma_idade = px.histogram(
        dados, 
        x="idade_aeronave_anos", 
        title="Distribuição da Idade das Aeronaves",
        nbins=20,
        color_discrete_sequence=['#1f77b4']
    )
    
    histograma_idade.update_layout(
        height=400,
        xaxis_title="Idade da Aeronave (anos)",
        yaxis_title="Número de Aeronaves",
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
else:
    histograma_idade = px.histogram(title="Dados não disponíveis")

# GRÁFICO 2: Taxa de Falha por Modelo 
if not dados.empty:
    falha_por_modelo = dados.groupby('modelo_aeronave')['falha_critica'].agg(['mean', 'count']).reset_index()
    falha_por_modelo.columns = ['modelo_aeronave', 'taxa_falha', 'total_aeronaves']
    
    grafico_modelo = px.bar(
        falha_por_modelo,
        x="modelo_aeronave",
        y="taxa_falha",
        title="Taxa de Falha por Modelo de Aeronave",
        color="taxa_falha",
        color_continuous_scale="RdYlGn_r"
    )
    
    grafico_modelo.update_layout(
        height=400,
        xaxis_title="Modelo da Aeronave",
        yaxis_title="Taxa de Falha",
        yaxis_tickformat=".0%",
        coloraxis_showscale=False,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
    
    grafico_modelo.update_traces(
        texttemplate='%{y:.1%}',
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Taxa de Falha: %{y:.1%}<br>Total: %{customdata} aeronaves<extra></extra>",
        customdata=falha_por_modelo['total_aeronaves']
    )
else:
    grafico_modelo = px.bar(title="Dados não disponíveis")

#GRÁFICO 3: Taxa de Falha por Tipo de Motor
if not dados.empty:
    falha_por_motor = dados.groupby('tipo_motor')['falha_critica'].agg(['mean', 'count']).reset_index()
    falha_por_motor.columns = ['tipo_motor', 'taxa_falha', 'total_aeronaves']
    
    grafico_motor = px.pie(
        falha_por_motor,
        values='total_aeronaves',
        names='tipo_motor',
        title="Distribuição por Tipo de Motor",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    grafico_motor.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12),
        showlegend=True
    )
    
    grafico_motor.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Taxa de Falha: %{customdata:.1%}<br>Total: %{value} aeronaves<extra></extra>",
        customdata=falha_por_motor['taxa_falha']
    )
else:
    grafico_motor = px.pie(title="Dados não disponíveis")

#GRÁFICO 4: Horas de Voo vs Falhas
if not dados.empty:
    scatter_horas_falha = px.scatter(
        dados,
        x="horas_voo_total",
        y="idade_aeronave_anos",
        color="falha_critica",
        title="Horas de Voo vs Idade",
        color_discrete_sequence=['green', 'red'],
        labels={
            "horas_voo_total": "Horas Totais de Voo",
            "idade_aeronave_anos": "Idade da Aeronave (anos)",
            "falha_critica": "Falha Crítica"
        },
        opacity=0.7
    )
    
    scatter_horas_falha.update_layout(
        height=400,
        xaxis_title="Horas Totais de Voo",
        yaxis_title="Idade da Aeronave (anos)",
        legend_title="Falha Crítica",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
else:
    scatter_horas_falha = px.scatter(title="Dados não disponíveis")

#GRÁFICO 5: Manutenção vs Falhas
if not dados.empty:
    dados['categoria_manutencao'] = pd.cut(
        dados['ultima_manutencao_meses'],
        bins=[0, 6, 12, 18, 24],
        labels=['0-6 meses', '7-12 meses', '13-18 meses', '19-24 meses']
    )
    
    falha_por_manutencao = dados.groupby('categoria_manutencao')['falha_critica'].mean().reset_index()
    
    grafico_manutencao = px.bar(
        falha_por_manutencao,
        x="categoria_manutencao",
        y="falha_critica",
        title="Taxa de Falha por Tempo desde Última Manutenção",
        color="falha_critica",
        color_continuous_scale="RdYlGn_r"
    )
    
    grafico_manutencao.update_layout(
        height=400,
        xaxis_title="Tempo desde Última Manutenção",
        yaxis_title="Taxa de Falha",
        yaxis_tickformat=".0%",
        coloraxis_showscale=False,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
    
    grafico_manutencao.update_traces(
        texttemplate='%{y:.1%}',
        textposition='outside'
    )
else:
    grafico_manutencao = px.bar(title="Dados não disponíveis")

# GRÁFICO 6: Tipos de Falha
if not dados.empty and 'tipo_falha' in dados.columns:
    tipos_falha = dados[dados['falha_critica'] == 1]['tipo_falha'].value_counts().reset_index()
    tipos_falha.columns = ['tipo_falha', 'quantidade']
    
    grafico_tipos_falha = px.bar(
        tipos_falha,
        x="quantidade",
        y="tipo_falha",
        title="Distribuição dos Tipos de Falha",
        orientation='h',
        color_discrete_sequence=['#ff6b6b']
    )
    
    grafico_tipos_falha.update_layout(
        height=400,
        xaxis_title="Número de Ocorrências",
        yaxis_title="Tipo de Falha",
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
else:
    grafico_tipos_falha = px.bar(title="Tipos de Falha (Dados não disponíveis)")

# GRÁFICO 7: Heatmap de Correlação 
if not dados.empty:
    colunas_numericas = ['idade_aeronave_anos', 'horas_voo_total', 'ultima_manutencao_meses', 
                        'ciclos_pouso_decolagem', 'temperatura_media_operacao', 'falha_critica']
    
    correlacao = dados[colunas_numericas].corr()
    
    heatmap_correlacao = px.imshow(
        correlacao,
        title="Matriz de Correlação entre Variáveis",
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )
    
    heatmap_correlacao.update_layout(
        height=500,
        xaxis_title="Variáveis",
        yaxis_title="Variáveis",
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
else:
    heatmap_correlacao = px.imshow(title="Dados não disponíveis")

#LAYOUT DO DASHBOARD 
layout = html.Div([
    # Cabeçalho
    html.Div([
        html.H1("Dashboard de Análise de Falhas em Aeronaves", 
            style={"textAlign": "center", "marginBottom": "10px", "color": "#2c3e50"}),
        html.P("Análise exploratória do dataset de falhas em aeronaves - Dados fictícios para demonstração",
            style={"textAlign": "center", "color": "#7f8c8d", "marginBottom": "30px"})
    ]),
    
    # Container principal com largura máxima
    html.Div(style={"maxWidth": "1400px", "margin": "0 auto", "padding": "10px"}, children=[
        
        # Primeira linha - 2 gráficos
        html.Div(style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "20px", "marginBottom": "30px"}, children=[
            html.Div(style={"flex": "1", "minWidth": "500px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
                html.H3("Distribuição da Idade", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
                dcc.Graph(
                    figure=histograma_idade,
                    config=CONFIG_GRAFICO,
                    style={'height': '400px'}
                )
            ]),
            
            html.Div(style={"flex": "1", "minWidth": "500px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
                html.H3("Falhas por Modelo", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
                dcc.Graph(
                    figure=grafico_modelo,
                    config=CONFIG_GRAFICO,
                    style={'height': '400px'}
                )
            ])
        ]),
        
        # Segunda linha - 2 gráficos
        html.Div(style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "20px", "marginBottom": "30px"}, children=[
            html.Div(style={"flex": "1", "minWidth": "500px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
                html.H3("Tipos de Motor", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
                dcc.Graph(
                    figure=grafico_motor,
                    config=CONFIG_GRAFICO,
                    style={'height': '400px'}
                )
            ]),
            
            html.Div(style={"flex": "1", "minWidth": "500px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
                html.H3("Horas de Voo vs Idade", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
                dcc.Graph(
                    figure=scatter_horas_falha,
                    config=CONFIG_GRAFICO,
                    style={'height': '400px'}
                )
            ])
        ]),
        
        # Terceira linha - 2 gráficos
        html.Div(style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "20px", "marginBottom": "30px"}, children=[
            html.Div(style={"flex": "1", "minWidth": "500px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
                html.H3("Impacto da Manutenção", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
                dcc.Graph(
                    figure=grafico_manutencao,
                    config=CONFIG_GRAFICO,
                    style={'height': '400px'}
                )
            ]),
            
            html.Div(style={"flex": "1", "minWidth": "500px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
                html.H3("Tipos de Falha", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
                dcc.Graph(
                    figure=grafico_tipos_falha,
                    config=CONFIG_GRAFICO,
                    style={'height': '400px'}
                )
            ])
        ]),
        
        # Quarta linha - Heatmap (largura total)
        html.Div(style={"marginBottom": "30px", "backgroundColor": "white", "padding": "15px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
            html.H3("Correlações entre Variáveis", style={"textAlign": "center", "color": "#34495e", "marginBottom": "15px"}),
            dcc.Graph(
                figure=heatmap_correlacao,
                config=CONFIG_GRAFICO,
                style={'height': '500px'}
            )
        ]),
        
        # Estatísticas resumidas
        html.Div(style={"backgroundColor": "white", "padding": "25px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"}, children=[
            html.H3("Estatísticas do Dataset", style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "25px"}),
            
            html.Div(style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "gap": "20px"}, children=[
                html.Div(style={"textAlign": "center", "padding": "15px", "minWidth": "200px"}, children=[
                    html.H4(f"{len(dados):,}" if not dados.empty else "0", 
                        style={"color": "#3498db", "fontSize": "2em", "margin": "0"}),
                    html.P("Total de Aeronaves", style={"color": "#7f8c8d", "margin": "5px 0 0 0"})
                ]),
                
                html.Div(style={"textAlign": "center", "padding": "15px", "minWidth": "200px"}, children=[
                    html.H4(f"{dados['falha_critica'].sum():,}" if not dados.empty else "0", 
                        style={"color": "#e74c3c", "fontSize": "2em", "margin": "0"}),
                    html.P("Falhas Críticas", style={"color": "#7f8c8d", "margin": "5px 0 0 0"})
                ]),
                
                html.Div(style={"textAlign": "center", "padding": "15px", "minWidth": "200px"}, children=[
                    html.H4(f"{dados['falha_critica'].mean()*100:.1f}%" if not dados.empty else "0%", 
                        style={"color": "#f39c12", "fontSize": "2em", "margin": "0"}),
                    html.P("Taxa de Falha Geral", style={"color": "#7f8c8d", "margin": "5px 0 0 0"})
                ]),
                
                html.Div(style={"textAlign": "center", "padding": "15px", "minWidth": "200px"}, children=[
                    html.H4(f"{dados['idade_aeronave_anos'].mean():.1f}" if not dados.empty else "0", 
                        style={"color": "#27ae60", "fontSize": "2em", "margin": "0"}),
                    html.P("Idade Média (anos)", style={"color": "#7f8c8d", "margin": "5px 0 0 0"})
                ])
            ])
        ])
    ])
])

print("Dashboard de gráficos atualizado com layout controlado")