import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter
from collections import Counter
import numpy as np
import folium
from folium.plugins import HeatMap
from folium import FeatureGroup, LayerControl

os.makedirs("PLOTS",exist_ok=True)
# LOAD DATA
url = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja = pd.read_csv(url)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)
#Colunas
# Produto,Categoria do Produto,Preço,Frete,Data da Compra,Vendedor,Local da compra,Avaliação da compra,Tipo de pagamento,Quantidade de parcelas,lat,lon
# 3 Tipos de graficos


#1. Análise do faturamento
def formatar_moeda(valor, pos):
    return f'R$ {valor:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

def calcular_faturamento(lojas: list[pd.DataFrame]):
    """Nesta primeira análise, você deve calcular o faturamento total de cada loja.
    Somando os valores da coluna Preço de cada loja para estimar o faturamento."""
    Faturamentos: list[float] = []
    Labels: list[str] = []
    faturamento_total: float = 0.0
    for index,loja in enumerate(lojas):
        faturamento_loja = (loja["Preço"].sum())

        Faturamentos.append(faturamento_loja)
        Labels.append(f"Loja {index+1}\n{formatar_moeda(faturamento_loja,0)}")

        print(f"Faturamento Loja{index+1}: {faturamento_loja:.2f} R$")
        faturamento_total += faturamento_loja
    print(f"\nFaturamento Total: {faturamento_total:.2f} R$")
    return (Labels,Faturamentos),faturamento_total

lojas = [loja,loja2,loja3,loja4]
Faturamentos_loja,Faturamento_total = calcular_faturamento(lojas)

fig, ax = plt.subplots(figsize=(8, 5))


fig.suptitle("Faturamento das lojas")
ax.set_title(f"Total Faturamento: {formatar_moeda(Faturamento_total,0)}")
ax.bar(Faturamentos_loja[0],Faturamentos_loja[1])

ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
ax.set_ylabel("Valor (R$)")
ax.set_xlabel("Lojas")

plt.tight_layout()
plt.savefig("PLOTS/Analise_Faturamento.png")
plt.close()


#2. Vendas por Categoria
def _vendas_por_categoria(loja: pd.DataFrame):
    contagem_loja: Counter = (Counter(loja["Categoria do Produto"]))
    mais_vendido = contagem_loja.most_common(1)[0]

    return contagem_loja,mais_vendido

def vendas_catergoria_Lojas(lojas: list[pd.DataFrame]) -> Counter:
    """Neste passo, deve calcular a quantidade de produtos vendidos por categoria em cada loja.
    A ideia é agrupar os dados por categoria e contar o número de vendas de cada tipo, mostrando as categoria mais populares de cada loja"""
    vendas_categoria = Counter()
    for index,loja in enumerate(lojas):

        vendas_loja, mais_vendido = _vendas_por_categoria(loja)
        vendas_categoria+=vendas_loja
        os.makedirs("PLOTS/vendas_categoria/",exist_ok=True)

        # Plotar
        plt.bar(vendas_loja.keys(), vendas_loja.values())
        plt.suptitle(f"Vendas por Categoria, Loja {index+1}")
        plt.title(f"Categoria mais Vendidos: {mais_vendido[0]}, Quantidade {mais_vendido[1]}")

        plt.ylabel("Quantidade Vendida")
        plt.xlabel("Categoria")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"PLOTS/vendas_categoria/loja_{index+1}.png")
        plt.close()
    mais_vendido_total = vendas_categoria.most_common(1)[0]
    return vendas_categoria,mais_vendido_total

def relatorio_categoria_todas_lojas_bars(vendas: Counter, mais_vendido):
        os.makedirs("PLOTS/",exist_ok=True)

        # Plotar
        plt.bar(vendas.keys(), vendas.values())
        plt.suptitle(f"Vendas por Categoria em todas as Lojas")
        plt.title(f"Categoria mais Vendidos: {mais_vendido[0]}, Quantidade {mais_vendido[1]}")

        plt.ylabel("Quantidade Vendida")
        plt.xlabel("Categoria")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"PLOTS/vendas_por_categoria_bars.png")
        plt.close()

