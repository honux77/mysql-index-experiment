import numpy as np
import pandas as pd

def generateMoney(numPlayers):
    # global variables and Constants
    MAX_MONEY = 9_999_900
    MIN_MONEY = 0
    STEP = 100
# 정규분포 설정
    mean = (MAX_MONEY - MIN_MONEY) / 2     # 중앙값을 평균으로
    std_dev = mean / 6  # 대략 ±3σ가 전체 범위가 되도록 설정
    # 정규분포로 난수 생성
    money_values = np.random.normal(loc=mean, scale=std_dev, size=numPlayers)

    # 범위를 벗어나는 값들을 잘라내기 (클리핑)
    money_values = np.clip(money_values, MIN_MONEY, MAX_MONEY)

    # 100원 단위로 반올림
    money_values = (np.round(money_values / STEP) * STEP).astype(int)
    return money_values

def generateRank(numPlayers):
    # game rank, B, S, G, P, D, C. B가 가장 빈도가 높고, C가 가장 낮음
    # B = 50%, S = 25%, G = 15%, P = 5%, D = 3%, C = 2%
    ranks = ["B", "S", "G", "P", "D", "C"]
    rank_values = np.random.choice(ranks, size=numPlayers, p=[0.5, 0.25, 0.15, 0.05, 0.03, 0.02])
    return rank_values


def generateStartDate(numPlayers):
    # start_date: 최근 1년 이내의 날짜, 정규분포, yyyy-mm-dd 포맷
    days = np.clip(np.random.normal(loc=180, scale=30, size=numPlayers), 0, 365)
    dates = pd.Timestamp.now() - pd.to_timedelta(days, unit="D")
    return pd.DatetimeIndex(dates).strftime("%Y-%m-%d").tolist()

def generateLastVisitDate(numPlayers):
    # last_visit: 최근 3개월 이내의 날짜, 감마분포, 최근으로 올수록 빈도가 높아야 함
    days = np.clip(np.random.gamma(2.0, 15.0, numPlayers), 0, 90)
    dates = pd.Timestamp.now() - pd.to_timedelta(days, unit="D")
    return pd.DatetimeIndex(dates).strftime("%Y-%m-%d %H:%M:%S").tolist()

if __name__ == "__main__":
    # 테스트
    print(generateMoney(10))
    print(generateRank(10))
    print(generateStartDate(10))
    print(generateLastVisitDate(10))