import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Função para transformar os valores de posição
def transformar_posicao(valor):
    if valor == 'F':
        return -1
    elif valor == '?':
        return -2
    else:
        return int(valor)

# Função para codificar as ações
def codificar_acao(acao):
    return acao if pd.notna(acao) else 'NA'

def train_with_epochs(data, n, n_epochs=100):
    # --- Pré-processamento dos dados ---
    colunas_pedras = ['coroa', 'escudo', 'espada', 'bandeira', 'cavaleiro', 'martelo', 'balanca']
    for coluna in colunas_pedras:
        data[coluna] = data[coluna].apply(transformar_posicao)
    
    colunas_acoes = []
    for i in range(1, n+1):
        colunas_acoes.append(f'acao_{i}')
    
    for coluna in colunas_acoes:
        data[coluna] = data[coluna].apply(codificar_acao)
    
    # Define X (entradas) e y (saídas)
    X = data[colunas_pedras + colunas_acoes]
    y = data[['final_coroa', 'final_escudo', 'final_espada', 
              'final_bandeira', 'final_cavaleiro', 'final_martelo', 'final_balanca']]
    y = y.applymap(transformar_posicao)
    
    # Codificar as ações
    le = LabelEncoder()
    for coluna in colunas_acoes:
        X[coluna] = le.fit_transform(X[coluna])
    
    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1
    )
    
    # Normalizar as colunas das pedras
    scaler = StandardScaler()
    X_train[colunas_pedras] = scaler.fit_transform(X_train[colunas_pedras])
    X_test[colunas_pedras] = scaler.transform(X_test[colunas_pedras])
    
    # --- Criação dos classificadores para cada saída ---
    n_targets = y_train.shape[1]
    classifiers = []
    # Para cada alvo, criamos um MLPClassifier com max_iter=1 e warm_start=True para podermos iterar
    for target in range(n_targets):
        clf = MLPClassifier(
            hidden_layer_sizes=(28,28), activation='tanh', solver='adam',
            max_iter=1, warm_start=True, random_state=1
        )
        # Inicializamos o classificador com o método partial_fit (necessário passar o parâmetro classes)
        classes = np.unique(y_train.iloc[:, target])
        clf.partial_fit(X_train, y_train.iloc[:, target], classes=classes)
        classifiers.append(clf)
    
    # --- Treinamento incremental e monitoramento da acurácia ---
    epoch_details = []  # Lista para armazenar as informações de cada época

    for epoch in range(n_epochs):
        # Em cada época, atualizamos cada classificador com partial_fit
        for target, clf in enumerate(classifiers):
            clf.partial_fit(X_train, y_train.iloc[:, target])
        
        # Avaliar cada classificador no conjunto de teste
        accuracies = []
        for target, clf in enumerate(classifiers):
            y_pred = clf.predict(X_test)
            acc = accuracy_score(y_test.iloc[:, target], y_pred)
            accuracies.append(acc)
        avg_acc = np.mean(accuracies)
        print(f"Época {epoch+1}/{n_epochs} - Acurácia Média: {avg_acc:.4f}")
        
        # Armazena os detalhes: época, acurácia média e a acurácia de cada alvo
        epoch_detail = {"epoch": epoch+1, "avg_accuracy": avg_acc}
        for target, acc in enumerate(accuracies):
            epoch_detail[f"target_{target+1}_accuracy"] = acc
        epoch_details.append(epoch_detail)
    
    # --- Salvando os dados em CSV ---
    df_epochs = pd.DataFrame(epoch_details)
    df_epochs.to_csv("accuracy_evolution.csv", index=False)
    print("Evolução da acurácia salva em 'accuracy_evolution.csv'.")
    
    # --- Plotando o gráfico da acurácia média ---
    plt.figure(figsize=(8, 5))
    plt.plot(df_epochs["epoch"], df_epochs["avg_accuracy"], marker='o')
    plt.title("Evolução da Acurácia Média")
    plt.xlabel("Época")
    plt.ylabel("Acurácia Média")
    plt.grid(True)
    plt.show()
    
    return classifiers, le, scaler, colunas_pedras, colunas_acoes

if __name__ == '__main__':
    n = int(input('Número de ações: '))
    data = pd.read_csv(f'tellstone_{n}a.csv', sep=';')
    # Ajuste o número de épocas conforme sua necessidade
    train_with_epochs(data, n, n_epochs=100)
