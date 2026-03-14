"""
Class de gestion des information de formations gpec
"""
import pandas as pd
import os
from fontTools.subset import subset


class Gpec:

    def __init__(self, source_path):
        self._source_path = self._control_path(source_path)
        self._df = None
        self._set_data()

    def _control_path(self, path):
        if os.path.isfile(path):
            return path
        else:
            raise FileNotFoundError(path)

    def _set_data(self):
        # Extraction des données
        try:
            df = pd.read_excel(
                self._source_path,
                header=0, sheet_name=None)

            df = pd.concat(df)[["Mle",	"NOM",	"PRENOM",	"FONCTIONS",	"DEPARTEMENTS",
                                      "GROUPE",	"DATE DEBUT",	"DATE FIN",	"HEURE DEBUT",	"HEURE FIN",
                                      "INTITULE",	"SALLE",	"REMARQUE",	"CODE"]
            ].rename_axis(['TYPE', 'index']).reset_index().drop('index', axis=1)
            # Nettoyage des données
            df["Mle"] = df["Mle"].astype(int)
            df["NOM"] = df["NOM"].str.upper().str.strip()
            df["PRENOM"] = df["PRENOM"].str.upper().str.strip()
            df["FONCTIONS"] = df["FONCTIONS"].str.upper().str.strip()
            df["DEPARTEMENTS"] = df["DEPARTEMENTS"].str.capitalize().str.strip()
            df["GROUPE"] = df["GROUPE"].str.upper().str.strip()
            df["INTITULE"] = df["INTITULE"].str.upper().str.strip()
            df["SALLE"] = df["SALLE"].str.upper().str.strip()
            self._df = df
            self._df.rename(columns={x:x.replace(" ", "_") for x in self.df.columns.tolist()}, inplace=True)
        except Exception:
            raise KeyError("Certainnes colonnes ne correspondent pas au fichier excel!")

    @property
    def df(self):
        return self._df



class Participant:
    def __init__(self,df_gpec):
        self._df_gpec = df_gpec
        self._type = None
        self._data =None
        self._set_type()
        self._set_data()


    def _set_data(self):
        if self._df_gpec is not None:
            df = self._df_gpec[["Mle",	"NOM",	"PRENOM",	"FONCTIONS",	"DEPARTEMENTS", "TYPE"]].drop_duplicates(subset=['Mle'])
            df["TYPE"] = df["TYPE"].str.upper()
            df["TYPE"] = df["TYPE"].replace({t: str(i) for t, i in zip(self._type["TYPE"], self._type["id_type"])})
            self._data = df
        else:
            raise ValueError("Pas de données à traiter")

    @property
    def data(self):
        return self._data

    def _set_type(self):
        self._type = self._df_gpec[["TYPE"]].drop_duplicates()

        list_type = []
        i = 1
        for nom in self._type["TYPE"]:
            if nom.upper() == "SECTION":
                list_type.append(1)
            else:
                i += 1
                list_type.append(i)

        self._type["TYPE"] = self._type["TYPE"].str.upper()
        self._type["id_type"] = list_type

    @property
    def type(self):
        return self._type


class Formation:

    def __init__(self,df_gpec):
        self._df_gpec = df_gpec
        self._sessions = None
        self._titres = None
        self._set_titres()
        self._set_sessions()


    def _set_titres(self):
        if self._df_gpec is not None:
            self._titres = self._df_gpec[["INTITULE"]].drop_duplicates()

    @property
    def titres(self):
        return self._titres


    def _set_sessions(self):
        if self._df_gpec is not None:
            self._sessions = self._df_gpec[["GROUPE",	"DATE_DEBUT",	"DATE_FIN",	"HEURE_DEBUT",	"HEURE_FIN",
                                      "INTITULE",	"SALLE",	"REMARQUE",	"CODE"]].drop_duplicates()

    @property
    def sessions(self):
        return self._sessions

class SessionParticipant:
    def __init__(self,df_gpec):
        self._df_gpec = df_gpec
        self._data = None
        self._set_data()

    def _set_data(self):
        if self._df_gpec is not None:
            self._data = self._df_gpec[["Mle", "CODE"]]

    @property
    def data(self):
        return self._data







