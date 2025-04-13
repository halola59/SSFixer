import os
import pandas as pd
import logging

def fix_03_02(input_file_path, alogger, clogger=None):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0020
        rows_with_spaces_in_c0020 = df[df['c0020'].astype(str).str.strip() != df['c0020'].astype(str)]
        for index, row in rows_with_spaces_in_c0020.iterrows():
            alogger.info(f"B_03.02: Rad {index} - c0020 '{row['c0020']}' har mellomrom, fjerner leading/trailing spaces.")
        df['c0020'] = df['c0020'].str.strip()

        # Fjern linjer der c0020 er tom (NaN eller tom verdi)
        rows_with_empty_c0020 = df[df['c0020'].isna() | (df['c0020'] == '')]
        for index, row in rows_with_empty_c0020.iterrows():
            clogger.info(f"B_03.02: Rad {index} - c0020 er tom, sletter raden.")
        df_cleaned = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df_cleaned.to_csv(temp_output_file_path, index=False)

        clogger.info(f"B_03.02: Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        clogger.info(f"B_03.02: Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        clogger.info(f"B_03.02: Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")
