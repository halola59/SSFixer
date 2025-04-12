# SSFixer

SSFixer er et Python-basert verktøy for validering, korrigering og verifisering av Steady State-data i henhold til EU-reguleringer. Verktøyet kan brukes til å prosessere og korrigere CSV-filer basert på spesifikasjoner fra Steady State-rapportering og DORA 4.0 taxonomi.

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

## Beskrivelse av filene
### validator.py
Hovedprogrammet som styrer hele validerings- og prosesseringsprosessen. Programmet bruker funksjoner fra andre moduler for å prosessere Steady State-rapportene.

- Pass 1: Prosesserer filene, fjerner tomme linjer og duplikater (process_customer_files_pass1.py)
- Pass 2: Korrigerer eventuelle feil og mangler i filene basert på EU-reguleringene (process_customer_files_pass2.py)
- Pass 3: Verifiserer filene mot DORA 4.0 taxonomi (process_customer_files_pass3.py)

### process_customer_files_pass1.py
Denne metoden rydder opp i filer i katalogene "META-INF" og "reports" for hver kunde i prosjektet. Prosessen skjer i flere trinn:

- Opprette nødvendige mapper: Først sørger koden for at hovedmappen for den nye katalogen (customer_path_p1) eksisterer, og oppretter den hvis den ikke finnes. Dette er mappen der de rensede filene skal lagres.

- Iterasjon gjennom undermapper: Deretter går programmet gjennom alle kundens filer i de to relevante undermappene ("META-INF" og "reports"). For hver av disse undermappene sjekker den om mappen eksisterer. Hvis den gjør det, går koden videre til å prosessere innholdet i mappen.

- Opprette undersmapper i den nye katalogen: I hver av de to undermappene opprettes en tilsvarende undermappe i den nye katalogen (customer_path_p1), hvis den ikke allerede finnes.

- Filbehandling – Rensing av filer: For hver fil i undermappene, åpnes filen, og den prosesseres ved hjelp av funksjonen clean_file. Denne funksjonen fjerner både tomme linjer og duplikatlinjer fra filene.

- Lagring av rensede filer: Etter at filene er renset, lagres de i den nye katalogen (customer_path_p1), som gjør at de opprinnelige filene forblir intakte, og de rensede versjonene kan brukes videre i prosessen.

- Logging og feilhåndtering: Hele prosessen logges for å gi oversikt over hva som skjer. Hvis det oppstår en feil under behandlingen av filene, logges feilen med en feilmelding som hjelper utvikleren eller brukeren å forstå hva som gikk galt.

Funksjonen håndterer filene for hver kunde, sørger for at nødvendige mapper opprettes i den nye katalogen, og sørger for at alle dataene i filene er renset fra unødvendige linjer før de lagres på nytt for videre behandling.

### process_customer_files_pass2.py
Denne etoden utfører en serie korrigeringer på CSV-filer som tilhører kunder. Den er delt opp i to hoveddeler (Pass 2a og Pass 2b), og utfører forskjellige typer korrigeringer basert på filnavn og innholdet i hver fil. Hver del er godt logget for å sikre at alle trinn kan spores. Her er en oversikt over hva koden gjør:

#### Pass 2a: Filbehandling og Korrigering
Mål: Denne delen av prosessen tar for seg filer i mappene "META-INF" og "reports" i kundens katalog og utfører nødvendige feilrettinger på CSV-filer i henhold til et spesifikt sett med regler.

For hver CSV-fil som finnes i disse mappene, utføres ulike funksjoner avhengig av filnavnet.

Hvis filen er relatert til spesifikke kategorier, som f.eks. "01.02", "02.01", "03.01", osv., kalles den tilsvarende korreksjonsfunksjonen som er definert tidligere i koden, for eksempel fix_01_02, fix_02_01, og så videre.

Funksjonene som kalles utfører operasjoner som å rydde opp i dataene, oppdatere verdier, fylle ut tomme felter, og annet som kreves for å sikre at filene er i samsvar med de nødvendige spesifikasjonene.

#### Pass 2b: Videre Korrigeringer
Mål: Denne delen tar for seg å utføre ytterligere behandling på filene som ble behandlet i Pass 2a. Den spesifikke funksjonen som blir brukt her er fix_02_02_pass2 for å behandle visse CSV-filer.

For filene relatert til "02.02", blir det utført en ekstra korreksjon som involverer å erstatte referanser til andre filkategorier, som "b_06.01" og "b_05.01", for å sikre at relasjonene mellom filene er riktig oppdatert.

Funksjonen fix_05_02_pass2 blir brukt for å behandle filer relatert til "05.02", og utføre ytterligere nødvendige korrigeringer.

#### Loggføring
Alle viktige operasjoner og feil blir logget ved hjelp av logger.info() og logger.error() metoder for å gi klar og detaljert innsikt i prosessen.

Hver fil som behandles får et logginnslag som spesifiserer hvilken fil som behandles og hvilken operasjon som blir utført.

