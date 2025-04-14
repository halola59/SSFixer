import os
import pandas as pd
import logging
from log_utils import CLOG

def fix_03_01(input_file_path, alogger, clogger=None):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Hvis c0020 er tom, slett hele linjen
        rows_with_empty_c0020 = df[df['c0020'].isna() | (df['c0020'] == '')]
        for index, row in rows_with_empty_c0020.iterrows():
            CLOG(clogger, "B_03.01", index, f"c0020 er tom", "Sletter raden")                
        df = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Sett inn True på alle linjer i c0030
        for index, row in df.iterrows():
            if row['c0030'] != 'true':
                CLOG(clogger, "B_03.01", index, f"c0030 er tom", "Setter c0030 til 'true'")                
        df['c0030'] = 'true'

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        #alogger.info(f"B_03.01: Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        #alogger.info(f"B_03.01: Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        #alogger.info(f"B_03.01: Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"EXCEPTION - fix_03_01 - ved behandling av fil {input_file_path}: {e}")

