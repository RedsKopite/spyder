from parsers.handles.handle_data import *
from parsers.handles.handle_starttag import *

HANDLE_DATA_DICT = {
    "001": handle_data_001,
    "002": handle_data_002
}

HANDLE_STARTTAG_DICT = {
    "001": handle_starttag_001,
    "002": handle_starttag_002
}