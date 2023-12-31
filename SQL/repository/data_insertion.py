from sqlalchemy import create_engine
from mapper import registraire_mappers

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/registraire')


def insert_entreprise(dataframe):
    df_entreprise = registraire_mappers.map_entreprise(dataframe)
    print("insert entreprise")
    df_entreprise.to_sql('entreprise', engine, if_exists='append', index=False)


def insert_etablissement(dataframe):
    df_etablissement = registraire_mappers.map_etablissement(dataframe)
    print("insert etab")
    df_etablissement.to_sql('etablissement', engine, if_exists='append', index=False)


def insert_conti_transfo(dataframe):
    df_conti_transfo = registraire_mappers.map_conti_transfo(dataframe)
    print("insert conti")
    df_conti_transfo.to_sql('continuationtransformation', engine, if_exists='append', index=False)


def insert_fu_sci(dataframe):
    df_fu_sci = registraire_mappers.map_fu_sci(dataframe)
    df_fu_sci.to_sql('fusionscission', engine, if_exists='append', index=False)


def insert_nom(dataframe):
    df_nom = registraire_mappers.map_nom(dataframe)
    df_nom.to_sql('nom', engine, if_exists='append', index=False)


def insert_domaine_valeur(dataframe):
    df_domaine_valeur = registraire_mappers.map_domaine_valeur(dataframe)
    df_domaine_valeur.to_sql('domainevaleur', engine, if_exists='append', index=False)
