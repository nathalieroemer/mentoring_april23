from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ment1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    def is_displayed(player: Player):
        return player.participant.treat == 'one'


class ResultsWaitPage(WaitPage):
    def is_displayed(player: Player):
        return player.participant.treat == 'one'


class Results(Page):
    def is_displayed(player: Player):
        return player.participant.treat == 'one'


page_sequence = [MyPage, ResultsWaitPage, Results]
