import pandas as pd
import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'investors2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    menteedata = pd.read_csv(
        "testdata_mentees.csv",
        delimiter=";",
        encoding="latin1"
    )
    mdf = pd.DataFrame(
        menteedata,
        columns=[
            "participant.code",
            "participant._current_page_name",
            "mentees2.1.player.guess",
            "mentees2.1.player.truevalue",
            "mentees2.1.player.evaluation2"
        ]
    )
    mdf = mdf[mdf["participant._current_page_name"] == "End"].reset_index(drop=True)
    # print(mdf)

    scenarios = list(dict.fromkeys(mdf["mentees2.1.player.evaluation2"]))
    # print(scenarios)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    inv_ter = models.FloatField()
    inv_vp = models.FloatField()
    inv_p = models.FloatField()
    inv_g = models.FloatField()
    inv_vg = models.FloatField()
    inv_exc = models.FloatField()

    scenario = models.StringField()
    worker = models.StringField()


# PAGES
class Task(Page):
    form_model = 'player'
    form_fields = [
        'inv_ter',
        'inv_vp',
        'inv_p',
        'inv_g',
        'inv_vg',
        'inv_exc',
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # random scenario drawn and random worker with respective self-evaluation assigned
        player.scenario = random.choice(C.scenarios)
        # print(player.scenario)
        # list of index values that refer to all workers with respective self-evaluation:
        potworkers = [i for i, x in enumerate(C.mdf["mentees2.1.player.evaluation2"]) if x == player.scenario]
        w = random.choice(potworkers)
        player.worker = C.mdf["participant.code"][w]

        rel_dev = abs((C.mdf["mentees2.1.player.guess"][w]-C.mdf["mentees2.1.player.truevalue"][w])/C.mdf["mentees2.1.player.truevalue"][w])

        if player.scenario == "terrible":
            player.payoff = cu(round((1 - (player.inv_ter/100)) + (player.inv_ter/100) * 3 * (1 - rel_dev), 2))
        elif player.scenario == "very poor":
            player.payoff = cu(round((1 - (player.inv_vp/100)) + (player.inv_vp/100) * 3 * (1 - rel_dev), 2))
        elif player.scenario == "poor":
            player.payoff = cu(round((1 - (player.inv_p/100)) + (player.inv_p/100) * 3 * (1 - rel_dev), 2))
        elif player.scenario == "good":
            player.payoff = cu(round((1 - (player.inv_g/100)) + (player.inv_g/100) * 3 * (1 - rel_dev), 2))
        elif player.scenario == "very good":
            player.payoff = cu(round((1 - (player.inv_vg/100)) + (player.inv_vg/100) * 3 * (1 - rel_dev), 2))
        elif player.scenario == "exceptional":
            player.payoff = cu(round((1 - (player.inv_exc/100)) + (player.inv_exc/100) * 3 * (1 - rel_dev), 2))


page_sequence = [Task]
