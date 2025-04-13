import os
import pandas as pd
from datetime import datetime
import logging

def fix_07_01(input_file_path, alogger, clogger=None):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0020
        rows_with_spaces_in_c0020 = df[df['c0020'].astype(str).str.strip() != df['c0020'].astype(str)]
        for index, row in rows_with_spaces_in_c0020.iterrows():
            clogger.info(f"B_07.01: Rad {index} - c0020 '{row['c0020']}' har mellomrom, fjerner leading/trailing spaces.")
        df['c0020'] = df['c0020'].str.strip()

        # Filtrer ut linjene der c0020 ikke er utfylt (NaN eller tom verdi)
        rows_with_empty_c0020 = df[df['c0020'].isna() | (df['c0020'] == '')]
        for index, row in rows_with_empty_c0020.iterrows():
            clogger.info(f"B_07.01: Rad {index} - c0020 er tom, sletter raden.")
        df_cleaned = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Fyll c0090 med "eba_ZZ:x798" hvis den er tom (NaN eller tom verdi)
        rows_with_empty_c0090 = df_cleaned[df_cleaned['c0090'].isna() | (df_cleaned['c0090'] == '')]
        for index, row in rows_with_empty_c0090.iterrows():
            clogger.info(f"B_07.01: Rad {index} - c0090 er tom, setter verdi til 'eba_ZZ:x798'.")
        df_cleaned['c0090'] = df_cleaned['c0090'].fillna('eba_ZZ:x798')

        # Sjekk og oppdater c0070 med 9999-12-31 hvis tom
        rows_with_empty_c0070 = df_cleaned[df_cleaned['c0070'].isna() | (df_cleaned['c0070'] == '')]
        for index, row in rows_with_empty_c0070.iterrows():
            clogger.info(f"B_07.01: Rad {index} - c0070 er tom, setter verdi til '9999-12-31'.")
        df_cleaned['c0070'] = df_cleaned['c0070'].fillna('9999-12-31')

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df_cleaned.to_csv(temp_output_file_path, index=False)

        alogger.info(f"B_07.01: Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        alogger.info(f"B_07.01: Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        alogger.info(f"B_07.01: Renset fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")
