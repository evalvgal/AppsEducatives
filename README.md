# 🧮 Apps Educatives de Matemàtiques i Llengua

Col·lecció d'aplicacions educatives interactives desenvolupades amb **Python** i **Pygame** orientades a nens i alumnes d'infantil, primària i secundària per aprendre el concepte de les centenes, desenes i unitats, la resolució visual de sumes, restes i multiplicacions amb portades, la descomposició factorial en nombres primers, el càlcul del mínim comú múltiple (m.c.m.) i màxim comú divisor (M.C.D.), les regles d'accentuació en català, els accents diacrítics, els diftongs i hiats, la lectoescriptura i el dibuix animat interactiu.

## 📂 Estructura del Projecte

El projecte està organitzat per etapes educatives sota una arquitectura Model-Vista-Controlador (MVC) neta i modular:

```text
AppsEducatives/
├── Infantil/
│   ├── Dibuix/
│   │   ├── dibuix.py
│   │   └── grafics_dibuix.py
│   └── Lectoescriptura/
│       ├── grafics_nombreslletres.py
│       └── nombreslletres.py
├── Primaria/
│   ├── Llengua/
│   │   ├── Accentuacio/
│   │   │   ├── Diacritica/
│   │   │   │   ├── diacritics.py
│   │   │   │   ├── diccionari_diacritics.py
│   │   │   │   └── grafics_diacritics.py
│   │   │   └── Paraules/
│   │   │       ├── accentuacio.py
│   │   │       ├── diccionari.py
│   │   │       └── grafics_accentuacio.py
│   │   ├── DiftongsHiats/
│   │   │   ├── diccionaridiftongshiat.py
│   │   │   ├── diftongshiat.py
│   │   │   └── grafics_diftongshiat.py
│   │   └── DUC/
│   │       ├── DUC.py
│   │       └── grafics_DUC.py
│   └── Matematiques/
│       ├── ConcepteUDC/
│       │   ├── concepteUDC.py
│       │   ├── concepteUDC2.py
│       │   ├── grafics_concepteUDC.py
│       │   └── grafics_concepteUDC2.py
│       ├── Descomposicio/
│       │   ├── descomposicio.py
│       │   ├── diccionariDescomposicio.py
│       │   └── grafics_descomposicio.py
│       ├── mcmMcd/
│       │   ├── diccionarimcmMcd.py
│       │   ├── grafics_mcmMcd.py
│       │   └── mcmMcd.py
│       └── Operacions/
│           └── Nombres/
│               ├── Multiplicacions/
│               │   ├── diccionarimultiplicacio.py
│               │   ├── grafics_multiplicacio.py
│               │   └── multiplicacio.py
│               ├── Restes/
│               │   ├── grafics_restes.py
│               │   └── resta_portades.py
│               └── Sumes/
│                   ├── grafics_sumes.py
│                   └── sumes_portades.py
└── README.md
```

### 🧸 Educació Infantil

