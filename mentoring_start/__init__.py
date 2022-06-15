from otree.api import *
import itertools
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentoring_start'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    job = models.StringField()
    groupno = models.IntegerField()
    idingroup = models.IntegerField()


# Methods
def creating_session(subsession: Subsession):
    session = subsession.session

    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    # players per treatment 2, 3 and 4
    p_per_treat = 90
    # mentors per treatment 2, 3 and 4
    m_per_treat = 10
    # workers per group:
    w_per_group = 8

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

    # out of the players of the treatments respectively, m_per_treat mentors are randomly chosen
    t2_mentors = random.sample(t2_players, m_per_treat)
    # list that only contains workers is created:
    t2_workers = t2_players
    for e in t2_mentors:
        if e in t2_workers:
            t2_workers.remove(e)

    # same for other treatments
    t3_mentors = random.sample(t3_players, m_per_treat)
    t3_workers = t3_players
    for e in t3_mentors:
        if e in t3_workers:
            t3_workers.remove(e)

    t4_mentors = random.sample(t4_players, m_per_treat)
    t4_workers = t4_players
    for e in t4_mentors:
        if e in t4_workers:
            t4_workers.remove(e)

    # all mentors are assigned mentor job
    mentors = itertools.chain(t2_mentors, t3_mentors, t4_mentors)
    for p in mentors:
        p.job = 'mentor'
        p.participant.job = 'mentor'
        p.participant.workerlist = random.sample(range(1, (w_per_group+1)), w_per_group)
        # TODO: see if performance is better if we just assign lists with values from 1 to 8 and choose randomly later
        #  on mentor task page

    # group assignment for treatment 2:
    t2_groups = {}
    gid = 1  # group ID
    t2_w_help = t2_workers
    while gid < (m_per_treat + 1):
        nextgroup = [t2_mentors[gid - 1]]  # nextgroup will be the list of players that will be one group
        ws = random.sample(t2_w_help, w_per_group)  # random choice of w_per_group workers matched with one mentor
        for e in ws:
            if e in t2_w_help:
                t2_w_help.remove(e)
        nextgroup.extend(ws)
        # eventually, not the whole player objects but only their ids will be added to the dict, as it seems to not
        # be possible to store whole player objects in session variables (which is needed later on)
        ids_nextgroup = []
        for p in nextgroup:
            p.groupno = gid
            p.participant.groupno = p.groupno
            # idingroup is not id_in_group! idingroup determines the id in the assigned groups
            # id_in_group is an otree default but as we don't work with the default groups and there basically is only
            # one group for otree, id_in_group is unique for every participant. We use it as a participant's id which
            # helps when one player has to access the other players' variable values.
            p.idingroup = nextgroup.index(p)
            p.participant.idingroup = p.idingroup
            ids_nextgroup.append(p.id_in_group)
        t2_groups[gid] = ids_nextgroup
        gid = gid + 1

    # ... treatment 3:
    t3_groups = {}
    gid = 1
    t3_w_help = t3_workers
    while gid < (m_per_treat + 1):
        nextgroup = [t3_mentors[gid - 1]]
        ws = random.sample(t3_w_help, w_per_group)
        for e in ws:
            if e in t3_w_help:
                t3_w_help.remove(e)
        nextgroup.extend(ws)
        ids_nextgroup = []
        for p in nextgroup:
            p.groupno = gid
            p.idingroup = nextgroup.index(p)
            ids_nextgroup.append(p.id_in_group)
        t3_groups[gid] = ids_nextgroup
        gid = gid + 1

    # ... and 4:
    t4_groups = {}
    gid = 1
    t4_w_help = t4_workers
    while gid < (m_per_treat + 1):
        nextgroup = [t4_mentors[gid - 1]]
        ws = random.sample(t4_w_help, w_per_group)
        for e in ws:
            if e in t4_w_help:
                t4_w_help.remove(e)
        nextgroup.extend(ws)
        ids_nextgroup = []
        for p in nextgroup:
            p.groupno = gid
            p.idingroup = nextgroup.index(p)
            ids_nextgroup.append(p.id_in_group)
        t4_groups[gid] = ids_nextgroup
        gid = gid + 1

    print(t2_groups)
    # print(len(t2_w_help))
    # print(len(t2_groups))
    # groupids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # for id in groupids:
    #     print(len(t4_groups["{}".format(id)]))

    session.t2_groups = t2_groups
    session.t3_groups = t3_groups
    session.t4_groups = t4_groups

    session.t2_promo = {}
    session.t3_promo = {}
    session.t4_promo = {}
    session.t2_feedback = {}
    session.t3_feedback = {}
    session.t4_feedback = {}
    gid = 1
    while gid < (m_per_treat + 1):
        session.t2_promo[gid] = [None]*(w_per_group+1)
        session.t3_promo[gid] = [None]*(w_per_group+1)
        session.t4_promo[gid] = [None]*(w_per_group+1)
        session.t2_feedback[gid] = [None]*(w_per_group+1)
        session.t3_feedback[gid] = [None]*(w_per_group+1)
        session.t4_feedback[gid] = [None]*(w_per_group+1)
        gid = gid + 1

    print(session.t2_feedback)


# PAGES
class Welcome(Page):
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        print(upcoming_apps)
        if player.treat == 't1':
            return upcoming_apps[0]
        elif player.treat == 't2':
            return upcoming_apps[1]
        elif player.treat == 't3':
            return upcoming_apps[2]
        elif player.treat == 't4':
            return upcoming_apps[3]


page_sequence = [Welcome]
