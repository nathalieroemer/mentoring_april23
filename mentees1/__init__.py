import itertools

from otree.api import *


doc = """
Your app description
"""

# TODO: Attention check
# TODO: Show advice by mentors


class C(BaseConstants):
    NAME_IN_URL = 'mentees1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    workerid = models.StringField()

    test1 = models.IntegerField()


# Methods
def creating_session(subsession: Subsession):
    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    # mentors per treatment 2, 3 and 4:
    m_per_treat = 10

    i = 0
    for p in subsession.get_players():
        #p.part_id = p.participant.id_in_session
        if i / 4 < m_per_treat:
            p.treat = next(treats)
        elif i / 4 >= m_per_treat:
            p.treat = 't1'
        p.participant.treat = p.treat
        i = i + 1


# PAGES
class Welcome(Page):
    pass


class Instructions(Page):
    pass


class Attention1(Page):
    pass


class Attention2(Page):
    pass


page_sequence = [Welcome, Instructions, Attention1, Attention2]
