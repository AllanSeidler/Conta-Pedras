import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Lê o CSV gerado pelo redes_neurais.py
df = pd.read_csv("predicoes_vs_reais.csv")

# Identifica as colunas de saída a partir dos sufixos "_true"
colunas_saida = [col.replace('_true', '') for col in df.columns if col.endswith('_true')]

# Para cada coluna de saída, calcule e plote a matriz de confusão
for coluna in colunas_saida:
    y_true = df[f'{coluna}_true']
    y_pred = df[f'{coluna}_pred']
    
    # Calcula a matriz de confusão
    cm = confusion_matrix(y_true, y_pred)
    
    # Plot com heatmap do seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Matriz de Confusão para {coluna}')
    plt.xlabel('Valor Preditivo')
    plt.ylabel('Valor Real')
    plt.show()
