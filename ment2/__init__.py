from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ment2'
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
        return player.participant.treat == 'two'


class ResultsWaitPage(WaitPage):
    def is_displayed(player: Player):
        return player.participant.treat == 'two'


class Results(Page):
    def is_displayed(player: Player):
        return player.participant.treat == 'two'


page_sequence = [MyPage, ResultsWaitPage, Results]
