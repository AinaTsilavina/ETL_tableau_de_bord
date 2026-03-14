import re

import pandas as pd
from .clients import Client


class Solde:
    def __init__(self, Client, sheet, columns):
        self._client = Client
        self._data = None
        self._semaine_cmd = None
        self.set_data(sheet, columns)



    @property
    def sheets_list(self):
        return self._client.xl.sheet_names

    def set_data(self, sheet, columns):
            solde = {}
            for k, v in sheet.items():
                try:
                    my_sheet = [sh for sh in self.sheets_list if sh.startswith(v)][0]
                    if k == "all":
                        self._semaine_cmd = re.findall(r'\d+(?:\.\d+)?', my_sheet)[0]
                    df = self._client.xl.parse(sheet_name=my_sheet, usecols=columns, skiprows=8).dropna(subset=['Unnamed: 0'])
                    df = df.rename(columns=lambda x: df.iloc[0][x])  # Prend la première ligne comme en-tête
                    df = df.iloc[1:]  # Supprime la ligne qui était l'ancien en-tête
                    df.columns = df.columns.str.strip()
                    df= df.drop(columns=df.columns[df.columns.isna()])
                    solde[k] = df
                except Exception:
                    print("solde_cmd data error!")
                    solde[k] = None

            self._data = pd.concat(solde)

    @property
    def data(self):
        return self._data

    @property
    def soldeBateau(self):
        try:
            return self._data['Qté BAT'].sum()
        except Exception:
            return None

    @property
    def soldeAvion(self):
        try:
            return self._data['Qté av'].sum()
        except Exception:
            return None

    @property
    def solde(self):
        try:
            return self.soldeAvion + self.soldeBateau
        except Exception:
            return None

    @property
    def cmdMere(self):
        try:
            return  self._data['cde mere'].sum()
        except Exception:
            return None

    @property
    def anneeCmd(self):
        return self._client.annee_cmd

    @property
    def nomClient(self):
        return self._client.nom_client

    @property
    def semaineCmd(self):
        return self._semaine_cmd

    @property
    def id_client(self):
        return self._client.num_client

    @property
    def decrire(self):
        return {
            "num_client": self.id_client ,
            "client": self.nomClient,
            "annee": self.anneeCmd,
            "semaine": self.semaineCmd,
            "cmd_mere": self.cmdMere,
            "solde_bateau": self.soldeBateau,
            "solde_avion": self.soldeAvion,
            "solde": self.solde,
        }




