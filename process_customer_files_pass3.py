import os
import json
import logging
from csv_validator import validate_csv_against_schema
from label_utils import load_labels

TAXONOMY_DIR = "./taxonomy"

def process_customer_files_pass3(customer_path_p1, alogger, clogger):
    """
    Prosesserer kundens filer i pass 3 (validering mot DORA 4.0 taxonomi).
    """

    try:
        reports_dir = os.path.join(customer_path_p1, "reports")
        meta_dir = os.path.join(customer_path_p1, "META-INF")

        for file in os.listdir(TAXONOMY_DIR):
            if file.endswith(".json"):
                base_name = file.replace(".json", "")
                json_path = os.path.join(TAXONOMY_DIR, file)
                csv_path = find_csv_insensitive(reports_dir, base_name + ".csv")
                label_path = os.path.join(TAXONOMY_DIR, base_name + "-lab-en.xml")
                
                if not os.path.exists(csv_path):
                    continue

                json_def = load_json_definition(json_path)
                labels = load_labels(label_path) if os.path.exists(label_path) else {}
                can_be_empty = "01.03" in base_name

                alogger.info(f"Starter validering for {base_name}.csv i {customer_path_p1}")

                errors = validate_csv_against_schema(csv_path, json_def, labels, can_be_empty)

                if errors:
                    alogger.error(f"Feil ved validering av {csv_path}:")
                    for r in errors:
                        alogger.error(f"  {r}")
                else:
                    alogger.info(f"Validering for {csv_path} fullført uten feil.")

    except Exception as e:
        alogger.error(f"Feil ved prosessering av katalog {customer_path_p1}: {e}")


def load_json_definition(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_csv_insensitive(folder, target_name):
    for f in os.listdir(folder):
        if f.lower() == target_name.lower():
            return os.path.join(folder, f)
    return None
