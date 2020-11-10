import requests
import os
path = os.path.dirname(os.path.abspath(__file__))
print(path)
CloudFile = os.path.join(path,'RG-CloudFile-Screen.apk')
Cloud = os.path.join(path,'RG_WhiteBoard_Screen.apk')
url = 'http://scp.ruijie.com.cn/update/public/software/file/RG-CloudFile-Screen.apk'
f = requests.get(url=url)
with open(CloudFile,'wb') as code:
    code.write(f.content)
url = 'http://scp.ruijie.com.cn/update/public/software/file/RG_WhiteBoard_Screen.apk'
f = requests.get(url=url)
with open(Cloud,'wb') as code:
    code.write(f.content)
