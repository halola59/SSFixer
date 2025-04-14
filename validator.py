### 📄 validator.py
import os
import logging
import zipfile
import shutil
from process_customer_files_pass1 import process_customer_files_pass1
from process_customer_files_pass2 import process_customer_files_pass2
from process_customer_files_pass3 import process_customer_files_pass3

DATA_ROOT = "./data"


def create_logger(logfile_path, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(logfile_path)
        formatter = logging.Formatter(f'%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def create_clogger(logfile_path, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(logfile_path)
        formatter = logging.Formatter(f'%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def setup_customer_environment(customer_input_file):
    if not customer_input_file.endswith(".zip"):
        raise ValueError("Inputfilen må være en .zip-fil")

    customer_name = os.path.splitext(customer_input_file)[0]
    customer_dir = os.path.join(DATA_ROOT, customer_name)
    zip_dir = os.path.join(customer_dir, "zip")
    org_dir = os.path.join(customer_dir, "org")
    res_dir = os.path.join(customer_dir, customer_name)
    log_dir = os.path.join(customer_dir, "log")

    org_zip = os.path.join(zip_dir, f"{customer_name}.org.zip")
    res_zip = os.path.join(zip_dir, f"{customer_name}.res.zip")
    input_zip_path = os.path.join(DATA_ROOT, customer_input_file)

    # Opprett mapper
    for d in [zip_dir, org_dir, res_dir, log_dir]:
        os.makedirs(d, exist_ok=True)

    # Flytt .zip til zip/<customer>.org.zip hvis ikke allerede der
    if os.path.exists(input_zip_path) and not os.path.exists(org_zip):
        shutil.move(input_zip_path, org_zip)
        print(f"Flyttet {input_zip_path} til {org_zip}")

    # Rydd res, log og .res.zip
    if os.path.exists(res_zip):
        os.remove(res_zip)
    for d in [res_dir, log_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # Lag loggere
    audit_logger = create_logger(os.path.join(log_dir, "audit.log"), f"audit_{customer_name}")
    change_logger = create_clogger(os.path.join(log_dir, "changelog.txt"), f"change_{customer_name}")

    return {
        "customer_name": customer_name,
        "customer_dir": customer_dir,
        "zip_dir": zip_dir,
        "org_dir": org_dir,
        "res_dir": res_dir,
        "log_dir": log_dir,
        "org_zip": org_zip,
        "res_zip": res_zip,
        "alogger": audit_logger,
        "clogger": change_logger,
    }

def unzip_strip_first_dir(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Fjern første katalognivå basert på "/" – ikke os.sep
            parts = member.split('/', 1)
            if len(parts) == 2:
                target_path = os.path.join(extract_to, parts[1])
            else:
                continue  # Hopp over selve toppnivåmappen

            if member.endswith('/'):
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with zip_ref.open(member) as src, open(target_path, 'wb') as dst:
                    shutil.copyfileobj(src, dst)

def zip_customer_result(res_dir, res_zip_path, customer_name):
    with zipfile.ZipFile(res_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(res_dir):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, res_dir)
                arcname = os.path.join(customer_name, relative_path)
                zipf.write(full_path, arcname)


def process_customer(context):
    alogger = context["alogger"]
    clogger = context["clogger"]

    # Pakk ut original zip
    unzip_strip_first_dir(context["org_zip"], context["org_dir"])
    context["alogger"].info("Original zip pakket ut uten toppnivå-mappe")

    # ---------- PASS 1 ----------
    alogger.info(f"***** Starter prosessering av {context['org_dir']} - PASS 1")
    process_customer_files_pass1(context["org_dir"], context["res_dir"], alogger, clogger)

    # ---------- PASS 2 ----------
    alogger.info(f"***** Starter prosessering av {context['org_dir']} - PASS 2")
    process_customer_files_pass2(context["res_dir"], alogger, clogger)

    # ---------- PASS 3 ----------
    #alogger.info(f"***** Starter prosessering av {context['org_dir']} - PASS 3")
    #process_customer_files_pass3(context["res_dir"], alogger, clogger)

    # ---------- ZIP RESULTAT ----------
    # Ny: pakker innholdet i res/ inn i <customer>/... i zip
    zip_customer_result(context["res_dir"],
                        context["res_zip"],
                        context["customer_name"])
    alogger.info(f"Ny res.zip skrevet til {context['res_zip']}")


def validate_all():
    customer_input_files = [
        f for f in os.listdir(DATA_ROOT)
        if f.endswith('.zip') and not f.endswith('.org.zip')
    ]

    # Hvis ingen nye zip-filer: se etter eksisterende .org.zip
    if not customer_input_files:
        print("Ingen nye .zip-filer funnet. Søker etter tidligere .org.zip...")
        for customer in os.listdir(DATA_ROOT):
            customer_zip_path = os.path.join(DATA_ROOT, customer, "zip", f"{customer}.org.zip")
            if os.path.exists(customer_zip_path):
                customer_input_files.append(f"{customer}.zip")  # Fiktiv filnavn – brukes for setup

    for customer_input_file in customer_input_files:
        context = setup_customer_environment(customer_input_file)
        process_customer(context)


if __name__ == "__main__":
    validate_all()