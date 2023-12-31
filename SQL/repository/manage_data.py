from sqlalchemy import create_engine, text
from mapper import registraire_mappers

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/registraire')

chunk_size = 10_000
entreprise = 'entreprise'
etablissement = 'etablissement'
continuationtransformation = 'continuationtransformation'
fusionscission = 'fusionscission'
nom = 'nom'
domainevaleur = 'domainevaleur'


def insert_entreprise(dataframe):
    df_entreprise = registraire_mappers.map_entreprise(dataframe)
    df_entreprise.to_sql(entreprise, engine, if_exists='append', index=False, chunksize=chunk_size)


def insert_etablissement(dataframe):
    df_etablissement = registraire_mappers.map_etablissement(dataframe)
    df_etablissement.to_sql(etablissement, engine, if_exists='append', index=False, chunksize=chunk_size)


def insert_conti_transfo(dataframe):
    df_conti_transfo = registraire_mappers.map_conti_transfo(dataframe)
    df_conti_transfo.to_sql(continuationtransformation, engine, if_exists='append', index=False, chunksize=chunk_size)


def insert_fu_sci(dataframe):
    df_fu_sci = registraire_mappers.map_fu_sci(dataframe)
    df_fu_sci.to_sql(fusionscission, engine, if_exists='append', index=False, chunksize=chunk_size)


def insert_nom(dataframe):
    df_nom = registraire_mappers.map_nom(dataframe)
    df_nom.to_sql(nom, engine, if_exists='append', index=False, chunksize=chunk_size)


def insert_domaine_valeur(dataframe):
    df_domaine_valeur = registraire_mappers.map_domaine_valeur(dataframe)
    df_domaine_valeur.to_sql(domainevaleur, engine, if_exists='append', index=False, chunksize=chunk_size)


def delete_all_table():
    with engine.connect() as connection:
        count = connection.execute(text(f"SELECT COUNT(*) FROM {entreprise};"))
        print(count.scalar())
        connection.execute(text(f"TRUNCATE TABLE {entreprise};"))
        connection.execute(text(f"TRUNCATE TABLE {etablissement};"))
        connection.execute(text(f"TRUNCATE TABLE {continuationtransformation};"))
        connection.execute(text(f"TRUNCATE TABLE {fusionscission};"))
        connection.execute(text(f"TRUNCATE TABLE {nom};"))
        connection.execute(text(f"TRUNCATE TABLE {domainevaleur};"))
        count = connection.execute(text(f"SELECT COUNT(*) FROM {entreprise};"))
        print(count.scalar())
        connection.commit()
