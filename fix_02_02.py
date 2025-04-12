import os
import pandas as pd
import logging

def fix_02_02(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Hvis c0090 er tom, sett inn 'eba_CO:x4'
        df['c0090'] = df['c0090'].fillna('eba_CO:x4')

        # Hvis c0100 er tom, sett verdi = 90
        df['c0100'] = df['c0100'].fillna(90)

        # Fjern leading og trailing spaces fra c0030
        df['c0030'] = df['c0030'].str.strip()        

        # Hvis c0110 er tom, sett verdi = c0100
        df['c0110'] = df['c0110'].fillna(df['c0100'])        

        # Hvis c0150 er tom og c0140 er tom, kopier verdien fra c0130 til c0150
        df.loc[df['c0150'].isna() & df['c0140'].isna(), 'c0150'] = df['c0130']

        # Finn radene der c0140 er 'eba_BT:x29' og c0150 er tom
        condition = (df['c0140'] == 'eba_BT:x29') & (df['c0150'].isna() | (df['c0150'] == ''))

        # Sett c0100 til 'Not applicable' for de radene som oppfyller betingelsene
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

        logger.info(f"Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        logger.info(f"Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        logger.info(f"Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")


def fix_02_02_pass2(input_file_b02, input_file_b06, logger):
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

        logger.info(f"Filen b_02.01 er renset og lagret som: {temp_output_file_b02}")

        # Slett original b_02.01 fil etter rensing
        os.remove(input_file_b02)
        logger.info(f"Originalfilen {input_file_b02} er slettet.")

        # Gi den rensede b_02.01 filen originalt navn
        os.rename(temp_output_file_b02, input_file_b02)
        logger.info(f"Renset b_02.01 fil er omdøpt tilbake til {input_file_b02}")
    
    except Exception as e:
        print(f"Feil ved behandling av filene {input_file_b02} og {input_file_b06}: {e}")



def fix_02_02_pass3(input_file_b0202, input_file_b0501, logger):
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
        logger.info(f"Originalfilen {input_file_b0202} er slettet.")

        # Gi den rensede b_02_02 filen originalt navn
        os.rename(temp_output_file_b0202, input_file_b0202)
        logger.info(f"Renset b_02_02 fil er omdøpt tilbake til {input_file_b0202}")
    
    except Exception as e:
        print(f"Feil ved behandling av filene {input_file_b0202} og {input_file_b0501}: {e}")
