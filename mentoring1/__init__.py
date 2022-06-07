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
    feedback = models.LongStringField()
    promotion = models.LongStringField()
    promotion2 = models.LongStringField()


# Methods
def creating_session(subsession: Subsession):
    session = subsession.session

    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    # players per treatment 2, 3 and 4
    p_per_treat = 90
    # mentors per treatment 2, 3 and 4
    m_per_treat = 10

    # assign players to treatments; treatments 2-4 will have p_per_treat players max, the excess will be assigned to
    # treatement 1:
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

    print(len(t2_players))

    # out of the players of the treatments respectively, m_per_treat mentors are randomly chosen
    t2_mentors = random.sample(t2_players, m_per_treat)
    # list that only contains workers is created:
    t2_workers = t2_players
    for e in t2_workers:
        if e in t2_mentors:
            t2_workers.remove(e)
    print(len(t2_workers))
    print(len(t2_mentors))

    # same for other treatments
    t3_mentors = random.sample(t3_players, m_per_treat)
    t3_workers = t3_players
    for e in t3_workers:
        if e in t3_mentors:
            t3_workers.remove(e)

    t4_mentors = random.sample(t4_players, m_per_treat)
    t4_workers = t4_players
    for e in t4_workers:
        if e in t4_mentors:
            t4_workers.remove(e)

    # all mentors are assigned mentor job
    mentors = itertools.chain(t2_mentors, t3_mentors, t4_mentors)
    for p in mentors:
        p.job = 'mentor'
        p.participant.job = 'mentor'

    # TODO: group assignment for treatment 2:
    #  no errors but doesn't work the way I want it to yet
    t2_groups = {}
    groupids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    gid = 1
    t2_w_help = t2_workers
    #print(len(t2_w_help))
    while gid < (m_per_treat + 1):
        nextgroup = []
        nextgroup.append(t2_mentors[gid-1])

        ws = random.sample(t2_w_help, 8)
        for e in t2_w_help:
            if e in ws:
                t2_w_help.remove(e)
        nextgroup.extend(ws)
        t2_groups["{}".format(gid)] = nextgroup
        gid = gid + 1
    #print(t2_groups)
    #print(len(t2_w_help))
    #print(len(t2_groups))
    #for id in groupids:
    #    print(len(t2_groups["{}".format(id)]))

    # TODO: add dicts and lists to session.vars

    #session.t1_players = t1_players
    #session.t2_players = t2_players
    #session.t3_players = t3_players
    #session.t4_players = t4_players
    #session.t2_workers = t2_workers
    #session.t3_workers = t2_workers
    #session.t4_workers = t2_workers
    #session.t2_mentors = t2_mentors
    #session.t3_mentors = t2_mentors
    #session.t4_mentors = t2_mentors


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

    def before_next_page(player: Player, timeout_happened):
        pass


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
