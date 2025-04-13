import pandas as pd
import os
import logging

def fix_05_02(input_file_path, alogger, clogger=None):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0030
        rows_with_spaces_in_c0030 = df[df['c0030'].astype(str).str.strip() != df['c0030'].astype(str)]
        for index, row in rows_with_spaces_in_c0030.iterrows():
            alogger.info(f"B_05.02: Rad {index} - c0030 '{row['c0030']}' har mellomrom, fjerner leading/trailing spaces.")
        df['c0030'] = df['c0030'].str.strip()
        
        # Fjern leading og trailing spaces fra c0060
        rows_with_spaces_in_c0060 = df[df['c0060'].astype(str).str.strip() != df['c0060'].astype(str)]
        for index, row in rows_with_spaces_in_c0060.iterrows():
            alogger.info(f"B_05.02: Rad {index} - c0060 '{row['c0060']}' har mellomrom, fjerner leading/trailing spaces.")
        df['c0060'] = df['c0060'].str.strip()
        
        # Fjern linjer der c0020 eller c0030 er tomme (NaN eller tom verdi)
        rows_with_empty_c0020_or_c0030 = df[(df['c0020'].isna() | (df['c0020'] == '')) | (df['c0030'].isna() | (df['c0030'] == ''))]
        for index, row in rows_with_empty_c0020_or_c0030.iterrows():
            alogger.info(f"B_05.02: Rad {index} - c0020 eller c0030 er tom, sletter raden.")
        df_cleaned = df[df['c0020'].notna() & (df['c0020'] != '') & df['c0030'].notna() & (df['c0030'] != '')]

        # Sjekk at c0050 er fylt ut når c0030 og c0060 matcher
        for i, row in df_cleaned.iterrows():
            if row['c0030'] == row['c0060'] and pd.isna(row['c0050']):
                # Hvis c0030 og c0060 er like, må c0050 være fylt ut
                alogger.info(f"B_05.02: Rad {i} - c0030 ('{row['c0030']}') og c0060 ('{row['c0060']}') er like, men c0050 er tom. Setter c0050 til 'Default_Value'.")
                df_cleaned.loc[i, 'c0050'] = "Default_Value"  # Sett en standardverdi hvis ønskelig, ellers kan du fjerne linjen

        # Lagre den rensede filen til midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df_cleaned.to_csv(temp_output_file_path, index=False)

        alogger.info(f"B_05.02: Filen er renset og lagret som: {temp_output_file_path}")

        # Slett original fil etter rensing
        os.remove(input_file_path)
        alogger.info(f"B_05.02: Originalfilen {input_file_path} er slettet.")

        # Gi den rensede filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        alogger.info(f"B_05.02: Renset fil er omdøpt tilbake til {input_file_path}")
    
    except Exception as e:
        print(f"Feil ved behandling av fil {input_file_path}: {e}")



def fix_05_02_pass2(input_file_b0502, input_file_b0501, alogger, clogger=None):
    try:
        # Les inn CSV-filene
        df_b0501 = pd.read_csv(input_file_b0501)
        df_b0502 = pd.read_csv(input_file_b0502)

        # For hver rad i b_05.02, sjekk om c0060 finnes i c0010 i b_05.01
        rows_to_keep = []
        rows_to_remove = []
        for index, row in df_b0502.iterrows():
            if row['c0060'] in df_b0501['c0010'].values:
                rows_to_keep.append(index)
            else:
                rows_to_remove.append(index)
                alogger.info(f"B_05.02_pass2: Rad {index} - c0060 '{row['c0060']}' finnes ikke i c0010 i b_05.01, sletter raden.")

        # Filtrer ut rader som ikke har en referanse i b_05.01
        df_b0502_cleaned = df_b0502.loc[rows_to_keep]

        # Lagre den rensede b_05.02 filen til midlertidig output-filbane
        temp_output_file_b0502 = f"{input_file_b0502}.temp"
        df_b0502_cleaned.to_csv(temp_output_file_b0502, index=False)

        # Slett original b_05.02 fil etter rensing
        os.remove(input_file_b0502)
        alogger.info(f"B_05.02_pass2: Originalfilen {input_file_b0502} er slettet.")

        # Gi den rensede b_05.02 filen originalt navn
        os.rename(temp_output_file_b0502, input_file_b0502)
        alogger.info(f"B_05.02_pass2: Renset b_05.02 fil er omdøpt tilbake til {input_file_b0502}")
    
    except Exception as e:
        print(f"Feil ved behandling av filene {input_file_b0502} og {input_file_b0501}: {e}")

