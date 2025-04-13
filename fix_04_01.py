import os
import pandas as pd
import logging

def fix_04_01(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Hvis c0020 er tom, slett hele linjen
        rows_with_empty_c0020 = df[df['c0020'].isna() | (df['c0020'] == '')]
        for index, row in rows_with_empty_c0020.iterrows():
            logger.info(f"B_04.01: Rad {index} - c0020 er tom, sletter raden.")
        df = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Fjern alle duplikatrader
        duplicate_rows = df[df.duplicated(keep=False)]
        for index, row in duplicate_rows.iterrows():
            logger.info(f"B_04.01: Rad {index} - duplikatrad, sletter duplikatet.")
        df = df.drop_duplicates()

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        logger.info(f"Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        logger.info(f"Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        logger.info(f"Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")

