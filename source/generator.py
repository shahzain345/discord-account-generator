from curl_cffi import requests
from .emailManager import EmailManager
from .captchaManager import CaptchaManager
from .utility import Utility, MPrint
from base64 import b64encode as encoder
import json as jsonLib
import random, time

console = MPrint()


class DiscordGenerator(requests.Session):
    """
    # Discord Generator class

    """

    def __init__(self):
        self.utils = Utility()
        self.email_manager = EmailManager(self.utils.config.get("Email").get("key"))
        self.captcha = CaptchaManager(self.utils.proxy)
        super().__init__(
            timeout=120,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en;q=0.9",
                "Connection": "keep-alive",
                "Host": "discord.com",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            },
            cookies={"locale": "en-GB"},
            impersonate="safari17_0",
            proxy=self.utils.proxy,
        )
        response = self.get(
            "http://ip-api.com/json/?fields=status,country,countryCode,timezone,offset"
        )
        self.timezone = response.json().get("timezone")
        self.get("https://discord.com")
        self.fingerprint = (
            self.get(
                "https://discord.com/api/v9/experiments?with_guild_experiments=true",
                headers={
                    "Accept": "*/*",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Connection": "keep-alive",
                    "Host": "discord.com",
                    "Referer": "https://discord.com/register",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                    "X-Context-Properties": "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0=",
                    "X-Debug-Options": "bugReporterEnabled",
                    "X-Discord-Locale": "en-GB",
                    "X-Discord-Timezone": self.timezone,
                    "X-Super-Properties": self._get_super_props(),
                },
            )
            .json()
            .get("fingerprint")
        )

    def _get_super_props(self):
        return encoder(
            jsonLib.dumps(
                {
                    "os": "iOS",
                    "browser": "Mobile Safari",
                    "device": "iPhone",
                    "system_locale": "en-GB",
                    "browser_user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                    "browser_version": "16.6",
                    "os_version": "16.6.1",
                    "referrer": "https://www.google.com/",
                    "referring_domain": "www.google.com",
                    "referrer_current": "https://google.com",
                    "referring_domain_current": "https://google.com",
                    "release_channel": "stable",
                    "client_build_number": 288065,
                    "client_event_source": None,
                },
                separators=(",", ":"),
            ).encode()
        ).decode()

    def sendRegister(self):
        resp = self.post(
            "https://discord.com/api/v9/auth/register",
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-GB,en;q=0.9",
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Host": "discord.com",
                "Origin": "https://discord.com",
                "Referer": "https://discord.com/register",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                "X-Debug-Options": "bugReporterEnabled",
                "X-Discord-Locale": "en-GB",
                "X-Discord-Timezone": self.timezone,
                "X-Fingerprint": self.fingerprint,
                "X-Super-Properties": self._get_super_props(),
            },
            json={
                "fingerprint": self.fingerprint,
                "email": self.email_manager.email,
                "username": self.email_manager.email.split("@")[0],
                "global_name": self.utils.username,
                "password": "QAZplm12@3",
                "invite": "zqfjkGU",
                "consent": True,
                "date_of_birth": f"{random.randint(1990, 2000)}-0{random.randint(1, 9)}-{random.randint(10,28)}",
                "gift_code_sku_id": None,
                "promotional_email_opt_in": True,
                "captcha_key": self.captcha.getCaptcha(),
            },
        )
        if "token" in resp.json():
            self.token = resp.json().get("token")
            console.s_print(f"Unclaimed: {self.token}")
            open("unclaimed.txt", "a").write(self.token + "\n")
            self.headers["Authorization"] = self.token
            verify_resp = self.verifyToken()
            print(verify_resp)

            if "token" in verify_resp:
                print(verify_resp)
                open("tokens.txt").write(verify_resp["token"] + "\n")

    def verifyToken(self):
        discord_email = self.email_manager.getDiscordEmail()
        print(discord_email)
        res = self.post(
            "https://discord.com/api/v9/auth/verify",
            json={"token": discord_email, "captcha_key": None},
        ).json()
        if "token" not in res:
            res = self.post(
                "https://discord.com/api/v9/auth/verify",
                json={"token": discord_email, "captcha_key": None},
            ).json()
        return res


if __name__ == "__main__":
    dc_gen = DiscordGenerator()
    dc_gen.sendRegister()
