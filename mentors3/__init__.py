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
    NAME_IN_URL = 'mp3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    diffadvice = make_7pointlikert("How difficult did you find it to provide advice?")
    ident_adv = models.IntegerField()
    ident_inv = models.IntegerField()
    # prob_fem = models.IntegerField()
    # prob_male = models.IntegerField()
    reciprocity = make_10pointlikert("When someone does me a favor, I am willing to return it.")
    intentions = make_10pointlikert("I assume that people have only the best intentions.")
    donation = models.FloatField()
    riskpref = make_7pointlikert("How do you see yourself: Are you someone who is willing to take risks or do you try to avoid them?")
    gender = models.IntegerField()
    stereotypes = make_7pointlikert("Do you think your advisee's task (guessing the number of blue dots in a picture) rather favors male or female participants?")


class Part2(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1


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
        'reciprocity',
        'intentions',
        'donation',
        'riskpref',
        'gender',
        'stereotypes'
    ]


class End(Page):
    pass


page_sequence = [Part2, Quest, End]
