import os
import pandas as pd
import logging

def fix_05_01(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fjern leading og trailing spaces fra c0010
        df['c0010'] = df['c0010'].str.strip()

        # Fjern alle duplikatrader
        df = df.drop_duplicates()

        # Hvis c0020 finnes i flere rader, behold den første og fjern påfølgende
        df = df.drop_duplicates(subset='c0010', keep='first')

        # Oppdater c0020 hvis den er 'eba_qCO:qx2003', sett den til 'eba_qCO:qx2002'
        df.loc[df['c0020'] == 'eba_qCO:qx2003', 'c0020'] = 'eba_qCO:qx2002'        

        # Sett c0070 til "eba_CT:x212" hvis c0070 er tom (NaN eller tom verdi)
        df['c0070'] = df['c0070'].fillna('eba_CT:x212')

        # Sjekk om c0110 er tom, hvis ja, sett den til verdien i c0010
        df['c0110'] = df['c0110'].fillna(df['c0010'])

        # Hvis c0100 er tom, sett verdi = 0
        df['c0100'] = df['c0100'].fillna(0)

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
