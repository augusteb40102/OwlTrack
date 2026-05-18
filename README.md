<div align="left"> <img src="assets/owl_clean.png" alt="OwlTrack logo" width="180" /> </div>

# OwlTrack

## Darbą atliko
* Augustė Bataitytė
* Austėja Jesiulionytė
* Agnė Merkelytė
## Trumpas programos aprašas

Sukurta programa, kurios tikslas yra šiek tiek palengvinti studentų kasdieninį gyvenimą. Atsidarius programą ir prisiregistravus galima naudotis programoje sukurtomis funkcijomis – kalendorius, To-Do list ir skaičiuoklė.

- **Kalendorius** skirtas dienų bei emocijų sekimui, veiklos pažymėjimui.
- **To-Do list'e** galima patogiai pridėti užduotis, kurios taip pat pasižymi ir kalendoriuje pagal parinktą užduoties pabaigos terminą. Taip pat šioje skiltyje galima sekti jau atliktų užduočių statistiką, stebėti progresą.
- **Skaičiuoklė** skirta mokymosi progreso sekimui. Galima įvesti siekiamą vidurkį, kurio prognozę programa apskaičiuoja pagal esamų modulio pažymių vidurkį. Skaičiuoklėje galima pridėti norimus modulius, pažymėti kreditus, gautus pažymius ir t.t.

Taip pat programoje patogu keisti fono temą, slaptažodį, bei prireikus pagalbos susisiekti su mūsų komanda el. paštu.

## Testavimas
<img width="531" height="737" alt="image" src="https://github.com/user-attachments/assets/893417d7-36a0-4169-b28b-42c97c2ff2a4" />
<img width="532" height="817" alt="image" src="https://github.com/user-attachments/assets/1dda3f14-69ac-4a9a-b1d3-7824989767e9" />
<img width="530" height="635" alt="image" src="https://github.com/user-attachments/assets/c704174f-8438-4d0e-9e7d-f12b958133f4" />
<img width="531" height="707" alt="image" src="https://github.com/user-attachments/assets/76492ba7-fdfc-4c88-9f53-bb1c5765d8d1" />
<img width="530" height="782" alt="image" src="https://github.com/user-attachments/assets/40fa90ff-709d-4bfc-b1f0-a3aff3d4429b" />
<img width="532" height="436" alt="image" src="https://github.com/user-attachments/assets/ad2cb4e0-588f-4bce-8b22-c54550fe791c" />
<img width="532" height="770" alt="image" src="https://github.com/user-attachments/assets/5ce0aefa-9e8e-4182-89e9-99404f92e6b2" />
<img width="531" height="126" alt="image" src="https://github.com/user-attachments/assets/837bf564-bfab-4044-94b7-2a3ab58b8499" />








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
Atidarius programėlę, vartotojas nukreipiamas į pradinį langą. Jei vartotojas neturi paskyros, visų pirma ją reiktų susikurti. Vartotojas, kuris neturi paskyros, spaudžia mygtuką „Register“. Priešingu atveju, prisijungiama naudojant mygtuką „Login“.

<img width="975" height="495" alt="image" src="https://github.com/user-attachments/assets/26ffbd67-b3df-4c45-89f1-37c66601517c" />

Atidaromas registracijos langas, kuriame prašoma suvesti reikiamus duomenis. Pirmajame langelyje suvedamas vartotojo elektroninis paštas, antrajame vardas, trečiajame ir ketvirtajame įvedamas, pakartojamas slaptažodis. Spaudžiame mygtuką „Create account“.

<img width="975" height="494" alt="image" src="https://github.com/user-attachments/assets/d917a596-362a-4f33-b6b5-d4b6447bb41e" />

Po sėkmingos registracijos, atidaromas naujas langas, kuriame vartotojas turi galimybę pasirinkti norima pelėdžiuką ir nustatyti šią ikonėlę kaip profilinę nuotrauką. Mygtukas „Skip“  leidžia praleisti šį žingsnį. Pasirinkus paveiksliuką, spaudžiame „Confirm Selection“.

<img width="975" height="494" alt="image" src="https://github.com/user-attachments/assets/67983aa1-4043-44a2-9f08-d6f4607efa14" />

