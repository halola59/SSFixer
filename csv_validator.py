import pandas as pd          # For å lese og håndtere CSV-filer
import re                    # For å validere datoformat med regex
from datetime import datetime  # For å kontrollere gyldige datoer

# Funksjon som legger til feilmeldinger
def add_error(errors, new_error):
    if new_error not in errors:  # Sjekker om feilmeldingen allerede finnes
        errors.append(new_error)  # Legger til feilmeldingen hvis den ikke er der fra før


def validate_csv_against_schema(csv_path, json_def, labels=None, can_be_empty=False):
    errors = []
    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return [f"❌ Klarte ikke å lese CSV-filen: {e}"]

    if df.empty:
        errors.append("⚠️ CSV-filen er tom – ingen rader funnet")
        return errors

    table_templates = json_def.get("tableTemplates", {})
    if not table_templates:
        return ["❌ Fant ingen tableTemplates i JSON-definisjonen"]

    table_name, table_data = next(iter(table_templates.items()))
    table_name = table_name.replace("-", ".")  # Replace hyphen with a period to match the expected format
    table_name = table_name.lower()  # Convert the table_name to lowercase to ensure consistency

    column_defs = table_data.get("columns", {})
    expected_cols = list(column_defs.keys())

    # Regler for obligatoriske/valgfrie kolonner per tabell
    table_rules = {
        "b_05.01": {  # Spesifikk regel for b_05.01
            "c0030": {"required": False},  # c0030 er valgfri i b_05.01
            "c0040": {"required_if_c0030_filled": True}  # c0040 er valgfri hvis c0030 er tom
        },
        "b_02.01": {  # Spesifikk regel for b_02.01
            "c0030": {"required_if_c0020_x3": True},  # c0030 må fylles ut hvis c0020 = eba_CO:x3
        }
    }

    # Default regel for alle andre tabeller (både c0030 og c0040 er obligatoriske)
    default_rules = {
        "c0030": {"required": True},  # c0030 er obligatorisk
        "c0040": {"required": True}   # c0040 er obligatorisk
    }

    # Bruk spesifikke regler for b_02.01 eller b_05.01, ellers bruk default regler
    rules = table_rules.get(table_name, default_rules)

    type_map = {
        "s": "string",
        "e": "string",
        "d": "date",
        "i": "integer",
        "n": "integer",
        "f": "float"
    }

    for i, row in df.iterrows():  # Bruker enumerate for å få radnummer
        for col_name in expected_cols:
            col_meta = column_defs.get(col_name, {})
            doc = col_meta.get("eba:documentation", {})
            short_type = doc.get("type", "s")
            expected_type = type_map.get(short_type, "string")
            is_required = rules.get(col_name, {}).get("required", True)

            concept_id = doc.get("CellCode", "").split(",")[-1].strip(" {}")  # e.g. c0060
            label = labels.get(concept_id, "") if labels else ""
            label_info = f" ({label})" if label else ""

            if col_name not in df.columns:
                msg = f"{'\u274c' if is_required else '\u26a0\ufe0f'} Mangler {'obligatorisk ' if is_required else ''}kolonne: {col_name}{label_info}"
                add_error(errors, msg)
                continue

            col_data = df[col_name]

            # Spesifik logikk for b_02.01: c0030 avhenger av c0020
            if table_name == "b_02.01":
                if "c0020" in df.columns:     
                    c0020_value = row["c0020"]
                    c0030_value = str(row.get("c0030", "")).strip()
                    if c0030_value == "nan":
                        c0030_value = ""

                    if c0020_value == "eba_CO:x3" and not c0030_value:
                        msg = f"❌ Rad {i+2} Kol c0030 må fylles ut når c0020 = 'eba_CO:x3'"
                        add_error(errors, msg)
                    elif c0020_value in ["eba_CO:x1", "eba_CO:x2"] and c0030_value == "":
                        # c0030 kan være tom for c0020 = x1 eller x2
                        continue
                    elif c0020_value not in ["eba_CO:x1", "eba_CO:x2", "eba_CO:x3"]:
                        msg = f"❌ Rad {i+2} Kol c0020 = {c0020_value}. Forventet eba_CO:x1, eba_CO:x2, eller eba_CO:x3."
                        add_error(errors, msg)


            if table_name == "b_05.01":           
                    c0030_value = str(row.get("c0030", "")).strip()
                    if c0030_value == "nan":
                        c0030_value = ""
                    c0040_value = str(row.get("c0040", "")).strip()
                    if c0040_value == "nan":
                        c0040_value = ""

                    if c0030_value != "" and not c0040_value:
                        msg = f"❌ Rad {i+2} Kol c0040 må fylles ut når c0030 har en verdi"
                        add_error(errors, msg)
                    elif c0030_value == "" and c0040_value == "":
                        # c0040 kan være tom når c0030 er tom
                        continue                                        

            if table_name == "b_06.01":           
                    c0070_value = str(row.get("c0070", "")).strip()
                    if c0070_value == "nan":
                        c0070_value = ""
                    if c0070_value == "":
                        # c0070_value kan være tom
                        continue                                        

            if col_data.isnull().all() or col_data.eq("").all():
                if is_required:
                    msg = f"{'\u274c' if is_required else '\u26a0\ufe0f'} Rad {i+2} Kol {col_name} er tom eller kun blanke verdier"
                    add_error(errors, msg)
                #continue

            try:
                if expected_type == "string":
                    col_data.astype(str)
                elif expected_type == "float":
                    col_data.astype(float)
                elif expected_type == "boolean":
                    col_data.astype(bool)
                elif expected_type == "integer":
                    col_data.astype(int)
                elif expected_type == "date":
                    for i, val in enumerate(col_data):
                        row_number = i + 2
                        if pd.isna(val) or str(val).strip() == "":
                            msg = f"{'\u274c' if is_required else '\u26a0\ufe0f'} Rad {i+2} Kol {col_name} Mangler datoverdi, obligatorisk felt"
                            add_error(errors, msg)
                            continue

                        val_str = str(val).strip()
                        if not date_regex.match(val_str):
                            msg = f"❌ Rad {i+2} Kol {col_name} - ugyldig datoformat: '{val_str}' (forventet YYYY-MM-DD)"
                            add_error(errors, msg)
                            continue

                        try:
                            datetime.strptime(val_str, "%Y-%m-%d")
                        except ValueError as e:
                            msg = f"❌ Rad {i+2} Kol {col_name} - Feil ved parsing av dato: '{val_str}' – {e}"
                            add_error(errors, msg)

            except Exception as e:
                msg = f"❌ Rad {i+2} Kol {col_name} - Feil datatype {label_info} (forventet {expected_type}): {e}"
                add_error(errors, msg)

    return errors
