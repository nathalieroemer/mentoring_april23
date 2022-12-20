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
    wtgive = make_10pointlikert(
        "How willing are you to give to good causes without expecting anything in return?")  # willingness to give
    native = models.IntegerField()
    eng_prof = make_7pointlikert("How would you describe your language proficiency in English?", True)
    gender = models.IntegerField()
    clarity_bin = models.IntegerField(
        label="Where the instructions clear to you or did you had difficulties to understanding them?",
        blank=True
    )

    clarity = models.LongStringField(
        label="Please shorty explain, where did you had difficulties to understand the instructions?",
        blank=True
    )

    tech_bin = models.IntegerField(
        label="Do you think, everything was displayed to you correctly during this study?",
        blank=True
    )
    tech = models.LongStringField(
        label="Could you shortly describe your problem?",
        blank=True
    )
    stereotypes = make_7pointlikert("Do you think the worker's task (guessing the number of blue dots in a picture) rather favors male or female participants?")


# PAGES
class Part2(Page):
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
        'wtgive',
        'native',
        'eng_prof',
        'gender',
        'clarity',
        'clarity_bin',
        'tech',
        'tech_bin',
        'stereotypes'
    ]


class End(Page):
    pass


page_sequence = [Part2, Quest, End]
