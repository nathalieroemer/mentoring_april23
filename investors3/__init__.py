from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'investors3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    native = models.IntegerField()
    eng_prof = models.IntegerField(
        blank=True
    )
    diff = models.IntegerField()
    bonusest = models.FloatField()
    riskpref = models.IntegerField()
    comp = models.IntegerField()


# PAGES
class Quest(Page):
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1

    form_model = 'player'
    form_fields = [
        'native',
        'eng_prof',
        'diff',
        'bonusest',
        'riskpref',
        'comp'
    ]


class End(Page):
    pass


page_sequence = [Quest, End]
