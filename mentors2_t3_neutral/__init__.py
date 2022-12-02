import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentors2_t3_neutral'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 24  # six possible answers with four cases for advisee rank

    SCENARIOS = [
        "Terrible_best",
        "Terrible_second-best",
        "Terrible_third-best",
        "Terrible_fourth-best",
        "Very poor_best",
        "Very poor_second-best",
        "Very poor_third-best",
        "Very poor_fourth-best",
        "Poor_best",
        "Poor_second-best",
        "Poor_third-best",
        "Poor_fourth-best",
        "Good_best",
        "Good_second-best",
        "Good_third-best",
        "Good_fourth-best",
        "Very good_best",
        "Very good_second-best",
        "Very good_third-best",
        "Very good_fourth-best",
        "Exceptional_best",
        "Exceptional_second-best",
        "Exceptional_third-best",
        "Exceptional_fourth-best"
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
