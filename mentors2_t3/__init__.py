from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentors2_t3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    terrible = models.IntegerField()
    verypoor = models.IntegerField()
    neutral = models.IntegerField()
    good = models.IntegerField()
    verygood = models.IntegerField()
    exceptional = models.IntegerField()


# PAGES
class TaskT3(Page):
    form_model = 'player'
    form_fields = [
        'terrible',
        'verypoor',
        'neutral',
        'good',
        'verygood',
        'exceptional'
    ]


page_sequence = [TaskT3]
