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
    NAME_IN_URL = 'p1_'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Lists all possible graphics:
    GRAPHICS = [f for f in listdir("_static/graphics") if isfile(join("_static/graphics", f))]

    mentordata = pd.read_csv(
        "mentor_data.csv",
        delimiter=",",
        encoding="latin1"
    )

    mdf = pd.DataFrame(  # mentor data frame
        mentordata,
        columns=[
            "participantcode",
            "treat",
            "top",
            "uppermiddle",
            "lowermiddle",
            "bottom",
            "top_terrible",
            "top_verypoor",
            "top_poor",
            "top_good",
            "top_verygood",
            "top_exceptional",
            "um_terrible",
            "um_verypoor",
            "um_poor",
            "um_good",
            "um_verygood",
            "um_exceptional",
            "lm_terrible",
            "lm_verypoor",
            "lm_poor",
            "lm_good",
            "lm_verygood",
            "lm_exceptional",
            "b_terrible",
            "b_verypoor",
            "b_poor",
            "b_good",
            "b_verygood",
            "b_exceptional"
        ]
    )

    # saves data only of mentors from treatments 1,2 and 4:
    t124_mentors = mdf[mdf['treat'] =="t124"].reset_index(drop=True)
    # same for treatment 3:
    t3_mentors = mdf[mdf['treat']=="t3"].reset_index(drop=True)
#    print(t3_mentors, "this is the mentors df for t3")

    pretestdata = pd.read_csv(
        "pretestdata.csv",
        delimiter=",",
        encoding="latin1"
    )

    predf = pd.DataFrame(
        pretestdata,
        columns=[
            "participantcode",
            "deviation"
        ]
    )
    # saves a list of performances in terms of deviation from true value of several workers from a previous task:
    benchmark = predf["deviation"].tolist()


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

    test1 = models.IntegerField(blank=True)
    test2 = models.IntegerField(blank=True)
    trial = models.IntegerField(blank=True)


# Methods
def creating_session(subsession: Subsession):
    session = subsession.session
    session.obs_t124 = [0] * len(C.t124_mentors)
    session.obs_t3 = [0] * len(C.t3_mentors)

    treats = itertools.cycle(['t1','t2','t3','t4'])
    # treatment 1: control, treatment 2: no advice, treatment 3: reactive, treatment 4: proactive
    # mentors per treatment 2, 3 and 4:
    # m_per_treat = 10

    # treatment and graphic assignment
    i = 0
    for p in subsession.get_players():
        # if i / 3 < m_per_treat:
        p.treat = next(treats)
        # elif i / 3 >= m_per_treat:
        #     p.treat = 't1'
        p.participant.treat = p.treat
        # i = i + 1
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
        if p.treat == 't4':
            min_obs_t124 = min(session.obs_t124)
            # gives a list of all indices of the obs_t124 list where the value of the obs is min
            mentors = [i for i, x in enumerate(session.obs_t124) if x == min_obs_t124]
            print(mentors, "these are the mentors")
            m = random.choice(mentors)
            # participant.mentor is an int: the index which refers to the specific mentor in the list of mentors for the
            # respective treatment(s) and the list of observations of mentors of the respective treatment(s)
            p.participant.mentor = m
            # player.mentor on the other hand will be the participant.code of the mentor from the mentor experiment in
            # order to have an intelligible data overview
            p.mentor = C.t124_mentors["participantcode"][m]
            session.obs_t124[m] = session.obs_t124[m] + 1
        elif p.treat == 't3':
            min_obs_t3 = min(session.obs_t3)
            mentors = [i for i, x in enumerate(session.obs_t3) if x == min_obs_t3]
            m = random.choice(mentors)
            p.participant.mentor = m
            p.mentor = C.t3_mentors["participantcode"][m]
            session.obs_t3[m] = session.obs_t3[m] + 1

    # values for relative performance
    # deviations of three random workers from previous task are saved in list specific to player to be used for
    # comparison later
    for p in subsession.get_players():
        p.trial = 1 ## for attention check
        # benchmark_deviations : deviations from pretest
        p.participant.bm_dev = []
        rand_indices = random.sample(range(len(C.benchmark)), 3)
        print(rand_indices, "these are the indices")
        for i in rand_indices:
            p.participant.bm_dev.append(C.benchmark[i])
        print(p.participant.bm_dev, "these are the players for deviation?")


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
        'consent3'
    ]

class Part1(Page):
    pass

class Instructions(Page):
    pass


class Attention1(Page):
    form_model = 'player'
    form_fields = [
        'test1',
        'test2'
    ]

    @staticmethod
    def error_message(player, values):
        solutions = dict(
            test1=1,
            test2=2,
        )
        error_messages = dict()

        for field_name in solutions:
            if values[field_name] =='None':
                error_messages[field_name] = 'Please choose an option'
            if values[field_name] != 'None' and values[field_name] != solutions[field_name] and player.trial == 1:
                error_messages[field_name] = 'You did not answer correctly. Please try again. If you answer incorrectly, you cannot take part in this study.'
                player.trial = 2
        return error_messages


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        par.test2_passed = 0
        if player.test1 == 1 and player.test2 == 2:
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


page_sequence = [Welcome, Consent, Part1, Instructions, Attention1]
