from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'old_mentoring_t2'
    PLAYERS_PER_GROUP = None
    # TODO: adjust NUM_ROUNDS so that it's the higher one of repetitions for worker or repetitions for mentor
    NUM_ROUNDS = 8


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    testquest = models.IntegerField(
        label='Please give me a number.'
    )
    feedback = models.LongStringField()
    promotion = models.LongStringField()


# PAGES
class WorkerTask(Page):
    form_model = 'player'
    form_fields = [
        'testquest'
    ]

    @staticmethod
    def is_displayed(player: Player):
        # TODO: might need to add a "and C.NUM_ROUNDS < ..." if mentor has more repetitions
        return player.participant.job == 'worker'


class Wait(Page):
    def is_displayed(player: Player):
        return player.session.t2_feedback[player.participant.groupno][player.participant.idingroup] is None \
               and player.round_number == C.NUM_ROUNDS

    # TODO: write function in Javascript on Wait page that only let's worker continue when advice is already given
    def js_vars(player: Player):
        return dict(
            advice=player.session.t2_feedback[player.participant.groupno][player.participant.idingroup]
        )


class Promotion(Page):
    form_model = 'player'
    form_fields = [
        'promotion'
    ]

    @staticmethod
    def is_displayed(player: Player):
        # TODO: might need to change C.NUM_ROUNDS to something else (if mentor has more repetitions)
        return player.participant.job == 'worker' and player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        par = player.participant
        session = player.session
        advice = session.t2_feedback[par.groupno][par.idingroup]

        return dict(
            advice=advice
        )

    # Following method has to be included in the last page the respective job sees in this app!
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[-1]


class MentorTask(Page):
    form_model = 'player'
    form_fields = [
        'feedback'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'mentor'

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        session = player.session
        if player.participant.treat == 't2':
            # TODO: random worker has to be chosen in vars for template already, because in other treatments, mentor
            #  sees promotion first
            # worker = random.randint(1, 8)
            print(par.workerlist)
            session.t2_feedback[par.groupno][par.workerlist.pop(0)] = player.feedback
        print(session.t2_feedback)

    # Following method has to be included in the last page the respective job sees in this app!
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        # TODO: might need to adjust C.NUM_ROUNDS for same reasons as above...
        if player.round_number == C.NUM_ROUNDS:
            return upcoming_apps[-1]


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [WorkerTask, Wait, Promotion, MentorTask]
