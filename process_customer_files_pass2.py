import os
import shutil
from fix_01_02 import fix_01_02
from fix_02_01 import fix_02_01
from fix_02_02 import fix_02_02
from fix_02_02 import fix_02_02_pass2
from fix_02_02 import fix_02_02_pass3
from fix_03_01 import fix_03_01
from fix_03_02 import fix_03_02
from fix_04_01 import fix_04_01
from fix_05_01 import fix_05_01
from fix_05_02 import fix_05_02
from fix_05_02 import fix_05_02_pass2
from fix_06_01 import fix_06_01
from fix_07_01 import fix_07_01

def process_customer_files_pass2(customer_path_p1, alogger, clogger):
    """
    Prosesserer kundens filer i pass 2, dvs. korrektur og behandling av CSV-filer,
    samt logging av relevante prosesser.
    """
    try:
        alogger.info(f"Prosessering av {customer_path_p1} - PASS 2a")
        
        # Iterer gjennom alle filene i både META-INF og reports underkataloger
        for subfolder in ['META-INF', 'reports']:
            subfolder_path = os.path.join(customer_path_p1, subfolder)

            # Sjekk at katalogen eksisterer
            if os.path.isdir(subfolder_path):
                for filename in os.listdir(subfolder_path):
                    csv_path = os.path.join(subfolder_path, filename)
                    
                    if filename.endswith(".csv"):
                        alogger.info(f"Prosesserer fil: {filename}")

                        # Kjør relevante funksjoner avhengig av filnavn
                        if "01.02" in csv_path:
                            alogger.info(f"Starter fix_01_02 på {csv_path}")
                            fix_01_02(csv_path, alogger)

                        elif "02.01" in csv_path:
                            alogger.info(f"Starter fix_02_01 på {csv_path}")
                            fix_02_01(csv_path, alogger, clogger)

                        elif "02.02" in csv_path:
                            alogger.info(f"Starter fix_02_02 på {csv_path}")
                            fix_02_02(csv_path, alogger, clogger)

                        elif "03.01" in csv_path:
                            alogger.info(f"Starter fix_03_01 på {csv_path}")
                            fix_03_01(csv_path, alogger)

                        elif "03.02" in csv_path:
                            alogger.info(f"Starter fix_03_02 på {csv_path}")
                            fix_03_02(csv_path, alogger)

                        elif "04.01" in csv_path:
                            alogger.info(f"Starter fix_04_01 på {csv_path}")
                            fix_04_01(csv_path, alogger)

                        elif "05.01" in csv_path:
                            alogger.info(f"Starter fix_05_01 på {csv_path}")
                            fix_05_01(csv_path, alogger)

                        elif "05.02" in csv_path:
                            alogger.info(f"Starter fix_05_02 på {csv_path}")
                            fix_05_02(csv_path, alogger)

                        elif "06.01" in csv_path:
                            alogger.info(f"Starter fix_06_01 på {csv_path}")
                            fix_06_01(csv_path, alogger)

                        elif "07.01" in csv_path:
                            alogger.info(f"Starter fix_07_01 på {csv_path}")
                            fix_07_01(csv_path, alogger)



        alogger.info(f"Prosessering av {customer_path_p1} - PASS 2b")
        for subfolder in ['META-INF', 'reports']:
            subfolder_path = os.path.join(customer_path_p1, subfolder)

            # Sjekk at katalogen eksisterer
            if os.path.isdir(subfolder_path):
                for filename in os.listdir(subfolder_path):
                    csv_path = os.path.join(subfolder_path, filename)
                    
                    if filename.endswith(".csv"):
                        alogger.info(f"Prosesserer fil: {filename}")

                        if "02.02" in csv_path:
                            csv_path_b06 = csv_path.replace("b_02.02", "b_06.01")
                            alogger.info(f"Starter fix_02_02_pass2 på {csv_path}")
                            fix_02_02_pass2(csv_path, csv_path_b06, alogger)

                            csv_path_b0501 = csv_path.replace("b_02.02", "b_05.01")
                            alogger.info(f"Starter fix_02_02_pass3 på {csv_path}")
                            #fix_02_02_pass3(csv_path, csv_path_b06, alogger)                    

                        elif "05.02" in csv_path:
                            csv_path_b0501 = csv_path.replace("b_05.02", "b_05.01")
                            alogger.info(f"Starter fix_05_02_pass2 på {csv_path}")
                            fix_05_02_pass2(csv_path, csv_path_b0501, alogger)


    except Exception as e:
        alogger.error(f"Feil ved prosessering av katalog {customer_path_p1}: {e}")

