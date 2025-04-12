import os
import pandas as pd
import logging

def fix_01_02(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Fyll ut rader der c0060 er NaN med verdien fra c0010
        df['c0060'] = df['c0060'].fillna(df['c0010'])

        # Erstatt beløp skrevet som tekst med mellomrom, f.eks. "914 321" skal bli 914321
        # Fjern mellomrom fra tall i c0110 (kun numeriske verdier)
        df['c0110'] = df['c0110'].replace({r'\s+': ''}, regex=True)        

        # Lagre den endrede DataFrame til en midlertidig output-filbane
        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        logger.info(f"Filen er oppdatert og lagret som: {temp_output_file_path}")

        # Slett original fil etter oppdatering
        os.remove(input_file_path)
        logger.info(f"Originalfilen {input_file_path} er slettet.")

        # Gi den oppdaterte filen originalt navn
        os.rename(temp_output_file_path, input_file_path)
        logger.info(f"Oppdatert fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"fix_01_02: Feil ved behandling av fil {input_file_path}: {e}")


