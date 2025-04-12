import os
import shutil
import logging

def process_customer_files_pass1(customer_path, customer_path_p1, logger):
    """
    Lager en kopi av katalogen, fjerner tomme linjer og duplikater fra filene,
    og lagrer dem i den nye katalogen.
    """

    try:
        # Sørg for at hovedmappen til customer_path_p1 eksisterer
        os.makedirs(customer_path_p1, exist_ok=True)

        # Iterer gjennom alle filene i både META-INF og reports underkataloger
        for subfolder in ['META-INF', 'reports']:
            subfolder_path = os.path.join(customer_path, subfolder)

            # Sjekk at katalogen eksisterer
            if os.path.isdir(subfolder_path):
                # Lag subfolder i customer_path_p1 hvis den ikke finnes
                subfolder_output_path = os.path.join(customer_path_p1, subfolder)
                os.makedirs(subfolder_output_path, exist_ok=True)

                for filename in os.listdir(subfolder_path):
                    input_file_path = os.path.join(subfolder_path, filename)
                    logger.info(f"Prosesserer fil: {input_file_path}")

                    if os.path.isfile(input_file_path):
                        # Lag output filbane i .P1 katalogen
                        output_file_path = os.path.join(subfolder_output_path, filename)

                        # Rens filen
                        clean_file(input_file_path, output_file_path, logger)

    except Exception as e:
        logger.error(f"Feil ved prosessering av katalog {customer_path}: {e}")


def clean_file(input_file_path, output_file_path, logger):
    """
    Fjerner tomme linjer og duplikat linjer fra en fil og lagrer resultatet i en ny fil.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # Fjern tomme linjer (linjer som bare inneholder kommaer eller er helt tomme)
        cleaned_lines = [line for line in lines if line.strip() and not line.strip().startswith(',')]

        # Fjern duplikat linjer
        cleaned_lines = list(dict.fromkeys(cleaned_lines))

        # Lagre den rensede filen
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(cleaned_lines)

        logger.info(f"Renset fil lagret: {output_file_path}")
    except Exception as e:
        logger.error(f"Feil ved behandling av fil {input_file_path}: {e}")
