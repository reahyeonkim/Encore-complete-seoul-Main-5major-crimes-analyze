# -*- coding: utf-8 -*-
"""
1.  

    모든 범죄가 아닌  중요 범죄만 분석 : 
        '강간검거율', '강도검거율', '살인검거율', '절도검거율', '폭력검거율'
    
    아래 파일을 이용하여 CCTV 갯수와 범죄 발생건수 및 인구수 에 대한 상관관계 분석    
        01. CCTV_result.csv / 
        02. crime_in_Seoul.csv / 02. crime_in_Seoul_include_gu_name.csv / 
        02. skorea_municipalities_geo_simple.json

    결과의 예 
    CCTV 갯수와 범죄 발생건수 / 범죄 발생건수 및 인구수 / CCTV 갯수와 인구수 상관관계 시각화
    CCTV 갯수와 범죄 발생건수 및 인구수 에 대한 상관관계 시각화
    범죄율에 대한 지도 시각화
    경찰서별 검거현황과 구별 범죄발생 현황을 시각화

2. 시계열 데이터 분석에 대하여 진행합니다..
"""
### 모듈 import
import numpy as np
import pandas as pd
import googlemaps

### 데이터 정리
## 데이터 로드 : 02. crime_in_Seoul.csv
'''
02. crime_in_Seoul.csv  파일 분석
1. 데이터내에 천단위 콤마(,) 
2. 한글 Encodiing :  euc-kr 
'''

crime_anal_police = pd.read_csv("./data/02. crime_in_Seoul.csv",
                                thousands=",",
                                encoding="euc-kr")


## 구글맵으로부터 경찰서 위치(위도/경도) 정보 요청
# 구글맵 APIkey 등록
gmaps_key = "AIzaSyC-ezB2J00Td105d4jqtdi2-JmZKuZ-5lY "
gmaps = googlemaps.Client(gmaps_key)

gmaps.geocode("서울중부경찰서", language="ko")
'''
[{'address_components': [{'long_name': '２７',
    'short_name': '２７',
    'types': ['premise']},
   {'long_name': '수표로',
    'short_name': '수표로',
    'types': ['political', 'sublocality', 'sublocality_level_4']},
   {'long_name': '을지로동',
    'short_name': '을지로동',
    'types': ['political', 'sublocality', 'sublocality_level_2']},
   {'long_name': '중구',
    'short_name': '중구',
    'types': ['political', 'sublocality', 'sublocality_level_1']},
   {'long_name': '서울특별시',
    'short_name': '서울특별시',
    'types': ['administrative_area_level_1', 'political']},
   {'long_name': '대한민국',
    'short_name': 'KR',
    'types': ['country', 'political']},
   {'long_name': '100-032',
    'short_name': '100-032',
    'types': ['postal_code']}],
  'formatted_address': '대한민국 서울특별시 중구 을지로동 수표로 27',
  'geometry': {'location': {'lat': 37.5636465, 'lng': 126.9895796},
   'location_type': 'ROOFTOP',
   'viewport': {'northeast': {'lat': 37.56499548029149,
     'lng': 126.9909285802915},
    'southwest': {'lat': 37.56229751970849, 'lng': 126.9882306197085}}},
  'place_id': 'ChIJc-9q5uSifDURLhQmr5wkXmc',
  'plus_code': {'compound_code': 'HX7Q+FR 대한민국 서울특별시',
   'global_code': '8Q98HX7Q+FR'},
  'types': ['establishment', 'point_of_interest', 'police']}]
'''

"""
구글맵으로 부터 관서명에 대한 위치를 얻기 위해서는
기존 "관서명" 컬럼의 데이터에 대한 정리가 필요.
중부서  =>  서울중부경찰서 로 변경이 필요~~
"""
## 관서명 데이터 정리
station_name = []     # 정리된 관서명 저장

for name in crime_anal_police['관서명'] :
    station_name.append('서울' + str(name[: -1])+'경찰서')



### 서울시 경찰서의 주소, 위치 저장
station_address = []    # 서울시 경찰서의 주소 ('formatted_address')

# 구글맵이 응답한 데이터 중, 'geometry': {'location': {'lat': 37.5636465, 'lng': 126.9895796},
station_lat = []        # 'lat': 37.5636465
station_lng = []        # 'lng': 126.9895796

