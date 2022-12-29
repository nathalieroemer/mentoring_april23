import pandas as pd
import string

from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'p2_'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

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
    t124_mentors = mdf[mdf['treat'] == "t124"].reset_index(drop=True)

    # same for treatment 3:
    t3_mentors = mdf[mdf['treat'] == "t3"].reset_index(drop=True)



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
                print(par.bm_dev, "who are those others?")
                if i < abs((player.guess-par.numdots)/par.numdots):
                    h = h + 1
            # the lower h the better (1<=h<=4)
            player.rel_perf = h

        player.treat = player.participant.treat

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.timeout:
            return upcoming_apps[1]
        else:
            pass

class Instructions_Advisor(Page):
    def is_displayed(player: Player):
        return player.treat != 't1'


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

    @staticmethod
    def js_vars(player):
        return dict(
            player_guess=player.guess,
        )


class Instructions2(Page):
    pass


class Instructions3(Page):
    pass


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
        if player.treat == 't4':
            if player.rel_perf == 1:
                a = C.t124_mentors["top"][par.mentor]
            elif player.rel_perf == 2:
                a = C.t124_mentors["uppermiddle"][par.mentor]
            elif player.rel_perf == 3:
                a = C.t124_mentors["lowermiddle"][par.mentor]
            elif player.rel_perf == 4:
                a = C.t124_mentors["bottom"][par.mentor]

            if a == "terrible":
                ad = "Terrible"
            elif a == "very poor":
                ad = "Very poor"
            elif a == "poor":
                ad = "Poor"
            elif a == "good":
                ad = "Good"
            elif a == "very good":
                ad = "Very good"
            elif a == "exceptional":
                ad = "Exceptional"
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
            print(C.t3_mentors)
            print(perf)
            print(answ)
            print(par.mentor)
            a = C.t3_mentors['{}_{}'.format(perf, answ)][par.mentor]

        elif player.treat == 't3':
            if player.rel_perf == 1:
                a = C.t124_mentors["top"][par.mentor]
            elif player.rel_perf == 2:
                a = C.t124_mentors["uppermiddle"][par.mentor]
            elif player.rel_perf == 3:
                a = C.t124_mentors["lowermiddle"][par.mentor]
            elif player.rel_perf == 4:
                a = C.t124_mentors["bottom"][par.mentor]

        if player.treat == 't3':
            if a == "terrible":
                ad = "Terrible"
            elif a == "very poor":
                ad = "Very poor"
            elif a == "poor":
                ad = "Poor"
            elif a == "good":
                ad = "Good"
            elif a == "very good":
                ad = "Very good"
            elif a == "exceptional":
                ad = "Exceptional"
        else:
            ad = ""

        if player.evaluation == "terrible":
            pa = "Terrible"
        elif player.evaluation == "very poor":
            pa = "Very poor"
        elif player.evaluation == "poor":
            pa = "Poor"
        elif player.evaluation == "good":
            pa = "Good"
        elif player.evaluation == "very good":
            pa = "Very good"
        elif player.evaluation == "exceptional":
            pa = "Exceptional"

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


page_sequence = [Task1, Instructions_Advisor, Evaluation1, FinalSub, Estimate1]
