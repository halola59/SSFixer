import os
import pandas as pd


def fix_01_02(input_file_path, logger):
    try:
        df = pd.read_csv(input_file_path)

        df['c0060'] = df['c0060'].fillna(df['c0010'])

        df['c0110'] = df['c0110'].replace({r'\s+': ''}, regex=True)

        temp_output_file_path = f"{input_file_path}.temp"
        df.to_csv(temp_output_file_path, index=False)

        logger.info(f"Filen er oppdatert og lagret som: "
                    f"{temp_output_file_path}")

        os.remove(input_file_path)
        logger.info(f"Originalfilen {input_file_path} er slettet.")

        os.rename(temp_output_file_path, input_file_path)
        logger.info(f"Oppdatert fil er omdøpt tilbake til {input_file_path}")

    except Exception as e:
        print(f"fix_01_02: Feil ved behandling av fil {input_file_path}: {e}")
