from os import environ

SESSION_CONFIGS = [
    #dict(
    #    name='Mentoring',
    #    app_sequence=[
    #        'old_mentoring_start',
    #        'old_mentoring_t1',
    #        'old_mentoring_t2',
    #        'old_mentoring_t3',
    #        'old_mentoring_t4',
    #        'old_mentoring_end',
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
#    dict(
#        name='old Mentees experiment with 4 treatments',
#        app_sequence=[
#            'old_mentees1',
#            'old_mentees2',
#            'old_mentees3',
#            'old_mentees4'
#        ],
#        num_demo_participants=100,
#    ),
    dict(
        name='Mentees',
        app_sequence=[
            'mentees1',
            'mentees2',
            'mentees3',
            'mentees4'
        ],
        num_demo_participants=4,
    ),
    dict(
        name='Mentees_test',
        app_sequence=[
            'mentees1',
        ],
        num_demo_participants=4,
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
    'g_treat',
    'job',
    'groupno',
    'idingroup',
    'workerlist',
    'test_passed',
    'test2_passed',
    'endmessage',
    'timeout',
    'timeout2',
    'mentor',
    't3_answers',
    'graphic',
    'numdots',
    'bm_dev',
    'performances',
    'scenarios',
    'invest_worker'
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1353908471533'