for name in station_name :
    tmp= gmaps.geocode(name, language='ko')   # [{'address_ ~~~~ 'police']}]
    station_address.append(tmp[0].get('formatted_address'))
    
    tmp_loc = tmp[0].get('geometry')    # {'location': {'lat': 37.5636465, 'lng': 126.9895796},
    
    station_lat.append(tmp_loc['location']['lat'])
    station_lng.append(tmp_loc['location']['lng'])
    
    # 바로 확인 (테스트용)
    print(name + "====> " + tmp[0].get('formatted_address'))


### 경찰서 주소중, '구' 부분만 추출하여 별도의 리스트에 저장
'''
'대한민국 서울특별시 중구 을지로동 수표로 27'   => '중구'

행정 구역이 변경된 경찰서가 있는 지 확인.

동일한 구내에 두 개 이상의 경찰서가 존재하는 지 확인, (존재시 주 경찰서의 데이터 합)
'''
# '대한민국 서울특별시 중구 을지로동 수표로 27'   => '중구'  : split()
gu_name =[]   # 구이름만 저장

for name in station_address:
    tmp = name.split()  
    '''
    '대한민국 서울특별시 중구 을지로동 수표로 27'   
    => '대한민국' '서울특별시' '중구' '을지로동'  '수표로'  '27'
    '''
    tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
    
    gu_name.append(tmp_gu)

    
# 추출된 구이름(gu_name)을 전체 데이터프레임(crime_anal_police)에 추가
crime_anal_police['구별'] = gu_name

# 만약 금천서가 금천구가 아닌 관악구(양천구)로 되어 있을 경우,
# 금천서의 구를 금천구로 변경...
crime_anal_police[crime_anal_police['관서명'] == '금천서', ['구별']] ='금천구'
# 와 같이 수작업으로 변경..



### 02. crime_in_Seoul_include_gu_name.csv
crime_anal_raw = pd.read_csv("./data/02. crime_in_Seoul_include_gu_name.csv",
                             encoding="utf-8",
                             index_col = 0)


## 1. pivot_table()을 이용하여 '관서별' => '구별' 
## 2. pivot_table()의 aggfunc=np.sum 을 설절하여 동일구내의 경찰서 데이터를 합하기
crime_anal = pd.pivot_table(crime_anal_raw, index='구별', aggfunc=np.sum)

# 5대 중요 범죄에 대한 검거율을 계산하여 crime_anal에 추가
crime_anal['강간검거율'] = crime_anal['강간 검거'] / crime_anal['강간 발생'] * 100
crime_anal['강도검거율'] = crime_anal['강도 검거'] / crime_anal['강도 발생'] * 100
crime_anal['살인검거율'] = crime_anal['살인 검거'] / crime_anal['살인 발생'] * 100
crime_anal['절도검거율'] = crime_anal['절도 검거'] / crime_anal['절도 발생'] * 100
crime_anal['폭력검거율'] = crime_anal['폭력 검거'] / crime_anal['폭력 발생'] * 100


#### 데이터 스케이링 작업 : 검거율이 100을 넘는 데이터는 100으로 변경..
col_list = ['강간검거율', '강도검거율', '살인검거율', '절도검거율', '폭력검거율' ]

for colum in col_list:
    crime_anal.loc[crime_anal[colum] > 100, colum] = 100
    
crime_anal.head()
crime_anal.tail()


## 컬럼명 변경 : "강간 발생"  => " 발생" 부분을 삭제 => "강간" : DataFrame.rename('변경전' : '변경후')

crime_anal.rename(columns={'강간 발생':'강간',
                           '강도 발생':'강도',
                           '살인 발생':'살인',
                           '절도 발생':'절도',
                           '폭력 발생':'폭력'}, inplace=True)

### 비교할 데이터의 크기가 아주 심할 경우(범위가 넓을 경우), 최소값과 최대값에 대한 비율 전처리.
### MinMaxScalar 방법을 적용
# 데이터 스케일링을 위한 모듈 impport : sklearn의 preprocessing
from sklearn import preprocessing

# preprocessing 의 클래스 중 MinMaxScalar 를 이용하여 전처리(데이터 스케일링)

# 1. 전처리할 데이터 설정을 위한 컬럼 추출
col = ['강간', '강도', '살인', '절도', '폭력']

# 2. 각 컬럼의 데이터를 추출
x = crime_anal[col].values

# 3. MinMaxScalar 객체 생성
min_max_scaler = preprocessing.MinMaxScaler()

