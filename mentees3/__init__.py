import random
from os import listdir
from os.path import isfile, join

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentees3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Lists all possible graphics:
    GRAPHICS = [f for f in listdir("_static/graphics") if isfile(join("_static/graphics", f))]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    graphic = models.StringField()
    numdots = models.IntegerField()

    timeout = models.BooleanField(initial=False)
    guess = models.IntegerField()
    lowest = models.IntegerField()
    highest = models.IntegerField()
    evaluation = models.StringField()
    own_perf = models.IntegerField()
    beliefrank = models.IntegerField(
        choices=[
            [1, 'First-best'],
            [2, 'Second-best'],
            [3, 'Third-best'],
            [4, 'Fourth-best'],
        ], blank=True
    )

def beliefrank_error_message(player, value):
    print(value, "this is the value")
    if value is None:
        return 'Please answer the question'



# Methods
def creating_session(subsession: Subsession):
    # graphic assignment
    for p in subsession.get_players():
        # p.participant.graphic still has graphic from first task saved, can be used to reduce possible graphics to
        # remaining three
        gr_left = [x for x in C.GRAPHICS if x != p.participant.graphic]
        p.graphic = random.choice(gr_left)
        # save number of dots of graphic:
        p.numdots = int(p.graphic[8:-4])

        p.treat = p.participant.treat


# PAGES

class Part2(Page):
    pass

class Instructions(Page):
    pass

class Task2(Page):
    form_model = 'player'
    form_fields = [
        'guess'
    ]
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        # print(player.participant.bm_dev)
        return dict(
            graphic="graphics/"+player.graphic
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

class Evaluation2(Page):
    @staticmethod
    def live_method(player: Player, data):
        player.evaluation = str(data)


class OwnPerf(Page):
    form_model = 'player'
    form_fields = [
        'beliefrank',
        'own_perf'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            graphic="graphics/"+player.graphic,
            guess=player.guess
        )

    @staticmethod
    def js_vars(player):
        return dict(
            player_guess=player.guess,
        )



page_sequence = [Part2, Instructions, Task2, Evaluation2, OwnPerf]
