from settings import PATH_DATA, PATH_DB
import pandas as pd
import sqlalchemy as sa
import glob
from sqlalchemy import create_engine
import dateparser

from db.db_source import DbConnexion

from cial.clients import Client
from cial.solde_cmd import Solde
from cial.production import Production

from gpec.gpec import Gpec, Participant, Formation, SessionParticipant



def df_Famille():
    chemin_complet = PATH_DATA["planning"]
    try:
        df = pd.read_excel(f"{chemin_complet}suivi production chaine famille Cepovett.xlsx", header=5, sheet_name=None, usecols="A:D")
    except FileNotFoundError:
        return None
    # dico = {"CH ANNUEL PANT":[],"CH HORS ANNUEL PANT":[],"CH  ANNUEL HAUT":[]}
    df = {k: v for k, v in df.items() if "HORS" not in k}
    df = pd.concat(df).rename_axis(['Chaine', 'index']).reset_index().drop('index', axis=1)

    df["Famille"], df["REF"] = df["Famille"].ffill(), df["REF"].ffill()

    df = df[df["Unnamed: 2"] == "ECART"].drop("Unnamed: 2", axis=1)
    # df["Chaine"] = "CH ANNUEL PANT"
    df = df.reindex(['Famille', 'Chaine', 'REF', 'MOYENNE'], axis=1).rename(
        columns={'Famille': 'id', 'Chaine': 'chaine', 'REF': 'references', 'MOYENNE': 'moyenne'})
    df['moyenne'] = df['moyenne'].round().astype(int)

    return df.replace({'id': r'\D'},value= '', regex=True)


def df_Qhse():
    # chemin_complet = "\\\\Appserver\\epsilon\\3- DOSSIERS SERVICES\\QHSE\\Système intégré QHSE\\9.2 Audits\\"
    try:
        chemin_complet = glob.glob(f"//Appserver/epsilon/3- DOSSIERS SERVICES/QHSE/Système intégré QHSE/9 EVALUATION DES PERFORMANCES/9.2 Audits/Ecran QHSE*.xlsx")[0]
        # Chargement de la source
        dfSource = pd.read_excel(chemin_complet, header=2)
    except FileNotFoundError:
        return None
    dfSource.dropna(how='all', axis=1, inplace=True)

    # Isolation des données de certifaction
    dfSertificat = pd.DataFrame(dfSource.columns[1:], columns=[dfSource.columns[0]])

    # Extraction des legendes
    dfLegende = dfSource[6:].dropna(axis=1)["CERTIFICATIONS"].str.split("=", expand=True)
    dfLegende.columns = ["couleur", "Description"]
    dfLegende["couleur"] = dfLegende["couleur"].str.strip()
    dfLegende["Description"] = dfLegende["Description"].str.strip()
    dfLegende["id"] = [x for x in range(1, len(dfLegende) + 1)]

    # Traitement des données sur les audits
    # Extraction
    dfAudit = dfSource[:5]

    # Mise en forme de la table de données
    dfTmp = dfAudit["CERTIFICATIONS"].str.extract(r"(DATE DERNIER AUDIT )(\D*)", expand=False)
    dfTmp[1] = dfTmp[1].ffill()
    dfTmp.drop([0], axis=1, inplace=True)
    dfTmp.columns = ["Type Audit"]
    dfAudit = pd.concat([dfAudit, dfTmp], axis=1)
    dfAudit["CERTIFICATIONS"] = dfAudit["CERTIFICATIONS"].replace(to_replace=r'^DATE(.*)', value='Date Audit', regex=True)
    dfAudit = dfAudit.pivot(index="Type Audit", columns='CERTIFICATIONS')

    df = pd.melt(dfAudit.T.reset_index(), id_vars=["level_0", "CERTIFICATIONS"], var_name="Type", value_name="Values")
    df.set_index(['Type', 'level_0'], inplace=True)
    df = df.pivot(columns='CERTIFICATIONS', values='Values').reset_index()
    df.dropna(subset=["RESULTAT"], inplace=True)
    # Mise en place de la colonne "RESULTAT" en corelation avec la table dfLegende
    df["RESULTAT"] = df["RESULTAT"].replace({c: str(i) for c, i in zip(dfLegende["couleur"], dfLegende["id"])})

    # renommage des colonnes
    df.columns = ["type", "certificat", "date", "resultat", "service"]
    df = df.reindex(["type", "certificat", "date", "service", "resultat"], axis=1)

    # traitement de la colonne 'date'
    df["date"] = df["date"].apply(lambda x: dateparser.parse("01" + x).date() if type(x) is str else x)


    return {"certification": dfSertificat, "legende": dfLegende, "data": df}