### Prisijungimas
Atidarius programą vartotojas nukreipiamas į pagrindinį langą, kur matomi mygtukai „Log in“ ir „Register“. Norėdamas prisijungti vartotojas turi paspausti „Log in“ mygtuką.

<img width="940" height="478" alt="image" src="https://github.com/user-attachments/assets/90898184-5e54-4cd1-ae58-0e58365836c4" />

Paspaudus „Log in“ vartotojas nukreipiamas į prisijungimo langą. Čia reikia įvesti el. pašto adresą ir slaptažodį. Jei naudotojas nori, kad programa jį atsimintų ir sekantį kartą nereikėtų vesti duomenų, reikia pažymėti „Remember me“ varnelę.

<img width="940" height="471" alt="image" src="https://github.com/user-attachments/assets/818d43fd-1ec6-441d-bc82-3578a688c08a" />

Vartotojui pamiršus slaptažodį reikia paspausti mygtuką „Forgot password?“. Vartotojas bus nukreipiamas i langą, kuriame reikės įvesti užregistruotą el. pašto adresą ir paspausti mygtuką „Send link“. Vartotojas į paštą gaus kodą, kurį reikės suvesti vietoje slaptažodžio ir tuomet naudotojas sėkmingai prisijungs prie paskyros.

<img width="940" height="461" alt="image" src="https://github.com/user-attachments/assets/efa7cb89-3bf5-4b9f-af7c-474eff3640be" />

Jei prisijungimas pavyko sėkmingai, atsivers pradinis programos langas:

<img width="940" height="482" alt="image" src="https://github.com/user-attachments/assets/4728b60b-e1c0-4cd7-9fd5-4328a4ea2f03" />

### Pagrindinis langas
Atidaromas pagrindinis vartotojo langas, kuriame galime atlikti skirtingas funkcijas: pažymėti įvykius kalendoriuje, sukurti įvykių atmintinę, sekti pažymių pasiekimų lygį naudojantis specialia skaičiuokle.

<img width="975" height="494" alt="image" src="https://github.com/user-attachments/assets/e7481620-bd89-4e30-87ce-a5a0a30df4af" />

Paspaudus mygtuką „Settings“ esančiame pagrindinio lango kairėje pusėje, galima pakeisti programėlės tematiką, profilio nuotrauką ir slaptažodį. Po atliktų pakeitimų svarbu paspausti mygtuką „Save“. Keičiamam slaptažodžiui papildomai pasirenkamas mygtukas „Confirm“.

<img width="975" height="490" alt="image" src="https://github.com/user-attachments/assets/b4a368ea-9b2b-4d13-bcdd-b1627fb9484d" />

Jei vartotojas nenori išsaugoti pasirinkimų, spaudžiama „Cancel“.

<img width="975" height="493" alt="image" src="https://github.com/user-attachments/assets/9c5e9c4c-0306-4a62-ad2b-03e885dfa0f5" />

Paspaudus mygtuką „Help“ esančiame pagrindinio lango kairėje pusėje,  galima gauti reikiamą informaciją apie programėlės kūrėjus, nurodomi kontaktai, kuriais galima kreiptis iškilus klausimams.

<img width="975" height="490" alt="image" src="https://github.com/user-attachments/assets/552c811b-b8d2-44a9-8c4a-d495cf0589ba" />

Paspaudus mygtuką „Log Out“ esančiame apačioje, pagrindinio lango kairėje pusėje, galima atsijungti nuo programėlės ir baigti sesiją. Po mygtuko paspaudimo, vartotojas nukreipiamas į prisijungimo langą.

<img width="975" height="490" alt="image" src="https://github.com/user-attachments/assets/d9f28483-b6fb-41c1-99c9-4973108f9320" />

### Kalendorius
Pradiniame lange paspaudus kalendoriaus rėmų plotą, vartotojui atsidarys kalendoriaus langas, kuriame galima matyti metus, mėnesius, dienas, pažymėtas veiklas.

<img width="940" height="471" alt="image" src="https://github.com/user-attachments/assets/f3ad7df1-b947-40d9-a721-3977535c7978" />

