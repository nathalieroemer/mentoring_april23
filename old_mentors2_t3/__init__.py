import random

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'old_mentors2_t3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 24

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
    """
    top_terrible = models.StringField()
    um_terrible = models.StringField()
    lm_terrible = models.StringField()
    b_terrible = models.StringField()

    top_verypoor = models.StringField()
    um_verypoor = models.StringField()
    lm_verypoor = models.StringField()
    b_verypoor = models.StringField()

    top_poor = models.StringField()
    um_poor = models.StringField()
    lm_poor = models.StringField()
    b_poor = models.StringField()

    top_good = models.StringField()
    um_good = models.StringField()
    lm_good = models.StringField()
    b_good = models.StringField()

    top_verygood = models.StringField()
    um_verygood = models.StringField()
    lm_verygood = models.StringField()
    b_verygood = models.StringField()

    top_exceptional = models.StringField()
    um_exceptional = models.StringField()
    lm_exceptional = models.StringField()
    b_exceptional = models.StringField()
    """

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


class TaskT3(Page):  # Not used at the moment
    @staticmethod
    def live_method(player: Player, data):
        # idea with a dict, can be ignored:
        # player.participant.t3_answers["{}".format(data["section"])] = str(data["value"])
        if data['section'] == 't_ter':
            player.top_terrible = str(data['value'])
        elif data['section'] == 't_vp':
            player.top_verypoor = str(data['value'])
        elif data['section'] == 't_poor':
            player.top_poor = str(data['value'])
        elif data['section'] == 't_good':
            player.top_good = str(data['value'])
        elif data['section'] == 't_vg':
            player.top_verygood = str(data['value'])
        elif data['section'] == 't_exc':
            player.top_exceptional = str(data['value'])

        elif data['section'] == 'um_ter':
            player.um_terrible = str(data['value'])
        elif data['section'] == 'um_vp':
            player.um_verypoor = str(data['value'])
        elif data['section'] == 'um_poor':
            player.um_poor = str(data['value'])
        elif data['section'] == 'um_good':
            player.um_good = str(data['value'])
        elif data['section'] == 'um_vg':
            player.um_verygood = str(data['value'])
        elif data['section'] == 'um_exc':
            player.um_exceptional = str(data['value'])

        elif data['section'] == 'lm_ter':
            player.lm_terrible = str(data['value'])
        elif data['section'] == 'lm_vp':
            player.lm_verypoor = str(data['value'])
        elif data['section'] == 'lm_poor':
            player.lm_poor = str(data['value'])
        elif data['section'] == 'lm_good':
            player.lm_good = str(data['value'])
        elif data['section'] == 'lm_vg':
            player.lm_verygood = str(data['value'])
        elif data['section'] == 'lm_exc':
            player.lm_exceptional = str(data['value'])

        elif data['section'] == 'b_ter':
            player.b_terrible = str(data['value'])
        elif data['section'] == 'b_vp':
            player.b_verypoor = str(data['value'])
        elif data['section'] == 'b_poor':
            player.b_poor = str(data['value'])
        elif data['section'] == 'b_good':
            player.b_good = str(data['value'])
        elif data['section'] == 'b_vg':
            player.b_verygood = str(data['value'])
        elif data['section'] == 'b_exc':
            player.b_exceptional = str(data['value'])
        # print(player.participant.t3_answers)


class T3Task1(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = [
        'top_terrible',
        'um_terrible',
        'lm_terrible',
        'b_terrible'
    ]


class T3Task2(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = [
        'top_verypoor',
        'um_verypoor',
        'lm_verypoor',
        'b_verypoor'
    ]


class T3Task3(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = [
        'top_poor',
        'um_poor',
        'lm_poor',
        'b_poor'
    ]


class T3Task4(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = [
        'top_good',
        'um_good',
        'lm_good',
        'b_good'
    ]


class T3Task5(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = [
        'top_verygood',
        'um_verygood',
        'lm_verygood',
        'b_verygood'
    ]


class T3Task6(Page):  # Not used at the moment
    form_model = 'player'
    form_fields = [
        'top_exceptional',
        'um_exceptional',
        'lm_exceptional',
        'b_exceptional'
    ]


page_sequence = [T3Task]
