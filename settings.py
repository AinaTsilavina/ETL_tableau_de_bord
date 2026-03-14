PATH_DATA = {

    "gpec": "\\\\172.31.220.251\\epsilon\\3- DOSSIERS SERVICES\\RH\\GPEC\\TAF\\2.Formation\\16. Tableau de bord\\Modele du PLANNING DE FORMATION.xlsx",
    "planning": "\\\\Appserver\\epsilon\\3- DOSSIERS SERVICES\\Production\\Production\\AINA2025\\FAMILLE\\",
    "qhse":"",
    "solde_cmde": """//appserver/EPSILON/1- COMMANDE/1- RECAP CDE/{client}/SUIVI COMMANDE/{annee}""",


}
PATH_DB = {
    # "db": "sqlite:///D:\\Dev\\project_django\\dashboard_eps\\db.sqlite3", # db pour test
    "db": "sqlite:///C:/inetpub/wwwroot/tableau_de_bord_prod/db.sqlite3", # db pour production
    "sqlApp": {
        'DRIVER_NAME': "mssql+pyodbc",
        'SERVER' : 'appserver',
        'DATABASE' : 'SPMCData',
        'DRIVER' : 'ODBC Driver 17 for SQL Server',
        'USERNAME' : 'sa',
        'PASSWORD' : 'epsilon_230',
    },
}
