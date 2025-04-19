### 📄 validator.py
import os
import logging
from process_customer_files_pass1 import process_customer_files_pass1
from process_customer_files_pass2 import process_customer_files_pass2
from process_customer_files_pass3 import process_customer_files_pass3

DATA_ROOT = "./data"


def create_audit_logger(customer_path):
    """
    Lager en egen logger for hver kunde og setter loggfilen til kundens katalog.
    """
    log_filename = f"{customer_path}".replace(".org", "_a.log")  # Audit log
    if os.path.exists(log_filename):
        os.remove(log_filename)

    logger = logging.getLogger(customer_path)
    logger.setLevel(logging.INFO)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger


def create_change_logger(customer_path):
    """
    Lager en egen change-logger for hver kunde og setter loggfilen til kundens katalog.
    Denne loggeren brukes til å logge endringer i filene.
    """
    log_filename = f"{customer_path}".replace(".org", "_c.log")  # Change log
    if os.path.exists(log_filename):
        os.remove(log_filename)

    logger = logging.getLogger(f"{customer_path}_change")
    logger.setLevel(logging.INFO)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger



def validate_all():
    all_customer_dirs = [d for d in os.listdir(DATA_ROOT) if os.path.isdir(os.path.join(DATA_ROOT, d))]

    customer_dirs = [d for d in all_customer_dirs if not (d.endswith('.p1'))]

    for customer_dir in customer_dirs:
        customer_path = os.path.join(DATA_ROOT, customer_dir)

        alogger = create_audit_logger(customer_path)
        clogger = create_change_logger(customer_path)   

        if not customer_dir.endswith(".org"):
            org_customer_dir = f"{customer_dir}.org"
            org_customer_path = os.path.join(DATA_ROOT, org_customer_dir)
            try:
                os.rename(customer_path, org_customer_path)
                customer_path = org_customer_path
                alogger.info(f"Katalogen {customer_path} ble omdøpt til {org_customer_path}.")
            except OSError as e:
                alogger.error(f"Feil ved omdøping av katalog {customer_path}: {e}")
                continue
        else:
            org_customer_dir = customer_dir            

        customer_path_p1 = f"{os.path.splitext(customer_path)[0]}.p1"
        try:
            os.makedirs(customer_path_p1, exist_ok=True)
            alogger.info(f"Katalogen {customer_path_p1} ble opprettet.")
        except OSError as e:
            alogger.error(f"Feil ved oppretting av katalog {customer_path_p1}: {e}")
            continue

        clogger.info(f"Changelog for {customer_path_p1}")

        alogger.info(f"***** Starter prosessering av {customer_path_p1} PASS 1 *****")
        process_customer_files_pass1(customer_path, customer_path_p1, alogger, clogger) 
        
        alogger.info(f"***** Starter prosessering av {customer_path_p1} PASS 2 *****")
        process_customer_files_pass2(customer_path_p1, alogger, clogger)

        alogger.info(f"***** Starter prosessering av {customer_path_p1} PASS 3 *****")
        process_customer_files_pass3(customer_path_p1, alogger, clogger)

if __name__ == "__main__":
    validate_all()
