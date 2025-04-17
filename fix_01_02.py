import os
import pandas as pd
from log_utils import CLOG


def fix_01_02(input_file_path, alogger, clogger=None):
    try:
        df = pd.read_csv(input_file_path)

        # c0060 er tom
        rows_with_empty_c0060 = df[df['c0060'].isna()]
        for index, row in rows_with_empty_c0060.iterrows():
            CLOG(clogger, "B_01.02", index, "c0060 er tom", f"Kopierer verdi fra c0010 ('{row['c0010']}')")
        df['c0060'] = df['c0060'].fillna(df['c0010'])

        # c0110 inneholder spaces foran eller bak
        rows_with_spaces_in_c0110 = df[df['c0110'].astype(str).str.contains(r'\s+')]
        for index, row in rows_with_spaces_in_c0110.iterrows():
            CLOG(clogger, "B_01.02", index, f"c0110 '{row['c0110']}' har spaces", "Fjerner leading/trailing spaces i c0110")
        df['c0110'] = df['c0110'].replace({r'\s+': ''}, regex=True)

        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        #alogger.info(f"B_01.02: Filen er oppdatert og lagret som: " f"{temp_output_file_path}")

        os.remove(input_file_path)
        #alogger.info(f"B_01.02: Originalfilen {input_file_path} er slettet.")

        os.rename(temp_output_file_path, input_file_path)
        #alogger.info(f"B_01.02: Oppdatert fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"EXCEPTION - fix_01_02: Feil ved behandling av fil {input_file_path}: {e}")


