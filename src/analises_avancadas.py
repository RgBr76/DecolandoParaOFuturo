import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
from datetime import datetime, timedelta
from app import app

# Carregar dados
try:
    dados = pd.read_csv('aviacao_falhas.csv')
    print("Dados carregados para análises avançadas")
except:
    print("Erro ao carregar dados")
    dados = pd.DataFrame()

# FUNÇÕES DE ANÁLISE 

def criar_analise_temporal():
    """Análise de tendências temporais"""
    if dados.empty:
        return px.line(title="Dados não disponíveis")
    
    # Simular dados temporais (adicionando coluna de data)
    datas = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(len(dados))]
    dados_temp = dados.copy()
    dados_temp['data'] = datas
    dados_temp['mes'] = dados_temp['data'].dt.to_period('M')
    
    # Agrupar por mês
    tendencias = dados_temp.groupby('mes').agg({
        'falha_critica': 'mean',
        'idade_aeronave_anos': 'mean',
        'horas_voo_total': 'mean'
    }).reset_index()
    tendencias['mes'] = tendencias['mes'].astype(str)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Tendência de Falhas ao Longo do Tempo', 'Métricas de Operação'),
        vertical_spacing=0.1
    )
    
    # Gráfico 1: Taxa de falhas
    fig.add_trace(
        go.Scatter(x=tendencias['mes'], y=tendencias['falha_critica'], 
                name='Taxa de Falha', line=dict(color='red', width=3)),
        row=1, col=1
    )
    
    # Gráfico 2: Idade e horas de voo
    fig.add_trace(
        go.Scatter(x=tendencias['mes'], y=tendencias['idade_aeronave_anos'],
                name='Idade Média', line=dict(color='blue')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=tendencias['mes'], y=tendencias['horas_voo_total']/1000,
                name='Horas de Voo (mil)', line=dict(color='green')),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=True)
    fig.update_yaxes(title_text="Taxa de Falha", row=1, col=1)
    fig.update_yaxes(title_text="Valores", row=2, col=1)
    fig.update_xaxes(title_text="Mês", row=2, col=1)
    
    return fig

def criar_analise_risco():
    """Análise de matriz de risco"""
    if dados.empty:
        return px.scatter(title="Dados não disponíveis")
    
    # Calcular score de risco baseado em múltiplos fatores
    dados_risco = dados.copy()
    dados_risco['score_risco'] = (
        dados_risco['idade_aeronave_anos'] / 30 * 0.3 +
        dados_risco['horas_voo_total'] / 50000 * 0.3 +
        dados_risco['ultima_manutencao_meses'] / 24 * 0.2 +
        dados_risco['ciclos_pouso_decolagem'] / 5000 * 0.2
    )
    
    fig = px.scatter(
        dados_risco, 
        x='idade_aeronave_anos', 
        y='horas_voo_total',
        size='score_risco',
        color='falha_critica',
        title='Matriz de Risco - Idade vs Horas de Voo',
        hover_data=['modelo_aeronave', 'tipo_motor', 'ultima_manutencao_meses'],
        color_discrete_sequence=['green', 'red']
    )
    
    fig.update_layout(
        xaxis_title="Idade da Aeronave (anos)",
        yaxis_title="Horas Totais de Voo",
        legend_title="Falha Crítica"
    )
    
    return fig

