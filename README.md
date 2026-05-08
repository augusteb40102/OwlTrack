# OwlTrack

## Trumpas programos aprašas

Sukurta programa, kurios tikslas yra šiek tiek palengvinti studentų kasdieninį gyvenimą. Atsidarius programą ir prisiregistravus galima naudotis programoje sukurtomis funkcijomis – kalendorius, To-Do list ir skaičiuoklė.

- **Kalendorius** skirtas dienų bei emocijų sekimui, veiklos pažymėjimui.
- **To-Do list'e** galima patogiai pridėti užduotis, kurios taip pat pasižymi ir kalendoriuje pagal parinktą užduoties pabaigos terminą. Taip pat šioje skiltyje galima sekti jau atliktų užduočių statistiką, stebėti progresą.
- **Skaičiuoklė** skirta mokymosi progreso sekimui. Galima įvesti siekiamą vidurkį, kurio prognozę programa apskaičiuoja pagal esamų modulio pažymių vidurkį. Skaičiuoklėje galima pridėti norimus modulius, pažymėti kreditus, gautus pažymius ir t.t.

Taip pat programoje patogu keisti fono temą, slaptažodį, bei prireikus pagalbos susisiekti su mūsų komanda el. paštu.

## Technologijos

OwlTrack programa sukurta naudojant šias atvirojo kodo technologijas:

* [Python](https://www.python.org) - pagrindinė programavimo kalba
* [Flet](https://flet.dev) - vartotojo sąsajos kūrimo sistema
* [SQLite](https://www.sqlite.org) - vietinė duomenų bazė
* [bcrypt](https://github.com/pyca/bcrypt) - saugiam slaptažodžių kodavimui
* [python-dotenv](https://github.com/theskumar/python-dotenv) - aplinkos kintamųjų valdymui (el. pašto konfigūracija)
* [httpx](https://www.python-httpx.org) - HTTP užklausoms
* [oauthlib](https://github.com/oauthlib/oauthlib) - autentifikavimo sprendimams
* [PyInstaller](https://pyinstaller.org) - programos supakavimui į vykdomąjį failą

## Įrankiai

Projektui kurti ir paleisti naudojami šie įrankiai:

* [Git](https://git-scm.com) - versijų kontrolei
* [pip](https://pip.pypa.io) - Python priklausomybių diegimui
* [venv](https://docs.python.org/3/library/venv.html) - virtualiai Python aplinkai sukurti

## Duomenų bazė

OwlTrack naudoja **SQLite** – lengvą, serverio nereikalaujančią duomenų bazę, kuri saugoma lokaliai kaip `owltrack.db` failas.

Duomenų bazėje saugoma:

- naudotojų paskyros (el. paštas, užkoduotas slaptažodis)
- To-Do užduotys su kategorijomis ir užduočių pabaigos termino datomis
- kalendoriaus įrašai
- pažymių skaičiuoklės duomenys

Duomenų bazės struktūrą galima peržiūrėti naudojant SQLite CLI:

```bash
sqlite3 owltrack.db
.tables
```

## Kaip įsidiegti ir paleisti programą

Žemiau pateikti žingsniai, kaip pasiruošti darbo aplinką ir paleisti programą savo kompiuteryje.

1. Įsidiekite [Python 3.8+](https://www.python.org/downloads/) ir [Git](https://git-scm.com).
2. Atsisiųskite projekto saugyklą:

```bash
git clone https://github.com/augusteb40102/OwlTrack.git
cd OwlTrack
```

3. Sukurkite virtualią aplinką:

```bash
python -m venv venv
```

4. Aktyvuokite virtualią aplinką:

- macOS/Linux:

```bash
source venv/bin/activate
```

- Windows:

```bash
venv\Scripts\activate
```

5. Įdiekite reikalingas bibliotekas:

```bash
pip install -r requirements.txt
```

6. Sukurkite `.env` failą projekto kataloge. Jame turi būti šie kintamieji:

```env
GMAIL_USER=jusu@gmail.com
GMAIL_PASSWORD=jusu_app_password
```

7. Paleiskite programą:

```bash
python main.py
```

> **Pastaba:** Jei programa paleidžiama iš vykdomojo failo, `assets/` aplankas turi būti toje pačioje direktorijoje.

## Programos instrukcija naudotojui
### Registracija
### Prisijungimas
Atidarius programą vartotojas nukreipiamas į pagrindinį langą, kur matomi mygtukai „Log in“ ir „Register“. Norėdamas prisijungti vartotojas turi paspausti „Log in“ mygtuką.

<img width="940" height="478" alt="image" src="https://github.com/user-attachments/assets/90898184-5e54-4cd1-ae58-0e58365836c4" />
