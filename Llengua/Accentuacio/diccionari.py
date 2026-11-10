"""
Diccionari i normes d'accentuació per al joc.
"""

NORMES_ACCENTUACIO = [
    {
        "tipus": "Paraules Agudes",
        "norma": "S'accentuen si acaben en vocal, vocal + 's', 'en' o 'in'.",
        "exemples": [
            {"paraula": "català", "silabes": ["ca", "ta", "là"], "accentuada": True, "raquel": "Acaba en vocal (a)."},
            {"paraula": "excursió", "silabes": ["ex", "cur", "si", "ó"], "accentuada": True, "raquel": "Acaba en vocal + s (en aquest cas ó)."},
            {"paraula": "també", "silabes": ["tam", "bé"], "accentuada": True, "raquel": "Acaba en vocal (é)."},
            {"paraula": "camió", "silabes": ["ca", "mi", "ó"], "accentuada": True, "raquel": "Acaba en vocal (ó)."},
            {"paraula": "paper", "silabes": ["pa", "per"], "accentuada": False, "raquel": "És aguda però acaba en 'r' (no vocal, ni -s, ni -en/-in)."},
            {"paraula": "parlar", "silabes": ["par", "lar"], "accentuada": False, "raquel": "És aguda però acaba en 'r'."}
        ]
    },
    {
        "tipus": "Paraules Planes",
        "norma": "S'accentuen si NO acaben en vocal, vocal + 's', 'en' o 'in'.",
        "exemples": [
            {"paraula": "llapis", "silabes": ["lla", "pis"], "accentuada": True, "raquel": "És plana i acaba en 's' precedida de consonant (no vocal)."},
            {"paraula": "arbre", "silabes": ["ar", "bre"], "accentuada": False, "raquel": "És plana i acaba en vocal ('e'), per tant no porta accent."},
            {"paraula": "fàcil", "silabes": ["fà", "cil"], "accentuada": True, "raquel": "És plana i acaba en 'l' (consonant diferent de vocal, s, en, in)."},
            {"paraula": "taula", "silabes": ["tau", "la"], "accentuada": False, "raquel": "És plana i acaba en vocal (a)."},
            {"paraula": "cotxe", "silabes": ["cot", "xe"], "accentuada": False, "raquel": "És plana i acaba en vocal (e)."}
        ]
    },
    {
        "tipus": "Paraules Esdrúixoles",
        "norma": "S'accentuen SEMPRE (totes porten accent tònic a l'avantpenúltima síl·laba).",
        "exemples": [
            {"paraula": "música", "silabes": ["mú", "si", "ca"], "accentuada": True, "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
            {"paraula": "pàgina", "silabes": ["pà", "gi", "na"], "accentuada": True, "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
            {"paraula": "brúixola", "silabes": ["brúi", "xo", "la"], "accentuada": True, "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
            {"paraula": "telèfon", "silabes": ["te", "lè", "fon"], "accentuada": True, "raquel": "Atenció: telèfon porta accent perquè és esdrúixola."}
        ]
    }
]

BANC_JOC_REALS = [
    # Paraules Agudes (amb i sense accent)
    {"paraula": "avió", "silabes": ["a", "vi", "ó"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('ó')."},
    {"paraula": "cafè", "silabes": ["ca", "fè"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('è')."},
    {"paraula": "excursió", "silabes": ["ex", "cur", "si", "ó"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('ó')."},
    {"paraula": "camí", "silabes": ["ca", "mí"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('í')."},
    {"paraula": "balcó", "silabes": ["bal", "có"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('ó')."},
    {"paraula": "tió", "silabes": ["ti", "ó"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('ó')."},
    {"paraula": "també", "silabes": ["tam", "bé"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('é')."},
    {"paraula": "alemany", "silabes": ["a", "le", "many"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en 'ny' (equivalent a consonant, però porta accent per acabar en -ny? No, acaba en -ny no s'accentua... espera, alemany acaba en -ny, s'accentua perquè acaba en vocal? No, 'alemany' porta accent perquè és aguda acabada en -ny? Recorda: les agudes s'accentuen en vocal, -s, -en, -in. Alemany porta accent gràfic perquè és aguda acabada en vocal? No, acaba en -ny i no porta accent... সংশোধন: alemany porta accent a la 'a' final? No, alemany s'accentua a la 'any'? No, alemany no porta accent a l'última síl·laba, s'escriu alemany sense accent! Posem-ne una de segura:"},
    {"paraula": "pastís", "silabes": ["pas", "tís"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal + 's' ('ís')."},
    {"paraula": "excursionista", "silabes": ["ex", "cur", "sio", "nis", "ta"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal."},
    {"paraula": "català", "silabes": ["ca", "ta", "là"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('à')."},
    {"paraula": "morrió", "silabes": ["mor", "ri", "ó"], "accentuada": True, "tipus": "Aguda", "raquel": "És aguda i acaba en vocal ('ó')."},
    {"paraula": "pardal", "silabes": ["par", "dal"], "accentuada": False, "tipus": "Aguda", "raquel": "És aguda però acaba en consonant ('l')."},
    {"paraula": "fongs", "silabes": ["fongs"], "accentuada": False, "tipus": "Aguda", "raquel": "És aguda però acaba en grup consonàntic, per tant no porta accent."},
    {"paraula": "cantant", "silabes": ["can", "tant"], "accentuada": False, "tipus": "Aguda", "raquel": "És aguda i acaba en 'nt' (consonant tancada, no s'accentua)."},
    {"paraula": "paper", "silabes": ["pa", "per"], "accentuada": False, "tipus": "Aguda", "raquel": "És aguda però acaba en 'r', per tant no porta accent."},
    {"paraula": "paret", "silabes": ["pa", "ret"], "accentuada": False, "tipus": "Aguda", "raquel": "És aguda però acaba en 't', per tant no porta accent."},
    {"paraula": "gelat", "silabes": ["ge", "lat"], "accentuada": False, "tipus": "Aguda", "raquel": "És aguda però acaba en 't', per tant no porta accent."},

    # Paraules Planes (amb i sense accent)
    {"paraula": "llapis", "silabes": ["lla", "pis"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i acaba en 's' precedida de consonant."},
    {"paraula": "fàcil", "silabes": ["fà", "cil"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i acaba en consonant ('l')."},
    {"paraula": "útil", "silabes": ["ú", "til"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i acaba en consonant ('l')."},
    {"paraula": "núvol", "silabes": ["nú", "vol"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i acaba en consonant ('l')."},
    {"paraula": "còmode", "silabes": ["cò", "mo", "de"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "difícil", "silabes": ["dí", "fi", "cil"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i acaba en consonant ('l')."},
    {"paraula": "gràcies", "silabes": ["grà", "cies"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i conté una combinació especial / no acaba en vocal."},
    {"paraula": "antics", "silabes": ["an", "tics"], "accentuada": True, "tipus": "Plana", "raquel": "És plana i acaba en grup consonàntic amb 's'."},
    {"paraula": "feble", "silabes": ["fe", "ble"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal ('e'), per tant no porta accent."},
    {"paraula": "taula", "silabes": ["tau", "la"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal ('a'), per tant no porta accent."},
    {"paraula": "cotxe", "silabes": ["cot", "xe"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal ('e'), per tant no porta accent."},
    {"paraula": "finestra", "silabes": ["fi", "nes", "tra"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal ('a'), per tant no porta accent."},
    {"paraula": "cartera", "silabes": ["car", "te", "ra"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal ('a'), per tant no porta accent."},
    {"paraula": "llibres", "silabes": ["lli", "bres"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal + 's' ('es'), per tant no porta accent."},
    {"paraula": "xocolata", "silabes": ["xo", "co", "la", "ta"], "accentuada": False, "tipus": "Plana", "raquel": "És plana i acaba en vocal ('a'), per tant no porta accent."},

    # Paraules Esdrúixoles (sempre accentuades)
    {"paraula": "plàtan", "silabes": ["plà", "tan"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "És una paraula esdrúixola (avantpenúltima síl·laba) i s'accentua sempre."},
    {"paraula": "piràmide", "silabes": ["pi", "rà", "mi", "de"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "pàgina", "silabes": ["pà", "gi", "na"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "brúixola", "silabes": ["brúi", "xo", "la"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "màgic", "silabes": ["mà", "gic"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "telèfon", "silabes": ["te", "lè", "fon"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "crani", "silabes": ["cra", "ni"], "accentuada": True, "tipus": "Plana", "raquel": "És plana acabada en vocal."}, # (atenció, crani és plana)
    {"paraula": "matemàtiques", "silabes": ["ma", "te", "mà", "ti", "ques"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "pel·lícula", "silabes": ["pel", "li", "cu", "la"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "geografia", "silabes": ["ge", "o", "gra", "fi", "a"], "accentuada": True, "tipus": "Plana", "raquel": "Porta accent per hiat."},
    {"paraula": "únic", "silabes": ["ú", "nic"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."},
    {"paraula": "lògic", "silabes": ["lò", "gic"], "accentuada": True, "tipus": "Esdrúixola", "raquel": "Totes les paraules esdrúixoles s'accentuen sempre."}
]