import pandas as pd
import string

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentees2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    mentordata = pd.read_csv(
        "testdata.csv",
        delimiter=";",
        encoding="latin1"
    )
    mdf = pd.DataFrame(
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


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    test2 = models.IntegerField()

    timeout = models.BooleanField(initial=False)
    guess = models.IntegerField()
    # rel_perf is placement: 1 is best, 4 is worst
    rel_perf = models.IntegerField()
    lowest = models.IntegerField()
    highest = models.IntegerField()
    evaluation = models.StringField()
    evaluation2 = models.StringField()


# Methods
def creating_session(subsession: Subsession):
    pass


# PAGES
class Task1(Page):
    form_model = 'player'
    form_fields = [
        'guess'
    ]
    timeout_seconds = 60

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            graphic="graphics/"+player.participant.graphic
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        if timeout_happened:
            player.timeout = True
            par.timeout = True
        else:
            par.timeout = False
            h = 1
            for i in par.bm_dev:
                if i < abs(par.numdots - player.guess):
                    h = h + 1
            # the lower h the better (1<=h<=4)
            player.rel_perf = h

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.timeout:
            return upcoming_apps[1]
        else:
            pass


class Estimate1(Page):
    form_model = 'player'
    form_fields = [
        'lowest',
        'highest'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            graphic="graphics/"+player.participant.graphic,
            guess=player.guess
        )


class Instructions2(Page):
    pass


class Instructions3(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.treat = player.participant.treat


class Attention2(Page):
    form_model = 'player'
    form_fields = [
        'test2'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        if player.test2 == 2:
            par.test2_passed = 1
        else:
            par.test2_passed = 0
            par.endmessage = 3

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        par = player.participant
        if par.test2_passed == 0:
            return upcoming_apps[1]
        else:
            pass


class Evaluation1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        par = player.participant
        if player.treat == 't2':
            if player.rel_perf == 1:
                a = C.t124_mentors["mentors2.1.player.top"][par.mentor]
            elif player.rel_perf == 2:
                a = C.t124_mentors["mentors2.1.player.uppermiddle"][par.mentor]
            elif player.rel_perf == 3:
                a = C.t124_mentors["mentors2.1.player.lowermiddle"][par.mentor]
            elif player.rel_perf == 4:
                a = C.t124_mentors["mentors2.1.player.bottom"][par.mentor]

            if a == "terrible":
                ad = "1-Terrible"
            elif a == "very poor":
                ad = "2-Very poor"
            elif a == "poor":
                ad = "3-Poor"
            elif a == "good":
                ad = "4-Good"
            elif a == "very good":
                ad = "5-Very good"
            elif a == "exceptional":
                ad = "6-Exceptional"
        else:
            ad = ""

        return dict(
            advice=ad
        )

    @staticmethod
    def live_method(player: Player, data):
        player.evaluation = str(data)


class FinalSub(Page):
    @staticmethod
    def vars_for_template(player: Player):
        par = player.participant
        if player.treat == 't3':
            if player.rel_perf == 1:
                perf = "top"
            elif player.rel_perf == 2:
                perf = "um"
            elif player.rel_perf == 3:
                perf = "lm"
            elif player.rel_perf == 4:
                perf = "b"

            # replace(" ", "") removes whitespaces
            answ = player.evaluation.replace(" ", "")

            a = C.t3_mentors['mentors2_t3.1.player.{}_{}'.format(perf, answ)][par.mentor]

        elif player.treat == 't4':
            if player.rel_perf == 1:
                a = C.t124_mentors["mentors2.1.player.top"][par.mentor]
            elif player.rel_perf == 2:
                a = C.t124_mentors["mentors2.1.player.uppermiddle"][par.mentor]
            elif player.rel_perf == 3:
                a = C.t124_mentors["mentors2.1.player.lowermiddle"][par.mentor]
            elif player.rel_perf == 4:
                a = C.t124_mentors["mentors2.1.player.bottom"][par.mentor]

        if player.treat == 't3' or player.treat == 't4':
            if a == "terrible":
                ad = "1-Terrible"
            elif a == "very poor":
                ad = "2-Very poor"
            elif a == "poor":
                ad = "3-Poor"
            elif a == "good":
                ad = "4-Good"
            elif a == "very good":
                ad = "5-Very good"
            elif a == "exceptional":
                ad = "6-Exceptional"
        else:
            ad = ""

        if player.evaluation == "terrible":
            pa = "1-Terrible"
        elif player.evaluation == "very poor":
            pa = "2-Very poor"
        elif player.evaluation == "poor":
            pa = "3-Poor"
        elif player.evaluation == "good":
            pa = "4-Good"
        elif player.evaluation == "very good":
            pa = "5-Very good"
        elif player.evaluation == "exceptional":
            pa = "6-Exceptional"

        return dict(
            advice=ad,
            prevansw=pa
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            prevansw=player.evaluation
        )

    @staticmethod
    def live_method(player: Player, data):
        player.evaluation2 = str(data)


page_sequence = [Task1, Estimate1, Instructions2, Instructions3, Attention2, Evaluation1, FinalSub]
