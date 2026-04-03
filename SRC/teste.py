import asyncio
from playwright.async_api import async_playwright

async def teste():
    async with async_playwright() as pw:
        print("Iniciando Chromium...")
        navegador = await pw.chromium.launch(headless=False)
        print("Chromium aberto!")
        await asyncio.sleep(3)
        await navegador.close()
        print("Fechado!")

asyncio.run(teste())