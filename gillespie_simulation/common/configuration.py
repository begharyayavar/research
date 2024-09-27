import numpy as np
from colors import colors

# Simulation Defaults
DEFAULT_NUM_CYCLES = 1000
DEFAULT_NUM_STEPS = 1000

# Datatype config
DtypeKey = np.uint8
DtypeCount = np.uint16
DtypeIndex = np.uint8
DtypeCoefficient = np.int8

DtypeCSA = np.uint16 # Counts,Species,Averages

DtypeTimestamps = np.float32
DtypeState = np.uint8
DtypeTrajectories = np.uint8

# printing config
DEFAULT_TAB_WIDTH = len("\t".expandtabs())
DEFAULT_COL_WIDTH = 24


# Delimiters for parser
REACTION_DELIMITERS=["--->","-->","->",">",] # !IMPORTANT order matters here due to it's checked to slice,superstrings need to come first.
REACTANT_DELIMITERS=["+",",","."]
RATE_CONSTANT_DELIMITERS=["@","|"]
COEFFICIENT_DELIMITERS=["."]
INITIAL_CONDITION_DELIMITERS = ["=",":"]
ALL_DELIMITERS =    REACTION_DELIMITERS + REACTANT_DELIMITERS + REACTANT_DELIMITERS +\
                    COEFFICIENT_DELIMITERS+ INITIAL_CONDITION_DELIMITERS + RATE_CONSTANT_DELIMITERS

# Theme
RESET = colors.reset
BOLD = colors.bold
LINE_COLOR = colors.fg.yellow
HEADING_COLOR = colors.fg.yellow
STATUS_COLOR = colors.fg.yellow
TEXT_COLOR = colors.fg.yellow
COUNT_COLOR = colors.fg.yellow
REACTANT_COLOR = colors.fg.yellow
PRODUCT_COLOR =colors.fg.yellow

# Vocabulary
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSSTUVWXYZ"
NUMBERS = "0123456789"