Norint užregistruoti veiklą, arba pridėti tam tikros dienos emociją, reikia paspausti ant norimos datos. Paspaudus atsidaro langelis, kuriame vartotojas gali įvesti norimą veiklą, bei pasirikti emociją.

<img width="940" height="475" alt="image" src="https://github.com/user-attachments/assets/8df10275-d9ad-432a-8891-231e80ee3c53" />

Paspaudus mygtuką „Save“ langelis pradings, o kalendoriuje pažymėta diena nusispalvins rožine spalva. Užvedus pelytę ant to langelio matysime užregistruotą veiklą:

<img width="940" height="468" alt="image" src="https://github.com/user-attachments/assets/5d7e94f3-9681-4cfc-a4bc-e59cc81a7657" />

Užregistravus užduotį To-Do list‘e, kalendoriuje taip pat atsiras pažymėta diena (pažymi tą dieną, kurią turi būti pabaigta užduotis), ji nusispalvina žydra spalva. Užvedus pelytę ant dienos vartotojas taip pat pamatys užduoties pavadinimą, bei tipą.

<img width="940" height="462" alt="image" src="https://github.com/user-attachments/assets/8d6d23d7-d27d-4d30-a2db-261511bdae00" />

### To-Do-List
Paspaudus ant „To-Do-List“ langelio esančiame viršuje, pagrindinio lango dešinėje pusėje. Atidaromas detalesnis langas, kuriame galima pridėti įvykius. Apskritimas, prie pavaizduoto įvykio, leidžia pažymėti šį kaip atliktą ir perkelti prie atliktųjų sąrašo. 

<img width="975" height="495" alt="image" src="https://github.com/user-attachments/assets/f9aad54c-4ddf-4047-b755-078aedf7af3f" />

Paspaudus mygtuką „Add new task“ išskleidžiamas nedidelis langelis, kuriame vartotojas gali suvesti duomenis apie artėjantį įvykį ir pridėti jį į sąrašą.

<img width="975" height="496" alt="image" src="https://github.com/user-attachments/assets/8a873c26-18fb-47dc-8b08-fbaa010309b6" />

Svarbiausi įvykiai sąraše pateikiami pradžioje. Kiekvienas pažymėtas įvykis sekamas, daroma mėnesio statistika apie atliktus darbus, praėjusius susitikimus. Vartotojui pateikiama diagrama apie jo produktyvumą.

<img width="975" height="495" alt="image" src="https://github.com/user-attachments/assets/67f2a16b-e565-4321-bc18-c75409cb6e9d" />

### Grade Calculator
Paspaudus ant „Grade Calculator“ langelio esančiame apačioje, pagrindinio lango dešinėje pusėje. Atidaromas detalesnis langas, kuriame galima sekti pažangumą, matyti ar gauti pažymiai, rezultatai tenkina stipendijos reikalavimus.  Vartotojas gali nurodyti siekiamą vidurkį. Pagal esamą ir siekiamą pažymį skaičiuojama ar tenkinama stipendijos sąlyga.

<img width="975" height="495" alt="image" src="https://github.com/user-attachments/assets/4cb66f58-3327-4cf3-adbd-14c8f6567bd8" />

Paspaudus mygtuką „Add New Module“ vartotojui rodomas langas, kuriame galima įvesti naują modulį bei jo atsiskaitymus. Įvestą informaciją būtina išsaugoti mygtuku „Save Module“ .  Ištrinti modulį galima paspaudus šiukšliadėžės ikonėlę, kuri pavaizduota dešinėje eilutės pusėje.

<img width="975" height="492" alt="image" src="https://github.com/user-attachments/assets/b2676117-ee4f-4a4d-9710-b71837e50b33" />

Norint pridėti ar redaguoti atsiskaitymą prie esančio modulio, vartotojas turi spausti pieštuko ikonėlę pavaizduotą dešinėje pusėje. Atskleidžiamas redagavimo langas, kuriame paspaudus „Add Assessment“ galima pridėti naują užduotį. Pakeitimai turi būti išsaugoti mygtuku „Save Changes“.

<img width="975" height="494" alt="image" src="https://github.com/user-attachments/assets/9b6e4c13-2e62-43e0-b60c-43dfe6dfdd4d" />










