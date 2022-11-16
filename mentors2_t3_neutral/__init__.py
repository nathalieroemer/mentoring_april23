import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentors2_t3_neutral'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    SCENARIOS = [
        "1-Terrible_best",
        "1-Terrible_second-best",
        "1-Terrible_third-best",
        "1-Terrible_fourth-best",
        "2-Very poor_best",
        "2-Very poor_second-best",
        "2-Very poor_third-best",
        "2-Very poor_fourth-best",
        "3-Poor_best",
        "3-Poor_second-best",
        "3-Poor_third-best",
        "3-Poor_fourth-best",
        "4-Good_best",
        "4-Good_second-best",
        "4-Good_third-best",
        "4-Good_fourth-best",
        "5-Very good_best",
        "5-Very good_second-best",
        "5-Very good_third-best",
        "5-Very good_fourth-best",
        "6-Exceptional_best",
        "6-Exceptional_second-best",
        "6-Exceptional_third-best",
        "6-Exceptional_fourth-best"
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    performance = models.StringField()
    previous = models.StringField()
    advice = models.StringField()


# METHODS
def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.participant.scenarios = C.SCENARIOS.copy()


# PAGES
class T3Task(Page):
    @staticmethod
    def vars_for_template(player: Player):
        par = player.participant

        scenario = random.choice(par.scenarios)

        player.previous = scenario.split("_")[0]
        player.performance = scenario.split("_")[1]

        return dict(
            prevansw=player.previous,
            perf=player.performance
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant

        scenario = player.previous + "_" + player.performance
        par.scenarios.remove(scenario)

    @staticmethod
    def live_method(player: Player, data):
        player.advice = str(data)


page_sequence = [T3Task]
