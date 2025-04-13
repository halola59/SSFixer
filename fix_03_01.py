import os
import pandas as pd
import logging

def fix_03_01(input_file_path, logger, clogger=None):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Hvis c0020 er tom, slett hele linjen
        rows_with_empty_c0020 = df[df['c0020'].isna() | (df['c0020'] == '')]
        for index, row in rows_with_empty_c0020.iterrows():
            clogger.info(f"B_03.01: Rad {index} - c0020 er tom, sletter raden.")
        df = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Sett inn True på alle linjer i c0030
        for index, row in df.iterrows():
            if row['c0030'] != 'true':
                clogger.info(f"B_03.01: Rad {index} - setter c0030 til 'true' (var: '{row['c0030']}').")
        df['c0030'] = 'true'

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        clogger.info(f"B_03.01: Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        clogger.info(f"B_03.01: Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        clogger.info(f"B_03.01: Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")

