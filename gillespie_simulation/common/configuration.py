import numpy as np


# Simulation Defaults
DEFAULT_CYCLES = 1000
DEFAULT_STEPS = 1000

# Datatype config
DtypeTimestamps = np.float32
DtypeState = np.uint8
DtypeTrajectories = np.uint8

# printing config
DEFAULT_TAB_WIDTH = len("\t".expandtabs())
DEFAULT_COL_WIDTH = 24

# Delimiters for parser
# !IMPORTANT order matters here due to it's checked to slice,superstrings need to come first.
REACTION_DELIMITERS=["--->","-->","->",">",]
REACTANT_DELIMITERS=["+",",","."]
RATE_CONSTANT_DELIMITERS=["@","|"]
COEFFICIENT_DELIMITERS=["."]
INITIAL_CONDITION_DELIMITERS = ["=",":"]
ALL_DELIMITERS =    REACTION_DELIMITERS + REACTANT_DELIMITERS + REACTANT_DELIMITERS +\
                    COEFFICIENT_DELIMITERS+ INITIAL_CONDITION_DELIMITERS
