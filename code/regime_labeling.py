import pandas as pd

def regime_labeling():
    ic = pd.read_csv("data/processed/cluster_model_ic.csv")
    yearly_ic = pd.read_csv("reports/yearly_ic_summary.csv")

    records = []

    for (year, cluster), g in ic.groupby(["year", "cluster"]):
        v_models = g["rank_ic"]
        final_ic = yearly_ic.loc[yearly_ic["test_year"] == year, "rank_ic"].values[0]

        if (v_models < 0).all():
            regime = 4
        elif (v_models > 0).sum() >= 3 and final_ic > 0:
            regime = 3
        elif (v_models > 0).sum() < 2 and final_ic > 0:
            regime = 2
        else:
            regime = 1

        records.append({
            "year": year,
            "cluster": cluster,
            "regime": regime
        })

    pd.DataFrame(records).to_csv("reports/cluster_regimes.csv", index=False)

if __name__ == "__main__":
    regime_labeling()
