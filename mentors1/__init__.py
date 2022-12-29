from otree.api import *
import itertools
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'm_p1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    part_id = models.IntegerField()
    treat = models.StringField()
    workerid = models.StringField()

    consent1 = models.IntegerField(initial=0)
    consent2 = models.IntegerField(initial=0)
    consent3 = models.IntegerField(initial=0)

    test1 = models.IntegerField(blank=True)
    test2 = models.IntegerField(blank=True)

    trial = models.IntegerField()


# Methods
def creating_session(subsession: Subsession):
    treats = itertools.cycle(['t124', 't3'])


    for p in subsession.get_players():
        p.trial = 1
        p.part_id = p.participant.id_in_session
        # had an idea to save the many answers of t3 mentors in a dict, but it seems to be less convenient eventually
        # p.participant.t3_answers = {}
        p.treat = next(treats)
        p.participant.treat = p.treat


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
    def error_message(player, values):
        solutions = dict(
            test1=3,
            test2=2,
        )
        error_messages = dict()

        for field_name in solutions:
            if values[field_name] =='None':
                error_messages[field_name] = 'Please choose an option'
            if values[field_name] != 'None' and values[field_name] != solutions[field_name] and player.trial == 1:
                print(values[field_name])
                print(solutions[field_name])
                error_messages[field_name] = 'You did not answer correctly. Please try again. If you answer incorrectly, you cannot take part in this study.'
                player.trial = 2
        return error_messages


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        if player.test1 == 3 and player.test2 == 2:
            par.test_passed = 1
        else:
            par.test_passed = 0

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        par = player.participant
        if par.test_passed == 0:
            return upcoming_apps[2]
        else:
            if player.treat == 't3':
                return upcoming_apps[1]
            else:
                pass


page_sequence = [Welcome, Consent, Part1, Instructions1, Instructions2, Attention1]
