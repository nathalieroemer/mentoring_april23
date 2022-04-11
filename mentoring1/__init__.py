from otree.api import *
import itertools


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentoring1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()


# Methods
def creating_session(subsession: Subsession):
    treats = itertools.cycle(['one', 'two'])
    for p in subsession.get_players():
        p.treat = next(treats)
        p.participant.treat = p.treat


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = []
