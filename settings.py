from os import environ

SESSION_CONFIGS = [
    #dict(
    #    name='Mentoring',
    #    app_sequence=[
    #        'mentoring_start',
    #        'mentoring_t1',
    #        'mentoring_t2',
    #        'mentoring_t3',
    #        'mentoring_t4',
    #        'mentoring_end',
    #    ],
    #    num_demo_participants=370,
    #),
    dict(
        name='Mentors',
        app_sequence=[
            'mentors1',
            'mentors2',
            'mentors2_t3',
            'mentors3'
        ],
        num_demo_participants=100,
    ),
    dict(
        name='Mentees',
        app_sequence=[
            'mentees1',
            'mentees2',
            'mentees3'
        ],
        num_demo_participants=100,
    ),
    dict(
        name='Investors',
        app_sequence=[
            'investors1',
            'investors2',
            'investors3'
        ],
        num_demo_participants=100,
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
    'job',
    'groupno',
    'idingroup',
    'workerlist',
    'test_passed',
    'test2_passed',
    'endmessage',
    'timeout',
    'mentor',
    't3_answers',
    'graphic',
    'bm_dev'
]
SESSION_FIELDS = [
    't2_groups',
    't3_groups',
    't4_groups',
    't2_promo',
    't3_promo',
    't4_promo',
    't2_feedback',
    't3_feedback',
    't4_feedback',

    'obs_t124'
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
