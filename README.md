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
│   ├── bronze/ - dados obtidos pela API via Playwright
│   └── silver/ - dados tratados 
    |__gold/     - analise


├── src/
└── README.md

## Tecnologias
- Python 3.11
- Playwright
- Pandas
- Databricks
- Estrutura medalhão databricks

## Aprendizados e Desafios

1. Cloudflare
O endpoint da API do ZAP é protegido por Cloudflare.
Tentativas com requests e cloudscraper retornaram 403.
Solução: Playwright simula um navegador real e passa 
pela proteção nativamente.

2. Ambiente
Conflito entre venv e Anaconda na configuração do kernel 
do Jupyter. Solução: ambiente conda dedicado (proj_imoveis) 
com Python 3.11.

3. 



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

1. Projeto_inicial.ipynb - Script inicial para com as informações obtidas no acesso do site zapimoveis pelo navegador Chrome, foi gerado o arquivo API_ZAP_IMOVEIS , por ele consegui verificar qual a API onde esta os dados e sua estrutura , depois foi usado o programa insomnia para acessar os tipos de cabeçalho para ser usado no script, foi verificado que este site é protegido por Cloudflare

2. coleta_01.py - Script para testar o pacote playwright ajustando as informações para acessar o site, passar pela proteção do Cloudflare e retornar a API com quantidade de  imoveis total.

3. coleta_02.py  - Script com ajustado para trazer os tipos de dados  (preço, area, bairro, quartos, estrutura) dos imoveis para montar o loop que ira coletar e transformar no dataframe deste projeto 

4. coleta_03.py - Script usado atraves do tipo de dados acima ,criar o loop para buscar na api e montar o dataframe, foi atualizado para acrescentar outros dados  dos imoveis para um dataset mais completo  

5. Bronze_delta 
- Criado a estrurtura de Medalhão dentro do databricks;
- ler o arquivo CSV e salva no formato delta;
- verificação de dados nulos , vou utilizar a regra abaixo e sera tratada na camada Silver 
 > % nulos	Ação
 . 0–10%	imputar ou ignorar
 . 10–40%	analisar caso
 . 40–50%	descartar ou reavaliar uso

6. Silver_delta 
- Ler os dados da camada Bronze;
- Criado uma coluna com  os nomes dos tipos de imoveis para português; 
- Padronização dos nomes das colunas para maiuscola;
- Padronizar nomes de bairros para maiuscola;
- Criar a coluna Valor por metro quadadro ;
- Devido a quantidade de dados nulos acima de 50 % as colunas latitude e longetude foram retiradas do dataset; 
- Verificado que na coluna Condominio temos quase 3 % de dados nulos porem devido a varidade de tipos de imoveis observado no dataset é de ser esperar que não são todos que tem taxa de condominio por este motivo dos dados não serão tratados; 
- Ja na coluna area apresentou 6 % de dados nulos , os mesmos foram tratados pela mediana onde para este projeto apresenta melhor uniformidade dos dados;
- Coluna vagas apresentou quase 2 % de dados nulos , estes foram tratados pela media do total de dados;
- Coluna iptu tem quase 5 % de dados nulos, obedecendo o mesmo criterio acima serão tratados pela mediana; 
- Criação da coluna custo total de aluguel que é a soma do ALUGUEL + CONDOMINIO + IPTU ;
- Descoberto um outlier com o valor muito acima dos outros imoveis, este sera tratado na camada golden 
- Salvar os dados na camada Silver. 

7. Golden_delta 


## Limitações conhecidas

A API do ZAP limita a paginação a 50 páginas por sessão, resultando em ~1.050 imóveis coletados de um total de 2.978.

A amostra é representativa para fins de análise exploratória.

## Pasta IMAGEM 

01. Dataset_imoveis - print do dataset gerado no VSCODE do projeto , como por boas praticas no Github não subimos os arquivos ;

02. Estrutura medalhão - estrutura dentro do ambiente databricks 


## Aprendizado 

1. Durante a busca do dados dos imoveis via script COLETA_03 foi verificado que estava faltando alguns dados importantes ( tipo de imovel , valor do IPTU, ) foi adicionado ao script.

2. Apos salvar o dataset em formato Delta no Databricks na camada Bronze , verificado que temos uma quantidade consideravel de dados nulos em algumas colunas acima de 50 % , eles serão tratatos na Silver . 

3. Descoberto um outlier este sera tratado na golden 
