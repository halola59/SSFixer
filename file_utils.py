
import os


def clean_file(input_file_path, output_file_path, alogger):
    """
    Fjerner tomme linjer og duplikat linjer fra en fil og lagrer resultatet i en ny fil.
    """
    try:
        subfolder, filename = os.path.split(input_file_path)
        
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # Fjern tomme linjer (linjer som bare inneholder kommaer eller er helt tomme)
        cleaned_lines = [line for line in lines if line.strip() and not line.strip().startswith(',')]

        # Fjern duplikat linjer
        cleaned_lines = list(dict.fromkeys(cleaned_lines))

        # Lagre den rensede filen
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(cleaned_lines)

        alogger.info(f"Renset fil lagret: {output_file_path}")
    except Exception as e:
        alogger.error(f"Feil ved behandling av fil {input_file_path}: {e}")
