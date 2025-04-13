import os
import pandas as pd


def fix_01_02(input_file_path, alogger, clogger=None):
    try:
        df = pd.read_csv(input_file_path)

        rows_with_empty_c0060 = df[df['c0060'].isna()]
        for index, row in rows_with_empty_c0060.iterrows():
            clogger.info(f"B_01.02: Rad {index} - c0060 er tom, kopierer verdi fra c0010 ('{row['c0010']}').")
        df['c0060'] = df['c0060'].fillna(df['c0010'])

        rows_with_spaces_in_c0110 = df[df['c0110'].astype(str).str.contains(r'\s+')]
        for index, row in rows_with_spaces_in_c0110.iterrows():
            clogger.info(f"B_01.02: Rad {index} - c0110 '{row['c0110']}' har mellomrom, fjerner alle mellomrom.")
        df['c0110'] = df['c0110'].replace({r'\s+': ''}, regex=True)

        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        clogger.info(f"B_01.02: Filen er oppdatert og lagret som: "
                    f"{temp_output_file_path}")

        os.remove(input_file_path)
        clogger.info(f"B_01.02: Originalfilen {input_file_path} er slettet.")

        os.rename(temp_output_file_path, input_file_path)
        clogger.info(f"B_01.02: Oppdatert fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"fix_01_02: Feil ved behandling av fil {input_file_path}: {e}")


