import pandas as pd
from scipy.stats import spearmanr

def cluster_ic_weighting():
    signal = pd.read_csv("data/processed/rolling_mean_signal.csv")
    clusters = pd.read_csv("data/processed/cluster_labels.csv")
    returns = pd.read_csv("data/processed/realized_returns.csv", index_col=0)

    df = signal.merge(clusters, on=["ticker", "year"])

    ic_records = []

    for (year, cluster, model), g in df.groupby(["year", "cluster", "model"]):
        tickers = g["ticker"]
        if str(year) not in returns.columns:
            continue

        realized = returns.loc[tickers, str(year)]
        ic, _ = spearmanr(g["signal"], realized)

        ic_records.append({
            "year": year,
            "cluster": cluster,
            "model": model,
            "rank_ic": ic
        })

    ic_df = pd.DataFrame(ic_records)
    ic_df.to_csv("data/processed/cluster_model_ic.csv", index=False)

    # IC → weights
    weights = ic_df.copy()
    weights["weight"] = (
        weights.groupby(["year", "cluster"])["rank_ic"]
        .transform(lambda x: x / x.abs().sum())
    )

    weights.to_csv("data/processed/cluster_model_weights.csv", index=False)

if __name__ == "__main__":
    cluster_ic_weighting()
