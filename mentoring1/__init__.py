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
    position = models.StringField()


# Methods
def creating_session(subsession: Subsession):
    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    p_per_treat = 90
    m_per_treat = 10
    i = 0
    for p in subsession.get_players():
        if i / 4 < p_per_treat:
            p.treat = next(treats)
        elif i / 4 >= p_per_treat:
            p.treat = 't1'
        p.participant.treat = p.treat
        i = i + 1


# PAGES
class Welcome(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class WorkerTask(Page):
    pass


class MentorTask(Page):
    pass


class Promotion(Page):
    pass


class PromotionII(Page):
    pass


class Questionnaire(Page):
    pass


class Endpage(Page):
    pass


page_sequence = [Welcome, ResultsWaitPage, WorkerTask, MentorTask, Promotion, PromotionII, Questionnaire, Endpage]
