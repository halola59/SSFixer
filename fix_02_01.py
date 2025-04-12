import os
import pandas as pd

def fix_02_01(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fyll c0050 med 0 hvis den er tom (NaN eller tom verdi)
        df['c0050'] = df['c0050'].fillna(0)

        # Erstatt "Not Applicable" med tomt felt i c0030 (uavhengig av stor/liten bokstav)
        df['c0030'] = df['c0030'].replace({"not applicable": "", "Not Applicable": "", "Not applicable": ""}, regex=True)

        # Erstatt beløp skrevet som tekst med mellomrom, f.eks. "914 321" skal bli 914321
        # Fjern mellomrom fra tall i c0050 (kun numeriske verdier)
        df['c0050'] = df['c0050'].replace({r'\s+': ''}, regex=True)

        # Konverter kolonne c0050 til numerisk, slik at eventuelle tekstverdier blir håndtert som tall
        df['c0050'] = pd.to_numeric(df['c0050'], errors='coerce').fillna(0).astype(int)

        # Fjern linjer der c0020 er 'eba_CO:x3' og c0030 er tom
        df = df[~((df['c0020'] == 'eba_CO:x3') & (df['c0030'].isna() | (df['c0030'] == '')))]

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
        print(f"fix_02_01: Feil ved behandling av fil {input_file_path}: {e}")




