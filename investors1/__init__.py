from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'investors1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    workerid = models.StringField()

    consent1 = models.IntegerField(initial=0)
    consent2 = models.IntegerField(initial=0)
    consent3 = models.IntegerField(initial=0)

    test1 = models.IntegerField()
    test2 = models.IntegerField()


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

class Instructions1(Page):
    pass


class Instructions2(Page):
    pass


class Attention1(Page):
    form_model = 'player'
    form_fields = [
        'test1',
        'test2'
    ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        if player.test1 == 2 and player.test2 == 4:
            par.test_passed = 1
        else:
            par.test_passed = 0

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        par = player.participant
        if par.test_passed == 0:
            return upcoming_apps[1]
        else:
            pass



page_sequence = [Welcome, Consent, Part1, Instructions1, Instructions2, Attention1]