def criar_analise_manutencao():
    """Análise de otimização de manutenção"""
    if dados.empty:
        return px.bar(title="Dados não disponíveis")
    
    # Simular custos de manutenção
    dados_manutencao = dados.copy()
    dados_manutencao['custo_manutencao'] = (
        dados_manutencao['idade_aeronave_anos'] * 1000 +
        dados_manutencao['horas_voo_total'] * 0.1 +
        np.where(dados_manutencao['falha_critica'] == 1, 50000, 0)
    )
    
    analise_modelo = dados_manutencao.groupby('modelo_aeronave').agg({
        'custo_manutencao': 'mean',
        'falha_critica': 'mean',
        'idade_aeronave_anos': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Custo Médio de Manutenção por Modelo', '🛠️ Eficiência da Manutenção'),
        specs=[[{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # Gráfico de custos
    fig.add_trace(
        go.Bar(x=analise_modelo['modelo_aeronave'], y=analise_modelo['custo_manutencao'],
            name='Custo Médio', marker_color='orange'),
        row=1, col=1
    )
    
    # Gráfico de eficiência
    fig.add_trace(
        go.Scatter(x=analise_modelo['custo_manutencao'], y=analise_modelo['falha_critica'],
                text=analise_modelo['modelo_aeronave'], mode='markers+text',
                marker=dict(size=analise_modelo['idade_aeronave_anos']*2, color='purple'),
                name='Eficiência'),
        row=1, col=2
    )
    
    fig.update_layout(height=500, showlegend=False)
    fig.update_xaxes(title_text="Modelo", row=1, col=1)
    fig.update_yaxes(title_text="Custo (R$)", row=1, col=1)
    fig.update_xaxes(title_text="Custo de Manutenção", row=1, col=2)
    fig.update_yaxes(title_text="Taxa de Falha", row=1, col=2)
    
    return fig

def criar_relatorio_kpis():
    """Relatório com KPIs principais"""
    if dados.empty:
        return []
    
    # Calcular KPIs
    total_aeronaves = len(dados)
    taxa_falha_geral = dados['falha_critica'].mean()
    idade_media = dados['idade_aeronave_anos'].mean()
    horas_voo_media = dados['horas_voo_total'].mean()
    
    # KPI por modelo
    kpis_modelo = dados.groupby('modelo_aeronave').agg({
        'falha_critica': 'mean',
        'idade_aeronave_anos': 'mean',
        'horas_voo_total': 'mean'
    }).round(3)
    
    # Encontrar modelo mais problemático
    modelo_mais_problematico = kpis_modelo['falha_critica'].idxmax()
    taxa_modelo_problematico = kpis_modelo['falha_critica'].max()
    
    # Encontrar motor mais confiável
    kpis_motor = dados.groupby('tipo_motor')['falha_critica'].mean()
    motor_mais_confiavel = kpis_motor.idxmin()
    taxa_motor_confiavel = kpis_motor.min()
    
    return [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_aeronaves}", className="card-title text-primary"),
                        html.P("Total de Aeronaves", className="card-text")
                    ])
                ], className="text-center border-0 shadow-sm")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{taxa_falha_geral:.1%}", className="card-title text-warning"),
                        html.P("Taxa de Falha Geral", className="card-text")
                    ])
                ], className="text-center border-0 shadow-sm")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{idade_media:.1f}", className="card-title text-info"),
                        html.P("Idade Média (anos)", className="card-text")
                    ])
                ], className="text-center border-0 shadow-sm")
            ], md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{horas_voo_media:,.0f}", className="card-title text-success"),
                        html.P("Horas de Voo Média", className="card-text")
                    ])
                ], className="text-center border-0 shadow-sm")
            ], md=3),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Insights Principais", className="text-dark"),
                        html.Hr(),
                        html.P(f"Modelo mais problemático: {modelo_mais_problematico} ({taxa_modelo_problematico:.1%})"),
                        html.P(f"Motor mais confiável: {motor_mais_confiavel} ({taxa_motor_confiavel:.1%})"),
                        html.P(f"Idade crítica: {dados['idade_aeronave_anos'].max()} anos (máxima)"),
                        html.P(f"Horas de voo crítica: {dados['horas_voo_total'].max():,}h (máxima)")
                    ])
                ], className="border-0 shadow-sm")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Recomendações", className="text-dark"),
                        html.Hr(),
                        html.P("Priorizar manutenção preventiva em aeronaves mais antigas"),
                        html.P("Revisar procedimentos para modelos com alta taxa de falha"),
                        html.P("Monitorar aeronaves com mais de 30.000 horas de voo"),
                        html.P("Otimizar custos focando nos motores mais confiáveis")
                    ])
                ], className="border-0 shadow-sm")
            ], md=6),
        ])
    ]

