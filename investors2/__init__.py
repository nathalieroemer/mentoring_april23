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
    mdf = mdf[mdf["participant._current_page_name"] == "End"]
    print(mdf)

    scenarios = list(dict.fromkeys(mdf["mentees2.1.player.evaluation2"]))
    print(scenarios)


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
    worker = models.StringField()  # TODO: participant id of worker


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
        par = player.participant

        # random scenario drawn and random worker with respective self-evaluation assigned
        player.scenario = random.choice(C.scenarios)
        potworkers = [i for i, x in enumerate(C.mdf["mentees2.1.player.evaluation2"]) if x == player.scenario]
        w = random.choice(potworkers)
        player.worker = C.mdf["participant.code"][w]

        # TODO: rel deviation is not correctly calculated! wait for Nathalies response
        rel_dev = abs((C.mdf["mentees2.1.player.truevalue"][w]-C.mdf["mentees2.1.player.guess"][w])/C.mdf["mentees2.1.player.truevalue"][w])
        print(rel_dev)

        if player.scenario == "terrible":
            par.payoff = (1 - player.inv_ter) + player.inv_ter * 3 * (1 - rel_dev)
        elif player.scenario == "very poor":
            par.payoff = (1 - player.inv_ter) + player.inv_vp * 3 * (1 - rel_dev)
        elif player.scenario == "poor":
            par.payoff = (1 - player.inv_ter) + player.inv_p * 3 * (1 - rel_dev)
        elif player.scenario == "good":
            par.payoff = (1 - player.inv_ter) + player.inv_g * 3 * (1 - rel_dev)
        elif player.scenario == "very good":
            par.payoff = (1 - player.inv_ter) + player.inv_vg * 3 * (1 - rel_dev)
        elif player.scenario == "exceptional":
            par.payoff = (1 - player.inv_ter) + player.inv_exc * 3 * (1 - rel_dev)
        print(par.payoff)


page_sequence = [Task]
