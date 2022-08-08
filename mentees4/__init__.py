from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentees4'
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
    stereo = models.IntegerField()
    bonusest = models.FloatField()
    deviation = models.IntegerField()
    riskpref = models.IntegerField()
    comp = models.IntegerField()


# PAGES
class Quest(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1 and par.test2_passed == 1 and par.timeout2 == 0

    form_model = 'player'
    form_fields = [
        'native',
        'eng_prof',
        'diff',
        'deviation',
        'stereo',
        'bonusest',
        'riskpref',
        'comp'
    ]


class End(Page):
    pass


page_sequence = [Quest, End]
