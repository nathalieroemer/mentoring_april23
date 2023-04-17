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
    bonusest = models.FloatField(min=0, max=300)
    ident_worker = models.IntegerField()
    reciprocity = make_10pointlikert("When someone does me a favor, I am willing to return it.")
    intentions = make_10pointlikert("I assume that people have only the best intentions.")
    donation = models.FloatField()
    gender = models.IntegerField()
    stereotypes = make_7pointlikert("Do you think the worker's task (guessing the number of blue dots in a picture) rather favors male or female participants?")
    bel_1 = models.FloatField()
    bel_2 = models.FloatField()
    bel_3 = models.FloatField()
    bel_4 = models.FloatField()
    bel_5 = models.FloatField()
    bel_6 = models.FloatField()



# PAGES
class Part2(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1

class PerfElic(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1

    form_model = 'player'
    form_fields = [
        'bel_1',
        'bel_2',
        'bel_3',
        'bel_4',
        'bel_5',
        'bel_6',
    ]

class Part3(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1

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
        'gender',
        'stereotypes'
    ]


class End(Page):
    pass


page_sequence = [Part2, PerfElic, Part3, Quest, End]
