# 🏠 Pipeline de Dados — Imóveis para Aluguel em BH

**Autor:** Eduardo Cosme Pereira dos Santos  
**Contatos:** https://www.linkedin.com/in/eduardocpsantos/ ; edu.cosme63@outlook.com.br

**Fonte de dados:** [ZAP Imóveis](https://www.zapimoveis.com.br/)  
**Status:** Concluido


---

## 📋 Objetivo

Construir um pipeline de dados completo para coletar, tratar e analisar anúncios de imóveis para aluguel em Belo Horizonte, utilizando a arquitetura Medalhão (Bronze → Silver → Gold) no Databricks.

---

## 🏗️ Arquitetura

```
ZAP Imóveis (API)
       │
       ▼
  [ Playwright ]          ← Coleta local via VSCode
       │
       ▼
  [ CSV / Bronze ]        ← Dados brutos em formato Delta
       │
       ▼
  [ Silver ]              ← Dados limpos e padronizados
       │
       ▼
  [ Gold ]                ← Análise exploratória final
```

| Camada | Tecnologia | Descrição |
|--------|-----------|-----------|
| Coleta | Python + Playwright | Simula navegador para contornar proteção Cloudflare |
| Bronze | Databricks + Delta | Ingestão dos dados brutos sem transformação |
| Silver | Databricks + PySpark | Limpeza, padronização e enriquecimento |
| Gold | Databricks + PySpark | Análise exploratória e métricas de negócio |

---

## 📁 Estrutura de Pastas

```
projeto/
│
├── notebooks/
│   ├── 01_Inicio.ipynb          # Exploração da API e headers
│   ├── 02_coleta.py             # Script de coleta com Playwright
│   └── 03_analise.ipynb        # Análise exploratória (Gold)
│
├── src/
│   ├── coleta_01.py             # Teste de acesso + contagem de imóveis
│   ├── coleta_02.py             # Extração dos tipos de dados (estrutura)
│   └── coleta_03.py             # Loop completo de coleta → DataFrame
│
├── data/                        # ⚠️ Ignorada pelo .gitignore
│   ├── bronze/                  # CSV bruto coletado pela API
│   ├── silver/                  # Dados tratados
│   └── gold/                    # Dataset final para análise
│
├── imagens/
│   ├── dataset_imoveis.png      # Print do dataset gerado no VSCode
│   └── estrutura_medalhao.png   # Estrutura no Databricks
│
│__Dashboord/
|  |_Analise imoveis_visão executiva.jpg
|  |_Analise imoveis_Perfil dos Imoveis.jpg
|  |_Analise imoveis_Analise Geografica.jpg
|
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11 | Coleta e manipulação de dados |
| Playwright | latest | Automação de navegador (coleta) |
| Pandas | latest | Montagem do DataFrame |
| Databricks CE | — | Processamento e armazenamento Delta |
| Apache Spark | — | Transformações nas camadas Silver/Gold |
| Delta Lake | — | Formato de armazenamento das camadas |
| Insomnia | — | Análise dos headers da API ZAP |

---

## 📜 Descrição dos Scripts

### 🔍 Coleta (local — VSCode)

| Script | Descrição |
|--------|-----------|
| `01_Inicio.ipynb` | Análise do tráfego da API ZAP via DevTools do Chrome. Gerou o arquivo `API_ZAP_IMOVEIS` com estrutura e headers. Identificado proteção Cloudflare. |
| `coleta_01.py` | Primeiro teste com Playwright: acessa o site, passa pelo Cloudflare e retorna a contagem total de imóveis disponíveis. |
| `coleta_02.py` | Mapeia os campos disponíveis na API (preço, área, bairro, quartos, tipo de estrutura) para estruturar o loop de coleta. |
| `coleta_03.py` | Loop completo de coleta paginada. Monta o DataFrame final com todos os campos selecionados: tipo de imóvel, aluguel, área, bairro, quartos, vagas, condomínio, IPTU. |

### 🥉 Bronze (Databricks)

- Leitura do CSV gerado pela coleta local
- Salvamento no formato Delta Lake
- Diagnóstico de valores nulos por coluna
- Regra de tratamento definida para a camada Silver:

| % de nulos | Ação |
|-----------|------|
| 0 – 10% | Imputar ou ignorar |
| 10 – 40% | Analisar caso a caso |
| 40 – 50% | Descartar coluna ou reavaliar uso |
| > 50% | Descartado |

### 🥈 Silver (Databricks)

- Leitura dos dados da camada Bronze
- Criação de coluna com tipo de imóvel traduzido para português
- Padronização dos nomes de colunas para MAIÚSCULAS
- Padronização dos nomes de bairros para MAIÚSCULAS
- Criação da coluna `VALOR_M2` (aluguel ÷ área)
- Remoção das colunas `LATITUDE` e `LONGITUDE` (> 50% nulos)
- Tratamento da coluna `AREA` (6% nulos → imputação por mediana)
- Tratamento da coluna `VAGAS` (2% nulos → imputação por média)
- Tratamento da coluna `IPTU` (5% nulos → imputação por mediana)
- Coluna `CONDOMINIO` mantida sem imputação (~3% nulos — ausência esperada conforme tipo de imóvel)
- Criação da coluna `CUSTO_TOTAL` = `ALUGUEL + CONDOMINIO + IPTU`
- Identificação de outlier com valor discrepante (tratamento pendente na Gold)
- Salvamento na camada Silver em formato Delta

### 🥇 Gold (Databricks)

> Concluido entregue os dashboard em powerbi as amostras então na pasta Imagens 

---

## ⚙️ Como Reproduzir

### 1. Criar e ativar o ambiente conda

```bash
conda create -n proj_imoveis python=3.11
conda activate proj_imoveis
```

### 2. Instalar dependências

```bash
pip install playwright pandas ipykernel
playwright install chromium
```

### 3. Executar os scripts em ordem

```
01_Inicio.ipynb  →  coleta_03.py  →  ZAP_BRONZE  →  ZAP_SILVER  →  ZAP_GOLD
```

### 4. Carregar o CSV no Databricks

Fazer upload do arquivo gerado em `data/bronze/` no DBFS do Databricks Community Edition e executar os notebooks na sequência.

---

## ⚠️ Desafios e Soluções

### 1. Proteção Cloudflare
A API do ZAP Imóveis retorna erro `403` ao ser acessada diretamente por `requests` ou `cloudscraper`.  
**Solução:** Playwright simula um navegador real (Chromium), passando pela verificação do Cloudflare nativamente.

### 2. Conflito de ambiente (venv × Anaconda)
A configuração do kernel Jupyter gerou conflito entre o ambiente virtual e a instalação do Anaconda.  
**Solução:** Criação de ambiente conda dedicado (`proj_imoveis`) com Python 3.11.

### 3. Campos incompletos na coleta
Durante os testes com `coleta_03.py`, foi identificado que campos importantes como `TIPO_IMOVEL` e `IPTU` estavam ausentes na primeira versão.  
**Solução:** Revisão e atualização do script para incluir todos os campos necessários.

### 4. Outlier na camada Silver
Identificado imóvel com valor de aluguel muito acima da distribuição dos demais.  
**Solução:** Registrado para tratamento na camada Gold.

---

## 📊 Limitações Conhecidas

- A API do ZAP Imóveis limita a paginação a **50 páginas por sessão**, resultando em aproximadamente **1.050 imóveis coletados** de um total de ~2.978 anúncios disponíveis.
- A amostra é considerada representativa para fins de **análise exploratória**.

---

## 🖼️ Imagens do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `imagens/dataset_imoveis.png` | Print do DataFrame gerado no VSCode após coleta |
| `imagens/Estrutura_medalhao_Databricks.jpg` | Estrutura das camadas Bronze/Silver/Gold no Databricks |
| `imagens/diagrama_pipeline_imoveis_bh.png`  | diagrama_pipeline_imoveis_bh

---

## 📝 Aprendizados

1. Uso do Playwright como alternativa robusta ao `requests` para APIs protegidas por Cloudflare
2. Importância do diagnóstico de nulos antes de decidir a estratégia de tratamento
3. A estrutura Medalhão organiza bem a evolução dos dados ao longo do pipeline
4. Iteração incremental nos scripts de coleta é necessária para garantir completude dos campos
5. Trabalhar dentro do ambiente Databricks com organização do workspace e Catalog
6. Verificação do tipo de grafico para cada analise dentro do powerbi
7. Desafio de trabalhar neste projeto com ambiente local ( VSCode) e nuvem (Databricks)
