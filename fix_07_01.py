import os
import pandas as pd
from datetime import datetime
import logging

def fix_07_01(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0020
        df['c0020'] = df['c0020'].str.strip()

        # Filtrer ut linjene der c0020 ikke er utfylt (NaN eller tom verdi)
        df_cleaned = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Fyll c0090 med "eba_ZZ:x798" hvis den er tom (NaN eller tom verdi)
        df_cleaned['c0090'] = df_cleaned['c0090'].fillna('eba_ZZ:x798')

        # Sjekk og oppdater c0070 med 9999-12-31 hvis tom
        df_cleaned['c0070'] = df_cleaned['c0070'].fillna('9999-12-31')

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df_cleaned.to_csv(temp_output_file_path, index=False)

        logger.info(f"Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        logger.info(f"Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        logger.info(f"Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")
