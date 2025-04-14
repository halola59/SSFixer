import os
import pandas as pd

from log_utils import CLOG

def fix_07_01(input_file_path, alogger, clogger=None):
    try:
        df = pd.read_csv(input_file_path)

        # --- Trim spaces i c0020 ---
        mask_spaces = df['c0020'].astype(str).str.strip() != df['c0020'].astype(str)
        for index in df[mask_spaces].index:
            verdi = df.at[index, 'c0020']
            CLOG(clogger, "B_07.01", index, f"c0020 '{verdi}' har spaces", "Fjerner leading/trailing spaces")

        df['c0020'] = df['c0020'].astype(str).str.strip()

        # --- Fjern rader med tom c0020 ---
        mask_empty_c0020 = df['c0020'].isna() | (df['c0020'] == '')
        for index in df[mask_empty_c0020].index:
            CLOG(clogger, "B_06.01", index, f"c0040 er tom", f"Sletter raden")
        df_cleaned = df[~mask_empty_c0020].copy()

        # --- Fyll ut c0090 med 'eba_ZZ:x798' hvis tom ---
        mask_empty_c0090 = df_cleaned['c0090'].isna() | (df_cleaned['c0090'] == '')
        for index in df_cleaned[mask_empty_c0090].index:
            CLOG(clogger, "B_07.01", index, f"c0090 er tom", f"Setter verdi til 'eba_ZZ:x798'")            
        df_cleaned.loc[mask_empty_c0090, 'c0090'] = 'eba_ZZ:x798'

        # --- Fyll ut c0070 med '9999-12-31' hvis tom ---
        mask_empty_c0070 = df_cleaned['c0070'].isna() | (df_cleaned['c0070'] == '')
        for index in df_cleaned[mask_empty_c0070].index:
            CLOG(clogger, "B_07.01", index, f"c0070 er tom", f"Setter verdi til '9999-12-31'")      
            
        df_cleaned['c0070'] = df_cleaned['c0070'].astype(str)
        df_cleaned.loc[mask_empty_c0070, 'c0070'] = '9999-12-31'

        # --- Sett c0050 til 'eba_ZZ:x963' hvis tom og c0110 == eba_BT:x21 ---
        mask_c0050_empty = df_cleaned['c0050'].isna() | (df_cleaned['c0050'] == '')
        mask_c0110 = df_cleaned['c0110'] == 'eba_BT:x21'
        mask_combined = mask_c0050_empty & mask_c0110
        for index in df_cleaned[mask_combined].index:
            CLOG(clogger, "B_07.01", index, f"c0050 er tom og c0110 = 'eba_BT:x21'", f"Setter verdi til 'eba_ZZ:x963'")               
        df_cleaned.loc[mask_combined, 'c0050'] = 'eba_ZZ:x963'

        # --- Lagre og bytt ut fil ---
        temp_output_file_path = f"{input_file_path}.temp"
        df_cleaned.to_csv(temp_output_file_path, index=False)
        #alogger.info(f"B_07.01: Filen er renset og lagret som: {temp_output_file_path}")

        os.remove(input_file_path)
        #alogger.info(f"B_07.01: Originalfilen {input_file_path} er slettet.")

        os.rename(temp_output_file_path, input_file_path)
        #alogger.info(f"B_07.01: Renset fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"EXCEPTION - fix_07_01 - ved behandling av fil {input_file_path}: {e}")