* **Infantil/Dibuix/**: Aplicació interactiva de dibuix lliure i animació procedimental intel·ligent. Classifica automàticament els traços dels infants (onades del mar, personatges caminant amb rebot i pas sincronitzat de braços i cames, mans que saluden amb els dits, o objectes saltant) i els dóna vida amb partícules. Està composta per `dibuix.py` i `grafics_dibuix.py`.

* **Infantil/Lectoescriptura/**: Aplicació interactiva per a pissarra digital orientada a infantil per aprendre a escriure lletres (majúscules i minúscules) i nombres (0 al 9) amb animació de traços guiats i resseguit tàctil. Està composta per `grafics_nombreslletres.py` i `nombreslletres.py`.

### 🎒 Educació Primària

#### Llengua Catalana

* **Primaria/Llengua/Accentuacio/Paraules/**: Aplicació interactiva de teoria i pràctica pas a pas de les normes d'accentuació en català (Agudes, Planes i Esdrúixoles). Està composta per `accentuacio.py`, `grafics_accentuacio.py` i `diccionari.py`.

* **Primaria/Llengua/Accentuacio/Diacritica/**: Aplicació interactiva per a pissarra digital de l'estudi dels accents diacrítics en català, amb paginació numèrica inferior, targetes duals (amb accent / sense accent) i ressaltat intel·ligent d'exemples. Està composta per `diacritics.py`, `grafics_diacritics.py` i `diccionari_diacritics.py`.

* **Primaria/Llengua/DiftongsHiats/**: Aplicació interactiva per a l'aprenentatge i pràctica dels diftongs (creixents i decreixents) i els hiats, així com exercicis interactius de classificació i separació sil·làbica. Està composta per `diftongshiat.py`, `grafics_diftongshiat.py` i `diccionaridiftongshiat.py`.

* **Primaria/Llengua/DUC/**: Aplicació del DUC (Regla mnemotècnica i descomposició de nombres en català), composta per `DUC.py` i `grafics_DUC.py`.

#### Matemàtiques

* **Primaria/Matematiques/ConcepteUDC/**: Visualització de blocs base 10 per entendre centenes, desenes i unitats.

* **Primaria/Matematiques/Descomposicio/**: Aplicació interactiva sota el patró MVC per aprendre els nombres primers del 1 al 1000 i practicar la descomposició factorial pas a pas amb el mètode clàssic de la ratlla vertical. Està composta per `descomposicio.py`, `grafics_descomposicio.py` i `diccionariDescomposicio.py`.

* **Primaria/Matematiques/mcmMcd/**: Aplicació interactiva sota el patró MVC per aprendre i practicar el càlcul del mínim comú múltiple (m.c.m.) i el màxim comú divisor (M.C.D.) pas a pas mitjançant la descomposició en factors primers amb ratlla vertical. Està composta per `mcmMcd.py`, `grafics_mcmMcd.py` i `diccionarimcmMcd.py`.

* **Primaria/Matematiques/Operacions/Nombres/Multiplicacions/**: Aplicació interactiva sota el patró MVC per practicar multiplicacions amb portades d'1, 2 i 3 xifres pas a pas amb visualització gràfica de les portades i explicacions detallades. Està composta per `multiplicacio.py`, `grafics_multiplicacio.py` i `diccionarimultiplicacio.py`.

* **Primaria/Matematiques/Operacions/Nombres/Restes/**: Aplicació interactiva de la resta amb portades (mètode de compensació), composta per `resta_portades.py` i `grafics_restes.py`.

* **Primaria/Matematiques/Operacions/Nombres/Sumes/**: Aplicació interactiva de la suma amb portades i animacions, composta per `sumes_portades.py` i `grafics_sumes.py`.

## ⚙️ Requisits del Sistema i Instal·lació

Abans de començar, necessites tenir instal·lat **Python** al teu ordinador.

### 1. Instal·lació de Python

#### 🪟 Windows Installation

1. Ves a la web oficial de [Python](https://www.python.org/downloads/) i descarrega l'última versió recomanada.

2. Durant la instal·lació, **marca obligatòriament la casella** *"Add Python to PATH"* abans de clicar a *Install Now*.

#### 🍎 macOS Installation

1. macOS sol venir amb una versió de Python o bé es pot instal·lar des del web oficial o mitjançant [Homebrew](https://brew.sh/):

   ```bash
   brew install python
   ```

### 2. Instal·lació de la llibreria Pygame

Un cop tinguis Python instal·lat, obre la teva terminal (Terminal a macOS o Command Prompt / PowerShell a Windows) i instal·la Pygame executant:

#### 🪟 Windows

```cmd
pip install pygame
```

#### 🍎 macOS

```bash
pip3 install pygame
```

## ▶️ Com executar les aplicacions

Per executar qualsevol de les aplicacions, situa't amb la terminal dins de la carpeta corresponent i llança l'arxiu principal:

### 🔹 Dibuix Animat Màgic (Infantil)

```bash
cd Infantil/Dibuix
python3 grafics_dibuix.py
```

### 🔹 Lectoescriptura (Infantil)

```bash
cd Infantil/Lectoescriptura
python3 nombreslletres.py
```

### 🔹 Diftongs i Hiats

```bash
cd Primaria/Llengua/DiftongsHiats
python3 diftongshiat.py
```

### 🔹 Accents Diacrítics en Català

```bash
cd Primaria/Llengua/Accentuacio/Diacritica
python3 diacritics.py
```

### 🔹 Accentuació en Català

```bash
cd Primaria/Llengua/Accentuacio/Paraules
python3 accentuacio.py
```

### 🔹 DUC de Llengua

```bash
cd Primaria/Llengua/DUC
python3 grafics_DUC.py
```

### 🔹 Descomposició en Factors Primers

```bash
cd Primaria/Matematiques/Descomposicio
python3 descomposicio.py
```

### 🔹 Mínim Comú Múltiple i Màxim Comú Divisor (m.c.m. i M.C.D.)

```bash
cd Primaria/Matematiques/mcmMcd
python3 mcmMcd.py
```

### 🔹 Multiplicacions amb Portades

```bash
cd Primaria/Matematiques/Operacions/Nombres/Multiplicacions
python3 multiplicacio.py
```

### 🔹 Suma amb Portades

```bash
cd Primaria/Matematiques/Operacions/Nombres/Sumes
python3 sumes_portades.py
```

### 🔹 Resta amb Portades

```bash
cd Primaria/Matematiques/Operacions/Nombres/Restes
python3 resta_portades.py
```

### 🔹 Concepte UDC

```bash
cd Primaria/Matematiques/ConcepteUDC
python3 grafics_concepteUDC2.py
```

*(Nota: A Windows, utilitza `python` en comptes de `python3`).*

## 📦 Generació d'Executables (.exe / .app)

Si vols convertir qualsevol d'aquests programes en un fitxer executable independent (perquè s'obri fent doble clic en qualsevol ordinador sense necessitat de tenir Python ni Pygame instal·lats), utilitzarem la llibreria **PyInstaller**.

### 1. Instal·lar PyInstaller

Instal·la PyInstaller al teu sistema:

* **Windows:**

  ```cmd
  pip install pyinstaller
  ```

* **macOS:**

  ```bash
  pip3 install pyinstaller
  ```

### 2. Crear l'executable

Situa't a la carpeta de l'aplicació que vulguis empaquetar (per exemple, a `Infantil/Dibuix`) i executa la comanda següent:

```bash
pyinstaller --noconsole --onefile grafics_dibuix.py
```

> **Nota:** L'opció `--noconsole` s'utilitza perquè s'obri directament la interfície gràfica de Pygame sense mostrar la finestra negra de fons de la terminal, i `--onefile` crea un sol fitxer executable.

### 3. On trobar l'executable generat?

Un cop finalitzi el procés de compilació, veuràs que s'ha creat una nova carpeta anomenada **`dist`** dins del directori on et trobis:

* **En Windows:** Trobaràs un arxiu `grafics_dibuix.exe`.

* **En macOS:** Trobaràs una aplicació autònoma `grafics_dibuix.app` (o executable d'Unix).

> **Nota:** Si vols crear executables per altres aplicacions del projecte, simplement substitueix `grafics_dibuix.py` pel nom del fitxer corresponent en les comandes anteriors.
