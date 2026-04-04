# Pipeline de Dados - Imóveis BH

# Autor: Eduardo Cosme Pereira dos Santos

## Objetivo
Coletar, tratar e analisar dados de imóveis para aluguel 
em Belo Horizonte a partir do ZAP Imóveis.

Site usado neste projeto: https://www.zapimoveis.com.br/

## Arquitetura do Projeto
- Coleta → Python + Playwright (VSCode local)
- Limpeza e Análise → Databricks Community Edition

## Estrutura de Pastas

projeto/

├── notebooks/
│   ├── 01_Inicio.ipynb
│   ├── 02_coleta.py
│   └── 03_analise.ipynb

├── data/
│   ├── raw/
│   └── processed/


├── src/
└── README.md

## Tecnologias
- Python 3.11
- Playwright
- Pandas
- Databricks

## Aprendizados e Desafios
### Cloudflare
O endpoint da API do ZAP é protegido por Cloudflare.
Tentativas com requests e cloudscraper retornaram 403.
Solução: Playwright simula um navegador real e passa 
pela proteção nativamente.

### Ambiente
Conflito entre venv e Anaconda na configuração do kernel 
do Jupyter. Solução: ambiente conda dedicado (proj_imoveis) 
com Python 3.11.



## Como Reproduzir
1. Criar ambiente conda
   conda create -n proj_imoveis python=3.11
   conda activate proj_imoveis

2. Instalar dependências
   pip install playwright pandas ipykernel
   playwright install chromium

3. Rodar os notebooks em ordem
   01_inicio → 02_coleta → 03_analise

## Estrutura de cada script :

1. inicio.ipynb - Script inicial para com as informações obtidas no acesso do site zapimoveis pelo navegador Chrome, foi gerado o arquivo API_ZAP_IMOVEIS , por ele consegui verificar qual a API onde esta os dados e sua estrutura , depois foi usado o programa insomnia para acessar os tipos de cabeçalho para ser usado no script, foi verificado que este site é protegido por Cloudflare

2. coleta_01.py - Script para testar o pacote playwright ajustando as informações para acessar o site, passar pela proteção do Cloudflare e retornar a API com quantidade de  imoveis total.

3. coleta_02.py  - Script com ajustado para trazer os tipos de dados  (preço, area, bairro, quartos, estrutura) dos imoveis para montar o loop que ira coletar e transformar no dataframe deste projeto 

4. coleta_03.py - Script usado atraves do tipo de dados acima ,criar o loop para buscar na api e montar o dataframe

## Limitações conhecidas

A API do ZAP limita a paginação a 50 páginas por sessão, resultando em ~1.050 imóveis coletados de um total de 2.978.

A amostra é representativa para fins de análise exploratória.

## Pasta IMAGEM 

Tem um print do dataset criado para este projeto , como por boas praticas no Github não subimos os arquivos eles serão tratatos dentro da arquiterura medalhão no Databricks 