from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'investors2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    inv_ter = models.FloatField()
    inv_vp = models.FloatField()
    inv_p = models.FloatField()
    inv_g = models.FloatField()
    inv_vg = models.FloatField()
    inv_exc = models.FloatField()


# PAGES
class Task(Page):
    form_model = 'player'
    form_fields = [
        'inv_ter',
        'inv_vp',
        'inv_p',
        'inv_g',
        'inv_vg',
        'inv_exc',
    ]


page_sequence = [Task]
