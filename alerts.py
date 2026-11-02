def show(label, conf, row):
    if label == 0:
        print(f"[NORMAL] pps={row['pps']:.0f} confidence={conf:.2f}")
    else:
        print(f"[ALERT]  attack detected | pps={row['pps']:.0f} "
              f"unique_src={int(row['unique_src'])} confidence={conf:.2f}")
