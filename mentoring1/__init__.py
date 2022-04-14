from otree.api import *
import itertools
import random


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
    job = models.StringField()
    testquest = models.IntegerField(
        label='Please give me a number.'
    )
    feedback = models.StringField()
    promotion = models.StringField()
    promotion2 = models.StringField()


# Methods
def creating_session(subsession: Subsession):
    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    # players per treatment 2, 3 and 4
    p_per_treat = 90
    # mentors per treatment 2, 3 and 4
    m_per_treat = 10
    t1_players = []
    t2_players = []
    t3_players = []
    t4_players = []
    i = 0
    for p in subsession.get_players():
        if i / 4 < p_per_treat:
            p.treat = next(treats)
        elif i / 4 >= p_per_treat:
            p.treat = 't1'
        p.participant.treat = p.treat
        i = i + 1

        if p.treat == 't1':
            t1_players.append(p)
        elif p.treat == 't2':
            t2_players.append(p)
        elif p.treat == 't3':
            t3_players.append(p)
        elif p.treat == 't4':
            t4_players.append(p)

        p.job = 'worker'
        p.participant.job = 'worker'

    t2_mentors = random.sample(t2_players, m_per_treat)
    t3_mentors = random.sample(t3_players, m_per_treat)
    t4_mentors = random.sample(t4_players, m_per_treat)
    mentors = itertools.chain(t2_mentors, t3_mentors, t4_mentors)
    for p in mentors:
        p.job = 'mentor'
        p.participant.job = 'mentor'


# PAGES
class Welcome(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class WorkerTask(Page):
    form_model = 'player'
    form_fields = [
        'testquest'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.job == 'worker'


class MentorTask(Page):
    form_model = 'player'
    form_fields = [
        'feedback'
    ]
    @staticmethod
    def is_displayed(player: Player):
        return player.job == 'mentor'


class Promotion(Page):
    form_model = 'player'
    form_fields = [
        'promotion'
    ]
    @staticmethod
    def is_displayed(player: Player):
        return player.job == 'worker'


class PromotionII(Page):
    form_model = 'player'
    form_fields = [
        'promotion2'
    ]
    @staticmethod
    def is_displayed(player: Player):
        return (player.treat == 't3' or player.treat == 't4') and player.job == 'worker'


class Questionnaire(Page):
    pass


class Endpage(Page):
    pass


page_sequence = [Welcome, WorkerTask, MentorTask, Promotion, PromotionII, Questionnaire, Endpage]
