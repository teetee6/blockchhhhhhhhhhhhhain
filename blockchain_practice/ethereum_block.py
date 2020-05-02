import pandas as pd
import numpy as np

### 블록크기
# https://etherscan.io/chart/blocksize 에서 .csv 파일을 다운로드 받는다.
# df['Value'] = 그 날 생성된 "블록 평균 크기"
# the most recent day로부터 180일 전까지 평균 블록크기   
file_path = './export-BlockSize.csv'
df = pd.read_csv(file_path)

today_timestamp = df.iloc[-1]['UnixTimeStamp']      # 파일에 기록된 the most recent day! (매일 오전 9시시간)
mean_size = df[df['UnixTimeStamp'] > today_timestamp - (24*60*60)*180 ].mean()['Value']     
print('180일간 생성된 블록의 평균 크기: %.2lf MB ' %(mean_size / 1000))


### 블록생성주기(Interval)
# https://etherscan.io/chart/blocktime 에서 .csv 파일을 다운로드 받는다.
# df2['Value'] = 그 날 "블록 평균 생성시간"
# the most recent day로부터 180일 전까지 평균 블록크기   
file_path = './export-BlockTime.csv'
df2 = pd.read_csv(file_path)

today_timestamp = df2.iloc[-1]['UnixTimeStamp']      
mean_time = df2[df2['UnixTimeStamp'] > today_timestamp - (24*60*60)*180 ].mean()['Value'] 
print('180일간 생성된 블록의 평균 생성주기: %.2lf 초 ' %(mean_time))


### 블록별 평균 트랜잭션 처리 개수
# https://etherscan.io/chart/tx 에서 .csv 파일을 다운로드 받는다.
# df3['Value'] = 그 날 처리된 "Total transactions수"
# https://etherscan.io/chart/blocks 에서 .csv 파일을 다운로드 받는다.
# df4['Value'] = 그 날 생성된 "Total Blocks수"
file_path = './export-TxGrowth.csv'
df3 = pd.read_csv(file_path)
file_path = './export-BlockCountRewards.csv'
df4 = pd.read_csv(file_path)

# df3 데이터 기준으로 조작하겠음. the most recent day가 불일치하면 df3가 df4의 부분집합 이도록 맞추겠음.
today_timestamp = df3.iloc[-1]['UnixTimeStamp']
today_timestamp2 = df3.iloc[-1]['UnixTimeStamp']
if( today_timestamp != today_timestamp2 ):
    if( today_timestamp > today_timestamp2):
        today_timestamp = df3[df3['UnixTimeStamp'] == today_timestamp2]['UnixTimeStamp']


tx_block = []

total_tx = df3[df3['UnixTimeStamp'] > today_timestamp - (24*60*60)*180 ]['Value']
total_block = df4[df3['UnixTimeStamp'] > today_timestamp - (24*60*60)*180 ]['Value']

for i in range(180):
    tx_block.append(total_tx.iloc[-i-1] / total_block.iloc[-i-1])

print('180일간 블록별 평균 트랜잭션 처리 갯수: %.2lf 개 ' % (np.mean(tx_block)))