from os import environ

SESSION_CONFIGS = [
    dict(
        name='Mentoring',
        app_sequence=[
            'mentoring1',
        ],
        num_demo_participants=370,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'treat',
    'job'
]
SESSION_FIELDS = [
    #'t1_players',
    #'t2_players',
    #'t3_players',
    #'t4_players',
    #'t2_workers',
    #'t3_workers',
    #'t4_workers',
    #'t2_mentors',
    #'t3_mentors',
    #'t4_mentors',
    't2_groups',
    't3_groups',
    't4_groups'
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1353908471533'
