const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const extensionPath = path.resolve('C:/Users/Viacheslav/Documents/CSFloatMarketChecker');
    const chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe';  // Замените на свой путь

    const browser = await puppeteer.launch({
        headless: false,
        executablePath: chromePath,
        args: [
            `--disable-extensions-except=${extensionPath}`,
            `--load-extension=${extensionPath}`
        ]
    });

    const page = await browser.newPage();
    await page.goto('https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Alpine%20Camo%20(Minimal%20Wear)');

    // Логика для получения данных
    try {
        await page.waitForSelector('.float_block', { timeout: 10000 });
        const floatValue = await page.$eval('.itemfloat span', el => el.textContent);
        const paintSeedValue = await page.$eval('.itemseed span', el => el.textContent);

        console.log(`Float: ${floatValue}`);
        console.log(`Paint Seed: ${paintSeedValue}`);
    } catch (error) {
        console.error('Ошибка:', error);
    } finally {
        await browser.close();
    }
})();
