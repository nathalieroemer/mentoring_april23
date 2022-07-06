from otree.api import *
import itertools
import random


doc = """
Your app description
"""

# TODO: add prev. instr.
# TODO: Add correct attention check
# TODO: error messages for buttons for task


class C(BaseConstants):
    NAME_IN_URL = 'mentors1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    part_id = models.IntegerField()
    treat = models.StringField()
    workerid = models.StringField()

    test1 = models.IntegerField()
    test2 = models.IntegerField()


# Methods
def creating_session(subsession: Subsession):
    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    # mentors per treatment 2, 3 and 4:
    m_per_treat = 10

    i = 0
    for p in subsession.get_players():
        p.part_id = p.participant.id_in_session
        if i / 4 < m_per_treat:
            p.treat = next(treats)
        elif i / 4 >= m_per_treat:
            p.treat = 't1'
        p.participant.treat = p.treat
        i = i + 1


# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = [
        'workerid'
    ]


class Instructions1(Page):
    pass


class Instructions2(Page):
    pass


class Attention1(Page):
    form_model = 'player'
    form_fields = [
        'test1'
    ]

    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        # TODO: change correct answer
        if player.test1 == 4:
            par.test_passed = 1
        else:
            par.test_passed = 0

    def app_after_this_page(player: Player, upcoming_apps):
        par = player.participant
        if par.test_passed == 0:
            return upcoming_apps[2]
        else:
            pass


class Attention2(Page):
    form_model = 'player'
    form_fields = [
        'test2'
    ]

    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        # TODO: change correct answer
        if player.test2 == 1:
            par.test_passed = 1
        else:
            par.test_passed = 0

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.test_passed == 0:
            return upcoming_apps[2]
        else:
            t = player.treat
            if t != 't3':
                return upcoming_apps[0]
            elif t == 't3':
                return upcoming_apps[1]


page_sequence = [Welcome, Instructions1, Instructions2, Attention1, Attention2]