# DATAFRAME QHSE VERSION 2
def df_Qhse2():
    #Extraction des données
    df = pd.read_excel(
        "\\\\appserver\\EPSILON\\3- DOSSIERS SERVICES\\QHSE\\Système intégré QHSE\\9 EVALUATION DES PERFORMANCES\\9.2 Audits\\SUIVI DES NC PAR REFERENTIEL V2.xlsx",
        header=0, sheet_name=None)

    # Fusion des deux feuilles
    df = pd.concat(df)[["REFERENTIEL", "DATE AUDIT", "NON-CONFORMITE MAJEURE", "NON-CONFORMITE MINEURE", "RESULTAT",
                        "SERVICES AUDITES"]].rename_axis(['TYPE', 'index']).reset_index().drop('index', axis=1)
    df['TYPE'] = df['TYPE'].str.upper().apply(lambda x: x.replace('AUDIT ', ''))

    #     Création de la table legende et faire correspondre les couleur à leur id
    df_legende = pd.DataFrame({'couleur': ['Rouge', 'Jaune', 'Vert'], 'id': [1, 2, 3]})
    df["RESULTAT"] = df["RESULTAT"].replace({c: str(i) for c, i in zip(df_legende["couleur"], df_legende["id"])})

    #     Extraction de la table audit
    df_audit = df[["TYPE", "REFERENTIEL", "DATE AUDIT", "SERVICES AUDITES", "RESULTAT"]]

    #     Extraction de la table NC
    df_NC = df.melt(id_vars=['TYPE', 'REFERENTIEL', 'DATE AUDIT', 'SERVICES AUDITES', 'RESULTAT'],
                    value_vars=['NON-CONFORMITE MAJEURE', 'NON-CONFORMITE MINEURE'], var_name='NC',
                    value_name='nombre').sort_values(['TYPE', 'REFERENTIEL', 'DATE AUDIT'],
                                                     ascending=[True, True, False])
    df_NC['NC'] = df_NC['NC'].apply(lambda x: x.replace('NON-CONFORMITE ', ''))

    df_audit.columns = ["type", "certificat", "date", "service", "resultat"]
    df_NC.columns = ["type", "certificat", "date", "service", "resultat", "nc", "nombre"]

    return {'audit': df_audit, 'legende': df_legende, 'NC': df_NC}


