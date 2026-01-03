import pandas as pd
from scipy.stats import spearmanr

MODELS = ["pe", "pb", "ps", "dcf", "re", "pe1"]

def compute_rank_ic():
    returns = pd.read_csv("data/processed/realized_returns.csv", index_col=0)

    records = []

    for model in MODELS:
        df = pd.read_csv(f"data/processed/{model}.csv", index_col=0)

        for year in df.columns:
            if year not in returns.columns:
                continue

            x = df[year]
            y = returns[year]

            common = x.index.intersection(y.index)
            ic, _ = spearmanr(x.loc[common], y.loc[common])

            records.append({
                "year": int(year),
                "model": model,
                "rank_ic": ic
            })

    ic_df = pd.DataFrame(records)
    ic_df.to_csv("data/processed/rank_ic.csv", index=False)

if __name__ == "__main__":
    compute_rank_ic()
