import asyncio


## Script usado para coletar os dados do site ZAP IMOVEIS via API descoberta 

from playwright.async_api import async_playwright

async def coletar():
    async with async_playwright() as pw:
        navegador = await pw.chromium.launch(headless=False)
        page = await navegador.new_page()

        async def capturar_resposta(response):
            if "v2/listings" in response.url:
                print("✓ Endpoint capturado!")
                print("URL:",response.url)
                dados =await response.json()
                print(dados)

        page.on("response", capturar_resposta)

        await page.goto('https://www.zapimoveis.com.br/aluguel/apartamentos/mg+belo-horizonte/3-quartos/?pagina=1')
        await page.wait_for_timeout(6000)
        await navegador.close()

asyncio.run(coletar())