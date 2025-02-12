# Importar bibliotecas necessárias
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Gerar dados de exemplo
np.random.seed(42)
X = np.random.rand(100, 2)

# Aplicar KMeans
modelo_kmeans = KMeans(n_clusters=3)
modelo_kmeans.fit(X)
labels = modelo_kmeans.labels_

# Obter os centróides dos clusters
centroides = modelo_kmeans.cluster_centers_

# Visualizar os resultados
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(centroides[:, 0], centroides[:, 1], s=300, c='red', marker='X') # Adicionar centróides ao gráfico
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Clusters de KMeans')
plt.show()


# Testar uma tupla específica
tupla_especifica = np.array([[0.7, 0.7]])  # Exemplo de tupla
cluster_predito = modelo_kmeans.predict(tupla_especifica)

print(f'A tupla {tupla_especifica} pertence ao cluster {cluster_predito[0]}')

# Exibir os centróides dos clusters
for i, centroide in enumerate(centroides):
    print(f'Cluster {i}: Centróide = {centroide}')
