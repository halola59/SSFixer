import os
import pandas as pd
import logging
from datetime import datetime, timedelta

def fix_02_02(input_file_path, alogger, clogger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Hvis c0090 er tom, sett inn 'eba_CO:x4'
        df['c0090'] = df['c0090'].fillna('eba_CO:x4')

        # 1. Finn og logg alle rader der c0080 er mindre enn c0070, Logg rader som trenger korrigering
        not_maxdate_condition = df['c0080'] != '31-12-9999'
        filtered_df = df[not_maxdate_condition].copy()

        filtered_df['c0070'] = filtered_df['c0070'].apply(pd.to_datetime, errors='coerce')
        filtered_df['c0080'] = filtered_df['c0080'].apply(pd.to_datetime, errors='coerce')

        condition = filtered_df['c0080'] < filtered_df['c0070']
        rows_to_correct = filtered_df[condition]

        for index, row in rows_to_correct.iterrows():
            clogger.info(f"B_02.02: Rad {index} - c0080 ({row['c0080']}) < c0070 ({row['c0070']}), endrer c0080 til c0070 + 1.")

        filtered_df.loc[condition, 'c0080'] = filtered_df['c0070'] + pd.Timedelta(days=1)
        filtered_df['c0070'] = filtered_df['c0070'].dt.strftime('%Y-%m-%d')
        filtered_df['c0080'] = filtered_df['c0080'].dt.strftime('%Y-%m-%d')

        df.update(filtered_df)

        # Hvis c0100 er tom, sett verdi = 90
        rows_with_empty_c0100 = df[df['c0100'].isna()]
        for index, row in rows_with_empty_c0100.iterrows():
            clogger.info(f"B_02.02: Rad {index} - c0100 er tom, setter verdi til 90.")
        df['c0100'] = df['c0100'].fillna(90)

        # Fjern leading og trailing spaces fra c0030
        rows_with_spaces_in_c0030 = df[df['c0030'].astype(str).str.strip() != df['c0030'].astype(str)]
        for index, row in rows_with_spaces_in_c0030.iterrows():
            clogger.info(f"B_02.02: Rad {index} - c0030 '{row['c0030']}' har mellomrom, fjerner leading/trailing spaces.")
        df['c0030'] = df['c0030'].str.strip()

        # Hvis c0110 er tom, sett verdi = c0100
        rows_with_empty_c0110 = df[df['c0110'].isna()]
        for index, row in rows_with_empty_c0110.iterrows():
            clogger.info(f"B_02.02: Rad {index} - c0110 er tom, setter verdi til c0100 ({row['c0100']}).")
        df['c0110'] = df['c0110'].fillna(df['c0100'])

        # Hvis c0150 er tom og c0140 er tom, kopier verdien fra c0130 til c0150
        rows_with_empty_c0150_c0140 = df[df['c0150'].isna() & df['c0140'].isna()]
        for index, row in rows_with_empty_c0150_c0140.iterrows():
            clogger.info(f"B_02.02: Rad {index} - c0150 og c0140 er tomme, kopierer verdi fra c0130 ({row['c0130']}) til c0150.")
        df.loc[df['c0150'].isna() & df['c0140'].isna(), 'c0150'] = df['c0130']

        # Finn radene der c0140 er 'eba_BT:x29' og c0150 er tom
        condition = (df['c0140'] == 'eba_BT:x29') & (df['c0150'].isna() | (df['c0150'] == ''))
        rows_to_set_not_applicable = df[condition]
        for index, row in rows_to_set_not_applicable.iterrows():
            clogger.info(f"B_02.02: Rad {index} - c0140 er 'eba_BT:x29' og c0150 er tom, setter c0150 til 'eba_GA:x28'.")

        df.loc[condition, 'c0150'] = 'eba_GA:x28'

        # Hvis c0160 er tom, kopier verdien fra c0130 til c0160
        df['c0160'] = df['c0160'].fillna(df['c0130'])

        # Slett rader der c0020 er tom
        df = df[df['c0020'].notna() & (df['c0020'] != '')]

        # Slett rader der c0040 er tom
        df = df[df['c0040'].notna() & (df['c0040'] != '')]

        # Slett rader der c0050 er tom
        df = df[df['c0050'].notna() & (df['c0050'] != '')]

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        alogger.info(f"Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        alogger.info(f"Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        alogger.info(f"Renset fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"EXCEPTION - fix_02_02: {input_file_path}: {e}")


def fix_02_02_pass2(input_file_b02, input_file_b06, alogger):
    try:
        # Les inn CSV-filene
        df_b02 = pd.read_csv(input_file_b02)
        df_b06 = pd.read_csv(input_file_b06)

        # Finn radene i b_02.01 hvor c0140 er tom
        rows_b02_with_empty_c0140 = df_b02[df_b02['c0140'].isna() | (df_b02['c0140'] == '')]

        # For hver rad med tom c0140 i b_02.01, fyll den med verdien fra b_06.01
        for index, row in rows_b02_with_empty_c0140.iterrows():
            matching_row_b06 = df_b06[df_b06['c0010'] == row['c0050']]  # Forbindelsen mellom b_06 og b_02 er via hhv c0010 og c0050
            if not matching_row_b06.empty:
                # Kopier verdien fra c0050 i b_06.01 til c0140 i b_02.01 (eller annen logikk for kopiering)
                df_b02.at[index, 'c0140'] = matching_row_b06.iloc[0]['c0050']

        # Finn radene i b_02.02 hvor c0170 er tom (NaN eller tom verdi)
        rows_b02_with_empty_c0170 = df_b02[df_b02['c0170'].isna() | (df_b02['c0170'] == '')]

        # For hver rad med tom c0170 i b_02.02, oppdater den med riktig verdi basert på c0100 i b_06.01
        for index, row in rows_b02_with_empty_c0170.iterrows():
            matching_row_b06 = df_b06[df_b06['c0010'] == row['c0050']]  # Forbindelsen mellom b_06 og b_02 er via c0010 og c0050
            if not matching_row_b06.empty:
                # Sjekk verdien i c0050 i b_06.01 og oppdater c0170 i b_02.02
                c0050_value = matching_row_b06.iloc[0]['c0050']
                if c0050_value == "eba_BT:x28":
                    df_b02.at[index, 'c0170'] = "eba_ZZ:x793"
                elif c0050_value == "eba_BT:x29":
                    df_b02.at[index, 'c0170'] = "eba_ZZ:x795"

        # Lagre den rensede b_02.01 filen til midlertidig output-filbane
        temp_output_file_b02 = f"{input_file_b02}.temp"
        df_b02.to_csv(temp_output_file_b02, index=False)

        alogger.info(f"Filen b_02.01 er renset og lagret som: {temp_output_file_b02}")

        # Slett original b_02.01 fil etter rensing
        os.remove(input_file_b02)
        alogger.info(f"Originalfilen {input_file_b02} er slettet.")

        # Gi den rensede b_02.01 filen originalt navn
        os.rename(temp_output_file_b02, input_file_b02)
        alogger.info(f"Renset b_02.01 fil er omdøpt tilbake til {input_file_b02}")

    except Exception as e:
        print(f"Feil ved behandling av filene {input_file_b02} og {input_file_b06}: {e}")



def fix_02_02_pass3(input_file_b0202, input_file_b0501, alogger):
    try:
        # Les inn CSV-filene
        df_b0501 = pd.read_csv(input_file_b0501)
        df_b0202 = pd.read_csv(input_file_b0202)

        # For hver rad i b_02_02, sjekk om c0030 finnes i c0010 i b_05.01
        rows_to_keep = []
        for index, row in df_b0202.iterrows():
            if row['c0030'] in df_b0501['c0010'].values:
                rows_to_keep.append(index)

        # Filtrer ut rader som ikke har en referanse i b_05.01
        df_b0202_cleaned = df_b0202.loc[rows_to_keep]

        # Lagre den rensede b_02_02 filen til midlertidig output-filbane
        temp_output_file_b0202 = f"{input_file_b0202}.temp"
        df_b0202_cleaned.to_csv(temp_output_file_b0202, index=False)

        # Slett original b_02_02 fil etter rensing
        os.remove(input_file_b0202)
        alogger.info(f"Originalfilen {input_file_b0202} er slettet.")

        # Gi den rensede b_02_02 filen originalt navn
        os.rename(temp_output_file_b0202, input_file_b0202)
        alogger.info(f"Renset b_02_02 fil er omdøpt tilbake til {input_file_b0202}")

    except Exception as e:
        print(f"Feil ved behandling av filene {input_file_b0202} og {input_file_b0501}: {e}")