# 4. MinMaxScaler 객체에 스케일링할 데이터를 전달
x_scaled = min_max_scaler.fit_transform(x.astype(float))

# 5. 결과 데이터를 데이터프레임에 저장
crime_anal_norm = pd.DataFrame(x_scaled, columns=col, index=crime_anal.index)


## crime_anal_norm 에 검거율 추가
col2 = ['강간검거율', '강도검거율', '살인검거율', '절도검거율', '폭력검거율']

crime_anal_norm[col2] = crime_anal[col2]

"""
현재까지의 작업 내용
1. 경찰서 위치 : 구글맵게게 요청하여 데이터 정리
2. 범죄 데이터 :분석 및 시각화를 위한 데이터 정리
"""

### CCTV 데이터 로드 : 01. CCTV_result.csv
result_CCTV = pd.read_csv("./data/01. CCTV_result.csv",
                          encoding="utf-8",
                          index_col='구별')


crime_anal_norm[['인구수', 'CCTV']] = result_CCTV[['인구수', '소계']]

## 5대 중요범죄의 합을 구하여 crime_anal_norm의 '범죄' 컬럼에 추가
# col =['강간', '강도', '살인', '절도', '폭력']
crime_anal_norm['범죄'] = np.sum(crime_anal_norm[col], axis=1)


###-----------------------####
### Seaborn을 이용한 사각화
###-----------------------####

# Seaborn 및 사각화 모듈 import
import matplotlib.pyplot as plt
import seaborn as sns

import platform

path = "c:/Windows/Fonts/malgun.ttf"
from matplotlib import font_manager, rc
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')


### 1. 강도, 살인, 폭력 : pairplot()
sns.pairplot(crime_anal_norm,
             vars=['강도', '살인', '폭력'],
             kind='reg',
             size=3)
plt.show()


### 2. ['인구수', 'CCTV']  ['살인', '강도']  : 발생 건수
sns.pairplot(crime_anal_norm,
             x_vars=['인구수', 'CCTV'],
             y_vars=['살인', '강도'],
             kind='reg',
             size=3
             )
plt.show()


### 3. ['인구수', 'CCTV']  ['살인검거율', '강도검거율']
sns.pairplot(crime_anal_norm,
             x_vars=['인구수', 'CCTV'],
             y_vars=['살인검거율', '강도검거율'],
             kind='reg',
             size=3
             )
plt.show()


##### 검거율에 대한 사긱화 : heatmap() 
# 검거율의 최대 값을 100으로 설정하여 heatmap() 을 통한 시각화
# col2 = ['강간검거율', '강도검거율', '살인검거율', '절도검거율', '폭력검거율']

# 검거율의 합 => crime_anal_norm
crime_anal_norm['검거'] = np.sum(crime_anal_norm[col2], axis=1)

tmp_max = crime_anal_norm['검거'].max()
# 432.593167122272

crime_anal_norm['검거'] = crime_anal_norm['검거'] / tmp_max * 100

# '검거' 컬럼을 기준으로 정렬
crime_anal_norm_sort = crime_anal_norm.sort_values(by='검거', ascending=False)


plt.figure(figsize=(10,10))
sns.heatmap(crime_anal_norm_sort[col2],
            annot=True,
            fmt='f',
            linewidths=0.5,
            cmap='RdPu')
plt.title('범죄 검거 비율')
plt.show()


# 범죄 발생 건수 
# col =['강간', '강도', '살인', '절도', '폭력']

crime_anal_norm['범죄'] = crime_anal_norm['범죄'] / 5
crime_anal_norm_sort = crime_anal_norm.sort_values(by='범죄', ascending=False)

plt.figure(figsize=(10,10))
sns.heatmap(crime_anal_norm_sort[col],
            annot=True,
            fmt='f',
            linewidths=0.5,
            cmap='RdPu')
plt.title('범죄 발생 건수')
plt.show()


##### 범죄율에 대한 지도 시각화 : folium
# 지도 시각화를 위한 모듈 import
import json
import folium

# 행정구역 데이터 로드 : 02. skorea_municipalities_geo_simple.json
geo_path = "./data/02. skorea_municipalities_geo_simple.json"
geo_str = json.load(open(geo_path, encoding="utf-8"))


# 살인, 범죄 시각화
map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11,
                 title = "살인, 범죄 시각화",
                 tiles="Stamen Toner")

