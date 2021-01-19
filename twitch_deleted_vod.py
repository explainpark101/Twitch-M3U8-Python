import datetime
import hashlib
import urllib.request
from bs4 import BeautifulSoup
import requests as req
import requests
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus
from fake_headers import Headers



def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6 

print('twitchtracker.com에서 스트리머 아이디로 검색 후, streams에 들어가 m3u8을 뽑아내시길 원하는 스트리밍을 선택하세요.')
URL=input('twitchtracker.com의 해당하는 vod의 URL을 입력하세요.')
streamername = URL.split('/')[3]
vodID = URL.split('streams/')[1]
if __name__ == "__main__":
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=False  # generate misc headers
    )
headers = header.generate()
res=req.get(URL,headers=headers)
soup=BeautifulSoup(res.text,features="html.parser")
href=soup.select('div')
href=str(href)
list1=href.split('<div class="stats-value to-dowdatetime">')
href=list1[1]
timestamp=href[:19] #시간 뽑아내기

year = int(timestamp[:4])
month = int(timestamp[5:7])
day = int(timestamp[8:10])

hour = int(timestamp[11:13])
minute = int(timestamp[14:16])
seconds = int(timestamp[17:])
seconds = 0


for i in range(0,60):
    td = datetime.datetime(year,month,day,hour,minute,seconds)
    converted_timestamp = totimestamp(td)
    formattedstring = streamername + "_" + vodID + "_" + str(int(converted_timestamp))
    hash = str(hashlib.sha1(formattedstring.encode('utf-8')).hexdigest())
    requiredhash = hash[:20]
    finalformattedstring = requiredhash + '_' +  formattedstring
    url = f"https://vod-secure.twitch.tv/{finalformattedstring}/chunked/index-dvr.m3u8"
    try:
        res = urllib.request.urlopen(url)
        print(url)
        input('추출이 완료되었습니다. 끝내시려면 enter를 눌러주세요.')
    except:
        print('',end='')
        seconds=seconds+1
