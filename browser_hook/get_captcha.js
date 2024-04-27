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
    page.route("https://api.hcaptcha.com/getcaptcha/4c672d35-0701-42b2-88c3-78380b0db560", async (route) => {
        if (route.request().method() == "POST") {
            if (!isMainThread) {
                await parentPort.postMessage({
                    event: "new_data",
                    value: route.request().postData(),
                    url: route.request().url(),
                    headers: route.request().headers()
                })
            }
            await route.fulfill({
                status: 200,
                contentType: "application/json",
                body: JSON.stringify({
                    "c": {
                        "type": "hsw",
                        "req": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmIjowLCJzIjoyLCJ0IjoidyIsImQiOiJFeHVvSVBmTGQ0WEMvblFvWDNMNHN1ZzNsRnVjbXhXVUQzM0NHckRmVWl5ekw2TXdJSDdPa25QbzM3SlB3ZjZGQ2V1YzUwdW5GYzJnbG0rb3RlNmlJa09yTER0MnBRNGRyaWFNK1o3WnNrVXk1QnlsaVdxU0pPb0dBNm9ieC9MM0t4aHUzYll5TmFybkJmdUhLTUtValhQS3QvYnN1Uy9tOWdNU3NFck1PeXdldkIzOTNKVG5VQnNWRGc9PXBZaWtMaU4yTStYcGtBbVkiLCJsIjoiaHR0cHM6Ly9uZXdhc3NldHMuaGNhcHRjaGEuY29tL2MvYTg2Mzg0NTIiLCJlIjoxNjYwMDU3ODY5fQ.iK0zFoSgzJVp5h7xn-24wOCIM50w3qPPM8DEIHZmKfc"
                    },
                    "challenge_uri": "https://hcaptcha.com/challenge/grid/challenge.js",
                    "key": "E0_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiSG5WSUJ6MTBMWVRHdEJSUllBQjJ3UHJjbE4vM1h0WDJ6Z1JyTjZUTVNPb1owVXNHT2o1bGJiVkJjczAvV0Q3Z096RnRUNXZhMk5saTRjcGtqeGRrMXZjZVZTWHUrQllNcG9oamdqa1pGaHYzRC9BWGtVaTRQbjBUbzRTNTdDK2xHZlYwUFlFN1ViVnhaaWsxc0pGR2gvMmlOQlV0QnpLZDZKMVgvUi9iMFhuRkhVQXVnOVY4UUpRTVNQSDBXY3RsdFpXZ2M0YkFsdXNaa21qMDI2QzRuaE5BOU9VS0o5bzQrUGtzaFNJWjN5L1BHMjJJSWJOK0ptUlR6TmRwcWxWenR1dml1aHNnVW9tZDl1b1p2dz09T0x6cm1scTNYOFV5MWtVayJ9.XXShmQc8Nw2mpqAjtqcEzz7pK1K5-9ENEdTtWOkyEhM",
                    "request_config": {
                        "version": 0,
                        "shape_type": null,
                        "min_points": null,
                        "max_points": null,
                        "min_shapes_per_image": null,
                        "max_shapes_per_image": null,
                        "restrict_to_coords": null,
                        "minimum_selection_area_per_shape": null,
                        "multiple_choice_max_choices": 1,
                        "multiple_choice_min_choices": 1,
                        "overlap_threshold": null
                    },
                    "request_type": "image_label_binary",
                    "requester_question": {
                        "en": "Please click each image containing a lun."
                    },
                    "requester_question_example": [
                        "https://hi.shahzain.me/r/lun.png",
                        "https://hi.shahzain.me/r/lun.png",
                        "https://hi.shahzain.me/r/lun.png"
                    ],
                    "tasklist": [
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "1760753b-81de-4f49-a2ea-271244653751"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "c1187494-235f-40df-8b52-bcac18b34daf"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "bd96a879-9ef6-4b34-9092-0316cdd4b214"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "65426a80-72bc-4deb-a4a5-0af961ec30bc"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "7bfb1b8c-7fff-419c-986e-89e29840d29a"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "7154f138-2129-41a2-b84e-ec135d33a445"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "8eec06df-2290-4fae-a7c5-f7bc345dba37"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "919fdc9c-f216-4743-98d2-f2a542f9d7b8"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "d1ce43e7-ec0f-441a-8d51-1bfa819bc0f2"
                        }
                    ],
                    "bypass-message": "NA"
                })
            })
            await page.reload()
            await click(page)
        } else {
            route.continue()
        }
    })
    page.route("https://api2.hcaptcha.com/getcaptcha/4c672d35-0701-42b2-88c3-78380b0db560", async (route) => {
        if (route.request().method() == "POST") {
            if (!isMainThread) {
                await parentPort.postMessage({
                    event: "new_data",
                    value: route.request().postData(),
                    url: route.request().url(),
                    headers: route.request().headers()
                })
            }
            await route.fulfill({
                status: 200,
                contentType: "application/json",
                body: JSON.stringify({
                    "c": {
                        "type": "hsw",
                        "req": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmIjowLCJzIjoyLCJ0IjoidyIsImQiOiJFeHVvSVBmTGQ0WEMvblFvWDNMNHN1ZzNsRnVjbXhXVUQzM0NHckRmVWl5ekw2TXdJSDdPa25QbzM3SlB3ZjZGQ2V1YzUwdW5GYzJnbG0rb3RlNmlJa09yTER0MnBRNGRyaWFNK1o3WnNrVXk1QnlsaVdxU0pPb0dBNm9ieC9MM0t4aHUzYll5TmFybkJmdUhLTUtValhQS3QvYnN1Uy9tOWdNU3NFck1PeXdldkIzOTNKVG5VQnNWRGc9PXBZaWtMaU4yTStYcGtBbVkiLCJsIjoiaHR0cHM6Ly9uZXdhc3NldHMuaGNhcHRjaGEuY29tL2MvYTg2Mzg0NTIiLCJlIjoxNjYwMDU3ODY5fQ.iK0zFoSgzJVp5h7xn-24wOCIM50w3qPPM8DEIHZmKfc"
                    },
                    "challenge_uri": "https://hcaptcha.com/challenge/grid/challenge.js",
                    "key": "E0_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiSG5WSUJ6MTBMWVRHdEJSUllBQjJ3UHJjbE4vM1h0WDJ6Z1JyTjZUTVNPb1owVXNHT2o1bGJiVkJjczAvV0Q3Z096RnRUNXZhMk5saTRjcGtqeGRrMXZjZVZTWHUrQllNcG9oamdqa1pGaHYzRC9BWGtVaTRQbjBUbzRTNTdDK2xHZlYwUFlFN1ViVnhaaWsxc0pGR2gvMmlOQlV0QnpLZDZKMVgvUi9iMFhuRkhVQXVnOVY4UUpRTVNQSDBXY3RsdFpXZ2M0YkFsdXNaa21qMDI2QzRuaE5BOU9VS0o5bzQrUGtzaFNJWjN5L1BHMjJJSWJOK0ptUlR6TmRwcWxWenR1dml1aHNnVW9tZDl1b1p2dz09T0x6cm1scTNYOFV5MWtVayJ9.XXShmQc8Nw2mpqAjtqcEzz7pK1K5-9ENEdTtWOkyEhM",
                    "request_config": {
                        "version": 0,
                        "shape_type": null,
                        "min_points": null,
                        "max_points": null,
                        "min_shapes_per_image": null,
                        "max_shapes_per_image": null,
                        "restrict_to_coords": null,
                        "minimum_selection_area_per_shape": null,
                        "multiple_choice_max_choices": 1,
                        "multiple_choice_min_choices": 1,
                        "overlap_threshold": null
                    },
                    "request_type": "image_label_binary",
                    "requester_question": {
                        "en": "Please click each image containing a lun."
                    },
                    "requester_question_example": [
                        "https://hi.shahzain.me/r/lun.png",
                        "https://hi.shahzain.me/r/lun.png",
                        "https://hi.shahzain.me/r/lun.png"
                    ],
                    "tasklist": [
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "1760753b-81de-4f49-a2ea-271244653751"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "c1187494-235f-40df-8b52-bcac18b34daf"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "bd96a879-9ef6-4b34-9092-0316cdd4b214"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "65426a80-72bc-4deb-a4a5-0af961ec30bc"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "7bfb1b8c-7fff-419c-986e-89e29840d29a"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "7154f138-2129-41a2-b84e-ec135d33a445"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "8eec06df-2290-4fae-a7c5-f7bc345dba37"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "919fdc9c-f216-4743-98d2-f2a542f9d7b8"
                        },
                        {
                            "datapoint_uri": "https://hi.shahzain.me/r/koku.png",
                            "task_key": "d1ce43e7-ec0f-441a-8d51-1bfa819bc0f2"
                        }
                    ],
                    "bypass-message": "NA"
                })
            })
            await page.reload()
            await click(page)
        } else {
            route.continue()
        }
    })
    await click(page)
}
if (isMainThread) {
    ready_browser()
} else {
    ready_browser()
}