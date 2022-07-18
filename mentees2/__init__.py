from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'mentees2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treat = models.StringField()
    guess = models.IntegerField()
    # rel_perf is placement: 1 is best, 4 is worst
    rel_perf = models.IntegerField()
    promotion = models.StringField()

    native = models.IntegerField()
    eng_prof = models.IntegerField(
        blank=True
    )
    diff = models.IntegerField()
    stereo = models.IntegerField()
    bonusest = models.FloatField()
    deviation = models.IntegerField()
    riskpref = models.IntegerField()
    comp = models.IntegerField()

    promotion2 = models.StringField()


# PAGES
class Task1(Page):
    form_model = 'player'
    form_fields = [
        'guess'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        print(player.participant.bm_dev)
        return dict(
            graphic=player.participant.graphic
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        par = player.participant
        h = 1
        for i in par.bm_dev:
            # TODO: 1500 has to be actual number of dots
            if i < abs(1500-player.guess):
                h = h + 1
        player.rel_perf = h


class BonusInstr(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.treat = player.participant.treat


class Task2(Page):
    @staticmethod
    def live_method(player: Player, data):
        player.promotion = str(data)


class Quest(Page):
    form_model = 'player'
    form_fields = [
        'native',
        'eng_prof',
        'diff',
        'deviation',
        'stereo',
        'bonusest',
        'riskpref',
        'comp'
    ]


class Task3(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(
            prevansw=player.promotion
        )

    @staticmethod
    def live_method(player: Player, data):
        player.promotion2 = str(data)


class End(Page):
    pass


page_sequence = [Task1, BonusInstr, Task2, Quest, Task3, End]
