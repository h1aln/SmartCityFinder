
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def main():
    demo = pd.read_csv(DATA_DIR / "uscities_2020.csv")
    crime = pd.read_csv(DATA_DIR / "violent_crime_2020.csv")
    income = pd.read_csv(DATA_DIR / "income_2020.csv")

    # merge income into city demographics
    df = demo.merge(income, on=["city","state"], how="left")

    # merge state-level crime
    df = df.merge(crime, on="state", how="left")

    # derived metrics
    df["SafetyIndex"] = 1.0 / df["violent_crime_rate_2020"]
    df["AffordabilityIndex"] = df["median_household_income_2020"] / df["avg_income"]

    # normalize for parallel coordinates & scoring
    for col in ["SafetyIndex", "median_household_income_2020", "AffordabilityIndex"]:
        min_v = df[col].min()
        max_v = df[col].max()
        if max_v > min_v:
            df[col + "_norm"] = (df[col] - min_v) / (max_v - min_v)
        else:
            df[col + "_norm"] = 0.0

    # default livability score
    df["LivabilityScore"] = (
        0.4 * df["SafetyIndex_norm"] +
        0.3 * df["median_household_income_2020_norm"] +
        0.3 * df["AffordabilityIndex_norm"]
    )

    out_path = DATA_DIR / "merged_smartcity.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved merged data to {out_path}")

if __name__ == "__main__":
    main()
