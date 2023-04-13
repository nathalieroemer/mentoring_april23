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
    # print(mdf)

    scenarios = list(dict.fromkeys(mdf["evaluation"]))
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
        potworkers = [i for i, x in enumerate(C.mdf["evaluation"]) if x == player.scenario]
        w = random.choice(potworkers)
        player.worker = C.mdf["participantcode"][w]

        ## with index [w] we use the corresponding performance of the randomly chosen worker w above
        rel_dev = (abs((C.mdf["guess"][w]-C.mdf["dots"][w]))/C.mdf["dots"][w])*100
        print(rel_dev, "this is the deviation for worker", w)
        if rel_dev <=100:
            acc = 100 - rel_dev
        if rel_dev > 100:
            acc = 0
        print(C.mdf["guess"][w], "this is the guess for true number", C.mdf["dots"][w])
        print(acc, "this is the prec")
        print(player.inv_g, player.inv_p, player.inv_vg, player.inv_vp, player.inv_exc, player.inv_exc)

        ## player.inv_ter is the investment the investor made
        ## we need to divide by 100 because it is in pence right now
        ## Did not simplify the calculation to make it clear why we do which computation
        if player.scenario == "terrible":
            player.payoff = cu(round(((3*((100 - player.inv_ter) - 0.005*((100-player.inv_ter)**2) + player.inv_ter * acc* 0.01))/100), 2))
        elif player.scenario == "very poor":
            player.payoff =  cu(round(((3*((100 - player.inv_vp) - 0.005*((100-player.inv_vp)**2) + player.inv_vp * acc*0.01))/100), 2))
        elif player.scenario == "poor":
            player.payoff = cu(round((3*(((100 - player.inv_p) - 0.005*((100-player.inv_p)**2) + player.inv_p * acc*0.01))/100), 2))
        elif player.scenario == "good":
            player.payoff = cu(round((3*(((100 - player.inv_g) - 0.005*((100-player.inv_g)**2) + player.inv_g * acc*0.01))/100), 2))
        elif player.scenario == "very good":
            player.payoff = cu(round((3*(((100 - player.inv_vg) - 0.005*((100-player.inv_vg)**2) + player.inv_vg * acc*0.01))/100), 2))
        elif player.scenario == "exceptional":
            player.payoff = cu(round((3*(((100 - player.inv_exc) - 0.005*((100-player.inv_exc)**2) + player.inv_exc * acc*0.01))/100), 2))

        if player.payoff < 0:
            player.payoff = 0

        print("this is the payoff", player.payoff, "for scenario ", player.scenario)

page_sequence = [Task]