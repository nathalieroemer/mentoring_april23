from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentors2_t3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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


# PAGES
class TaskT3(Page):
    @staticmethod
    def live_method(player: Player, data):
        # idea with the dict, can be ignored:
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


class T3Task1(Page):
    form_model = 'player'
    form_fields = [
        'top_terrible',
        'um_terrible',
        'lm_terrible',
        'b_terrible'
    ]


class T3Task2(Page):
    form_model = 'player'
    form_fields = [
        'top_verypoor',
        'um_verypoor',
        'lm_verypoor',
        'b_verypoor'
    ]


class T3Task3(Page):
    form_model = 'player'
    form_fields = [
        'top_poor',
        'um_poor',
        'lm_poor',
        'b_poor'
    ]


class T3Task4(Page):
    form_model = 'player'
    form_fields = [
        'top_good',
        'um_good',
        'lm_good',
        'b_good'
    ]


class T3Task5(Page):
    form_model = 'player'
    form_fields = [
        'top_verygood',
        'um_verygood',
        'lm_verygood',
        'b_verygood'
    ]


class T3Task6(Page):
    form_model = 'player'
    form_fields = [
        'top_exceptional',
        'um_exceptional',
        'lm_exceptional',
        'b_exceptional'
    ]


page_sequence = [T3Task1, T3Task2, T3Task3, T3Task4, T3Task5, T3Task6]
