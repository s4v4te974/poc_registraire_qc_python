import os

# begin part donwload and unzip

# url to download file
URL_REGISTRE: str = ('https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_22A_PIU_RecupDonnPub_PC'
                     '/FichierDonneesOuvertes.aspx')

DOWNLOAD_PATH: str = os.path.join(os.path.dirname(__file__), r'download\\')
DOWNLOAD_FILE_PATH: str = os.path.join(DOWNLOAD_PATH, 'jeuxDonnees.zip')

# error message
FAILED_TO_DOWNLOAD: str = 'failed to download the file'
FAILED_TO_UNZIP: str = 'failed to unzip file'

# good message
DOWNLOAD_SUCCESS: str = 'Download files with success'
CONNEXION_SUCCESS: str = 'Connexion with server success : '

# Http utils
HEADERS: dict = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                  'Safari/537.3',
    'Connection': 'keep-alive',
}

# end part download and unzip

# filter constant
STATUS_IMMAT: str = 'IM'
EMPLOYEE_NUMBER: str = 'A'
CODE_FORME_JURI: str = 'IND'
LAST_UPDATE: int = 2013