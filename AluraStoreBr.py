import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter
from collections import Counter

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

os.system('cls')
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

def relatorio_categoria_todas_lojas(vendas: Counter, mais_vendido):
        os.makedirs("PLOTS/",exist_ok=True)

        # Plotar
        plt.bar(vendas.keys(), vendas.values())
        plt.suptitle(f"Vendas por Categoria em todas as Lojas")
        plt.title(f"Categoria mais Vendidos: {mais_vendido[0]}, Quantidade {mais_vendido[1]}")

        plt.ylabel("Quantidade Vendida")
        plt.xlabel("Categoria")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"PLOTS/vendas_por_categoria.png")
        plt.close()

counter,mais_v = vendas_catergoria_Lojas(lojas)
relatorio_categoria_todas_lojas(counter,mais_v)
#3. Média de Avaliação das Lojas


#4. Produtos Mais e Menos Vendidos


#5. Frete Médio por Loja


# Relatorio:
# Qual Loja o seu João deve vender