def df_Prod():

    appserver = PATH_DB["sqlApp"]
    connexion = DbConnexion(appserver)

    SQL_QUERY_INFO_CHAINE = """
        SELECT S.SectionCode as num, Responsible as chef_ch, Module as chef_prod,   S.CheckPointDescription02 AS chef_depart
        FROM GP_Site_Section S
        WHERE S.CheckPointDescription02 IS NOT NULL AND S.SectionCode LIKE 'CH%' AND S.SectionCode NOT LIKE 'CHAINE%'
        ORDER BY S.SectionCode       
    """

    SQL_QUERY_CHAINE = """            
        DECLARE @DateDebut as DateTime
        DECLARE @DateFin as DateTime
        
        
        SET @DateFin  = CONVERT (date, DATEADD(day,1,GETDATE()))
        SET @DateDebut = DATEADD(day,1, EOMONTH(@DateFin,-1));
        --SET @DateDebut ='01 JUN 25'
        --SET @DateFin  ='31 JUN 25';
        
        
        WITH tb_prod AS (Select S.*,
               ISNULL((SELECT SUM(Quantity) FROM GP_Conveyor_Data AS CD
                         WHERE CD.ScanDate    = S.ScanDate
                         AND   CD.SiteCode    = S.SiteCode
                         AND   CD.SectionCode = S.SectionCode
                         AND   CD.Post        = 'LM0300'
                        ),0) AS Qty_Rep,
                ISNULL((SELECT SUM(Quantity) FROM GP_Conveyor_Data AS CD
                         WHERE CD.ScanDate    = S.ScanDate
                         AND   CD.SiteCode    = S.SiteCode
                         AND   CD.SectionCode = S.SectionCode
                         AND   CD.Post        = 'HA0002'
                ),0) AS Qty_Pack,
                    ISNULL((SELECT SUM(Quantity) FROM GP_Conveyor_Data AS CD
                         WHERE CD.ScanDate    = S.ScanDate
                         AND   CD.SiteCode    = S.SiteCode
                         AND   CD.SectionCode = S.SectionCode
                         AND   CD.Post        = 'LM0400'
                       ),0) AS Qty_Sec,
                        ISNULL((SELECT SUM(Quantity) FROM GP_Conveyor_Data AS CD
                         WHERE CD.ScanDate    = S.ScanDate
                         AND   CD.SiteCode    = S.SiteCode
                         AND   CD.SectionCode = S.SectionCode
                         AND   CD.Post        = 'HA0002'
                        ),0) AS Qty_Prod
        FROM vw_Lean_Section_Max_Scan AS S)
        
        SELECT P.[ScanDate] as SDate, P.[SectionCode] as num_chaine
            ,CASE SUM([MinutesPresent]) WHEN 0 THEN NULL ELSE convert(numeric(10,2),(SUM([MinutesWorked])/SUM([MinutesPresent]))* 100) END AS [Eff],	  

           (CASE sum(Qty_Pack) WHEN 0 THEN 0
            ELSE
            ROUND(((convert(numeric(10,2),SUM(Qty_Rep)) / (convert(numeric(10,2),SUM(Qty_Prod)))*100)),1)
            END
           ) AS [Taux_Retouche],
           
           (CASE sum(Qty_Pack) WHEN 0 THEN 0
            ELSE
            ROUND(((convert(numeric(10,2),SUM(Qty_Sec)) / (convert(numeric(10,2),SUM(Qty_prod)))*100)),1)
            END
           ) AS [Taux_2nd_Choix]
        FROM [SPMCData].[dbo].[GP_Site_Presence_Summary] P INNER JOIN tb_prod ON tb_prod.ScanDate = P.ScanDate AND tb_prod.SectionCode = P.SectionCode
        WHERE P.[SectionCode] LIKE 'CH%'
        GROUP BY P.[ScanDate], P.[SectionCode]
        HAVING P.[ScanDate] BETWEEN @DateDebut AND @DateFin
        ORDER BY P.[ScanDate], P.[SectionCode]
    """
    # connection_url = sa.engine.URL.create(
    #     "mssql+pyodbc",
    #     username=appserver["USERNAME"],
    #     password=appserver["PASSWORD"],
    #     host=appserver["SERVER"],
    #     database=appserver["DATABASE"],
    #     query={
    #         "driver": "ODBC Driver 17 for SQL Server",
    #         "autocommit": "True",
    #     },
    # )
    #
    # engine = create_engine(connection_url).execution_options(
    #     isolation_level="AUTOCOMMIT"
    # )

    df_chaine = pd.read_sql_query(SQL_QUERY_CHAINE, connexion.engine)

    df_chaine['SDate'] = pd.to_datetime(df_chaine["SDate"])


    df_info_chaine = pd.read_sql_query(SQL_QUERY_INFO_CHAINE, connexion.engine)
    
    return {'prod_chaine': df_chaine, 'info_chaine': df_info_chaine}


def df_solde_cmd():

    Client.pattern_dossier(PATH_DATA["solde_cmde"])

    params_y = 2025
    client_list = []

    feuille = {"all":"SOLDE COMMANDE", "avion":"SOLDE AVION CDE"}
    column_use = "A:AB"
    client_files = {
        "Cepovett": "RECAP COMMANDE CEPOVETT LAFONT 2025.xlsx",
        "Fristads Kansas": "SOLDE COMMANDE FRISTADS 2025.xlsx",
        "Hexonia": "SOLDE COMMANDE HEXONIA 2025.xlsx",
        "Petit Bateau": "SOLDE COMMANDE  PETIT BATEAU 2025..xlsx",
        "WENAAS": "SOLDE COMMANDE WENAAS 2025.xlsx",
        "Locaux": "SOLDE COMMANDE LOCAL 2025.xlsx",
    }

    solde_list = [Solde(Client(cl, params_y, xl), feuille, column_use) for cl, xl in client_files.items()]

    return pd.DataFrame([solde.decrire for solde in solde_list])

def df_prod_solde():
    connexion = DbConnexion(PATH_DB['sqlApp'])
    prod = Production(connexion)
    return prod.df


def df_gpec():
    gpec = Gpec(PATH_DATA["gpec"])
    formation = Formation(gpec.df)
    participants = Participant(gpec.df)
    sessionsParticipant = SessionParticipant(gpec.df)

    return {"formation": formation.titres,
            "participant": participants.data,
            "sessions": formation.sessions,
            "type": participants.type,
            "sessionsParticipant": sessionsParticipant.data}






