import numpy
import matplotlib.pyplot as plt
import pyupbit
import pandas as pd
import time
import pprint

coin_list = pyupbit.get_tickers(fiat='KRW')
excep\

    
            #만약에 K값이 18보다 작고, D값이 25보다 작으며, 1분전 k가 d보다 크고, 현재 RSI가 20보다 작을 시 만원 매수, 만원보다 적으면 최대 금액 매수
            if first_k < 18 and first_d < 25 and second_k < second_d and first_k < first_d and rsi_first < 21 :
                krw = get_balance("KRW")
                if krw > 10000:
                    upbit.buy_market_order(ticker, 10000)
                elif krw < 10000 and krw > 5000:
                    upbit.buy_market_order(ticker,krw*0.9995)
                elif krw < 5000:
                    continue
            
            # 급등주도 매입
            elif current_price(ticker) > data_base['open'][-1]*1.025:
                upbit.buy_market_order(ticker, 10000)
                if krw < 10000:
                    continue

            # 만약에 현재가가 매수 평균가보다 1% 수익일 때, 전량 매도한다

            elif rsi_first > 70 and current_price(ticker)> (average_price(ticker)*1.0105) or current_price(ticker)> (average_price(ticker)*1.0155):
                upbit.sell_market_order(ticker, coin)

            # 만약에 현재가격이 매수가 대비 1% 감소 시, 전량 매도 
            elif current_price(ticker) < (average_price(ticker)*0.992):
                upbit.sell_market_order(ticker, coin)
            else:
                continue
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(0.5)


# except KeyboarrdInterrupt:
# print('시세조회 초과')

    # upbit.buy_limit_order(ticker, data_base['low'][-1], max_amount(ticker)-1
