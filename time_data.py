# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:47:54 2021

@author: Playdata

시계열 데이터 다루기

야후증권 데이터 : yfinance
야후증권데이터 다루기 위한 pandas_datareader
"""
# 모듈 import

# pip install pandas_datareader
from pandas_datareader import data

# pip install yfinance
import yfinance as yf

# 오픈소스인 야후증권을 통한 시계열 데이터 
'''
시계열 데이터 : 시간의 흐름에 따른 데이터
주의 : 주기가 필요..
'''

### 야후증권 데이터 요청
# 1. 야후증권 데이터사용을 위한 허가
yf.pdr_override()

# 2. 증권 데이터 요청시 필요한 자원
'''
1. 종목코드    : KIA(종목명) / '000270.KS' (종목코드)
2. 요청 시작일 : '2021-1-1'
2. 요청 종료일 : '2021-12-10'
'''

start_date = '2017-1-1'
end_date = '2017-6-30'

# 3. 증권데이터 요청 : pandas_datareader.get_data_yahoo('종목코드', '시작일', '종료일')
KIA = data.get_data_yahoo('000270.KS', start_date, end_date)
'''
               Open     High      Low    Close     Adj Close   Volume
Date                                                                 
2017-01-02  39000.0  39600.0  38850.0  39500.0  35970.968750   436193
2017-01-03  39650.0  40900.0  39650.0  40750.0  37109.289062  1158874
2017-01-04  40900.0  41450.0  40550.0  41300.0  37610.148438  1159086
2017-01-05  41300.0  41350.0  40750.0  41100.0  37428.019531  1116473
2017-01-06  40700.0  40850.0  40550.0  40750.0  37109.289062   888652
            ...      ...      ...      ...           ...      ...
2017-06-23  38500.0  38950.0  38450.0  38850.0  35379.039062   694185
2017-06-26  38800.0  39000.0  38450.0  38650.0  35196.906250   439880
2017-06-27  38550.0  38550.0  37850.0  38000.0  34604.980469   896530
2017-06-28  38000.0  38300.0  37600.0  37850.0  34468.382812   749536
2017-06-29  38000.0  38450.0  37800.0  38150.0  34741.578125   491434

[121 rows x 6 columns]
Open : 장 시작가격
High : 장중 상한가
Low  : 장중 하한가
Close: 장 마감가격
'''

KIA['Close'].plot(figsize=(12,6), grid=True)

type(KIA)  # pandas.core.frame.DataFrame

KIA_trunc = KIA[ :'2017-4-30']


#### 웹 트래픽 : 08. PinkWink Web Traffic.csv
import pandas as pd
web = pd.read_csv("./data2/08. PinkWink Web Traffic.csv",
                  encoding='utf-8',
                  thousands=',',
                  names=['data', 'hit'],
                  index_col=0)

web_not_null = web[web['hit'].notnull()]

web_not_null['hit'].plot(figsize=(12, 6), grid=True)

### Numpy의 ployfit을 이용한 회귀분석
## 주기성파악

import numpy as np
# 1. 시간축 설정
time = np.arange(0, len(web_not_null))
'''
array([  0,  ~~~~  364])
'''

# 2. 웹 트래픽 데이터 추출
traffic = web_not_null['hit'].values
'''
array([ 766.,  ~~~~ 1193.])
'''

# 3. 추출된 데이터를 이용하여 간단한 모델작성
'''
회귀 : 데이터가 주기성을이용하여 한바퀴돌고, 제자리로 오는 ..
모델 : 1차, 2차, 3차, 15차등 다항식으로 표현하고 그 결과 값을 이용하여 결정
다항식 : 1개 이상의 단항식을 대수의 합으로 연결한 식 
단항식 : 숫자 또는 몇 개의 문자의 곱으로 이루어진 식.
'''

# 모델의 작합성 확인을 위한 사용자 정의 함수
fx = np.linspace(0, time[-1], 1000)
'''
array([  0.        ,   0.36436436,   ~~~  363.63563564, 364.        ])
'''

def error(f, x, y):
    return np.sqrt(np.mean((f(x)-y)**2))

# 1차 다항식
fp1 = np.polyfit(time, traffic, 1)
'''
array([  2.94751137, 678.39950595])
'''
f1 = np.poly1d(fp1)
'''
poly1d([  2.94751137, 678.39950595])
'''

# 2차 다항식
fp2 = np.polyfit(time, traffic, 2)
'''
array([-1.42164283e-03,  3.46498936e+00,  6.47092087e+02])
'''

f2 = np.poly1d(fp2)
'''
poly1d([-1.42164283e-03,  3.46498936e+00,  6.47092087e+02])
'''


# 3차 다항식
fp3 = np.polyfit(time, traffic, 3)
'''
array([ 3.34072153e-05, -1.96619824e-02,  6.11714142e+00,  5.67195752e+02])
'''
f3 = np.poly1d(fp3)
'''
poly1d([ 3.34072153e-05, -1.96619824e-02,  6.11714142e+00,  5.67195752e+02])
'''


# 15차 다항식
fp15 = np.polyfit(time, traffic, 15)
'''
array([ 2.37543221e-29, -6.18482109e-26,  7.30047131e-23, -5.16076797e-20,
        2.42917128e-17, -8.00158814e-15,  1.88603602e-12, -3.19726003e-10,
        3.86603336e-08, -3.26709727e-06,  1.87092568e-04, -7.04462601e-03,
        1.76801543e-01, -3.15303097e+00,  3.27803683e+01,  6.17394693e+02])
'''

f15 = np.poly1d(fp15)
'''
poly1d([ 2.37543221e-29, -6.18482109e-26,  7.30047131e-23, -5.16076797e-20,
        2.42917128e-17, -8.00158814e-15,  1.88603602e-12, -3.19726003e-10,
        3.86603336e-08, -3.26709727e-06,  1.87092568e-04, -7.04462601e-03,
        1.76801543e-01, -3.15303097e+00,  3.27803683e+01,  6.17394693e+02])
'''

print(error(f1, time, traffic))
print(error(f2, time, traffic))
print(error(f3, time, traffic))
print(error(f15, time, traffic))
'''
430.85973081109626
430.6284101894695
429.53280466762925
330.4777304274343
'''

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.scatter(time, traffic, s=10)

plt.plot(fx, f1(fx), lw=4, label='f1')
plt.plot(fx, f2(fx), lw=4, label='f2')
plt.plot(fx, f3(fx), lw=4, label='f3')
plt.plot(fx, f15(fx), lw=4, label='f15')

plt.legend(loc=2)
plt.show()

"""
1차, 2차, 3차 별차이가 없기 때문에 1차를 사용
15차의 경우에는 과적합(over=fitting)일 가능성이 높기 때문에,
모델로는 부적합
"""

### 과적합(over=fitting) 이란
'''
기계학습에서 학습 데이터를 과하게 학습하는 것을 의미

일반적으로 학습데이터는
실제 데이터의 일부이기 때문에, 학습데이터에 대하여 오차가 감소할 수 있지만,

실제 데이터에 대해서는 오차가 증가할 수 있다.


학습 데이터는 실제데이터의 일부분이기 때문에
실제 데이터를 모두 수집하기 어렵고, 
실제 데이터를 수집한다하더라도
모든 데이터를 학습시키기위한 시간이 측정 불가능한 수중으로 증가할 수 있다..

따라서 학습 데이터만 가지고는 
실제 데이터의 오차가 증가하는 시점을 예측하는 것은 매우 어렵다..
'''


"""
시계열 데이터 
=> 시간의 흐름에 따라 변화하는 추이가 있는 데이터
=> 주기성

