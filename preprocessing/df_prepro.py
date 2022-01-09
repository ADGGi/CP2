'''
[note]
- row data의 행, 렬, 날짜 등을 다듬는 함수
- label 컬럼에 대한 작업을 포함하지 않음
- 데이터를 받으면, 먼저 이 함수로 데이터를 전처리 한 후, labeling을 하는 것을 추천
'''

import pandas as pd
import numpy as np
from numpy.core.numeric import NaN

### 구글드라이브 연동 (코랩 환경일 경우)
# from google.colab import drive
# drive.mount('/content/drive')

PATH = '파일경로'
data = pd.read_excel(PATH, keep_default_na=False)

def CP2_preprocessing(data):
  
  '''
  1. celeb 컬럼 만들기
  '''

  # 대화 내용을 제외한 행들 추출 날짜와 회원 코드가 있어야 함.
  filter1 = data[(data['날짜'] != '') & (data['회원 코드'] != '')]

  # 중복 없애기 (먼저 받은 데이터에서 중복이 생긴 경우가 있었음)
  filter1 = filter1.dropna()
  filter1 = filter1.drop_duplicates(['회원 코드'])
  filter1 = filter1[['날짜', '회원 코드']]

  # 특정 셀럽에 대한 내용이 시작하는 part 찾기
  celeb_list = []
  celeb_index_list = []
  for index, row in filter1.iterrows():
    celeb_list.append((row['날짜'], row['회원 코드']))
    celeb_index_list.append(index)

  # 새 컬럼 추가
  data['celeb'] = '' 

  # 셀렙 이름 붙여주기 위한 코드 (index가 끝까지 있어야 범위 설정 가능!)
  celeb_index_list.append(len(data)-1)

  # 일정범위의 index에 해당하는 celeb 컬럼에 셀럽 이름 추가
  for i in range(len(celeb_index_list)-1): # -1인 이유는 i+1까지의 범위를 바꿔주기 때문
    index_from = celeb_index_list[i] 
    index_to = celeb_index_list[i+1] 
    who = celeb_list[i][1] # 셀럽 누구인지 / i는 index만 모아놓은 list의 순서(넘버)를 말함. 
    data.loc[index_from+1:index_to, ['celeb']] = who # 일정범위의 indexd에 해당하는 celeb 컬럼에 셀럽 이름 추가

  '''
  2. 날짜 통일 해주기
  '''

  filter2 = data[(data['날짜'] != '')]
  date_list = []
  date_index_list = []
  for index, row in filter2.iterrows():
    date_list.append((row['날짜']))
    date_index_list.append(index)

  # 마지막 인덱스 추가해주기 
  last_index = len(data)-1 
  date_index_list.append(last_index)


  # 일정범위의 index에 해당하는 날짜 컬럼에 날짜 추가
  for i in range(len(date_index_list)-1):
    index_from = date_index_list[i] 
    index_to = date_index_list[i+1] 
    when = date_list[i]
    data.loc[index_from+1:index_to, ['날짜']] = when 

  # 필요없는 row 삭제
  # 대화내용이 있거나, 파일이나 사진을 보낸 row만 걸러내기
  data = data[(data['대화 내용'] != '') | (data['파일(영상, 음성), 사진 여부'] != '')] 

  data = data[['날짜', '시간', 'celeb', '회원 코드', '대화 내용', '파일(영상, 음성), 사진 여부']]

  data.columns = ['date', 'time', 'celeb', 'code', 'comments', 'file']

  return data

result = CP2_preprocessing(data)

result.to_csv('파일경로/이름.csv')