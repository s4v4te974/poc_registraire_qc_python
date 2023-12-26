import os.path

import const as ct
import cloudscraper
import zipfile
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
except psycopg2.Error as e:
    print("Error connecting to the database:")
    print(e)
else:
    print("Connection established successfully")


def download_files():
    scraper = cloudscraper.create_scraper()
    response = scraper.get(ct.URL_REGISTRE, headers=ct.HEADERS)
    if response.status_code == 200:
        print(ct.CONNEXION_SUCCESS, response.status_code)
        content = response.content
        with open(ct.DOWNLOAD_FILE_PATH, 'wb') as file:
            file.write(content)
    else:
        print(ct.FAILED_TO_DOWNLOAD, response.status_code)


def unzip_files():
    with zipfile.ZipFile(ct.DOWNLOAD_FILE_PATH, 'r') as jdzip:
        jdzip.extractall(ct.DOWNLOAD_PATH)
    os.remove(ct.DOWNLOAD_FILE_PATH)


def filter_entreprise_file():
    filtered_chunks: list = []
    chunk_size: int = 100_000

    df = pd.read_csv(ct.ENTREPRISE_BASE, chunksize=chunk_size, iterator=True)

    for chunk in df:
        chunk['DAT_DEPO_DECLR'] = pd.to_datetime(chunk['DAT_DEPO_DECLR'])
        filtered_chunk = chunk.loc[
            ((chunk['IND_FAIL'] == ct.INDICE_FAILLITE) | chunk['IND_FAIL'].isnull()) &
            ((chunk['DAT_CESS_PREVU'] == ct.EMPTY) | (chunk['DAT_CESS_PREVU'].isnull())) &
            (chunk['COD_STAT_IMMAT'] == ct.STATUS_IMMAT) &
            (chunk['COD_FORME_JURI'] != ct.CODE_FORME_JURI) &
            (chunk['DAT_DEPO_DECLR'].dt.year >= ct.LAST_UPDATE)
            ]
        filtered_chunks.append(filtered_chunk)

    return pd.concat(filtered_chunks)


def filter_other_file_by_neq(path: str, df_entreprise):
    df = pd.read_csv(path)
    index_comparison = df['NEQ'].isin(df_entreprise['NEQ'])
    return df[index_comparison]


def filter_other_files_by_code(path: str, df_entreprise):
    df = pd.read_csv(path)
    df['COD_DOM_VAL'] = pd.to_numeric(df['COD_DOM_VAL'], errors='coerce')
    df_entreprise['COD_ACT_ECON_CAE'] = pd.to_numeric(df_entreprise['COD_ACT_ECON_CAE'], errors='coerce')
    index_comparison = df['COD_DOM_VAL'].isin(df_entreprise['COD_ACT_ECON_CAE'])
    return df[index_comparison]


def remove_file():
    files = os.listdir(ct.DOWNLOAD_PATH)
    for file_name in files:
        file_path = os.path.join(ct.DOWNLOAD_PATH, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def main():
    download_files()
    print(ct.DOWNLOAD_SUCCESS)
    unzip_files()
    print(ct.UNZIP_SUCCESS)

    df_entreprise = filter_entreprise_file()
    df_etablissements = filter_other_file_by_neq(ct.ETABLISSEMENT_BASE, df_entreprise)
    df_conti_transfo = filter_other_file_by_neq(ct.TRANSFO_BASE, df_entreprise)
    df_fu_sci = filter_other_file_by_neq(ct.FUSCI_BASE, df_entreprise)
    df_nom = filter_other_file_by_neq(ct.NOM_BASE, df_entreprise)
    df_domaine_valeur = filter_other_files_by_code(ct.DOMAINE_BASE, df_entreprise)
    print("all csv are filtered with success")

    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/registraire')
    df_entreprise.to_sql('entreprise', engine, if_exists='replace', index=False)
    df_etablissements.to_sql('etablissement', engine, if_exists='replace', index=False)
    df_conti_transfo.to_sql('continuationtransformation', engine, if_exists='replace', index=False)
    df_fu_sci.to_sql('fusionscission', engine, if_exists='replace', index=False)
    df_nom.to_sql('nom', engine, if_exists='replace', index=False)
    df_domaine_valeur.to_sql('domainevaleur', engine, if_exists='replace', index=False)
    print("DB insertion success")

    conn.close()

    remove_file()


main()
