import sys
import os
import numpy as np
from tqdm import tqdm
from ninckname import generate_items

'''
create table trade (
    id int primary key auto_increment,
    seller int,
    item_name varchar(255),
    price dec(7, 0),
    trade_date date,
    foreign key (seller) references guser(id)
) character set utf8mb4;
'''

CSV_DIR   = os.path.join(os.path.dirname(__file__), "csv_files")
GUSER_CSV = os.path.join(CSV_DIR, "guser.csv")
TRADE_CSV = os.path.join(CSV_DIR, "trade.csv")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <numTrades>")
        sys.exit(1)

    size = int(sys.argv[1])

    # guser.csv 행수로 유저 수 결정
    import pandas as pd
    with tqdm(total=1, desc="guser.csv 읽기", unit="파일") as pbar:
        usize = sum(1 for _ in open(GUSER_CSV)) - 1  # 헤더 제외
        pbar.update(1)
    print(f"  → 유저 수: {usize:,}명")

    steps = [
        ("아이템 생성",   lambda: generate_items(size)),
        ("판매자 생성",   lambda: np.random.randint(1, usize + 1, size)),
        ("가격 생성",     lambda: (np.random.randint(0, 1000, size) * 100)),
        ("거래일자 생성", lambda: (
            (pd.Timestamp.now() - pd.to_timedelta(np.random.randint(0, 366, size), unit="D"))
            .strftime("%Y-%m-%d").tolist()
        )),
    ]

    results = []
    for label, fn in tqdm(steps, desc="데이터 생성", unit="단계"):
        results.append(fn())
    items, uids, prices, trade_dates = results

    df = pd.DataFrame({
        "id":         np.arange(1, size + 1),
        "seller":     uids,
        "item_name":  items,
        "price":      prices,
        "trade_date": trade_dates,
    })

    print(df.head())

    os.makedirs(CSV_DIR, exist_ok=True)
    with tqdm(total=size, desc="CSV 저장", unit="rows") as pbar:
        df.to_csv(TRADE_CSV, index=False)
        pbar.update(size)

    size_mb = os.path.getsize(TRADE_CSV) / 1024 / 1024
    print(f"Generated {size:,} records → {TRADE_CSV} ({size_mb:.1f} MB)")
