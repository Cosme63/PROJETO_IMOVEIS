# Pipeline de Dados - Imóveis BH

## Objetivo
Coletar, tratar e analisar dados de imóveis para aluguel 
em Belo Horizonte a partir do ZAP Imóveis.

## Arquitetura do Projeto
- Coleta → Python + Playwright (VSCode local)
- Limpeza e Análise → Databricks Community Edition

## Estrutura de Pastas
projeto/
├── notebooks/
│   ├── 01_primeiros passos.py
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
   01_INICIO → 02_limpeza → 03_analise