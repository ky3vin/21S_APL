import pandas as pd
import numpy as np
from pandas import Series
import json
from pandas import json_normalize
import time

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

#같은 방식으로 INTENT_VAL, INST_NM 추출
