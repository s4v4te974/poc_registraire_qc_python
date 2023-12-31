from utils import const as ct
import psycopg2
import service.dataframe_service as df_service
import repository.data_insertion as dao
from service import retrieve_file as retrieve

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


def main():
    try:
        retrieve.remove_file()
        retrieve.download_and_unzip_file()

        df_entreprise = df_service.filter_entreprise_file()
        df_etablissements = df_service.filter_other_file_by_neq(ct.ETABLISSEMENT_BASE, df_entreprise)
        df_conti_transfo = df_service.filter_other_file_by_neq(ct.TRANSFO_BASE, df_entreprise)
        df_fu_sci = df_service.filter_other_file_by_neq(ct.FUSCI_BASE, df_entreprise)
        df_nom = df_service.filter_other_file_by_neq(ct.NOM_BASE, df_entreprise)
        df_domaine_valeur = df_service.filter_other_files_by_code(ct.DOMAINE_BASE, df_entreprise)
        print("all df_service are filtered with success")

        list_df_uuid = [df_etablissements, df_conti_transfo, df_fu_sci, df_nom]
        df_service.generate_uuid(list_df_uuid)
        print("uuid generated with success")

        list_df_rename = [df_entreprise, df_domaine_valeur, df_fu_sci, df_etablissements, df_conti_transfo, df_nom]
        df_service.rename_dfs(list_df_rename)
        print("column rename with success")

        dao.insert_entreprise(df_entreprise)
        dao.insert_etablissement(df_etablissements)
        dao.insert_conti_transfo(df_conti_transfo)
        dao.insert_nom(df_nom)
        dao.insert_domaine_valeur(df_domaine_valeur)
        dao.insert_fu_sci(df_fu_sci)

        print("DB insertion success")

        conn.close()
    except BaseException as be:
        print("error occurred during the process")
        print(be)
    finally:
        print("final")
        retrieve.remove_file()


main()
