"""Test gateway to country rate data."""

import warnings

# suppress spurious "numpy.ufunc size changed" warnings
# According to
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
# these warnings are benign.
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="numpy.dtype size changed")
    warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
    import pandas as pd

from ssacc.adapters import countyrate_gateway
from ssacc.factories.factory import Factory, InjectionKeys
from ssacc.utils import utils

# Tests do not need to be DRY
# pylint: disable=duplicate-code
# pylint: disable=R0801


def test_read_csv():
    """Test read_csv() on the happy path."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "test1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = countyrate_gateway.read_csv(file_path)
    assert not df.empty
    for column_name in required_columns:
        assert column_name in df.columns


def test_read_csv_file_not_found():
    """Test read_csv() for bad path."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "file_not_found.csv")
    print(file_path)
    df = None
    try:
        df = countyrate_gateway.read_csv(file_path)
    except FileNotFoundError:
        pass
    assert df is None


def test_clean_csv():
    """Test CSV cleaning."""
    cars = {
        "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000],
        "ssacounty": ["12015", "22013", "32018", "42018"],
        "partsab5bonus2018rate": [2200, 2500, 2700, 3500],
        "partsab35bonus2018rate": [220, 250, 270, 350],
        "partsab0bonus2018rate": [22, 25, 27, 35],
        "partsabesrd2018rate": [2, 3, 4, 5],
    }
    df = pd.DataFrame(
        cars,
        columns=[
            "Brand",
            "Price",
            "ssacounty",
            "partsab5bonus2018rate",
            "partsab35bonus2018rate",
            "partsab0bonus2018rate",
            "partsabesrd2018rate",
        ],
    )
    df1 = countyrate_gateway.clean_ssa_fips_data(df)
    assert df1 is not None
    assert "partsab5bonus2018rate" not in df1.columns


def test_clean_csv_wrong_column():
    """Test CSV cleaning with bad column."""
    cars = {
        "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000],
        "ssacounty": ["12015", "22013", "32018", "42018"],
        "partsab5bonus2018rate": [2200, 2500, 2700, 3500],
        "partsab35bonus2018rate": [220, 250, 270, 350],
        "xxpartsab0bonus2018rate": [22, 25, 27, 35],
    }
    df = pd.DataFrame(
        cars,
        columns=[
            "Brand",
            "Price",
            "ssacounty",
            "partsab5bonus2018rate",
            "partsab35bonus2018rate",
            "xxpartsab0bonus2018rate",
        ],
    )
    df1 = countyrate_gateway.clean_ssa_fips_data(df)
    assert df1 is not None
    assert "partsab5bonus2018rate" not in df1.columns


def test_read_ssa_fips():
    """Test read_csv() on the happy path."""
    project_root = utils.get_project_root()
    file_path = project_root.joinpath("tests", "data", "test_ssa_fips_1.csv")
    print(file_path)
    required_columns = {"ssacounty", "rating", "year", "runtime"}
    df = countyrate_gateway.read_csv(file_path)
    assert not df.empty
    for column_name in required_columns:
        assert column_name in df.columns


def test_split_ssacnty_column():
    """Test split_ssacnty_column."""
    cars = {
        "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000],
        "ssastco": ["12015", "22013", "32018", "42018"],
    }
    df = pd.DataFrame(
        cars,
        columns=[
            "Brand",
            "Price",
            "ssastco",
        ],
    )
    df1 = countyrate_gateway.split_ssacnty_column(df)
    assert df1 is not None
    assert "ssacnty" in df1.columns
    assert "ssastco" in df1.columns


def test_rename_ssacounty_column():
    """Test rename_ssacounty_column."""
    cars = {
        "Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000],
        "ssacounty": ["12015", "22013", "32018", "42018"],
    }
    df = pd.DataFrame(
        cars,
        columns=[
            "Brand",
            "Price",
            "ssacounty",
        ],
    )
    df1 = countyrate_gateway.rename_ssacounty_column(df)
    assert df1 is not None
    assert "ssacounty" not in df1.columns
    assert "ssastco" in df1.columns


def test_get_countyrate_filepath():
    """Make sure it returns a filepath that is valid but may not exist."""
    file_path = countyrate_gateway.get_countyrate_filepath()
    assert file_path


def test_get_ssa_fips_cc_df():
    """Test get_ssa_fips_cc_df on the happy path with mock CSV."""

    def mock_countyrate_filepath():
        project_root = utils.get_project_root()
        file_path = project_root.joinpath("tests", "data", "test_ssa_fips_1.csv")
        return file_path

    Factory.register(InjectionKeys.COUNTYRATE_FILEPATH, mock_countyrate_filepath)

    required_columns = {"ssastco", "rating", "year", "runtime"}
    df = countyrate_gateway.get_ssa_fips_cc_df()
    assert not df.empty
    for column_name in required_columns:
        assert column_name in df.columns