Hvis det oppstår feil under prosesseringen av katalogene, blir disse logget som en feilmelding, som gjør det mulig å diagnostisere og rette eventuelle problemer raskt.

#### Feilhåndtering
Hver prosess er omsluttet i en try-except blokk som sørger for at feil som skjer under filbehandling blir fanget og logget.

Ved feilprosesser blir det skrevet ut en feilmelding som inneholder detaljer om hvilke filer som forårsaket problemet, slik at de kan håndteres på en effektiv måte.

### process_customer_files_pass3.py

Denne filen håndterer pass 3 i en prosess som involverer validering av kundens CSV-filer mot den offisielle DORA 4.0 taxonomien. Hovedmålet med pass 3 er å forsikre at kundens data er i samsvar med de strenge reglene og strukturen definert i DORA (Digital Operational Resilience Act).

#### Struktur og Funksjon
Filens hovedfunksjon er prosesserings- og valideringsoperasjoner på kundens filer etter at de har blitt behandlet i tidligere trinn. Det gjøres på følgende måte:

- Mappestruktur og Filhåndtering:

-- Koden navigerer gjennom mappene reports og META-INF som er en del av kundens prosesserte data.
-- For hver JSON-fil som finnes i TAXONOMY_DIR (som inneholder spesifikasjonene for DORA 4.0), ser den etter tilsvarende CSV-fil i reports-mappen.
-- Det benyttes en case-insensitive søkefunksjon (find_csv_insensitive) for å finne CSV-filen, som gjør at den finner filen uavhengig av små og store bokstaver i filnavnet.

- Validering mot DORA 4.0 Taxonomi:

-- Når de relevante filene er funnet, leses JSON-definisjonen som beskriver strukturen og reglene for validering.
-- Et ekstra sett med etiketter (labels) kan også lastes inn fra en tilhørende XML-fil som beskriver feltene på en mer forståelig måte (dette er nyttig for feilmeldingene som genereres senere).
-- Koden sjekker om filen kan inneholde tomme felter ved å analysere filens navn. Hvis navnet indikerer at tomme verdier er tillatt (som for noen spesifikke CSV-filer), justeres valideringen for dette.

- Validering med validate_csv_against_schema:

Funksjonen validate_csv_against_schema kalles for å validere hver fil i henhold til DORA 4.0-reglene som er lastet inn fra JSON-filen.

-- Hvis valideringen gir feil (f.eks. uoverensstemmelser med DORA 4.0-reglene), blir disse feilene logget via logger-instansen. For hver feil gir loggen en detaljert beskrivelse av hva som er galt.
-- Hvis valideringen ikke gir noen feil, blir det logget at valideringen er fullført uten problemer.
- Feilhåndtering:

-- Koden håndterer potensielle feil under prosesseringen ved å bruke en try-except blokk, som fanger opp eventuelle problemer med filhåndtering, JSON-lasting, eller validering og logger dem som feilmeldinger.

- Ekstra Funksjoner:

-- load_json_definition: Denne funksjonen åpner og laster JSON-definisjonen som inneholder spesifikasjonene for validering.
-- find_csv_insensitive: Denne funksjonen søker etter en CSV-fil i en katalog, uavhengig av om filnavnet er skrevet med store eller små bokstaver.

#### Loggføring og Sporing
All aktivitet blir logget ved hjelp av loggeren som er overført som parameter i funksjonen:

- Det logges informasjon om hvilken fil som behandles.
- Det logges også spesifikke feil som oppstår under valideringen, samt en suksessmelding hvis filen er validert uten feil.
- Loggeren gir detaljert informasjon om eventuelle problemer som kan oppstå, og gjør det lettere å spore feilsituasjoner tilbake til de spesifikke CSV-filene som forårsaket dem.

### fix_01_02.py til fix_07_01.py
Disse filene inneholder funksjoner som er ansvarlige for spesifikke korrigeringer som kreves i Steady State-rapportene. Hver fil tar for seg et sett med regler og logikk for å endre eller korrigere feltene i CSV-filene.

process_customer_files_pass1.py, process_customer_files_pass2.py, process_customer_files_pass3.py
Modulene som inneholder funksjonene for å prosessere filene under de tre forskjellige passene. De er ansvarlige for å håndtere og korrigere dataene i de ulike trinnene i prosessen.

### csv_validator.py
Verktøy for validering av CSV-filene mot spesifikasjonene for DORA 4.0 taxonomi. Brukes til å sjekke at filene samsvarer med de nødvendige kravene før de blir prosessert.

### label_utils.py
En hjelpefil som håndterer lastingen av etikettdefinisjoner for DORA 4.0 taxonomi. Brukes til å laste og håndtere de nødvendige etikettene som trengs for validering.

### taxonomy
Inneholder taxonomifilene som definere strukturen og spesifikasjonene for Steady State-rapporteringen.