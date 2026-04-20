import sys
import os
import numpy as np
import random
from tqdm import tqdm

from namae import generate_names
from ninckname import generate_usernames
from amoosoo import generateMoney, generateRank, generateStartDate, generateLastVisitDate

"""
Generate player data for testing

# Player(id, name, nickname, rank, money, start_date, last_login)
# id: int pk auto_increment
# name: 한글 2-5글자
# nickname: 영문 32글자 이내, unique
# grank: 1 - 10, 정규분포로 1 쪽으로 갈수록 빈도가 높을 것
# money: $ 0.00- 99,999,999.99, 정규분포
# start_date: 최근 1년 이내의 날짜, 정규분포의 절반, 오래된 플레이어가 더 많을 것, yyyy-mm-dd 포맷
# last_login: start_date 보다 클 것, 최근 3개월 이내, 정규분포의 절반, 최근 플레이어가 더 많을 것, NUNLL 허용, yyyy-mm-dd hh:mm:ss 포맷
"""

np.random.seed(0)

CSV_DIR = os.path.join(os.path.dirname(__file__), "csv_files")
GUSER_CSV = os.path.join(CSV_DIR, "guser.csv")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen-player.py [numPlayers]")
        exit(1)
    else:
        import pandas as pd
        numPlayers = int(sys.argv[1])
        os.makedirs(CSV_DIR, exist_ok=True)

        steps = [
            ("이름 생성",       lambda: generate_names(numPlayers, include_compound_surname=True)),
            ("닉네임 생성",     lambda: generate_usernames(numPlayers, style="underscore", add_number=True, number_range=(0, 9999), max_length=32)),
            ("랭크 생성",       lambda: generateRank(numPlayers)),
            ("재화 생성",       lambda: generateMoney(numPlayers)),
            ("가입일 생성",     lambda: generateStartDate(numPlayers)),
            ("최근접속일 생성", lambda: generateLastVisitDate(numPlayers)),
        ]

        results = []
        for label, fn in tqdm(steps, desc="데이터 생성", unit="단계"):
            results.append(fn())
        names, nicknames, ranks, moneys, start_dates, last_visit_dates = results

        # DataFrame 생성
        df = pd.DataFrame({
            "id": np.arange(1, numPlayers + 1),
            "name": names,
            "nickname": nicknames,
            "rank": ranks,
            "money": moneys,
            "start_date": start_dates,
            "last_login": last_visit_dates
        })

        print(df.head())

        with tqdm(total=numPlayers, desc="CSV 저장", unit="rows") as pbar:
            df.to_csv(GUSER_CSV, index=False)
            pbar.update(numPlayers)

        size_mb = os.path.getsize(GUSER_CSV) / 1024 / 1024
        print(f"Generated {numPlayers:,} records → {GUSER_CSV} ({size_mb:.1f} MB)")
