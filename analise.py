import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de estilo para os gráficos
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

n = int(input('Insira o numero de acoes: '))
# Carregar o dataset
data = pd.read_csv(f'tellstone_{n}a.csv', sep=';')

# Listas de colunas
colunas_pedras = ['coroa', 'escudo', 'espada', 'bandeira', 'cavaleiro', 'martelo', 'balanca']
colunas_final = ['final_coroa', 'final_escudo', 'final_espada', 'final_bandeira', 'final_cavaleiro', 'final_martelo', 'final_balanca']

# Contagem de pedras ocultas reveladas e desconhecidas
ocultas_reveladas = 0
ocultas_desconhecidas = 0

for i, row in data.iterrows():
    for pedra, final in zip(colunas_pedras, colunas_final):
        if row[pedra] == '?':
            if row[final] not in ['?', 'F']:
                ocultas_reveladas += 1
            else:
                ocultas_desconhecidas += 1

# Gráfico: Pedras ocultas reveladas vs desconhecidas
plt.figure(figsize=(8, 5))
sns.barplot(x=['Ocultas Conhecidas', 'Ocultas Desconhecidas'], y=[ocultas_reveladas, ocultas_desconhecidas], palette='pastel')
plt.title('Pedras Ocultas Conhecidas vs Desconhecidas')
plt.ylabel('Frequência')
plt.show()

# Contagem de pedras ocultas e conhecidas na saída final
total_ocultas_saida = 0
total_conhecidas_saida = 0

for i, row in data.iterrows():
    for final in colunas_final:
        if row[final] == '?':
            total_ocultas_saida += 1
        else:
            total_conhecidas_saida += 1

# Gráfico: Total de pedras ocultas vs conhecidas na saída final
plt.figure(figsize=(8, 5))
sns.barplot(x=['Desconhecidas na Saída Final', 'Conhecidas na Saída Final'], y=[total_ocultas_saida, total_conhecidas_saida], palette='coolwarm')
plt.title('Total de Pedras Desconhecidas vs Conhecidas na Saída Final')
plt.ylabel('Frequência')
plt.show()

# Contagem do total de ações realizadas (considerando o primeiro número de acao_3)
acoes_realizadas = data[f'acao_{n}'].dropna().apply(lambda x: int(str(x).split(',')[0]) if str(x).split(',')[0].isdigit() else None).dropna()

# Gráfico: Total de ações realizadas
plt.figure(figsize=(10, 6))
sns.countplot(x=acoes_realizadas, palette='mako')
plt.title('Distribuição de Ações Realizadas')
plt.xlabel('Tipo de Ação')
plt.ylabel('Frequência')
plt.show()
