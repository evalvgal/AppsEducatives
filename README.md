# 🧮 Apps Educatives de Matemàtiques i Llengua

Col·lecció d'aplicacions educatives interactives desenvolupades amb **Python** i **Pygame** orientades a nens i alumnes de primària i secundària per aprendre el concepte de les centenes, desenes i unitats, la resolució visual de sumes i restes amb portades, les regles d'accentuació en català i els accents diacrítics.

---

## 📂 Estructura del Projecte

El projecte està organitzat sota una arquitectura Model-Vista (MVC) neta i modular:
- **Llengua/Accentuacio/**: Aplicació interactiva de teoria i pràctica pas a pas de les normes d'accentuació en català (Agudes, Planes i Esdrúixoles), estructurada amb `grafics_accentuacio.py`, `accentuacio.py` i `diccionari.py`.
- **Llengua/Diacritica/**: Aplicació interactiva per a pissarra digital de l'estudi dels accents diacrítics en català, amb paginació numèrica inferior, targetes duals (amb accent / sense accent) i ressaltat intel·ligent d'exemples. Està composta per `grafics_diacritics.py`, `diacritics.py` i `diccionari_diacritics.py`.
- **Llengua/DUC/**: Aplicació del DUC (Regla mnemotècnica i descomposició de nombres en català).
- **Matematiques/ConcepteUDC/**: Visualització de blocs base 10 per entendre centenes, desenes i unitats.
- **Matematiques/Restes/**: Aplicació interactiva de la resta amb portades (mètode de compensació).
- **Matematiques/Sumes/**: Aplicació interactiva de la suma amb portades i animacions.

---

## ⚙️ Requisits del Sistema i Instal·lació

Abans de començar, necessites tenir instal·lat **Python** al teu ordinador.

### 1. Instal·lació de Python

#### 🪟 Windows:
1. Ves a la web oficial de [Python](https://www.python.org/downloads/) i descarrega l'última versió recomanada.
2. Durant la instal·lació, **marca obligatòriament la casella** *"Add Python to PATH"* abans de clicar a *Install Now*.

#### 🍎 macOS:
1. macOS sol venir amb una versió de Python o bé es pot instal·lar des del web oficial o mitjançant [Homebrew](https://brew.sh/):
   ```bash
   brew install python
   ```

---

### 2. Instal·lació de la llibreria Pygame

Un cop tinguis Python instal·lat, obre la teva terminal (Terminal a macOS o Command Prompt / PowerShell a Windows) i instal·la Pygame executant:

#### 🪟 Windows:
```cmd
pip install pygame
```

#### 🍎 macOS:
```bash
pip3 install pygame
```

---

## ▶️ Com executar les aplicacions

Per executar qualsevol de les aplicacions, situa't amb la terminal dins de la carpeta corresponent i llança l'arxiu gràfic:

### 🔹 Accents Diacrítics en Català:
```bash
cd Llengua/Diacritica
python grafics_diacritics.py
```

### 🔹 Accentuació en Català:
```bash
cd Llengua/Accentuacio
python grafics_accentuacio.py
```

### 🔹 DUC de Llengua:
```bash
cd Llengua/DUC
python grafics_DUC.py
```

### 🔹 Suma amb Portades:
```bash
cd Matematiques/Sumes
python grafics_sumes.py
```

### 🔹 Resta amb Portades:
```bash
cd Matematiques/Restes
python grafics_restes.py
```

### 🔹 Concepte UDC:
```bash
cd Matematiques/ConcepteUDC
python grafics_concepteUDC2.py
```

*(Nota: A macOS, si tens diferents versions de Python instal·lades, utilitza `python3` en comptes de `python`).*

---

## 📦 Generació d'Executables (.exe / .app)

Si vols convertir qualsevol d'aquests programes en un fitxer executable independent (perquè s'obri fent doble clic en qualsevol ordinador sense necessitat de tenir Python ni Pygame instal·lats), utilitzarem la llibreria **PyInstaller**.

### 1. Instal·lar PyInstaller

Instal·la PyInstaller al teu sistema:

- **Windows:**
  ```cmd
  pip install pyinstaller
  ```
- **macOS:**
  ```bash
  pip3 install pyinstaller
  ```

---

### 2. Crear l'executable

Situa't a la carpeta de l'aplicació que vulguis empaquetar (per exemple, a `Diacritica`) i executa la comanda següent:

```bash
pyinstaller --noconsole --onefile grafics_diacritics.py
```

> **Nota:** L'opció `--noconsole` s'utilitza perquè s'obri directament la interfície gràfica de Pygame sense mostrar la finestra negra de fons de la terminal, i `--onefile` crea un sol fitxer executable.

---

### 3. On trobar l'executable generat?

Un cop finalitzi el procés de compilació, veuràs que s'ha creat una nova carpeta anomenada **`dist`** dins del directori on et trobis:
- **En Windows:** Trobaràs un arxiu `grafics_diacritics.exe`.
- **En macOS:** Trobaràs una aplicació autònoma `grafics_diacritics.app` (o executable d'Unix).