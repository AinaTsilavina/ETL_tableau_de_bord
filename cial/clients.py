"""
Class de gestion des information et données clients.
"""
import pandas as pd

class Client:

    _pattern = ""
    _numInstance = 0

    def __init__(self, nom_client, annee_cmd, fichier_cmd):
        Client._numInstance += 1
        self._nom_client = nom_client
        self.fichier_cmd = fichier_cmd
        self._dossier_cmd = ""
        self._annee_cmd = 1900
        self._num_client = Client._numInstance

        self.set_annee(annee_cmd)
        self.set_dossier()
        self._xl = None



    def set_annee(self, annee):
        try:
            self._annee_cmd = int(annee)
        except ValueError:
            raise TypeError("'annee' must be an integer.")

    def set_dossier(self):
        if Client._pattern != "":
            self._dossier_cmd = Client._pattern.format(client=self.nom_client, annee=self._annee_cmd)
        else:
            raise ValueError("Pattern not defined!!! ")

    @property
    def num_client(self):
        if self._nom_client.upper() == 'LOCAUX':
            self._num_client = 100
        return self._num_client

    @property
    def nom_client(self):
        return self._nom_client

    @property
    def annee_cmd(self):
        return self._annee_cmd

    @property
    def dossier(self):
        self.set_dossier()
        return self._dossier_cmd


    @property
    def xl(self):
        self._xl = pd.ExcelFile(self._dossier_cmd + "/" + self.fichier_cmd, engine="calamine")
        return self._xl


    @classmethod
    def pattern_dossier(cls, dossier):
        cls._pattern = dossier

