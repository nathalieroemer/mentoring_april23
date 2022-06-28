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
    top = models.IntegerField()
    uppermiddle = models.IntegerField()
    lowermiddle = models.IntegerField()
    bottom = models.IntegerField()


# PAGES
class Task(Page):
    form_model = 'player'
    form_fields = [
        'top',
        'uppermiddle',
        'lowermiddle',
        'bottom'
    ]

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[1]


page_sequence = [Task]
