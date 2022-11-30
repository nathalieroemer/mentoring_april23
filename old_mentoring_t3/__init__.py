from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'old_mentoring_t3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


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
    promotion2 = models.LongStringField()


# PAGES
class WorkerTask(Page):
    form_model = 'player'
    form_fields = [
        'testquest'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'worker'


class Promotion(Page):
    form_model = 'player'
    form_fields = [
        'promotion'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'worker'


class MentorTask(Page):
    form_model = 'player'
    form_fields = [
        'feedback'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'mentor'

    def vars_for_template(player: Player):
        pass

    def before_next_page(player: Player, timeout_happened):
        session = player.session
        if player.participant.treat == 't2':
            # TODO: random worker has to be chosen in vars for template already, because in other treatments, mentor
            #  sees promotion first
            worker = random.randint(1, 8)
            session.t2_feedback[player.participant.groupno][worker] = player.feedback
        print(session.t2_feedback)

    # Following method has to be included in the last page the respective job sees in this app!
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[-1]


class PromotionII(Page):
    form_model = 'player'
    form_fields = [
        'promotion2'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'worker'

    # Following method has to be included in the last page the respective job sees in this app!
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[-1]


page_sequence = [WorkerTask, Promotion, MentorTask, PromotionII]
