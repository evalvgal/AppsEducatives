DADES_TEORIA = {
    "diftongs": {
        "decreixents": {
            "títol": "Diftongs Decreixents",
            "definicio": "Un diftong decreixent es forma quan s'unta una vocal oberta (a, e, o) i una vocal tancada (i, u) en la mateixa síl·laba, sent la primera la vocal forta.",
            "classificacio": "En català tenim els següents diftongs decreixents: -ai, -ei, -ii, -oi, -ui, -au, -eu, -iu, -ou.",
            "exemples": [
                {"paraula": "aina", "silabes": "ai - na"},
                {"paraula": "peu", "silabes": "peu"}
            ]
        },
        "creixents": {
            "títol": "Diftongs Creixents",
            "definicio": "Un diftong creixent es forma amb una vocal tancada (i, u) davant d'una vocal oberta (a, e, o), pronunciades en la mateixa síl·laba (sovint amb i/u inicials o després de consonants gu/qu).",
            "classificacio": "Exemples de combinacions: gua, güe, güi, guo, qua, qüé, qüí, quo, ia, ie, io, ua, ue, uo.",
            "exemples": [
                {"paraula": "aigua", "silabes": "ai - gua"},
                {"paraula": "quota", "silabes": "quo - ta"}
            ]
        }
    },
    "hiats": {
        "títol": "Els Hiats",
        "definicio": "Un hiat es produeix quan dues vocals seguides es pronuncien en síl·labes diferents (no formen diftong). Això passa amb dues vocals obertes o quan una vocal tancada porta accent de tresi (ï, ü).",
        "exemples": [
            {"paraula": "país", "silabes": "pa - ís"},
            {"paraula": "teatre", "silabes": "te - a - tre"},
            {"paraula": "Cairo", "silabes": "Cai - ro (Excepció/Hiat segons accentuació)"}, # Simplificat educativament
            {"paraula": "faen", "silabes": "fa - en"},
            {"paraula": "biologia", "silabes": "bi - o - lo - gi - a"},
            {"paraula": "dia", "silabes": "di - a"},
            {"paraula": "rio", "silabes": "ri - o"},
            {"paraula": "suar", "silabes": "su - ar"},
            {"paraula": "nucli", "silabes": "nu - cli"}, # Ajustat a exemple clar d'hiat o dièresi
            {"paraula": "veure", "silabes": "veu - re"}
        ]
    }
}

# Banc de paraules per a la secció d'Exercicis (tipus: 'creixent', 'decreixent', 'hiat')
BANCH_EXERCICIS = [
    {"paraula": "taula", "tipus": "decreixent", "silabes_correctes": "tau - la"},
    {"paraula": "veure", "tipus": "decreixent", "silabes_correctes": "veu - re"},
    {"paraula": "aigua", "tipus": "creixent", "silabes_correctes": "ai - gua"},
    {"paraula": "quota", "tipus": "creixent", "silabes_correctes": "quo - ta"},
    {"paraula": "país", "tipus": "hiat", "silabes_correctes": "pa - ís"},
    {"paraula": "teatre", "tipus": "hiat", "silabes_correctes": "te - a - tre"},
    {"paraula": "diari", "tipus": "creixent", "silabes_correctes": "dia - ri"}, # o depenent
    {"paraula": "rei", "tipus": "decreixent", "silabes_correctes": "rei"},
    {"paraula": "oasi", "tipus": "hiat", "silabes_correctes": "o - a - si"},
    {"paraula": "nou", "tipus": "decreixent", "silabes_correctes": "nou"}
]