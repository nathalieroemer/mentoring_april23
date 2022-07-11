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
    terrible = models.StringField()
    verypoor = models.StringField()
    poor = models.StringField()
    good = models.StringField()
    verygood = models.StringField()
    exceptional = models.StringField()


# PAGES
class TaskT3(Page):
    @staticmethod
    def live_method(player: Player, data):
        if data['section'] == 'ter':
            player.terrible = str(data['value'])
        elif data['section'] == 'vp':
            player.verypoor = str(data['value'])
        elif data['section'] == 'poor':
            player.poor = str(data['value'])
        elif data['section'] == 'good':
            player.good = str(data['value'])
        elif data['section'] == 'vg':
            player.verygood = str(data['value'])
        elif data['section'] == 'exc':
            player.exceptional = str(data['value'])


page_sequence = [TaskT3]