시계열 데이터 분석
1. 원래 데이터의 안정성을 판단
2. 안정된 형태로 변환
3. 예측 모델의 선정 및 검증

참고 : 페이스북(메타)에서 개바발하여 배포된 모듈
 => fbprophet 모듈
 => 시계열 데이터를 분석 예측하기 위한 모듈.
"""


### 자연어 처리 ###
### 웹 페이지를 읽어 분석하는 크롤링(스크래핑) ###


'''
Python 팀 프로젝트 명단 
(명단은 가나다순으로 입력되어 있습니다)					
1 조	강재균	김기환	이성찬	정훈오	
2 조	권기철	김치우	서두현	조용기	주현준

4 조	김종성	이예지	신우주	전재연
5 조	김지영	남지희	정광수	정치영	


Python 팀 프로젝트 주제 :
Python을 이용한 작업이면 어떤 것이든 무관
예) Python을 이용한 웹 (배포해드렸던 640 page 를 이용 가능)
    Python을 이용한 분석 (이번주까지 분석한 내용 이용 가능)
    Python을 이용한 웹 및 분석 

Python 팀 프로젝트 발표 : 2021.12. 30
'''
"""
회의시간 : 
이번 주 : 7,8교시
다음 주 : 아직 미정(요청사항이 있을 경우, 오후 4교시 예)
마지막 주 : 1~8교시
"""












































