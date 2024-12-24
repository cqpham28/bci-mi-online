"""
config
"""

# SECTION home screen
MARGIN = 100
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 75
GAP = 75


# SECTION select trial screen
SELECT_BOX_HEIGHT = 300
SELECT_BOX_WIDTH = 300
BOX_GAP = int(SELECT_BOX_WIDTH / 2) + GAP
DEFAULT_TRIAL = 2


# SECTION experiment screen
SHOW_INSTRUCTION_TIME = 2000  # millisec
BUTTON_BACKGROUND_COLOR_TIME = 2000  # millisec
WAIT_SHOW_INSTRUCTION_TIME = 2000  # millisec
FORECAST_TIME = 4000  # millisec
DISPLAY_FORECAST_TIME = 2500  # millisec
# deploy
DISPLAY_CURSORWINDOW_TIME = 1000

BREAK_TIME = 3000


THICKNESS = 50

STEP_RELAXING = 'relaxing'
STEP_INSTRUCTION = 'instruction'
STEP_THINKING = 'thinking'
STEP_RESULT = 'result'
STEP_BREAK = 'break'

PROTOCOL_MAPPING = {
    "2-class": {
        "num_arrow":2, 
        "num_class":2,
        "list_button": ["btn_left", "btn_right"],
    },
    "4-class": {
        "num_arrow":4, 
        "num_class":4,
        "list_button": ["btn_left", "btn_right", "btn_up", "btn_down"],
    },
    "8-class*": {
        "num_arrow":4,
        "num_class":8,
        "list_button": ["btn_left", "btn_right", "btn_up", "btn_down",
            "btn_top_right", "btn_bot_right", "btn_top_left", "btn_bot_left"], 
    },
}

NUMBER_ARROW_MAPPING = {
    1: "./asset/new/right",
    2: "./asset/new/left",
    3: "./asset/new/up",
    4: "./asset/new/down",
}


ARROW_RIGHT_INT = 1
ARROW_LEFT_INT = 2
ARROW_UP_INT = 3
ARROW_DOWN_INT = 4
ARROW_TOP_RIGHT_INT = 5
ARROW_BOT_RIGHT_INT = 6
ARROW_TOP_LEFT_INT = 7
ARROW_BOT_LEFT_INT = 8


##
DATA_DEFAULT = {
    "n_trials": 2,
    "n_classes": 2
    }


## Cortex.export
DURATION_OF_TRIAL = 12
DELAY_BETWEEN_TRIALS = 0

########
STREAM_ONLINE = True