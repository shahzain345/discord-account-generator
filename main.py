from source import DiscordGenerator
import threading
import os


def main():
    while True:
        try:
            dc_gen = DiscordGenerator()
            dc_gen.sendRegister()
        except:
            continue


if __name__ == "__main__":
    os.system("cls") if os.name == "nt" else os.system("clear")
    print(
        """
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗      ██████╗ ███████╗███╗   ██╗
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝ ██╔════╝████╗  ██║
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██║  ███╗█████╗  ██╔██╗ ██║
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ╚██████╔╝███████╗██║ ╚████║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝ ╚══════╝╚═╝  ╚═══╝
BY SHAHZAIN
"""
    )
    for _ in range(int(input("Threads: "))):
        threading.Thread(target=main).start()
