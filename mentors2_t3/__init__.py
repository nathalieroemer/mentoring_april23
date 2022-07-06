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
    terrible = models.IntegerField()
    verypoor = models.IntegerField()
    poor = models.IntegerField()
    good = models.IntegerField()
    verygood = models.IntegerField()
    exceptional = models.IntegerField()


# PAGES
class TaskT3(Page):
    @staticmethod
    def live_method(player: Player, data):
        if data['section'] == 'ter':
            player.terrible = int(data['value'])
        elif data['section'] == 'vp':
            player.verypoor = int(data['value'])
        elif data['section'] == 'poor':
            player.poor = int(data['value'])
        elif data['section'] == 'good':
            player.good = int(data['value'])
        elif data['section'] == 'vg':
            player.verygood = int(data['value'])
        elif data['section'] == 'exc':
            player.exceptional = int(data['value'])


page_sequence = [TaskT3]
