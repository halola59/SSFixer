import os
import shutil
import logging
from file_utils import clean_file

def process_customer_files_pass1(org_path, res_path, alogger, clogger):
    """
    Lager en kopi av katalogen, fjerner tomme linjer og duplikater fra filene,
    og lagrer dem i den nye katalogen.
    """

    try:
        alogger.info(f"process_customer_files_pass1: {org_path} -> {res_path}")
    
        # Sørg for at hovedmappen til res_path eksisterer
        os.makedirs(res_path, exist_ok=True)

        # Iterer gjennom alle filene i både META-INF og reports underkataloger
        for subfolder in ['META-INF', 'reports']:
            subfolder_path = os.path.join(org_path, subfolder)

            # Sjekk at katalogen eksisterer
            if os.path.isdir(subfolder_path):
                # Lag subfolder i res_path hvis den ikke finnes
                subfolder_output_path = os.path.join(res_path, subfolder)
                os.makedirs(subfolder_output_path, exist_ok=True)

                for filename in os.listdir(subfolder_path):
                    input_file_path = os.path.join(subfolder_path, filename)
                    alogger.info(f"Prosesserer fil: {input_file_path}")

                    if os.path.isfile(input_file_path):
                        # Lag output filbane i .P1 katalogen
                        output_file_path = os.path.join(subfolder_output_path, filename)

                        # Rens filen
                        clean_file(input_file_path, output_file_path, alogger)

    except Exception as e:
        alogger.error(f"EXCEPTION: process_customer_files_pass1 - Feil ved prosessering av katalog {org_path}: {e}")

