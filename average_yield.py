#!/usr/bin/env python3

import pandas as pd
import os
import sys

SIMULATIONS = [
    "WE38-1",
    "WE38-2",
    "WE38-3",
    "WE38-4",
]
CROP = "CornRM.90"
OUTPUT_FILE = "Cycles.txt"

def read_season(simulation):
    '''Read season output file for harvested crop, harvest time, plant time, and yield
    '''
    fn = f"output/{simulation}/season.dat"

    if not os.path.exists(fn):
        print("%s season output file (%s) does not exist." % (simulation, file_name))
        sys.exit(0)

    df = pd.read_csv(
        fn,
        sep="\t",
        header=0,
        skiprows=[1],
        skipinitialspace=True,
    )

    df = df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"))

    df["crop"] = df["crop"].str.strip()

    return df


def main():
    df = []
    for s in SIMULATIONS:
        _df = read_season(s)
        _df["year"] = _df["date"].str[0:4]
        _df = _df[_df["crop"] == CROP]
        df.append(_df)

    df = pd.concat(df)
    exdf = df.groupby("year").mean()
    exdf.to_csv(OUTPUT_FILE)


if __name__ == "__main__":
    main()
