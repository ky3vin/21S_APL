#!/usr/bin/env python
# coding: utf-8

# 결과 예시 :<br/>
# (['210.123.38.21', '80', 'TCP', '국민대학교'...],['웹해킹'],99) <br/>
# 1. 첫 번째 []는 `INST_NM`, `ASSETS_VAL_1-22`, `TW_ATT_IP`,`TW_ATT_PORT`,`TW_DMG_IP`,`TW_DMG_PORT`,`TW_ATT_CT_CODE`, `INTENT_VAL_0-6` <br/>
# 2. 두 번째 []는 `DRULE_ATT_TYPE_CODE1`
# 3. 빈도수

# In[1]:


# 원하는 파일 불러오기
import pandas as pd
df = pd.read_csv("./data/ts_data_accident-2020_sample.csv")
df.head()


# In[2]:


#필요한 라이브러리 불러오기
import numpy as np
from pandas import Series
import json
from pandas import json_normalize
import time


# ### 데이터 추출하기 : INST_NM, ASSETS_VAL, INTENT_VAL

# In[3]:


'''
#RISK_V2에서 ASSETS_VAL 추출
df_ASSET = df.loc[:,['RISK_V2']] #전체 dataframe에서 'RISK_V2'col만 추출하여 만든 dataframe
df_temp = pd.DataFrame() #df_risk의 i번째 row의 값을 임시로 저장할 df

start = time.time()  # 시작 시간 저장

for i in range(len(df)): #len(df) : 26043
    js = df_ASSET['RISK_V2'][i] #type(js) : str
    js = js.replace("'", "\"") # 홑따옴표->겹따옴표(JSON 표준)
    js_string = json.loads(js) #JSON 문자열을 Python 객체로 변환
    json_df = json_normalize(js_string) #JSON 객체를json_normalize()에 전달하면 필요한 데이터가 포함 된 Pandas DataFrame이 반환
    df_temp = pd.concat([df_temp,json_df],ignore_index=True) 
    #방금 구한 json_df를 기존df에 추가(json_df의 index는 모두 0이므로 ignore_index로 새롭게 index 설정 필요)
    
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

# 시간이 오래 걸려서 매번 실행할 때 마다 처리하는건 불편. 따로 파일 만들어 저장

ASSETS_VAL= df_temp.copy()[['ASSETS_VAL_1','ASSETS_VAL_2','ASSETS_VAL_3','ASSETS_VAL_4','ASSETS_VAL_5'
                            ,'ASSETS_VAL_6','ASSETS_VAL_7','ASSETS_VAL_8','ASSETS_VAL_9','ASSETS_VAL_10','ASSETS_VAL_11',
                            'ASSETS_VAL_12','ASSETS_VAL_13','ASSETS_VAL_14','ASSETS_VAL_15','ASSETS_VAL_16','ASSETS_VAL_17',
                            'ASSETS_VAL_18','ASSETS_VAL_19','ASSETS_VAL_20','ASSETS_VAL_21','ASSETS_VAL_22']]
ASSETS_VAL.to_csv("./data/ts_data_accident-2020_sample_ASSETS_VAL.csv")

# 마찬가지로 INTENT_VAL 과 INST_NM 추출 및 저장
'''
print() #주석 markdown 출력 방지용


# ### 필요한 데이터로 데이터프레임 만들기 : TW_ATT_IP, TW_ATT_PORT, TW_DMG_PORT, TW_DMG_IP, DRULE_ATT_TYPE_CODE1, TW_ATT_CT_CODE, INTENT_VAL, ASSETS_VAL, INST_NM

# In[4]:


#1.기관
INST_NM = pd.read_csv("./data/ts_data_accident-2020_sample_INST_NM.csv")
INST_NM.drop(['Unnamed: 0'], axis = 1, inplace = True)
#2.위협공격ip
ATT_IP = df.copy()['TW_ATT_IP']
#3.위협공격port
ATT_PORT = df.copy()['TW_ATT_PORT']
#4.위협피해port
DMG_PORT = df.copy()['TW_DMG_PORT']
#5.위협피해ip
DMG_IP = df.copy()['TW_DMG_IP']
#6.공격
DRULE_ATT_TYPE_CODE1=df.copy()['DRULE_ATT_TYPE_CODE1']
#7.공격국가
TW_ATT_CT_CODE = df.copy()['TW_ATT_CT_CODE']
#8.의도
INTENT_VAL=pd.read_csv("./data/ts_data_accident-2020_sample_INTENT_VAL.csv")
INTENT_VAL.drop(['Unnamed: 0'], axis = 1, inplace = True)
#9.자산
ASSETS_VAL_temp = pd.read_csv("./data/ts_data_accident-2020_sample_ASSETS_VAL.csv")
ASSETS_VAL_temp.drop(['Unnamed: 0'], axis = 1, inplace = True)


