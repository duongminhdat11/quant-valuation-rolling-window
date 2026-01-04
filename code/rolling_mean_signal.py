import pandas as pd

MODELS = ["pe", "pe1", "pb", "ps", "dcf", "re"]
WINDOW = 3

def rolling_mean_signal():
    signals = []

    for model in MODELS:
        df = pd.read_csv(f"data/processed/{model}.csv", index_col=0)

        for year in df.columns[WINDOW:]:
            past_years = df.columns[df.columns.get_loc(year)-WINDOW:df.columns.get_loc(year)]
            mean_er = df[past_years].mean(axis=1)

            tmp = pd.DataFrame({
                "ticker": mean_er.index,
                "year": int(year),
                "model": model,
                "signal": mean_er.values
            })
            signals.append(tmp)

    signal_df = pd.concat(signals, ignore_index=True)
    signal_df.to_csv("data/processed/rolling_mean_signal.csv", index=False)

if __name__ == "__main__":
    rolling_mean_signal()
