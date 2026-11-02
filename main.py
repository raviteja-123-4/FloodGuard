import pandas as pd
from detect import load, predict, FEATURES
from alerts import show
from respond import block

model = load()
df = pd.read_csv("data/dataset.csv")

# oka normal row, oka attack row teesukundam
samples = [df[df["label"] == 0].iloc[0], df[df["label"] == 1].iloc[0]]

for s in samples:
    row = s[FEATURES].to_dict()
    label, conf = predict(model, row)
    show(label, conf, row)
    if label == 1:
        block(row)
