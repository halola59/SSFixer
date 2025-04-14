import os
import pandas as pd
import logging

from log_utils import CLOG

def fix_05_01(input_file_path, alogger, clogger=None):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0010
        rows_with_spaces_in_c0010 = df[df['c0010'].astype(str).str.strip() != df['c0010'].astype(str)]
        for index, row in rows_with_spaces_in_c0010.iterrows():
            CLOG(clogger, "B_05.01", index, f"c0010 '{row['c0010']}' har spaces", "Fjerner leading/trailing spaces")
        df['c0010'] = df['c0010'].str.strip()

        # Fjern alle duplikatrader
        duplicate_rows = df[df.duplicated(keep=False)]
        for index, row in duplicate_rows.iterrows():
            CLOG(clogger, "B_05.01", index, "Raden er duplikatrad", "Sletter raden")   
        df = df.drop_duplicates()

        # Hvis c0020 finnes i flere rader, behold den første og fjern påfølgende
        duplicate_c0010_rows = df[df.duplicated(subset='c0010', keep=False)]
        for index, row in duplicate_c0010_rows.iterrows():
            CLOG(clogger, "B_05.01", index, f"{row['c0010']}' finnes i flere rader", "Sletter raden, beholder kun en forekomst")   
        df = df.drop_duplicates(subset='c0010', keep='first')

        # Oppdater c0020 hvis den er 'eba_qCO:qx2003', sett den til 'eba_qCO:qx2002'
        rows_to_update_c0020 = df[df['c0020'] == 'eba_qCO:qx2003']
        for index, row in rows_to_update_c0020.iterrows():
            CLOG(clogger, "B_05.01", index, "c0020 = 'eba_qCO:qx2003'", "Setter ny verdi til 'eba_qCO:qx2002'") 
        df.loc[df['c0020'] == 'eba_qCO:qx2003', 'c0020'] = 'eba_qCO:qx2002'

        # Sett c0070 til "eba_CT:x212" hvis c0070 er tom (NaN eller tom verdi)
        rows_with_empty_c0070 = df[df['c0070'].isna() | (df['c0070'] == '')]
        for index, row in rows_with_empty_c0070.iterrows():
            CLOG(clogger, "B_05.01", index, "c0070 er tom", "Setter ny verdi til 'eba_CT:x212'") 
        df['c0070'] = df['c0070'].fillna('eba_CT:x212')

        # Sjekk om c0110 er tom, hvis ja, sett den til verdien i c0010
        rows_with_empty_c0110 = df[df['c0110'].isna()]
        for index, row in rows_with_empty_c0110.iterrows():
            CLOG(clogger, "B_05.01", index, "c0110 er tom", f"Kopierer verdi fra c0010 ('{row['c0010']}')") 
        df['c0110'] = df['c0110'].fillna(df['c0010'])

        # Hvis c0100 er tom, sett verdi = 0
        rows_with_empty_c0100 = df[df['c0100'].isna()]
        for index, row in rows_with_empty_c0100.iterrows():
            CLOG(clogger, "B_05.01", index, "c0100 er tom", f"Setter verdien til 0")             
        df['c0100'] = df['c0100'].fillna(0)

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        alogger.info(f"B_05.01: Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        alogger.info(f"B_05.01: Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        alogger.info(f"B_05.01: Renset fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"EXCEPTION - fix_05_01 - ved behandling av fil {input_file_path}: {e}")
