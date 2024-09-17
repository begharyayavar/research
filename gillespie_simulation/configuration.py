








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
                    COEFFICIENT_DELIMITERS+ INITIAL_CONDITION_DELIMITERS
