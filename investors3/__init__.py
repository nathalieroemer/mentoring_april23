from otree.api import *


doc = """
Your app description
"""


# METHODS
def make_7pointlikert(label, blank=False):
    if not blank:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7],
            label=label,
            widget=widgets.RadioSelect
        )
    else:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7],
            label=label,
            widget=widgets.RadioSelect,
            blank=True
        )


def make_10pointlikert(label, blank=False):
    if not blank:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            label=label,
            widget=widgets.RadioSelect
        )
    else:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            label=label,
            widget=widgets.RadioSelect,
            blank=True
        )


# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'investors3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    riskpref = make_7pointlikert("How do you see yourself: Are you someone who is willing to take risks or do you try to avoid them?")
    diff = make_7pointlikert("How difficult did you find the investment task?")
    bonusest = models.FloatField()
    ident_worker = models.IntegerField()
    reciprocity = make_10pointlikert("When someone does me a favor, I am willing to return it.")
    intentions = make_10pointlikert("I assume that people have only the best intentions.")
    donation = models.FloatField()
    wtgive = make_10pointlikert(
        "How willing are you to give to good causes without expecting anything in return?")  # willingness to give
    native = models.IntegerField()
    eng_prof = make_7pointlikert("How would you describe your language proficiency in English?", True)
    gender = models.IntegerField()


# PAGES
class Quest(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1

    form_model = 'player'
    form_fields = [
        'riskpref',
        'diff',
        'bonusest',
        'ident_worker',
        'reciprocity',
        'intentions',
        'donation',
        'wtgive',
        'native',
        'eng_prof',
        'gender'
    ]


class End(Page):
    pass


page_sequence = [Quest, End]
