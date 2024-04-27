import httpx
from .utility import Utility
from hcaptcha_new.source import hCaptchaSolver


class Captcha:
    def __init__(
        self, api_key: str, url: str, sitekey: str, proxy: str, rqdata: str = None
    ) -> None:
        self.api_key = api_key
        self.url = url
        self.sitekey = sitekey
        self.proxy = proxy
        self.rqdata = rqdata

    def solve(self) -> str:
        print("Solving Captcha...")
        payload = {
            "api_key": self.api_key,
            "url": self.url,
            "sitekey": self.sitekey,
            "proxy": self.proxy,
        }

        while True:
            try:
                result = httpx.post(
                    "http://solver.dexv.lol:1000/api/solve_hcap", json=payload
                )
                data = result.json()
                if data.get("success"):
                    print(f"Solved Captcha / {data['message'][:70]} ")
                    return data["message"]
                print(f"Failed To Solve Captcha -> {data.get('message')}")
                break
            except Exception as e:
                pass
                print(f"Failed To Solve Captcha -> {e}")


class CaptchaManager:
    def __init__(self, proxy: str):
        self._client = httpx.Client()
        self._utils = Utility()
        self.hcaptcha = hCaptchaSolver(
            "4c672d35-0701-42b2-88c3-78380b0db560", "discord.com", proxy
        )
        self._proxy = proxy
        self.api = self._utils.config["Captcha"]["api"]
        self.key = self._utils.config["Captcha"]["key"]

    def getBalance(self):
        if self.api == "anti-captcha.com" or self.api == "capsolver.com":
            resp = self._client.post(
                f"https://api.{self.api}/getBalance", json={"clientKey": self.key}
            ).json()
            if resp.get("errorId") > 0:
                print(
                    f"Error while getting captcha balance: {resp.get('errorDescription')}"
                )
                return 0.0
            return resp.get("balance")

    def getCaptcha(self):
        return self.hcaptcha.solve()
