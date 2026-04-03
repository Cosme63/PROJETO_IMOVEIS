## Script usado para montar o dataset .

import asyncio
import json
import pandas as pd
from playwright.async_api import async_playwright

async def coletar():
    async with async_playwright() as pw:
        navegador = await pw.chromium.launch(headless=False)
        page = await navegador.new_page()

        # Acessa o site para autenticar com o Cloudflare
        await page.goto('https://www.zapimoveis.com.br/aluguel/apartamentos/mg+belo-horizonte/3-quartos/')
        await page.wait_for_timeout(5000)

        # Primeira requisição para pegar o total de imóveis
        primeira_resposta = await page.evaluate('''async () => {
            const res = await fetch("https://glue-api.zapimoveis.com.br/v2/listings?bedrooms=3&business=RENTAL&addressCity=Belo+Horizonte&addressState=Minas+Gerais&addressLocationId=BR%3EMinas+Gerais%3ENULL%3EBelo+Horizonte&addressType=city&listingType=USED&page=1&size=24&from=0&categoryPage=RESULT", {
                headers: { "x-domain": ".zapimoveis.com.br" }
            });
            return await res.json();
        }''')

        # Calcula número de páginas
        total = primeira_resposta['page']['uriPagination']['totalListingCounter']
        tamanho = 24
        paginas = (total // tamanho) + 1
        print(f"Total de imóveis: {total} | Páginas: {paginas}")

        # Lista para guardar todos os imóveis
        imoveis = []

        # Loop de paginação
        for pagina in range(1, paginas + 1):
            print(f"Coletando página {pagina} de {paginas}...")

            resposta = await page.evaluate(f'''async () => {{
                const res = await fetch("https://glue-api.zapimoveis.com.br/v2/listings?bedrooms=3&business=RENTAL&addressCity=Belo+Horizonte&addressState=Minas+Gerais&addressLocationId=BR%3EMinas+Gerais%3ENULL%3EBelo+Horizonte&addressType=city&listingType=USED&page={pagina}&size=24&from={( pagina - 1) * 24}&categoryPage=RESULT", {{
                    headers: {{ "x-domain": ".zapimoveis.com.br" }}
                }});
                return await res.json();
            }}''')

            # Extrai os listings da resposta
            try:
                listings = resposta['search']['result']['listings']
            except (KeyError, TypeError):
                print(f"Página {pagina} sem dados, pulando...")
                continue

            # Extrai os campos de cada imóvel
            for item in listings:
                listing = item.get('listing', {})
                pricing = listing.get('pricingInfos', [{}])[0]
                address = listing.get('address', {})
                point = address.get('point', {})

                imovel = {
                    'preco':      pricing.get('price', None),
                    'condominio': pricing.get('monthlyCondoFee', None),
                    'area':       listing.get('totalAreas', [None])[0],
                    'quartos':    listing.get('bedrooms', [None])[0],
                    'bairro':     address.get('neighborhood', None),
                    'latitude':   point.get('lat', None),
                    'longitude':  point.get('lon', None),
                }
                imoveis.append(imovel)

            # Pausa entre páginas para não sobrecarregar o servidor
            await asyncio.sleep(2)

        # Converte para DataFrame e salva
        df = pd.DataFrame(imoveis)
        df.to_csv('data/raw/zap_raw.csv', index=False, encoding='utf-8-sig')
        print(f"Coleta finalizada! {len(df)} imóveis salvos em data/raw/zap_raw.csv")

        await navegador.close()

asyncio.run(coletar())

