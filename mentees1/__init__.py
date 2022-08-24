import itertools
import pandas as pd
import random
from os import listdir
from os.path import isfile, join

from otree.api import *


doc = """
Your app description
"""

# TODO: add partial payment when timeout in second round?


class C(BaseConstants):
    NAME_IN_URL = 'mentees1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Lists all possible graphics:
    GRAPHICS = [f for f in listdir("_static/graphics") if isfile(join("_static/graphics", f))]

    mentordata = pd.read_csv(
        "testdata.csv",
        delimiter=";",
        encoding="latin1"
    )
    mdf = pd.DataFrame(  # mentor data frame
        mentordata,
        columns=[
            "participant.code",
            "participant._current_page_name",
            "participant.treat",
            "mentors2.1.player.top",
            "mentors2.1.player.uppermiddle",
            "mentors2.1.player.lowermiddle",
            "mentors2.1.player.bottom",
            "mentors2_t3.1.player.top_terrible",
            "mentors2_t3.1.player.top_verypoor",
            "mentors2_t3.1.player.top_poor",
            "mentors2_t3.1.player.top_good",
            "mentors2_t3.1.player.top_verygood",
            "mentors2_t3.1.player.top_exceptional",
            "mentors2_t3.1.player.um_terrible",
            "mentors2_t3.1.player.um_verypoor",
            "mentors2_t3.1.player.um_poor",
            "mentors2_t3.1.player.um_good",
            "mentors2_t3.1.player.um_verygood",
            "mentors2_t3.1.player.um_exceptional",
            "mentors2_t3.1.player.lm_terrible",
            "mentors2_t3.1.player.lm_verypoor",
            "mentors2_t3.1.player.lm_poor",
            "mentors2_t3.1.player.lm_good",
            "mentors2_t3.1.player.lm_verygood",
            "mentors2_t3.1.player.lm_exceptional",
            "mentors2_t3.1.player.b_terrible",
            "mentors2_t3.1.player.b_verypoor",
            "mentors2_t3.1.player.b_poor",
            "mentors2_t3.1.player.b_good",
            "mentors2_t3.1.player.b_verygood",
            "mentors2_t3.1.player.b_exceptional"
        ]
    )
    mdf = mdf[mdf["participant._current_page_name"] == "End"]
    # saves data only of mentors from treatments 1,2 and 4:
    t124_mentors = mdf[pd.isna(mdf["mentors2_t3.1.player.top_terrible"])].reset_index(drop=True)
    # same for treatment 3:
    t3_mentors = mdf[pd.isna(mdf["mentors2.1.player.top"])].reset_index(drop=True)

    pretestdata = pd.read_csv(
        "pretestdata.csv",
        delimiter=";",
        encoding="latin1"
    )

    predf = pd.DataFrame(
        pretestdata,
        columns=[
            "participant.id_in_session",
            "participant.code",
            "participant.deviation"
        ]
    )
    # saves a list of performances in terms of deviation from true value of several workers from a previous task:
    benchmark = predf["participant.deviation"].tolist()


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    workerid = models.StringField()
    mentor = models.StringField()
    graphic = models.StringField()
    numdots = models.IntegerField()

    consent1 = models.IntegerField(initial=0)
    consent2 = models.IntegerField(initial=0)
    consent3 = models.IntegerField(initial=0)
    consent4 = models.IntegerField(initial=0)
    consent5 = models.IntegerField(initial=0)

    test1 = models.IntegerField()


# Methods
def creating_session(subsession: Subsession):
    session = subsession.session
    session.obs_t124 = [0] * len(C.t124_mentors)
    session.obs_t3 = [0] * len(C.t3_mentors)

    treats = itertools.cycle(['t1', 't2', 't3', 't4'])
    # mentors per treatment 2, 3 and 4:
    m_per_treat = 10

    # treatment and graphic assignment
    i = 0
    for p in subsession.get_players():
        if i / 4 < m_per_treat:
            p.treat = next(treats)
        elif i / 4 >= m_per_treat:
            p.treat = 't1'
        p.participant.treat = p.treat
        i = i + 1
        p.graphic = random.choice(C.GRAPHICS)
        p.participant.graphic = p.graphic
        # save number of dots of graphic:
        p.numdots = int(p.graphic[8:-4])
        p.participant.numdots = p.numdots
        # timeout booleans set to initial:
        p.participant.timeout = 0
        p.participant.timeout2 = 0

    # mentor assignment
    for p in subsession.get_players():
        if p.treat != 't3':
            min_obs_t124 = min(session.obs_t124)
            # gives a list of all indices of the obs_t124 list where the value of the obs is min
            mentors = [i for i, x in enumerate(session.obs_t124) if x == min_obs_t124]
            m = random.choice(mentors)
            # participant.mentor is an int: the index which refers to the specific mentor in the list of mentors for the
            # respective treatment(s) and the list of observations of mentors of the respective treatment(s)
            p.participant.mentor = m
            # player.mentor on the other hand will be the participant.code of the mentor from the mentor experiment in
            # order to have an intelligible data overview
            p.mentor = C.t124_mentors["participant.code"][m]
            session.obs_t124[m] = session.obs_t124[m] + 1
        elif p.treat == 't3':
            min_obs_t3 = min(session.obs_t3)
            mentors = [i for i, x in enumerate(session.obs_t3) if x == min_obs_t3]
            m = random.choice(mentors)
            p.participant.mentor = m
            p.mentor = C.t3_mentors["participant.code"][m]
            session.obs_t3[m] = session.obs_t3[m] + 1

    # values for relative performance
    # deviations of three random workers from previous task are saved in list specific to player to be used for
    # comparison later
    for p in subsession.get_players():
        # benchmark_deviations
        p.participant.bm_dev = []
        rand_indices = random.sample(range(len(C.benchmark)), 3)
        # print(rand_indices)
        for i in rand_indices:
            p.participant.bm_dev.append(C.benchmark[i])
        # print(p.participant.bm_dev)


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
        'consent4',
        'consent5'
    ]


class Instructions(Page):
    pass


class Attention1(Page):
    form_model = 'player'
    form_fields = [
        'test1'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        par.test2_passed = 0
        if player.test1 == 1:
            par.test_passed = 1
            # endmessage is variable helping with display of goodbye message, depending on which test was (not) passed
            par.endmessage = 1
        else:
            par.test_passed = 0
            par.endmessage = 2

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        par = player.participant
        if par.test_passed == 0:
            return upcoming_apps[2]
        else:
            pass


page_sequence = [Welcome, Consent, Instructions, Attention1]