map.choropleth(geo_data=geo_str, 
               data=crime_anal_norm['살인'], 
               columns=[crime_anal_norm.index, crime_anal_norm['살인']],
               fill_color="RdPu",
               key_on="feature.id")
map.save('살인.html')

import webbrowser
webbrowser.open_new('살인.html')


# 인구 대비 범죄 시각화
# 범죄 데이터를 인구로 나눈 후, 시각화
tmp_criminal = crime_anal_norm['범죄'] / crime_anal_norm['인구수'] * 1000000   # 백
# => 위도 경도가 1/1000000 이기 때문에.. 값을 조절

map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11,
                 tiles="Stamen Toner")

map.choropleth(geo_data=geo_str, 
               data=tmp_criminal, 
               columns=[crime_anal_norm.index, tmp_criminal],
               fill_color="RdPu",
               key_on="feature.id")

map.save('인구대비범죄율.html')


# 검거 시각화
map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11,
                 title = "살인, 범죄 시각화",
                 tiles="Stamen Toner")

map.choropleth(geo_data=geo_str, 
               data=crime_anal_norm['검거'], 
               columns=[crime_anal_norm.index, crime_anal_norm['검거']],
               fill_color="RdPu",
               key_on="feature.id")
map.save('검거.html')

# 인구대비 절도 시각화
tmp_criminal = crime_anal_norm['절도'] / crime_anal_norm['인구수'] * 1000000   # 백
# => 위도 경도가 1/1000000 이기 때문에.. 값을 조절

map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11,
                 tiles="Stamen Toner")

map.choropleth(geo_data=geo_str, 
               data=tmp_criminal, 
               columns=[crime_anal_norm.index, tmp_criminal],
               fill_color="RdPu",
               key_on="feature.id")

map.save('인구대비절도.html')



##### 실제 지도에 
# 경찰서별 검거현황과 범죄발생 현황 시각화

crime_anal_raw['lat'] = station_lat
crime_anal_raw['lng'] = station_lng

col = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
tmp = crime_anal_raw[col] / crime_anal_raw[col].max()

crime_anal_raw['검거'] = np.sum(tmp, axis=1)


## 경찰서 위치 표시
# Map 객체 
map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11)

# 위도/경도 값을 이용하여 Marker 표시
for n in crime_anal_raw.index:
    folium.Marker([crime_anal_raw['lat'][n],
                   crime_anal_raw['lng'][n]],
                  tooltip=crime_anal_raw['관서명'][n]
                  ).add_to(map)

# Map을 html 파일로 저장
map.save('각 경찰서 위치.html')

# 저장된 html 파일을 파이썬 코드로 바로 실행 : import webbrowser 가 선행되어야 함!
webbrowser.open_new('각 경찰서 위치.html')


## 겅찰서별 검거율 (분포형태) 표시
# Map 객체 
map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11)

# 위도/경도 값을 이용하여 CircleMarker 표시
for n in crime_anal_raw.index:
    
    folium.CircleMarker([crime_anal_raw['lat'][n],
                         crime_anal_raw['lng'][n]],
                         radius=crime_anal_raw['검거'][n]*10,
                         color='#ff0000',
                         fill_color='#00ff00',
                         fill=True,
                         tooltip=crime_anal_raw['관서명'][n]).add_to(map)

# Map을 html 파일로 저장
map.save('경찰서별 검거율.html')
webbrowser.open_new('경찰서별 검거율.html')


## 행정 구역별 범죄와 경찰서별 검거율을 한번에 표시
# Map 객체 
map = folium.Map(location=[37.5502, 126.982],
                 zoom_start=11)

# 행정구역별 범죄
map.choropleth(geo_data=geo_str, 
               data=crime_anal_norm['범죄'], 
               columns=[crime_anal_norm.index, crime_anal_norm['범죄']],
               fill_color="RdPu",
               key_on="feature.id")

# 경찰서변 검거
for n in crime_anal_raw.index:
    
    folium.CircleMarker([crime_anal_raw['lat'][n],
                         crime_anal_raw['lng'][n]],
                         radius=crime_anal_raw['검거'][n]*10,
                         color='#ff0000',
                         fill_color='#00ff00',
                         fill=True,
                         tooltip=crime_anal_raw['관서명'][n]).add_to(map)

# Map을 html 파일로 저장
map.save('행정 구역별 범죄와 경찰서별 검거율.html')
webbrowser.open_new('행정 구역별 범죄와 경찰서별 검거율.html')













