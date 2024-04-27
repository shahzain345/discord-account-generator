const { isMainThread, parentPort } = require("worker_threads")
const {
    firefox
} = require("playwright-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
firefox.use(StealthPlugin());

const sleep = (ms) => {
    return new Promise(res => setTimeout(res, ms))
}

const click = async (page) => {
    await sleep(500)
    await page.click("iframe")
}


const ready_browser = async () => {
    const browser = await firefox.launch({
        headless: true
    });
    const page = await browser.newPage();
    page.route("https://discord.com", async (route) => {
        await route.fulfill({
            status: 200,
            body: `
            <html>
                <head>
                  <title>Discord</title>
                  <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
                </head>
                <body>
                  <form>
                    <div class="h-captcha" data-sitekey="4c672d35-0701-42b2-88c3-78380b0db560"></div>
                  </form>
                </body>
              </html>
            `
        })
    })

    await page.goto("https://discord.com")
    await page.waitForSelector("iframe");
    const frame = await page.frames()[1]
    await frame.evaluate(`const se = new WebSocket("ws://127.0.0.1:1234");

    se.onmessage = async (message) => {
        const payload = JSON.parse(message.data);
        window.focus();
    
        const reply = {
            type: "solved",
            token: ""
        };
    
        try {
            reply.token = await hsw(payload.solve, "https://discord.com");
        } catch (err) {
            reply.type = "failed";
            reply.token = err.message
        } finally {
            se.send(JSON.stringify(reply));
        }
    };`)
}
if (isMainThread) {
    ready_browser()
} else {
    ready_browser()
}