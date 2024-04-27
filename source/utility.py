import json
import string, threading
import random
from colorama import Fore, Style

threadLock = threading.RLock()


class MPrint:
    def __print(self, text: str):
        threadLock.acquire()
        print(text)
        threadLock.release()

    def w_print(self, message: str):
        """Print warning"""
        self.__print(
            f"[{Style.BRIGHT}{Fore.RED}?{Style.RESET_ALL}] {Style.BRIGHT}{Fore.YELLOW}{message}{Style.RESET_ALL}"
        )

    def s_print(self, message: str):
        """Print SUCCESS"""
        self.__print(
            f"[{Style.BRIGHT}{Fore.MAGENTA}+{Style.RESET_ALL}] {Style.BRIGHT}{Fore.GREEN}{message}{Style.RESET_ALL}"
        )

    def f_print(self, message: str):
        """Print FAIL"""
        self.__print(
            f"[{Style.BRIGHT}{Fore.YELLOW}-{Style.RESET_ALL}] {Style.BRIGHT}{Fore.RED}{message}{Style.RESET_ALL}"
        )


class Utility:
    def __init__(self) -> None:
        self.config = self.getConfig()
        self.proxy = self.getProxy()
        self.username = self.getUsername()

    def getConfig(self):
        return json.load(open("Data/config.json"))

    def getUsername(self):
        if self.config.get("Usernames").get("username_from_file"):
            return random.choice(open("Data/usernames.txt").readlines())

    def getPwd(self):
        if self.config.get("Password").get("random_password"):
            return "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(6)
            )
        else:
            return self.config.get("Password").get("Password")

    def getProxy(self):
        if self.config.get("Proxy").get("proxyless"):
            return None
        else:
            return (
                f'http://{random.choice(open("Data/proxies.txt").readlines())}'.replace(
                    "\n", ""
                )
            )
