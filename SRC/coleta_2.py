## Script usado para coletar os dados e visualizar o json da API e coletar os dados para criar o dataset final

import asyncio
import json
from playwright.async_api import async_playwright

async def coletar():
    async with async_playwright() as pw:
        navegador = await pw.chromium.launch(headless=False)
        page = await navegador.new_page()

        # Primeiro acessa o site para pegar os cookies do Cloudflare
        await page.goto('https://www.zapimoveis.com.br/aluguel/apartamentos/mg+belo-horizonte/3-quartos/')
        await page.wait_for_timeout(5000)

        # Agora faz a requisição direto pela sessão autenticada
        resposta = await page.evaluate('''async () => {
            const res = await fetch("https://glue-api.zapimoveis.com.br/v2/listings?bedrooms=3&business=RENTAL&addressCity=Belo+Horizonte&addressState=Minas+Gerais&addressLocationId=BR%3EMinas+Gerais%3ENULL%3EBelo+Horizonte&addressType=city&listingType=USED&page=1&size=24&from=0&categoryPage=RESULT", {
                headers: {
                    "x-domain": ".zapimoveis.com.br"
                }
            });
            return await res.json();
        }''')
        
        print(json.dumps(resposta, indent=2, ensure_ascii=False))
        await navegador.close()

asyncio.run(coletar())