def relatorio_categoria_todas_lojas_pizza(vendas: Counter):
    os.makedirs("PLOTS/", exist_ok=True)

    categorias = list(vendas.keys())
    quantidades = list(vendas.values())

    # Criar gráfico de pizza
    plt.figure(figsize=(7, 5))
    plt.pie(
        quantidades,
        labels=categorias,
        autopct='%1.1f%%',        
        startangle=90,            
    )

    # Título
    plt.suptitle("Vendas por Categoria em Todas as Lojas", fontsize=14)
    # Salvar imagem
    plt.savefig("PLOTS/vendas_por_categoria_pizza.png")
    plt.close()
counter,mais_v = vendas_catergoria_Lojas(lojas)
relatorio_categoria_todas_lojas_bars(counter,mais_v)
relatorio_categoria_todas_lojas_pizza(counter)

#3. Média de Avaliação das Lojas


def media_avaliacao(lojas: list[pd.DataFrame]):
    """ Neste passo, vamos calcular a média das avaliações dos clientes para cada loja.
    O objetivo é entender a satisfação dos clientes com os produtos vendidos."""
    labels=[]
    media_lojas=[]

    print("Media da avaliação dos Clientes Por lojas")
    for index,loja in enumerate(lojas):
        media_loja = loja["Avaliação da compra"].mean()

        labels.append(f"Loja {index+1}\n{media_loja:.2f}")
        media_lojas.append(media_loja)
        print(f"Loja {index+1}: {media_loja:.2f}")
    
    plt.bar(labels, media_lojas)
    plt.suptitle("Media da avaliação dos Clientes Por lojas")


    plt.ylabel("Avaliações (Estrelas)")
    plt.xlabel("Lojas")
    plt.tight_layout()
    plt.savefig(f"PLOTS/media_avaliaçao.png")
    plt.close()

media_avaliacao(lojas)


#4. Produtos Mais e Menos Vendidos
def mais_e_menos_vendidos(lojas: list[pd.DataFrame]):
    """Neste passo, vamos calcular a média das avaliações dos clientes para cada loja.
    O objetivo é entender a satisfação dos clientes com os produtos vendidos."""
    labels = []  # Loja 1, Loja 2, etc.
    mais_vendidos_nomes = []
    mais_vendidos_qtd = []
    menos_vendidos_nomes = []
    menos_vendidos_qtd = []

    for index, loja in enumerate(lojas):
        loja_counter = Counter(loja["Produto"])
        mais_vendido = loja_counter.most_common(1)[0]
        menos_vendido = loja_counter.most_common()[-1]

        labels.append(f"Loja {index+1}")
        mais_vendidos_nomes.append(mais_vendido[0])
        mais_vendidos_qtd.append(mais_vendido[1])
        menos_vendidos_nomes.append(menos_vendido[0])
        menos_vendidos_qtd.append(menos_vendido[1])

        print(f"\nLoja {index+1}")
        print("Mais vendido:", mais_vendido)
        print("Menos vendido:", menos_vendido)

    # Plotar os dois conjuntos de barras lado a lado
    x = np.arange(len(labels))  # posições das lojas no eixo x
    largura = 0.35

    fig, ax = plt.subplots(figsize=(15, 6))
    barras_mais = ax.bar(x - largura/2, mais_vendidos_qtd, largura, label='Mais Vendido', color='green')
    barras_menos = ax.bar(x + largura/2, menos_vendidos_qtd, largura, label='Menos Vendido', color='red')

    # Adicionar texto em cima das barras
    for i in range(len(labels)):
        ax.text(x[i] - largura/2, mais_vendidos_qtd[i] + 0.1, mais_vendidos_nomes[i], ha='center', va='bottom', fontsize=9, rotation=0)
        ax.text(x[i] + largura/2, menos_vendidos_qtd[i] + 0.1, menos_vendidos_nomes[i], ha='center', va='bottom', fontsize=9, rotation=0)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Quantidade Vendida")
    ax.set_xlabel("Lojas")
    ax.set_title("Mais e Menos Vendidos por Loja")
    ax.legend()

    plt.tight_layout()
    plt.savefig("PLOTS/produtos_mais_e_menos_vendidos")
    plt.close()
