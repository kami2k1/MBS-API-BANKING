import requests ,re
import util
from urllib.parse import urlparse, parse_qs
import random
import capcha , time
from PIL import Image
import io 
import httpx
class Msb:
    def __init__(self, User , Passwd):
        self.user = User
        self.Passwd = Passwd
        self.token = None
        self.url = "https://ebank.msb.com.vn"
        self.s = requests.session()
    def extraPath(self, data):
         path = re.search(r"window\.location\.href\s*=\s*'([^']+)'", data)
         path = path.group(1)
         return path
    def Extreaurl(self, url):
            data = urlparse(url)
            data = parse_qs(data.query)
            data = {key: value[0] for key, value in data.items()}
            return data
    def login(self):
        # get link 

        path = "/IBSRetail"
        kami = self.s.get(self.url+path,headers=util.Hed)
        
        data = kami.text
        path = self.extraPath(data)
        
        url = self.url + path
        
        kami = self.s.get(url, headers=util.Hed).text
        path = self.extraPath(kami)
        url = self.url + path
        
        kami = self.s.get(url, headers=util.Hed)
        print(kami.text)
        head = util.Hed
        head.update({
             "host":"ebank.msb.com.vn",
             "referer":url
        }
        )
        
        kami = self.s.get("https://ebank.msb.com.vn/IBSRetail/servlet/ImageServlet", cookies=kami.cookies, headers=head)
        ran = random.randint(1,1000)
        data = self.Extreaurl(url)
        imgz = f"data/{ran}.png"
        print(imgz)
        # with open(img, "wb") as f:
        #      f.write(kami.content)
        #      f.close()
        img = Image.open(io.BytesIO(kami.content))
        img.save(imgz)  # Lưu ảnh
        time.sleep(1)
        capchap = capcha.img(imgz)
        if len(capchap) < 4:
    
                capchap = capchap + capchap[2]
        print(data["dse_pageId"])
        data = {
            " dse_sessionId": data["dse_sessionId"],
                "dse_applicationId": -1,
                "dse_pageId": f"{int(data["dse_pageId"]) +1}",
                "dse_operationName": data["dse_operationName"],

                "dse_errorPage": "index.jsp",
                "dse_processorState": "initial",
                "dse_nextEventName":" start",
                "orderId":"" ,
                "_userNameEncode": self.user,
                "_userName": self.user,
                "_password": self.Passwd,
                "_verifyCode": f"{int(capchap)}"

        }
        print(data)
        headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://ebank.msb.com.vn",
    "Referer": kami.url,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Sec-CH-UA": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Upgrade-Insecure-Requests": "1",
}
       
        kami = self.s.post("https://ebank.msb.com.vn/IBSRetail/Request",cookies=kami.cookies,headers=headers, data=data)
        print(kami.status_code)
        print(kami.text)
        path = self.extraPath(kami.text)
        kami =self.s.get(self.url+path,headers=head,cookies=kami.cookies)
        print(kami.status_code)
        print(kami.text)
        

kami = Msb("0364854825","Kami123@1")
kami.login()