# In[5]:


# INTENT_VAL 수정
# 보는 사람이 이해하기 쉽게 -> 0인 값은 지우되, 남아있는 값이 무엇의 값인지 알아볼 수 있도록 가공.
cols = INTENT_VAL.columns.tolist()
INTENT_list=[]
for i in range(0,len(INTENT_VAL)):
    temp_str=[]
    for j in range(len(cols)):
        temp_val = INTENT_VAL.loc[i][j]
        temp = str(cols[j])+': '+str(temp_val)
        if(temp_val!=0):
            temp_str.append(temp)
    INTENT_list.append(temp_str)
INTENT = pd.DataFrame(INTENT_list)
INTENT = INTENT.rename(columns={INTENT.columns[0]:'INTENT_VAL'}, inplace=False)
INTENT.head()


# In[6]:


# ASSETS_VAL 수정
cols = ASSETS_VAL_temp.columns.tolist()
ASSETS_list=[]
for i in range(0,len(ASSETS_VAL_temp)):
    temp_str=[]
    for j in range(len(cols)):
        temp_val = ASSETS_VAL_temp.loc[i][j]
        temp = str(cols[j])+': '+str(temp_val)
        if(temp_val!=0):
            temp_str.append(temp)
    ASSETS_list.append(temp_str)
ASSETS = pd.DataFrame(ASSETS_list)
#ASSETS.head()


# In[ ]:


'''
# 의도 합치기
# 값이 0인 INTENT_VAL 값을 지우다보니 INTENT_VAL_5만 살아남아 INTENT를 합칠 이유가 사라졌습니다...
cols=INTENT_VAL.columns
INTENT_combined = pd.DataFrame()
INTENT_combined['INTENT_VAL'] = INTENT_VAL[cols].apply(lambda row: ', '.join(row.values.astype(str)), axis=1)
INTENT_combined.head()
'''


# In[8]:


# 자산 합치기
cols = ASSETS.columns.tolist()
ASSETS_combined = pd.DataFrame()
ASSETS_combined['ASSETS_VAL'] = ASSETS[cols].apply(lambda row: ', '.join(row.values.astype(str)), axis=1)
ASSETS_combined.head()


# ### PrefixSpan 에 필요한 라이브러리 설치 : pypi, prefixspan

# In[ ]:


get_ipython().system('pip install pypi')
get_ipython().system('pip install prefixspan')


# ### 필요한 라이브러리 불러오기 : PrefixSpan

# In[10]:


from prefixspan import PrefixSpan


# ### PrefixSpan에 쓸 수 있게 list로 데이터 처리

# In[11]:


data = []
for i in range(0,len(ASSETS_combined)):
    temp_list = []
    temp_asset=[]
    temp_asset=ASSETS_combined['ASSETS_VAL'].loc[i]
    temp_intent=[]
    temp_intent=INTENT['INTENT_VAL'].loc[i]
    temp_name = []
    temp_name = INST_NM['ATT_INST_NM'].loc[i]
    temp_list.append([temp_asset, temp_intent, temp_name, ATT_IP[i], ATT_PORT[i], 
                      DMG_PORT[i], DMG_IP[i], DRULE_ATT_TYPE_CODE1[i], TW_ATT_CT_CODE[i]])
    data.extend(temp_list)


# In[12]:


ps = PrefixSpan(data)


# ### 결과 확인

# In[13]:


# 1. 빈도수가 데이터의 절반 이상인 것을 빈도순으로 배열
print(ps.frequent(len(data)/2))


# In[ ]:





# In[14]:


# 2. 빈도수 TOP 5, closed : A pattern is closed if there is no super-pattern with the same frequency.
print(ps.topk(5, closed=True))


# In[15]:


# 3. 빈도수 2 이상, closed 
print(ps.frequent(2, closed=True))


# In[16]:


# 4. 빈도수 2 이상, generator :  A pattern is generator if there is no sub-pattern with the same frequency
print(ps.frequent(2, generator=True))

