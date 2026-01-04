import pandas as pd
from sklearn.cluster import KMeans

K = 4

def cluster_models():
    df = pd.read_csv("data/processed/rolling_mean_signal.csv")

    clusters = []

    for year, g in df.groupby("year"):
        pivot = g.pivot(index="ticker", columns="model", values="signal").dropna()

        km = KMeans(n_clusters=K, random_state=42)
        labels = km.fit_predict(pivot)

        out = pd.DataFrame({
            "ticker": pivot.index,
            "year": year,
            "cluster": labels
        })
        clusters.append(out)

    cluster_df = pd.concat(clusters, ignore_index=True)
    cluster_df.to_csv("data/processed/cluster_labels.csv", index=False)

if __name__ == "__main__":
    cluster_models()
