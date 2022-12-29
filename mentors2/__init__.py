import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'm_p2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4

    PERFORMANCES = ["best", "second-best", "third-best", "fourth-best"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    """
    top = models.StringField()
    uppermiddle = models.StringField()
    lowermiddle = models.StringField()
    bottom = models.StringField()
    """
    performance = models.StringField()
    advice = models.StringField()


# METHODS
def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        p.participant.performances = C.PERFORMANCES.copy()


# PAGES
class TaskOld(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = []

    @staticmethod
    def live_method(player: Player, data):
        if data['section'] == 'top':
            player.top = str(data['value'])
        elif data['section'] == 'um':
            player.uppermiddle = str(data['value'])
        elif data['section'] == 'lm':
            player.lowermiddle = str(data['value'])
        elif data['section'] == 'bottom':
            player.bottom = str(data['value'])

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[1]


class Task(Page):


    @staticmethod
    def vars_for_template(player: Player):
        par = player.participant
        player.performance = random.choice(par.performances)

        return dict(
            perf=player.performance
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.performances.remove(player.performance)
        # print(player.participant.performances)

    @staticmethod
    def live_method(player: Player, data):
        player.advice = str(data)

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.round_number == C.NUM_ROUNDS:
            return upcoming_apps[1]


page_sequence = [Task]
