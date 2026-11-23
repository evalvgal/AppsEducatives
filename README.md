# 🧮 Apps Educatives de Matemàtiques i Llengua

Col·lecció d'aplicacions educatives interactives desenvolupades amb **Python** i **Pygame** orientades a nens i alumnes d'infantil, primària i secundària per aprendre el concepte de les centenes, desenes i unitats, la resolució visual de sumes, restes i multiplicacions amb portades, la pràctica de divisions pas a pas amb prova, la suma i la resta de fraccions amb mateix i diferent denominador (amb reducció al màxim per M.C.D.), la descomposició factorial en nombres primers, el càlcul del mínim comú múltiple (m.c.m.) i màxim comú divisor (M.C.D.), les regles d'accentuació en català, els accents diacrítics, els diftongs i hiats, la lectoescriptura i el dibuix animat interactiu.

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
│           ├── Fraccions/
│           │   ├── Restes/
│           │   │   ├── diccionariRestaFraccio.py
│           │   │   ├── grafics_restaFraccio.py
│           │   │   └── restaFraccio.py
│           │   └── Sumes/
│           │       ├── diccionariSumaFraccio.py
│           │       ├── grafics_sumaFraccio.py
│           │       └── sumaFraccio.py
│           └── Nombres/
│               ├── Divisions/
│               │   ├── diccionaridivisio.py
│               │   ├── divisio.py
│               │   └── grafics_divisio.py
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

* **Primaria/Matematiques/Operacions/Fraccions/Restes/**: Aplicació interactiva sota el patró MVC per aprendre pas a pas la resta de dues fraccions (garantint sempre que la segona fracció és menor que la primera) amb el mateix denominador (valors de l'1 al 999) i amb denominadors diferents (valors de l'1 al 50, amb descomposició en ratlla vertical per calcular l'm.c.m. i obtenir fraccions equivalents), així com la reducció al màxim de la fracció resultant mitjançant el càlcul del Màxim Comú Divisor (M.C.D.) i la divisió del numerador i denominador. Està composta per `restaFraccio.py`, `grafics_restaFraccio.py` i `diccionariRestaFraccio.py`.

* **Primaria/Matematiques/Operacions/Fraccions/Sumes/**: Aplicació interactiva sota el patró MVC per aprendre pas a pas la suma de dues fraccions amb el mateix denominador (valors de l'1 al 999) i amb denominadors diferents (valors de l'1 al 50, amb descomposició en ratlla vertical per calcular l'm.c.m. i obtenir fraccions equivalents), així com la reducció al màxim de la fracció resultant mitjançant el càlcul del Màxim Comú Divisor (M.C.D.) i la divisió del numerador i denominador. Està composta per `sumaFraccio.py`, `grafics_sumaFraccio.py` i `diccionariSumaFraccio.py`.

* **Primaria/Matematiques/Operacions/Nombres/Divisions/**: Aplicació interactiva sota el patró MVC per practicar divisions amb divisors d'1, 2 i 3 xifres (amb residu i sense residu) pas a pas amb el mètode de la caixa, explicacions detallades i prova de la divisió. Està composta per `divisio.py`, `grafics_divisio.py` i `diccionaridivisio.py`.

* **Primaria/Matematiques/Operacions/Nombres/Multiplicacions/**: Aplicació interactiva sota el patró MVC per practicar multiplicacions amb portades d'1, 2 i 3 xifres pas a pas amb visualització gràfica de les portades i explicacions detallades. Està composta per `multiplicacio.py`, `grafics_multiplicacio.py` i `diccionarimultiplicacio.py`.

* **Primaria/Matematiques/Operacions/Nombres/Restes/**: Aplicació interactiva de la resta amb portades (mètode de compensació), composta per `resta_portades.py` i `grafics_restes.py`.

* **Primaria/Matematiques/Operacions/Nombres/Sumes/**: Aplicació interactiva de la suma amb portades i animacions, composta per `sumes_portades.py` i `grafics_sumes.py`.

## ⚙️ Requisits del Sistema i Instal·lació

Abans de començar, necessites tenir instal·lat **Python** al teu ordinador.
