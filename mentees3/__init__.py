import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentees3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_GRAPHICS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    graphic = models.StringField()

    timeout = models.BooleanField(initial=False)
    guess = models.IntegerField()
    lowest = models.IntegerField()
    highest = models.IntegerField()
    evaluation = models.StringField()


# Methods
def creating_session(subsession: Subsession):
    # graphic assignment
    for p in subsession.get_players():
        p.graphic = 'graphic{}.png'.format(random.randint(1, C.NUM_GRAPHICS))
        p.treat = p.participant.treat


# PAGES
class Task2(Page):
    form_model = 'player'
    form_fields = [
        'guess'
    ]
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        print(player.participant.bm_dev)
        return dict(
            graphic=player.graphic
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        if timeout_happened:
            player.timeout = True
            par.timeout2 = True
        else:
            par.timeout2 = False

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.timeout:
            return upcoming_apps[0]
        else:
            pass


class Estimate2(Page):
    form_model = 'player'
    form_fields = [
        'lowest',
        'highest'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            graphic=player.graphic,
            guess=player.guess
        )


class Evaluation2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treat == 't1'

    @staticmethod
    def live_method(player: Player, data):
        player.evaluation = str(data)


page_sequence = [Task2, Estimate2, Evaluation2]