def criar_analise_detalhada_modelo():
    """Análise detalhada por modelo de aeronave"""
    if dados.empty:
        return px.bar(title="Dados não disponíveis")
    
    analise_detalhada = dados.groupby('modelo_aeronave').agg({
        'falha_critica': ['count', 'mean', 'sum'],
        'idade_aeronave_anos': 'mean',
        'horas_voo_total': 'mean',
        'ultima_manutencao_meses': 'mean'
    }).round(3)
    
    # Simplificar nomes das colunas
    analise_detalhada.columns = ['total', 'taxa_falha', 'falhas', 'idade_media', 'horas_voo_media', 'manutencao_media']
    analise_detalhada = analise_detalhada.reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Total Aeronaves', x=analise_detalhada['modelo_aeronave'], y=analise_detalhada['total']),
        go.Bar(name='Falhas', x=analise_detalhada['modelo_aeronave'], y=analise_detalhada['falhas']),
        go.Scatter(name='Taxa de Falha', x=analise_detalhada['modelo_aeronave'], 
                y=analise_detalhada['taxa_falha']*100, yaxis='y2', mode='lines+markers', line=dict(color='red'))
    ])
    
    fig.update_layout(
        title='Análise Detalhada por Modelo de Aeronave',
        xaxis_title="Modelo",
        yaxis_title="Quantidade",
        yaxis2=dict(title="Taxa de Falha (%)", overlaying='y', side='right', range=[0, 100]),
        barmode='group'
    )
    
    return fig

# ========== LAYOUT DA PÁGINA ==========

layout = html.Div([
    html.H1("Análises Avançadas", className="text-center my-4 text-dark"),
    html.P("Relatórios técnicos detalhados e análises preditivas", 
        className="text-center text-muted lead mb-5"),
    
    # Seção de KPIs e Insights
    html.Div(id="kpis-relatorio", className="mb-5"),
    
    # Abas para diferentes tipos de análise
    dbc.Tabs([
        dbc.Tab([
            html.Div([
                html.H3("Análise Temporal e Tendências", className="mb-4"),
                dcc.Graph(id="analise-temporal", className="mb-4"),
                html.P("""
                    Esta análise mostra a evolução das taxas de falha e métricas operacionais ao longo do tempo. 
                    Use estas tendências para planejar manutenções preventivas e identificar padrões sazonais.
                """, className="text-muted")
            ], className="p-4")
        ], label="Tendências"),
        
        dbc.Tab([
            html.Div([
                html.H3("Matriz de Risco", className="mb-4"),
                dcc.Graph(id="analise-risco", className="mb-4"),
                html.P("""
                    A matriz de risco classifica as aeronaves baseado em múltiplos fatores. 
                    Tamanho do ponto indica o score de risco calculado. Foque nas aeronaves no quadrante superior direito.
                """, className="text-muted")
            ], className="p-4")
        ], label="Risco"),
        
        dbc.Tab([
            html.Div([
                html.H3("Otimização de Manutenção", className="mb-4"),
                dcc.Graph(id="analise-manutencao", className="mb-4"),
                html.P("""
                    Análise de custo-benefício da manutenção. Modelos no quadrante inferior esquerdo 
                    oferecem melhor relação custo-efetividade (baixo custo, baixa taxa de falha).
                """, className="text-muted")
            ], className="p-4")
        ], label="Manutenção"),
        
        dbc.Tab([
            html.Div([
                html.H3("Análise por Modelo", className="mb-4"),
                dcc.Graph(id="analise-modelo", className="mb-4"),
                html.P("""
                    Visão detalhada do performance de cada modelo de aeronave. 
                    A linha vermelha mostra a taxa de falha percentual para cada modelo.
                """, className="text-muted")
            ], className="p-4")
        ], label="Modelos"),
        
    ], className="mb-4"),
    
    # Seção de downloads (futura implementação)
    dbc.Card([
        dbc.CardHeader("Exportar Relatórios"),
        dbc.CardBody([
            html.P("Em breve: exporte relatórios completos em PDF e Excel"),
            dbc.Button("Gerar Relatório PDF", color="primary", disabled=True, className="me-2"),
            dbc.Button("Exportar para Excel", color="success", disabled=True),
        ])
    ], className="mt-5")
])

# CALLBACKS

@app.callback(
    [Output("analise-temporal", "figure"),
    Output("analise-risco", "figure"),
    Output("analise-manutencao", "figure"),
    Output("analise-modelo", "figure"),
    Output("kpis-relatorio", "children")],
    [Input("analise-temporal", "id")]  # Trigger inicial
)
def atualizar_analises(_):
    """Atualiza todas as análises quando a página carrega"""
    return (
        criar_analise_temporal(),
        criar_analise_risco(),
        criar_analise_manutencao(),
        criar_analise_detalhada_modelo(),
        criar_relatorio_kpis()
    )

print("Módulo de análises avançadas carregado!")