from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentors2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    top = models.StringField()
    uppermiddle = models.StringField()
    lowermiddle = models.StringField()
    bottom = models.StringField()


# PAGES
class Task(Page):
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


page_sequence = [Task]
