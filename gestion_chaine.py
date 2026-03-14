from db.database import SessionLocal
from models.prod import Chaine, InfoChaine
from dataframe import df_Prod


class GestionInfoChaine:

    def __init__(self):
        self.session = SessionLocal()
        self.data_chaine = df_Prod()["info_chaine"]


    def add_chaine(self):
        try:
            for chaine in self.data_chaine.itertuples():
                print(chaine.num, chaine.chef_ch, chaine.chef_prod, chaine.chef_depart)
                chaine_query = self.session.query(InfoChaine).filter(InfoChaine.num == chaine.num).first()
                if chaine_query:
                    chaine_query.chef_ch = chaine.chef_ch
                    chaine_query.chef_prod = chaine.chef_prod
                    chaine_query.chef_depart = chaine.chef_depart
                else:
                    self.session.add(InfoChaine(num = chaine.num,
                                                chef_ch = chaine.chef_ch ,
                                                chef_prod = chaine.chef_prod,
                                                chef_depart = chaine.chef_depart))
                    # pass
                self.session.commit()
                self.session.close()

        except:
            print('insert error!')


class GestionProdChaine:

    def __init__(self):
        self.session = SessionLocal()
        self.data_prod = df_Prod()["prod_chaine"]


    def add_pord(self):
        # try:
            for chaine in self.data_prod.itertuples():
                # print(chaine)
                print(chaine.SDate, chaine.num_chaine, chaine.Eff, chaine.Taux_Retouche)
                chaine_query = self.session.query(Chaine).filter(Chaine.date == chaine.SDate, Chaine.num_chaine_id == chaine.num_chaine).first()
                if chaine_query:
                    chaine_query.efficience = chaine.Eff
                    chaine_query.retouche = chaine.Taux_Retouche
                else:

                    self.session.add(Chaine(efficience = chaine.Eff,
                                                retouche = chaine.Taux_Retouche,
                                                date = chaine.SDate,
                                                num_chaine_id = chaine.num_chaine
                                            )
                                     )
                #     pass
                self.session.commit()
                self.session.close()
        #
        # except:
        #     print('insert error!')





