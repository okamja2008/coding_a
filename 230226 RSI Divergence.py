import numpy
import matplotlib.pyplot as plt
import pyupbit
import pandas as pd
import time
import pprint

coin_list = pyupbit.get_tickers(fiat='KRW')
except_symbol = ['KRW-BTT', 'KRW-SHIB', 'KRW-XEC', 'DOGE/KRW', 'COR/KRW']
coin_list= [coin for coin in coin_list if coin not in except_symbol]

# 나중에 while문 돌릴 때, 전체 ticker 대상으로 돌리기

#코인별 5분봉 기준 데이터 베이스 생성
def ticker_db(ticker):
    data = pyupbit.get_ohlcv(ticker, interval = "minute5", count=200)
    return data

#코인별 60분봉 기준 거래량 확인
def ticker_volume(ticker):
    data_volume = pyupbit.get_ohlcv(ticker, interval = "minute60", count=24)
    return data_volume['value'].sum()

#급등주 확인
def ticker_rise(ticker):
    data_rise = pyupbit.get_ohlcv(ticker, interval = "minute1", count=200)
    return data_rise


#Fast %K = ((현재가 - n기간 중 최저가) / (n기간 중 최저가 - n기간 중 최저가)) * 100

def sto_fast_k(close_price, low, high, n):
    fast_k = ((close_price - low.rolling(n).min()) / (high.rolling(n).max() - low.rolling(n).min()))*100
    return fast_k

# Slow %K = Fast %K의 n기간 이동평균 (SMA)

def sto_slow_k(fast_k, n):
    slow_k = fast_k.rolling(n).mean()
    return slow_k

# Slow %D = Slow %K의 t기간 이동평균 (SMA)

def sto_slow_d(slow_k, t):
    slow_d = slow_k.rolling(t).mean()
    return slow_d


# 잔고 조회 함수
def get_balance(ticker):
    coin_balance = upbit.get_balance(ticker)
    return coin_balance

# 매수 평균가
def average_price(ticker):
    return upbit.get_avg_buy_price(ticker)

# 현재가격
def current_price(ticker):
    return pyupbit.get_current_price(ticker)

# 최대 구매 가능 수량
def max_amount(ticker):
    amount_get = (get_balance('KRW')*0.9995) / ticker_db(ticker)['low'][-1]
    return amount_get

# RSI 함수
def rsi(ticker, n=14):
    data_rsi = pyupbit.get_ohlcv(ticker, interval = "minute5", count=200)
    delta = data_rsi["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = n-1, min_periods = n).mean()
    AD = downs.abs().ewm(com = n-1, min_periods = n).mean()
    RS = AU/AD

    return pd.Series(100 - (100/(1 + RS)), name = "RSI")  


access = "xI8XzTKPlr6AnMIewo6HMlO4H1l1bPLDxcS09vub"
secret = "jCTVIdgTSPlOL1aGx5x5uGwTm0oOGS3PevzyPQOH"

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 코인해우소 
while True:
    try:
        for ticker in coin_list:
            data_base = ticker_db(ticker)
            data_rise = ticker_rise(ticker)
            data_base['fast_k'] = sto_fast_k(data_base['close'], data_base['low'], data_base['high'], 5)
            data_base['slow_k'] = sto_slow_k(data_base['fast_k'], 3)
            data_base['slow_d'] = sto_slow_d(data_base['slow_k'], 3)
            data_base['rsi'] = rsi(ticker,5)
            first_k = data_base['slow_k'][-1]
            first_d = data_base['slow_d'][-1]
            second_k = data_base['slow_k'][-2]
            second_d = data_base['slow_d'][-2]
            third_k = data_base['slow_k'][-3]
            third_d = data_base['slow_d'][-3]
            rsi_first = data_base['rsi'][-1]
            rsi_second = data_base['rsi'][-2]
            coin = get_balance(ticker)
        # 임시 다이버전스 구현해보기
    
            #만약에 K값이 18보다 작고, D값이 25보다 작으며, 1분전 k가 d보다 크고, 현재 RSI가 20보다 작을 시 만원 매수, 만원보다 적으면 최대 금액 매수
            if first_k < second_k and first_k < 25 and rsi_second < 25 and rsi_first < 20 and rsi_first < rsi_second and ticker_volume(ticker)>10000000000 :
                krw = get_balance("KRW")
                if krw > 10000:
                    upbit.buy_market_order(ticker, 10000)
                if krw < 10000 and krw > 5000:
                    upbit.buy_market_order(ticker,krw*0.9995)
                elif krw < 5000:
                    continue
            
            # 급등주도 매입
            elif current_price(ticker) > data_rise['low'][-1]*1.025:
                upbit.buy_market_order(ticker, krw*0.9995)
                if krw < 5000:
                    continue

            # 만약에 현재가가 매수 평균가보다 1% 수익일 때, 전량 매도한다

            elif rsi_first > 75 and current_price(ticker)> (average_price(ticker)*1.0055) or current_price(ticker)> (average_price(ticker)*1.0505):
                upbit.sell_market_order(ticker, coin)

            elif current_price(ticker) < average_price(ticker) * 0.98:
                upbit.buy_market_order(ticker,10000)
                if krw < 10000:
                    upbit.buy_market_order(ticker, 5000)
                else:
                    continue
            # 만약에 현재가격이 매수가 대비 5% 감소 시, 전량 매도 
            elif current_price(ticker) < (average_price(ticker)*0.95):
                upbit.sell_market_order(ticker, coin)
            else:
                continue
            time.sleep(0.1)

    except Exception as e:
        print(e)
        time.sleep(0.1)


# except KeyboarrdInterrupt:
# print('시세조회 초과')

    # upbit.buy_limit_order(ticker, data_base['low'][-1], max_amount(ticker)-1