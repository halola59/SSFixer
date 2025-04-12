import os
import pandas as pd
import logging

def fix_03_02(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0020
        df['c0020'] = df['c0020'].str.strip()

        # Fjern linjer der c0020 er tom (NaN eller tom verdi)
        df_cleaned = df[df['c0020'].notna() & (df['c0020'] != '')]

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
