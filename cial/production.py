"""
Class de gestion des information et données productions.
"""

import pandas as pd


class Production:
    def __init__(self, connexion):
        self._query = """
            Select CAST(CD.ScanDate AS DATE) as Date, PO.Client, SUM(Quantity) Prod from GP_Conveyor_Data CD, GP_Production_Order AS PO
            WHERE PO.ProductionOrderNo = CD.ProductionOrderNo 
            AND CD.Post  = 'HA0002'
            AND YEAR(CD.ScanDate) = YEAR(GetDate())
            GROUP BY CD.ScanDate, PO.Client
            ORDER BY CD.ScanDate DESC
        """

        self._df = None

        self._set_df(connexion)

    def _set_df(self, connexion):
        self._df = pd.read_sql_query(self._query, connexion.engine)

        #Transformation
        self._df["Client"] = self._df["Client"].replace("LAFONT", "CEPOVETT")

        cli_externe = ["CEPOVETT","FRISTADS KANSAS","HEXONIA","PETIT BATEAU","WENAAS","YATCHING","SAE","LACOSTE"]
        self._df.loc[~self._df["Client"].isin(cli_externe), "Client"] = "LOCAUX"

        #Création mapping ID
        mapping_id = {client: idx+1 for idx, client in enumerate(cli_externe)}
        mapping_id["LOCAUX"] = 100

        self._df["IDClient"] = self._df["Client"].map(mapping_id)

        self._df = (
            self._df.groupby(["Date", "Client", "IDClient"], as_index=False)
            .agg({"Prod": "sum"})
            .sort_values(["Client", "Date"], ascending=[True, True])
            .reset_index(drop=True)
        )

        #Calcule moyenne des 20 dernières valeurs par client
        self._df["Moyenne"] = (
            self._df.groupby("Client")["Prod"]
            .transform(lambda x: x.shift(1).rolling(window=20, min_periods=1).mean())
            .fillna(self._df["Prod"])#Remplacement de NaN
            .astype(int)
        )

       

    @property
    def df(self):
        return self._df
    
#This is my comment