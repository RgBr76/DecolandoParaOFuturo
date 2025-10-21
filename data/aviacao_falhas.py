import pandas as pd
import numpy as np

# Configurar seed para reproducibilidade
np.random.seed(42)

# Número de registros
n_registros = 2000

# Dados fictícios realistas
dados_aviacao = {
    'modelo_aeronave': np.random.choice([
        'Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A330', 
        'Embraer E190', 'Boeing 777', 'Airbus A350', 'Bombardier CRJ'
    ], n_registros),
    'idade_aeronave_anos': np.random.randint(1, 30, n_registros),
    'horas_voo_total': np.random.randint(500, 50000, n_registros),
    'tipo_motor': np.random.choice(['Turbojato', 'Turbofan', 'Turboprop'], n_registros),
    'companhia_aerea': np.random.choice([
        'LATAM', 'GOL', 'Azul', 'American', 'Delta', 'United', 'British', 'Emirates'
    ], n_registros),
    'ultima_manutencao_meses': np.random.randint(1, 24, n_registros),
    'ciclos_pouso_decolagem': np.random.randint(50, 5000, n_registros),
    'temperatura_media_operacao': np.random.uniform(-40, 45, n_registros),
    'falha_critica': np.zeros(n_registros)  # Inicializar com zeros
}

df = pd.DataFrame(dados_aviacao)

# Criar regras realistas para falhas críticas baseadas em fatores de risco
def calcular_probabilidade_falha(row):
    prob = 0
    
    # Idade da aeronave (mais velha = maior risco)
    if row['idade_aeronave_anos'] > 20:
        prob += 0.3
    elif row['idade_aeronave_anos'] > 15:
        prob += 0.2
    elif row['idade_aeronave_anos'] > 10:
        prob += 0.1
    
    # Horas de voo (mais horas = maior desgaste)
    if row['horas_voo_total'] > 40000:
        prob += 0.25
    elif row['horas_voo_total'] > 30000:
        prob += 0.15
    elif row['horas_voo_total'] > 20000:
        prob += 0.05
    
    # Manutenção (mais tempo desde a última = maior risco)
    if row['ultima_manutencao_meses'] > 18:
        prob += 0.2
    elif row['ultima_manutencao_meses'] > 12:
        prob += 0.1
    
    # Ciclos (mais pousos/decolagens = mais estresse)
    if row['ciclos_pouso_decolagem'] > 4000:
        prob += 0.15
    elif row['ciclos_pouso_decolagem'] > 3000:
        prob += 0.08
    
    # Tipo de motor (alguns têm taxas de falha diferentes)
    if row['tipo_motor'] == 'Turbojato':
        prob += 0.05
    elif row['tipo_motor'] == 'Turboprop':
        prob += 0.03
    
    # Temperatura extrema
    if abs(row['temperatura_media_operacao']) > 35:
        prob += 0.1
    
    return prob

# Aplicar a função e determinar falhas
for i, row in df.iterrows():
    prob_falha = calcular_probabilidade_falha(row)
    # Adicionar algum ruído aleatório
    prob_falha += np.random.uniform(-0.1, 0.1)
    prob_falha = max(0, min(1, prob_falha))  # Manter entre 0 e 1
    
    # Determinar falha baseada na probabilidade
    if np.random.random() < prob_falha:
        df.at[i, 'falha_critica'] = 1

# Adicionar tipo de falha baseado nas características
def definir_tipo_falha(row):
    if row['falha_critica'] == 1:
        if row['idade_aeronave_anos'] > 20:
            return np.random.choice(['Sistema Hidráulico', 'Estrutural', 'Elétrico'], p=[0.4, 0.3, 0.3])
        elif row['horas_voo_total'] > 40000:
            return np.random.choice(['Motor', 'Sistema de Combustível', 'APU'], p=[0.5, 0.3, 0.2])
        elif row['ultima_manutencao_meses'] > 18:
            return np.random.choice(['Sistemas de Navegação', 'Comunicações', 'Instrumentos'], p=[0.4, 0.3, 0.3])
        else:
            return np.random.choice(['Sistema de Pouso', 'Pressurização', 'Outros'])
    else:
        return 'Nenhuma'

df['tipo_falha'] = df.apply(definir_tipo_falha, axis=1)

# Estatísticas básicas
print("Estatísticas do Dataset:")
print(f"Total de registros: {len(df)}")
print(f"Falhas críticas: {df['falha_critica'].sum()} ({df['falha_critica'].mean()*100:.1f}%)")
print("\nDistribuição por modelo:")
print(df['modelo_aeronave'].value_counts())
print("\nDistribuição por companhia:")
print(df['companhia_aerea'].value_counts())
print("\nTipos de falha:")
print(df['tipo_falha'].value_counts())

# Salvar CSV
df.to_csv('aviacao_falhas.csv', index=False, encoding='utf-8')
print(f"\nDataset salvo como 'aviacao_falhas.csv'")

# Mostrar primeiras linhas
print("\nPrimeiras 10 linhas do dataset:")
print(df.head(10))