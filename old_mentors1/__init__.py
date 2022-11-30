from otree.api import *
import itertools
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'old_mentors1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    part_id = models.IntegerField()
    treat = models.StringField()
    g_treat = models.IntegerField()  # 1 for female, 0 for male
    workerid = models.StringField()

    consent1 = models.IntegerField(initial=0)
    consent2 = models.IntegerField(initial=0)
    consent3 = models.IntegerField(initial=0)
    consent4 = models.IntegerField(initial=0)

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
        # had an idea to save the many answers of t3 mentors in a dict, but it seems to be less convenient eventually
        # p.participant.t3_answers = {}
        if i / 4 < m_per_treat:
            p.treat = next(treats)
        elif i / 4 >= m_per_treat:
            p.treat = 't1'
        p.participant.treat = p.treat
        p.g_treat = random.randint(0, 1)
        p.participant.g_treat = p.g_treat
        i = i + 1


# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = [
        'workerid'
    ]


class Consent(Page):
    form_model = 'player'
    form_fields = [
        'consent1',
        'consent2',
        'consent3',
        'consent4'
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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        if player.test1 == 3:
            par.test_passed = 1
        else:
            par.test_passed = 0

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        par = player.participant
        if par.test_passed == 0:
            return upcoming_apps[2]
        else:
            if player.treat == 't3':
                return upcoming_apps[1]
            else:
                pass


page_sequence = [Welcome, Consent, Instructions1, Instructions2, Attention1]
