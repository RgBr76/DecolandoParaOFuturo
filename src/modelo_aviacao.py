import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from sklearn.preprocessing import LabelEncoder

# Carregando o Dataset de Aviação
dados = pd.read_csv('../data/aviacao_falhas.csv')

print("📊 Estatísticas do Dataset:")
print(f"Total de registros: {len(dados)}")
print(f"Falhas críticas: {dados['falha_critica'].sum()} ({dados['falha_critica'].mean()*100:.1f}%)")
print("\nColunas disponíveis:")
print(dados.columns.tolist())

# Pré-processamento dos dados
print("\n🔧 Pré-processando dados...")

# Codificar variáveis categóricas (SEM companhia_aerea)
label_encoders = {}
categorical_columns = ['modelo_aeronave', 'tipo_motor', 'tipo_falha']

for col in categorical_columns:
    if col in dados.columns:
        le = LabelEncoder()
        dados[f'{col}_encoded'] = le.fit_transform(dados[col])
        label_encoders[col] = le
        print(f"Codificada coluna: {col} -> {col}_encoded")

# Selecionar features para o modelo (SEM companhia_aerea)
features = [
    'idade_aeronave_anos', 
    'horas_voo_total', 
    'ultima_manutencao_meses',
    'ciclos_pouso_decolagem', 
    'temperatura_media_operacao',
    'modelo_aeronave_encoded', 
    'tipo_motor_encoded'
]

X = dados[features]
y = dados['falha_critica']

print(f"\nFeatures utilizadas: {features}")
print(f"Shape de X: {X.shape}")
print(f"Shape de y: {y.shape}")

# Separando os dados
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)

print(f"\nDivisão dos dados:")
print(f"Treino: {X_train.shape[0]} amostras")
print(f"Teste: {X_test.shape[0]} amostras")
print(f"Taxa de falhas no treino: {y_train.mean():.3f}")
print(f"Taxa de falhas no teste: {y_test.mean():.3f}")

# Criando e treinando modelo XGBoost
print("\nTreinando modelo XGBoost...")
modelo = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)

modelo.fit(X_train, y_train)

# Fazendo previsões
print("\nAvaliando o modelo...")
preds_train = modelo.predict(X_train)
preds_test = modelo.predict(X_test)

# Avaliando o modelo
acuracia_train = accuracy_score(y_train, preds_train)
acuracia_test = accuracy_score(y_test, preds_test)

print(f"Acurácia no treino: {acuracia_train:.2%}")
print(f"Acurácia no teste: {acuracia_test:.2%}")

print("\nRelatório de classificação (teste):")
print(classification_report(y_test, preds_test))

# Importância das features
print("\nImportância das features:")
importancias = modelo.feature_importances_
feature_importance_df = pd.DataFrame({
    'feature': features,
    'importance': importancias
}).sort_values('importance', ascending=False)

print(feature_importance_df)

# Salvando o modelo treinado e informações
print("\nSalvando modelo e metadados...")
joblib.dump(modelo, "modelo_aviacao.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(features, "features_modelo.pkl")

# Salvar mapeamentos para uso no formulário
mapeamento_categorias = {}
for col in categorical_columns:
    if col in label_encoders:
        mapeamento_categorias[col] = {
            'classes': label_encoders[col].classes_.tolist(),
            'encoded': list(range(len(label_encoders[col].classes_)))
        }

joblib.dump(mapeamento_categorias, "mapeamento_categorias.pkl")

print("Modelo e arquivos auxiliares salvos com sucesso!")
print("Modelo treinado e pronto para uso!")