import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report

def codificar_acao(acao):
    return acao if pd.notna(acao) else 'NA'

def transformar_posicao(valor):
    if valor == 'F':
        return -1
    elif valor == '?':
        return -2
    else:
        return int(valor)

def treina_rn(data, n):
    colunas_pedras = ['coroa', 'escudo', 'espada', 'bandeira', 'cavaleiro', 'martelo', 'balanca']
    for coluna in colunas_pedras:
        data[coluna] = data[coluna].apply(transformar_posicao)

    
    colunas_acoes = []
    for i in range(1, n+1):
        colunas_acoes.append(f'acao_{i}')

    for coluna in colunas_acoes:
        data[coluna] = data[coluna].apply(codificar_acao)

    X = data[colunas_pedras + colunas_acoes]
    y = data[['final_coroa', 'final_escudo', 'final_espada', 'final_bandeira', 'final_cavaleiro', 'final_martelo', 'final_balanca']].map(transformar_posicao)

    le = LabelEncoder()
    for coluna in colunas_acoes:
        X.loc[:, coluna] = le.fit_transform(X[coluna])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    scaler = StandardScaler() 
    X_train[colunas_pedras] = scaler.fit_transform(X_train[colunas_pedras])
    X_test[colunas_pedras] = scaler.transform(X_test[colunas_pedras])


    mlp = MLPClassifier(hidden_layer_sizes=(28,28), activation='tanh', solver='adam', max_iter=2500, random_state=1)
    multi_target_mlp = MultiOutputClassifier(mlp)
    multi_target_mlp.fit(X_train, y_train)

    y_pred = multi_target_mlp.predict(X_test) # Faz previsões

    # Avaliar a acurácia para cada coluna de saída
    media = 0
    for i, coluna in enumerate(y.columns):
        media+=accuracy_score(y_test[coluna], y_pred[:, i])
        print(f"\nRelatório de classificação para {coluna}:\n", classification_report(y_test[coluna], y_pred[:, i],zero_division=0))
        print(f"Acurácia para {coluna}: {accuracy_score(y_test[coluna], y_pred[:, i])}")
    print(f'Acurácia média: {media/7.0}')

    return colunas_pedras, colunas_acoes, le, scaler, multi_target_mlp


def realiza_teste(entrada, colunas_pedras, colunas_acoes, le, scaler, multi_target_mlp):
    entrada_transformada = pd.DataFrame([entrada])
    for coluna in colunas_pedras:
        entrada_transformada[coluna] = entrada_transformada[coluna].apply(transformar_posicao)
    for coluna in colunas_acoes:
        entrada_transformada[coluna] = le.transform(entrada_transformada[coluna])

    entrada_transformada[colunas_pedras] = scaler.transform(entrada_transformada[colunas_pedras])

    predicao = multi_target_mlp.predict(entrada_transformada)
    print("Previsão para a nova entrada:", predicao)




if __name__=='__main__':
    n = int(input('numero de acoes: '))
    data = pd.read_csv(f'tellstone_{n}a.csv', sep=';')

    colunas_pedras, colunas_acoes, le, scaler, multi_target_mlp = treina_rn(data,n)

    nova_entrada = {
        "coroa": "F",
        "escudo": "F",
        "espada": "F",
        "bandeira": "F",
        "cavaleiro": "?",
        "martelo": "F",
        "balanca": "F",
    }
    for i in range(1,n+1):
        nova_entrada[f'acao_{i}'] = '4,2'
    
    print('\n\n')
    cmd = ['']
    while cmd[0] != 'exit':
        cmd = input('> ').split(sep=' ')

        if cmd[0] == 't':
            realiza_teste(nova_entrada, colunas_pedras, colunas_acoes, le, scaler, multi_target_mlp)
        elif cmd[0] == 'u':
            nova_entrada[cmd[1]] = cmd[2]
        elif cmd[0] == 'p':
            print(nova_entrada)