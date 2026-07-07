import random

EVENTS=[
 'Fusion reactor maintenance completed.',
 'Greenhouse harvest increased.',
 'Dust storm approaching.',
 'Water recycling efficiency improved.',
 'Citizen submitted a proposal.',
 'Research project started.'
]

def random_event()->str:
    return random.choice(EVENTS)
