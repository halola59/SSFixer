import pandas as pd
import os
import logging

def fix_06_01(input_file_path, logger):
    try:
        # Les inn CSV-filen
        df = pd.read_csv(input_file_path)

        # Endre overskriften fra "c0010,c0020,c0030,c0040,c0060,c0070,c0080,c0090,c0100,c0110"
        # til "c0010,c0020,c0030,c0040,c0050,c0060,c0070,c0080,c0090,c0100"
        new_columns = ["c0010", "c0020", "c0030", "c0040", "c0050", "c0060", "c0070", "c0080", "c0090", "c0100"]
        df.columns = new_columns

        # Fjern alle mellomrom i c0010 (men behold teksten)
        df['c0010'] = df['c0010'].astype(str).replace(r'\s+', '', regex=True)

        # Hent verdier fra de radene der c0040 er fylt ut
        c0040_values = df['c0040'].dropna().unique()

        # Hvis det finnes c0040-verdier, fyll ut de radene som mangler c0040
        if c0040_values.size > 0:
            # Sett c0040 til første tilgjengelige verdi fra c0040
            fill_value = c0040_values[0]
            df['c0040'].fillna(fill_value, inplace=True)

        # Kombiner c0010 og c0040 for å sikre at det er unikt per rad
        df['c0010_c0040_combination'] = df['c0010'] + df['c0040']

        # Sjekk for duplikater i kombinasjonen c0010 + c0040
        duplicates = df[df.duplicated(subset=['c0010_c0040_combination'], keep=False)]

        if not duplicates.empty:
            logger.info(f"Duplikater funnet i kombinasjonen 'c0010 + c0040':")
            logger.info(duplicates[['c0010', 'c0040', 'c0010_c0040_combination']])

            # Hvis du ønsker å fjerne duplikater, kan vi gjøre dette
            df = df.drop_duplicates(subset=['c0010_c0040_combination'], keep='first')

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
