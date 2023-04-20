from otree.api import *
import random
import pandas as pd

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

    menteedata = pd.read_csv(
        "mentees_data.csv",
        delimiter=",",
        encoding="latin1"
    )
    mdf = pd.DataFrame(
        menteedata,
        columns=[
            "participantcode",
            "guess",
            "dots",
            "evaluation"
        ]
    )
    mdf = mdf.dropna().reset_index(drop=True)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    riskpref = make_7pointlikert("How do you see yourself: Are you someone who is willing to take risks or do you try to avoid them?")
    diff = make_7pointlikert("How difficult did you find the investment task?")
    bonusest_1 = models.FloatField(min=0, max=3)
    bonusest_2 = models.FloatField(min=0, max=1)
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
    worker_bonus = models.StringField()

def calc_bonus(predicted_acc, acc):
    dev = abs(predicted_acc - acc)
    print("this is the predicted acc", predicted_acc, "this is the accuracy", acc)
    if dev <= 10 :
        bonus = 1
    if 10 < dev <= 20:
        bonus = 0.75
    if 20 < dev <= 30:
        bonus = 0.25
    if dev > 30:
        bonus = 0

    return cu(bonus)


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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # generate list of indices of all workers, but the one who was chosen before
        potworkers = [i for i, x in enumerate(C.mdf["participantcode"]) if x != player.participant.invest_worker]
        w = random.choice(potworkers)
        player.worker_bonus = C.mdf["participantcode"][w]

        ## with index [w] we use the corresponding performance of the randomly chosen worker w above
        rel_dev = (abs((C.mdf["guess"][w]-C.mdf["dots"][w]))/C.mdf["dots"][w])*100
        evaluation = C.mdf["evaluation"][w]

        if rel_dev >=100:
            acc = 0
        if rel_dev <100:
            acc = 100 - rel_dev

        if evaluation == "terrible":
            player.payoff = calc_bonus(player.bel_1, acc)
        elif evaluation == "very poor":
            player.payoff = calc_bonus(player.bel_1, acc)
        elif evaluation == "poor":
            player.payoff = calc_bonus(player.bel_1, acc)
        elif evaluation == "good":
            player.payoff = calc_bonus(player.bel_4, acc)
        elif evaluation == "very good":
            player.payoff = calc_bonus(player.bel_5, acc)
        elif evaluation== "exceptional":
            player.payoff = calc_bonus(player.bel_6, acc)

        if player.payoff < 0:
            player.payoff = 0

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
        'bonusest_1',
        'bonusest_2',
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
