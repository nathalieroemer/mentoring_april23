from otree.api import *


doc = """
Your app description
"""


# METHODS
def make_7pointlikert(label, blank=False):
    if not blank:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7],
            label=label,
            widget=widgets.RadioSelect
        )
    else:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7],
            label=label,
            widget=widgets.RadioSelect,
            blank=True
        )


def make_10pointlikert(label, blank=False):
    if not blank:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            label=label,
            widget=widgets.RadioSelect
        )
    else:
        return models.IntegerField(
            choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            label=label,
            widget=widgets.RadioSelect,
            blank=True
        )


# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'mentees4'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    diff = make_7pointlikert("How difficult did you find it to guess the number of dots in the pictures?")
    stereotypes = make_7pointlikert("Do you think this task rather favors male or female participants?")
    bonusest = models.FloatField(min=0, max=2)
    own_perf = models.StringField()
    others_perf = models.StringField()
    ident_adv = models.IntegerField()
    ident_inv = models.IntegerField()
    reciprocity = make_10pointlikert("When someone does me a favor, I am willing to return it.")
    intentions = make_10pointlikert("I assume that people have only the best intentions.")
    donation = models.FloatField()
    riskpref = make_7pointlikert(
        "How do you see yourself: Are you someone who is willing to take risks or do you try to avoid them?")
    gender = models.IntegerField()
#    clarity_bin = models.IntegerField(
#        label="Where the instructions clear to you or did you had difficulties to understanding them?",
#        blank=True
#    )

#    clarity = models.LongStringField(
#        label="Please shorty explain, where did you had difficulties to understand the instructions?",
#        blank=True
#    )

#    tech_bin = models.IntegerField(
#        label="Do you think, everything was displayed to you correctly during this study?",
#        blank=True
#    )
#    tech = models.LongStringField(
#        label="Could you shortly describe your problem?",
#        blank=True
#    )


# PAGES
class Part3(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1 and par.timeout2 == 0 and par.timeout == 0


class Quest(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1 and par.timeout2 == 0 and par.timeout == 0 and par.treat != 't1'

    form_model = 'player'
    form_fields = [
        'diff',
        'stereotypes',
        'bonusest',
        'ident_adv',
        'ident_inv',
        'reciprocity',
        'intentions',
        'donation',
        'riskpref',
        'gender',
#        'clarity',
#        'clarity_bin',
#        'tech',
#        'tech_bin'
    ]

    @staticmethod
    def live_method(player: Player, data):
        if data['section'] == 'own_p':
            player.own_perf = str(data['value'])
        elif data['section'] == 'others_p':
            player.others_perf = str(data['value'])

class Quest_t1(Page):
    @staticmethod
    def is_displayed(player: Player):
        par = player.participant
        return par.test_passed == 1 and par.timeout2 == 0 and par.timeout == 0 and par.treat == 't1'

    form_model = 'player'
    form_fields = [
        'diff',
        'stereotypes',
        'bonusest',
        'ident_inv',
        'reciprocity',
        'intentions',
        'donation',
        'riskpref',
        'gender',
#        'clarity',
#        'clarity_bin',
#        'tech',
#        'tech_bin'
    ]

    def before_next_page(player, timeout_happened):
        player.ident_adv = 0

    @staticmethod
    def live_method(player: Player, data):
        if data['section'] == 'own_p':
            player.own_perf = str(data['value'])
        elif data['section'] == 'others_p':
            player.others_perf = str(data['value'])

class End(Page):
    pass


page_sequence = [Part3, Quest, Quest_t1, End]
