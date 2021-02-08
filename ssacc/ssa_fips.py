"""Read and clean SSA and FIPS county codes."""
import pandas as pd
from pandas.io.parsers import ParserError

from ssacc.clean_df import CleanDF
from ssacc.wrappers.timing_wrapper import timing


class SsaFips:

    """Read and clean SSA and FIPS county codes."""

    @staticmethod
    @timing
    def read_ssa_fips(input_file_path):
        """Return clean SSA and FIPS county codes in a dataframe."""
        df = SsaFips.read_csv(input_file_path)
        df1 = SsaFips.clean_ssa_fips_data(df)
        print(df1.head())
        return df1

    @staticmethod
    def read_csv(input_file_path):
        """Read data from CSV file."""
        try:
            df = pd.read_csv(filepath_or_buffer=input_file_path, header=0, dtype=str)
            return df
        except FileNotFoundError:
            print(f"File {input_file_path} not found")
        except ParserError:
            print(f"Parser error {input_file_path} ")
        except Exception:
            print(f"Any other error reading {input_file_path}")
        return None

    @staticmethod
    @timing
    def clean_ssa_fips_data(df):
        """ Clean up SSA FIPS county code data."""
        df = CleanDF.drop_columns(
            df,
            [
                "partsab5bonus2018rate",
                "partsab35bonus2018rate",
                "partsab0bonus2018rate",
                "partsabesrd2018rate",
            ],
        )
        # change misleading name
        df = CleanDF.rename_columns(df, ["ssacounty"], ["ssastco"])  # SSA STate COunty
        # add column ssacnty with 3 digit SSA county code: strip off state code from ssastco
        df["ssacnty"] = df["ssastco"].str[2:]
        print(df.head())
        return df
