import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report

# Carregar o dataset
data = pd.read_csv('tellstone_3a.csv', sep=';')

# Função para transformar as colunas de posições ("F" -> -1, "?" -> -2, número -> int)
def transformar_posicao(valor):
    if valor == 'F':
        return -1
    elif valor == '?':
        return -2
    else:
        return int(valor)

# Aplicar a transformação nas colunas de posição
colunas_pedras = ['coroa', 'escudo', 'espada', 'bandeira', 'cavaleiro', 'martelo', 'balanca']
for coluna in colunas_pedras:
    data[coluna] = data[coluna].apply(transformar_posicao)

# Codificar as ações como strings únicas para simplificação
def codificar_acao(acao):
    return acao if pd.notna(acao) else 'NA'

colunas_acoes = ['acao_1', 'acao_2', 'acao_3'] #, 'acao_4', 'acao_5']
for coluna in colunas_acoes:
    data[coluna] = data[coluna].apply(codificar_acao)

# Preparar os dados para o modelo
X = data[colunas_pedras + colunas_acoes]
y = data[['final_coroa', 'final_escudo', 'final_espada', 'final_bandeira', 'final_cavaleiro', 'final_martelo', 'final_balanca']].map(transformar_posicao)

# Codificar as ações usando LabelEncoder
le = LabelEncoder()
for coluna in colunas_acoes:
    X.loc[:, coluna] = le.fit_transform(X[coluna])

# Dividir o dataset em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Normalizar os dados de entrada
scaler = StandardScaler()
X_train[colunas_pedras] = scaler.fit_transform(X_train[colunas_pedras])
X_test[colunas_pedras] = scaler.transform(X_test[colunas_pedras])



# Criar e treinar a rede neural com MultiOutputClassifier
mlp = MLPClassifier(hidden_layer_sizes=(28,28), activation='tanh', solver='adam', max_iter=2500, random_state=1)
multi_target_mlp = MultiOutputClassifier(mlp)
multi_target_mlp.fit(X_train, y_train)

# Fazer previsões e avaliar o modelo
y_pred = multi_target_mlp.predict(X_test)

# Avaliar a acurácia para cada coluna de saída
media = 0
for i, coluna in enumerate(y.columns):
    media+=accuracy_score(y_test[coluna], y_pred[:, i])
    # print(f"\nRelatório de classificação para {coluna}:\n", classification_report(y_test[coluna], y_pred[:, i],zero_division=0))
    print(f"Acurácia para {coluna}: {accuracy_score(y_test[coluna], y_pred[:, i])}")
print(f'Acurácia média: {media/7.0}')


# Exemplo de entrada para teste (substitua pelos valores desejados)
nova_entrada = {
    "coroa": "F",
    "escudo": "F",
    "espada": "?",
    "bandeira": "F",
    "cavaleiro": "F",
    "martelo": "3",
    "balanca": "F",
    "acao_1": "1,4", # inseriu espada na posicao 4
    "acao_2": "1,3", # inseriu martelo na posicao 3
    "acao_3": "2,4"  # escondeu a espada
}

# Converter os valores da nova entrada para o formato correto
entrada_transformada = pd.DataFrame([nova_entrada])
for coluna in colunas_pedras:
    entrada_transformada[coluna] = entrada_transformada[coluna].apply(transformar_posicao)
for coluna in colunas_acoes:
    entrada_transformada[coluna] = le.transform(entrada_transformada[coluna])

# Aplicar a mesma normalização
entrada_transformada[colunas_pedras] = scaler.transform(entrada_transformada[colunas_pedras])

# Fazer a previsão
predicao = multi_target_mlp.predict(entrada_transformada)
# print("entrada transformada: ", entrada_transformada)
print("Previsão para a nova entrada:", predicao)