# SSFIXER

SSFIXER er et Python-basert verktøy for validering, korrigering og verifisering av Steady State-data i henhold til EU-reguleringer. Verktøyet kan brukes til å prosessere og korrigere CSV-filer basert på spesifikasjoner fra Steady State-rapportering og DORA 4.0 taxonomi.

## Installering og oppsett

### 1. Klone prosjektet
Først må du klone prosjektet til din lokale maskin:

```bash
git clone https://github.com/brukernavn/ssfixer.git
cd ssfixer
```

### 2. Oppsett av virtual environment
For å isolere prosjektets avhengigheter, anbefales det å bruke et virtuelt miljø. Dette kan opprettes og aktiveres med følgende kommandoer:

#### a) Opprett et virtuelt miljø:

```bash
python -m venv .venv
```

#### b) Aktiver det virtuelle miljøet:
På Windows:

```bash
.venv\Scripts\activate
```

### 3. Installer nødvendige avhengigheter
Når det virtuelle miljøet er aktivert, installerer du alle nødvendige avhengigheter ved å bruke pip:

```bash
pip install -r requirements.txt
Hvis requirements.txt ikke finnes, kan du installere nødvendige biblioteker manuelt (se eksempel nedenfor).
```

#### Eksempler på nødvendige biblioteker:
```bash
pip install pandas
pip install openpyxl
```

### 4. Konfigurasjon med .env
Opprett en .env-fil i prosjektmappen for å lagre eventuelle konfigurasjonsinnstillinger. En typisk .env-fil kan inneholde miljøvariabler som f.eks. filbaner, API-nøkler eller annen viktig informasjon.

Eksempel på en .env-fil:

```bash
DATA_PATH=./data
LOGGING_LEVEL=INFO
```

### 5. Kjøre programmet
Programmet kan kjøres ved å bruke Python, og det er laget for å prosessere Steady State-data gjennom tre pass (Pass 1, Pass 2, Pass 3):

```bash
python validator.py
Dette vil prosessere alle relevante filer i ./data katalogen og bruke de definisjonene og korrigeringene som er spesifisert i filene.
```

### Beskrivelse av filene
**validator.py**
Hovedprogrammet som styrer hele validerings- og prosesseringsprosessen. Programmet bruker funksjoner fra andre moduler for å prosessere Steady State-rapportene.

- Pass 1: Prosesserer filene, fjerner tomme linjer og duplikater.
- Pass 2: Korrigerer eventuelle feil og mangler i filene basert på EU-reguleringene.
- Pass 3: Verifiserer filene mot DORA 4.0 taxonomi.

**process_customer_files_pass1.py**

Denne metoden rydder opp i filer som er lagret i "META-INF" og "reports" for hver kunde i prosjektet. Prosessen skjer i flere trinn:

- Opprette nødvendige mapper: Først sørger koden for at hovedmappen for den nye katalogen (customer_path_p1) eksisterer, og oppretter den hvis den ikke finnes. Dette er mappen der de rensede filene skal lagres.

- Iterasjon gjennom undermapper: Deretter går programmet gjennom alle kundens filer i de to relevante undermappene ("META-INF" og "reports"). For hver av disse undermappene sjekker den om mappen eksisterer. Hvis den gjør det, går koden videre til å prosessere innholdet i mappen.

- Opprette undersmapper i den nye katalogen: I hver av de to undermappene opprettes en tilsvarende undermappe i den nye katalogen (customer_path_p1), hvis den ikke allerede finnes.

- Filbehandling – Rensing av filer: For hver fil i undermappene, åpnes filen, og den prosesseres ved hjelp av funksjonen clean_file. Denne funksjonen fjerner både tomme linjer og duplikatlinjer fra filene.

- Lagring av rensede filer: Etter at filene er renset, lagres de i den nye katalogen (customer_path_p1), som gjør at de opprinnelige filene forblir intakte, og de rensede versjonene kan brukes videre i prosessen.

- Logging og feilhåndtering: Hele prosessen logges for å gi oversikt over hva som skjer. Hvis det oppstår en feil under behandlingen av filene, logges feilen med en feilmelding som hjelper utvikleren eller brukeren å forstå hva som gikk galt.

Totalt sett håndterer denne koden filene for hver kunde, sørger for at nødvendige mapper opprettes i den nye katalogen, og sørger for at alle dataene i filene er renset fra unødvendige linjer før de lagres på nytt for videre behandling.


**fix_01_02.py til fix_07_01.py**
Disse filene inneholder funksjoner som er ansvarlige for spesifikke korrigeringer som kreves i Steady State-rapportene. Hver fil tar for seg et sett med regler og logikk for å endre eller korrigere feltene i CSV-filene.

process_customer_files_pass1.py, process_customer_files_pass2.py, process_customer_files_pass3.py
Modulene som inneholder funksjonene for å prosessere filene under de tre forskjellige passene. De er ansvarlige for å håndtere og korrigere dataene i de ulike trinnene i prosessen.

**csv_validator.py**
Verktøy for validering av CSV-filene mot spesifikasjonene for DORA 4.0 taxonomi. Brukes til å sjekke at filene samsvarer med de nødvendige kravene før de blir prosessert.

**label_utils.py**
En hjelpefil som håndterer lastingen av etikettdefinisjoner for DORA 4.0 taxonomi. Brukes til å laste og håndtere de nødvendige etikettene som trengs for validering.

**taxonomy**
Inneholder taxonomifilene som definere strukturen og spesifikasjonene for Steady State-rapporteringen.