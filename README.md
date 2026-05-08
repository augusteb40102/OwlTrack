<div align="left"> <img src="assets/owl_clean.png" alt="OwlTrack logo" width="180" /> </div>

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

Paspaudus „Log in“ vartotojas nukreipiamas į prisijungimo langą. Čia reikia įvesti el. pašto adresą ir slaptažodį. Jei naudotojas nori, kad programa jį atsimintų ir sekantį kartą nereikėtų vesti duomenų, reikia pažymėti „Remember me“ varnelę.

<img width="940" height="471" alt="image" src="https://github.com/user-attachments/assets/818d43fd-1ec6-441d-bc82-3578a688c08a" />

Vartotojui pamiršus slaptažodį reikia paspausti mygtuką „Forgot password?“. Vartotojas bus nukreipiamas i langą, kuriame reikės įvesti užregistruotą el. pašto adresą ir paspausti mygtuką „Send link“. Vartotojas į paštą gaus kodą, kurį reikės suvesti vietoje slaptažodžio ir tuomet naudotojas sėkmingai prisijungs prie paskyros.

<img width="940" height="461" alt="image" src="https://github.com/user-attachments/assets/efa7cb89-3bf5-4b9f-af7c-474eff3640be" />

Jei prisijungimas pavyko sėkmingai, atsivers pradinis programos langas:

<img width="940" height="482" alt="image" src="https://github.com/user-attachments/assets/4728b60b-e1c0-4cd7-9fd5-4328a4ea2f03" />

### Kalendorius
Pradiniame lange paspaudus kalendoriaus rėmų plotą, vartotojui atsidarys kalendoriaus langas, kuriame galima matyti metus, mėnesius, dienas, pažymėtas veiklas.

<img width="940" height="471" alt="image" src="https://github.com/user-attachments/assets/f3ad7df1-b947-40d9-a721-3977535c7978" />

Norint užregistruoti veiklą, arba pridėti tam tikros dienos emociją, reikia paspausti ant norimos datos. Paspaudus atsidaro langelis, kuriame vartotojas gali įvesti norimą veiklą, bei pasirikti emociją.

<img width="940" height="475" alt="image" src="https://github.com/user-attachments/assets/8df10275-d9ad-432a-8891-231e80ee3c53" />

Paspaudus mygtuką „Save“ langelis pradings, o kalendoriuje pažymėta diena nusispalvins rožine spalva. Užvedus pelytę ant to langelio matysime užregistruotą veiklą:

<img width="940" height="468" alt="image" src="https://github.com/user-attachments/assets/5d7e94f3-9681-4cfc-a4bc-e59cc81a7657" />

Užregistravus užduotį To-Do list‘e, kalendoriuje taip pat atsiras pažymėta diena (pažymi tą dieną, kurią turi būti pabaigta užduotis), ji nusispalvina žydra spalva. Užvedus pelytę ant dienos vartotojas taip pat pamatys užduoties pavadinimą, bei tipą.

<img width="940" height="462" alt="image" src="https://github.com/user-attachments/assets/8d6d23d7-d27d-4d30-a2db-261511bdae00" />
