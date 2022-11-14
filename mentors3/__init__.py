from otree.api import *


doc = """
Your app description
"""


# METHODS
def make_7pointikert(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label=label,
        widget=widgets.RadioSelect
    )


def make_10pointikert(label):
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label=label,
        widget=widgets.RadioSelect
    )


# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'mentors3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    diffadvice = make_7pointikert("How difficult did you find it to provide advice?")
    ident_adv = models.IntegerField()
    ident_inv = models.IntegerField()
    prob_fem = models.IntegerField()
    prob_male = models.IntegerField()
    wtgive = make_10pointikert("How willing are you to give to good causes without expecting anything in return?")  # willingness to give
    riskpref = make_7pointikert("How do you see yourself: Are you someone who is willing to take risks or do you try to avoid them?")
    native = models.IntegerField()
    eng_prof = models.IntegerField(
        blank=True
    )
    gender = models.IntegerField()


# PAGES
class Quest(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1

    form_model = 'player'
    form_fields = [
        'diffadvice',
        'ident_adv',
        'ident_inv',
        'prob_fem',
        'prob_male',
        'wtgive',
        'riskpref',
        'native',
        'eng_prof',
        'gender'
    ]


class End(Page):
    pass


page_sequence = [Quest, End]
