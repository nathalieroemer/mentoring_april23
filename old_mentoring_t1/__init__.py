from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'old_mentoring_t1'
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
    promotion = models.LongStringField()


# PAGES
class WorkerTask(Page):
    form_model = 'player'
    form_fields = [
        'testquest'
    ]

    # TODO: Not really necessary since only workers in this treatment.
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'worker'


class Promotion(Page):
    form_model = 'player'
    form_fields = [
        'promotion'
    ]

    # TODO: Not really necessary since only workers in this treatment.
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.job == 'worker'

    # Following method has to be included in the last page the respective job sees in this app!
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[-1]


page_sequence = [WorkerTask, Promotion]
