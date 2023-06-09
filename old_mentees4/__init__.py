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
    NAME_IN_URL = 'mentees4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    diff = make_7pointlikert("How difficult did you find it to guess the number of dots in the pictures?")
    stereotypes = make_7pointlikert("Do you think this task rather favors male or female participants?")
    bonusest = models.FloatField()
    own_perf = models.StringField()
    others_perf = models.StringField()
    ident_adv = models.IntegerField()
    ident_inv = models.IntegerField()
    reciprocity = make_10pointlikert("When someone does me a favor, I am willing to return it.")
    intentions = make_10pointlikert("I assume that people have only the best intentions.")
    donation = models.FloatField()
    wtgive = make_10pointlikert(
        "How willing are you to give to good causes without expecting anything in return?")  # willingness to give
    riskpref = make_7pointlikert(
        "How do you see yourself: Are you someone who is willing to take risks or do you try to avoid them?")
    native = models.IntegerField()
    eng_prof = make_7pointlikert("How would you describe your language proficiency in English?", True)
    gender = models.IntegerField()


# PAGES
class Quest(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1 and par.timeout2 == 0 and par.timeout == 0

    form_model = 'player'
    form_fields = [
        'diff',
        'stereotypes',
        'bonusest',
        'ident_adv',
        'ident_inv',
        'reciprocity',
        'intentions',
        'donation',
        'wtgive',
        'riskpref',
        'native',
        'eng_prof',
        'gender'
    ]

    @staticmethod
    def live_method(player: Player, data):
        if data['section'] == 'own_p':
            player.own_perf = str(data['value'])
        elif data['section'] == 'others_p':
            player.others_perf = str(data['value'])


class End(Page):
    pass


page_sequence = [Quest, End]