mais_e_menos_vendidos(lojas)
#5. Frete Médio por Loja

def calcular_frete_medio(lojas: list[pd.DataFrame]):
    """Neste passo, vamos calcular o custo médio de frete para cada loja.
    O objetivo é entender quanto, em média, está sendo gasto com frete para cada uma das lojas."""  
    medias = []
    labels = []

    for index, loja in enumerate(lojas):
        media_frete = loja["Frete"].mean()
        medias.append(media_frete)
        labels.append(f"Loja {index+1}")
        print(f"Loja {index+1} - Frete médio: R$ {media_frete:.2f}")

    # Plotar o gráfico de barras
    plt.figure(figsize=(8, 5))
    plt.bar(labels, medias, color='skyblue')
    plt.title("Custo Médio de Frete por Loja")
    plt.xlabel("Lojas")
    plt.ylabel("Frete Médio (R$)")
    
    # Adicionar os valores acima das barras
    for i, valor in enumerate(medias):
        plt.text(i, valor + 0.1, f"R$ {valor:.2f}", ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("PLOTS/Frete_medio_por_loja.png")
    plt.close()    
calcular_frete_medio(lojas)



os.system('cls')
# EXTRA HEAPMAPS:

def mapa_dispersao_vendas(lojas: list[pd.DataFrame]):
    plt.figure(figsize=(10, 6))
    
    for index, loja in enumerate(lojas):
        latitudes = loja["lat"]
        longitudes = loja["lon"]
        plt.scatter(longitudes, latitudes, label=f"Loja {index+1}", alpha=0.6)

    plt.title("Distribuição Geográfica das Vendas por Loja")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("PLOTS/mapa_dispersao_vendas.png")
    plt.show()


def mapa_heatmap_vendas(lojas: list[pd.DataFrame]): #
    mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4) 

    for loja in lojas:
        heat_data = [[row['lat'], row['lon']] for _, row in loja.iterrows()]
        HeatMap(heat_data, radius=10).add_to(mapa)

    mapa.save("PLOTS/heatmap_vendas.html")

def mapa_interativo_por_loja(lojas: list[pd.DataFrame]):
    """Vendas de lojas diferentes foram feitas no mesmo local, logo sem um sistema de camadas não seria possivl visualizar todas."""
    mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
    cores = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue']

    centroides = []

    for i, loja in enumerate(lojas):
        grupo = FeatureGroup(name=f"Loja {i+1}")
        
        latlon = loja[['lat', 'lon']].dropna()
        latitudes = latlon['lat'].values
        longitudes = latlon['lon'].values

        
        centro_lat = np.mean(latitudes)
        centro_lon = np.mean(longitudes)
        centroides.append((centro_lat, centro_lon))


        for _, row in loja.iterrows():
            folium.CircleMarker(
                location=(row['lat'], row['lon']),
                radius=5,
                color=cores[i % len(cores)],
                fill=True,
                fill_opacity=0.5
            ).add_to(grupo)

        grupo.add_to(mapa)

    folium.LayerControl(collapsed=False).add_to(mapa)
    mapa.save("PLOTS/mapa_interativo_lojas.html")

mapa_heatmap_vendas(lojas)
mapa_interativo_por_loja(lojas)

os.system('cls') # Limpar Terminal Após gerar Tudo
# Relatorio:
# Qual Loja o seu João deve vender