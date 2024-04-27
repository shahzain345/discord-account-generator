from httpx import Client
import os


def get_hsw(task: str) -> str:
    with Client() as cl:
        while True:
            try:
                resp = cl.post(
                    f"http://localhost:5435/getn", json={"task": task}, timeout=None
                ).text
                return resp
            except:
                continue


def main():
    os.exec("cd ./browser_hook && node app.js")
