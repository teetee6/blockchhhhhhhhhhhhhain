import requests
import time
import pandas as pd
import numpy as np
import time

url = 'https://api.blockchair.com/monero/raw/block/1'
resp = requests.get(url=url)
data = resp.json()

block = data['data']
current_height = block['1']['block']['current_height']

header = []

#1분에 30 requests 트래픽제한걸어놔서 적당히 함
print("최근 생성된 %s번째 블록으로 부터 100개의 블록을 읽어옵니다" % (current_height-1))
for n in range(100):
    if (n % 30 == 0) & (n != 0):
        print("%i 번째 입니다. 10초만 쉬세요" %(n))
        time.sleep(10)
        print("다시 출발!")

    url = 'https://api.blockchair.com/monero/raw/block/' + str(current_height - 1 - n)
    resp = requests.get(url=url)
    data = resp.json()

    block = data['data'][str(current_height-1 - n)]['block']
    #블록 사이즈
    bsize = block['size']
    #블록 생성시간
    btime = block['timestamp']
    # 해당 블록에서 처리한 트랜잭션의 수 (-1 : 코인베이스)
    btx = len(block['txs']) - 1 

    header.append([bsize, btime, btx])
    print(str(n+1) + '/100번째의 ' + str(block['block_height']) + '블럭을 읽었습니다')

df = pd.DataFrame(header, columns=['Size','Time','Tx'])
sdf = df.sort_values('Time')
sdf = sdf.reset_index()
sdf2 = df.sort_values('Size')
sdf2 = sdf2.reset_index()
sdf3 = df.sort_values('Tx')
sdf3 = sdf3.reset_index()

mtime = sdf['Time'].diff().values
mtime = mtime[np.logical_not(np.isnan(mtime))]
print("평균 블록 생성주기 = %d 초" % np.mean(mtime))
msize = sdf2['Size'].diff().values
msize = msize[np.logical_not(np.isnan(msize))]
print("평균 블록 크기 = %.2lf MB" % (int(np.mean(msize)) / 1000)) 
print("블록 별 평균 트랜잭션 처리 갯수 = %d 개" % np.mean(sdf3['Tx']))