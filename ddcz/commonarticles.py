"""
Module for helping with and handling common articles.
"""

# Normative directory of Creative Pages allowed on the page
# Key is the common "short" identification of creative page,
# as present in database (as string) and data model
COMMON_ARTICLES_CREATIVE_PAGES = {
    'clanky': {
        'name': 'Články&Eseje',
        'sections': [
            'Doplňky k pravidlům',
            'Historie postavy',
            'Hlod :-)',
            'Ostatní',
            'Poezie',
            'Popis dobrodružství',
            'Povídky',
            'Publicistika',
            'Recenze',
            'Úvahy',
        ]
    },
    'novapovolani': {
        'name': 'Nová Povolání',
        'sections': [
            'Kompletní povolání',
            'Nový obor pro experty',
            'Nový obor pro pokročilé',
            'Obor',
            'Ostatní',
            'Specializace',
            'Specializace pro experty',
            'Specializace pro pokročilé',
            'Začátečnické povolání',
        ]
    },
    'noverasy': {
        'name': 'Nové Rasy',
        'sections': [
            'Kříženec',
            'Nová rasa',
            'Odrůda',
            'Ostatní,'
        ]
    },
    # Not a common article, in fact
    # 'predmety': {
    #     'name': 'Předměty',
    #     'sections': [
    #         'Zbraně',
    #         'Zbroj',
    #         'Artefakty',
    #         'Kouzelné zbraně',
    #         'Kouzelná zbroj',
    #         'Kouzelné předměty',
    #         'Obyčejné předměty',
    #     ]
    # },
    'expanze': {
        'name': 'Rozvoj DrD',
        'sections': [
            'Alternativní pravidla',
            'Armády a vojenství',
            'Ekonomika a obchod',
            'Nadpřirozeno',
            'Ostatní',
            'Politika a diplomacie',
            'Světy a prostředí',
            'Teorie RPG',
        ]
    },
    'alchymistazvl': {
        'name': 'Alchymista',
        'sections': [
            'Alchymista',
            'Ostatní',
            'Pyrofor',
            'Theurg',
        ]
    },
    'hranicar': {
        'name': 'Hraničář',
        'sections': [
            'Chodec',
            'Druid',
            'Hraničář',
            'Ostatní',
        ]
    },
    'kouzelnikzvl': {
        'name': 'Kouzelník',
        'sections': [
            'Čaroděj',
            'Kouzelník',
            'Mág',
            'Ostatní',
            'Přítel',

        ]
    },
    'valecnik': {
        'name': 'Válečník',
        'sections': [
            'Alternativní pravidla',
            'Bojovník',
            'Ostatní',
            'Válečník',
            'Šermíř',
        ]
    },
    'zlodej': {
        'name': 'Zloděj',
        'sections': [
            'Lupič',
            'Ostatní',
            'Sicco',
            'Zloděj',
            'Zlodějský předmět',
        ]
    },
}


SLUG_NAME_TRANSLATION_FROM_CZ = {
    'clanky': 'articles-and-essays',
    'novapovolani': 'new-classes',
    'noverasy': 'new-races',
    # 'predmety': 'items',
    'expanze': 'extending-rules',
    'alchymistazvl': 'alchemist',
    'hranicar': 'ranger',
    'kouzelnikzvl': 'wizard',
    'valecnik': 'warrior',
    'zlodej': 'rogue',

}

SLUG_NAME_TRANSLATION_TO_CZ = {v:k for k,v in SLUG_NAME_TRANSLATION_FROM_CZ.items()}

