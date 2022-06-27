from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentoring_end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.IntegerField()
    native = models.IntegerField()
    eng_prof = models.IntegerField()


# PAGES
class Questionnaire(Page):
    form_model = 'player'
    form_fields = [
        'gender',
        'native',
        'eng_prof'
    ]


class Endpage(Page):
    pass


page_sequence = [Questionnaire, Endpage]
