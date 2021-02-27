"""Gateway to read state code to state FIPS JSON file."""

import json

#  from ssacc.clean_df import CleanDF
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils
from ssacc.wrappers.timing_wrapper import timing


def get_state_json_filepath():
    """Inject filepath to state to FIPS data."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("reference", "state_fips.json")
    return file_path


@timing
def get_state_fips_json():
    """Return state code and FIPS state codes in a dict."""
    get_path = Factory.get(InjectionKeys.STATE_JSON_FILEPATH)
    input_path = get_path()
    print(f"reading State FIPS JSON in {input_path}")
    read_json = Factory.get(InjectionKeys.STATE_JSON_READ)
    df = read_json(input_path)
    print(df.head())

    return df


@timing
def read_state_json(input_path):
    """Read the state JSON file and return the results."""
    with open(input_path) as state_file:
        statecodes = json.load(state_file)
    return statecodes
