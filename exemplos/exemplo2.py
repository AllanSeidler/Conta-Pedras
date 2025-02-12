# Importar bibliotecas necessárias
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder

# Exemplo de dados categóricos
dados = pd.DataFrame({
    'Categoria': ['A', 'B', 'A', 'C', 'B', 'C', 'A']
})

# Aplicar codificação one-hot
encoder = OneHotEncoder(sparse_output=False)
dados_codificados = encoder.fit_transform(dados)

# Aplicar KMeans nos dados codificados
modelo_kmeans = KMeans(n_clusters=2)
modelo_kmeans.fit(dados_codificados)
labels = modelo_kmeans.labels_

# Visualizar os resultados
plt.scatter(dados_codificados[:, 0], dados_codificados[:, 1], c=labels, cmap='viridis')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Clusters de KMeans')
plt.show()

# Testar uma tupla específica
tupla_especifica = pd.DataFrame({'Categoria': ['B']})  # Exemplo de tupla
tupla_codificada = encoder.transform(tupla_especifica)
cluster_predito = modelo_kmeans.predict(tupla_codificada)

print(f'A tupla {tupla_especifica.values[0]} pertence ao cluster {cluster_predito[0]}')

print(cluster_predito)
