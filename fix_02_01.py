import os
import pandas as pd

from log_utils import CLOG

def fix_02_01(input_file_path, alogger, clogger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # 1. Finn og logg alle rader hvor c0050 er tom
        rows_with_empty_c0050 = df[df['c0050'].isna() | (df['c0050'] == '')]
        for index, row in rows_with_empty_c0050.iterrows():
            CLOG(clogger, "B_02.01", index, "c0050 er tom", f"Setter verdien til 0")

        df['c0050'] = df['c0050'].fillna(0)

        # 2. Finn og logg alle rader der c0030 er "Not Applicable" (uavhengig av stor/liten bokstav)
        df['c0030'] = df['c0030'].fillna('')  # Erstatt NaN med tomt felt først
        df['c0030'] = df['c0030'].astype(str)  # Konverterer til strenger
        rows_with_not_applicable_c0030 = df[df['c0030'].str.contains("Not Applicable", case=False, na=False)]
        for index, row in rows_with_not_applicable_c0030.iterrows():
            CLOG(clogger, "B_02.01", index, "c0030 har verdi 'NA'", f"Setter verdien til 0")

        df['c0030'] = df['c0030'].replace({"not applicable": "", "Not Applicable": "", "Not applicable": ""}, regex=True)

        # 3. Erstatt beløp skrevet som tekst med mellomrom, f.eks. "914 321" skal bli 914321, fjern mellomrom fra tall i c0050
        df['c0050'] = df['c0050'].astype(str)
        rows_with_spaces_in_c0050 = df[df['c0050'].str.contains(r'\s+', regex=True, na=False)]
        for index, row in rows_with_spaces_in_c0050.iterrows():
            CLOG(clogger, "B_02.01", index, f"c0050 '{row['c0050']}' har spaces", "Fjerner alle spaces i c0050")  

        df['c0050'] = df['c0050'].replace({r'\s+': ''}, regex=True)

        # 4. Finn og logg alle rader hvor c0050 ikke er numerisk, konverter kolonne c0050 til numerisk
        rows_with_non_numeric_c0050 = df[~df['c0050'].apply(lambda x: x.replace('.', '', 1).isdigit())]

        for index, row in rows_with_non_numeric_c0050.iterrows():
            CLOG(clogger, "B_02.01", index, f"c0050 '{row['c0050']}' har ikke-numerisk verdi", "Satte verdi til 0")  

        df['c0050'] = pd.to_numeric(df['c0050'], errors='coerce').fillna(0).astype(int)

        # 5. Finn rader der c0020 er 'eba_CO:x3' og c0030 er tom eller c0030 ikke finnes i c0010
        condition = (df['c0020'] == 'eba_CO:x3') & (
            (df['c0030'].isna() | (df['c0030'] == '')) | (~df['c0030'].isin(df['c0010']))
        )
        rows_to_remove = df[condition]
        for index, row in rows_to_remove.iterrows():
            CLOG(clogger, "B_02.01", index, f"c0020={row['c0020']} og c0030='' eksisterer ikke i c0010", "Rad fjernes")  
            
        df_cleaned = df[~condition]

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df_cleaned.to_csv(temp_output_file_path, index=False)

        # Slett original fil etter rensing
        os.remove(input_file_path)
        alogger.info(f"Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        alogger.info(f"Ferdig med rensing av fil: {input_file_path}")

    except Exception as e:
        alogger.error(f"EXCEPTION - fix_02_01: Fil {input_file_path}: {e}")
