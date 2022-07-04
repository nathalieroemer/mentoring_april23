from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentors3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # gender = models.IntegerField()
    native = models.IntegerField()
    eng_prof = models.IntegerField(
        blank=True
    )
    diffdots = models.IntegerField()
    deviation = models.IntegerField()
    diffadvice = models.IntegerField()
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
        'diffdots',
        'deviation',
        'diffadvice',
        'bonusest',
        'riskpref',
        'comp'
    ]


class End(Page):
    pass


page_sequence = [Quest, End]
