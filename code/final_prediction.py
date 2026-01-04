import pandas as pd
from scipy.stats import spearmanr

def final_prediction():
    signal = pd.read_csv("data/processed/rolling_mean_signal.csv")
    clusters = pd.read_csv("data/processed/cluster_labels.csv")
    weights = pd.read_csv("data/processed/cluster_model_weights.csv")
    returns = pd.read_csv("data/processed/realized_returns.csv", index_col=0)

    df = signal.merge(clusters, on=["ticker", "year"])
    df = df.merge(weights, on=["year", "cluster", "model"])

    df["weighted_signal"] = df["signal"] * df["weight"]

    final_er = (
        df.groupby(["ticker", "year"])["weighted_signal"]
        .sum()
        .reset_index(name="E_hat")
    )

    results = []

    for year, g in final_er.groupby("year"):
        realized = returns.loc[g["ticker"], str(year)]
        ic, _ = spearmanr(g["E_hat"], realized)

        top = realized.loc[g.nlargest(30, "E_hat")["ticker"]].mean()
        bottom = realized.loc[g.nsmallest(30, "E_hat")["ticker"]].mean()

        results.append({
            "test_year": year,
            "rank_ic": ic,
            "spread_30": top - bottom,
            "n_stocks": len(g)
        })

    pd.DataFrame(results).to_csv("reports/yearly_ic_summary.csv", index=False)
    final_er.to_csv("reports/final_predictions.csv", index=False)

if __name__ == "__main__":
    final_prediction()
