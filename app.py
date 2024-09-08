from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException 
import time , os
import requests
import pytesseract
from PIL import Image
import capcha
import random 
taikhoan = ""
matkahu = ""

token = None
chutaikhoan = None
stkbank = None
cookie = None
loog = False
bodanglogin = False
from flask import Flask, request, jsonify ,send_from_directory, current_app
app = Flask(__name__)
app_root = os.path.dirname(os.path.abspath(__file__))
def checkchustk(cokiee,tokenno):
        global stkbank ,chutaikhoan
        url = 'https://ebank.msb.com.vn/IBSRetail/history/byAccount.do'

        # Header của yêu cầu
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cokiee,
            'Host': 'ebank.msb.com.vn',
            'Origin': 'https://ebank.msb.com.vn',
            # 'Referer': 'https://ebank.msb.com.vn/IBSRetail/Request?&dse_sessionId=jn5oyQ5iKwqJrOA26OoFgXv&dse_applicationId=-1&dse_pageId=4&dse_operationName=retailHomeProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Payload (dữ liệu gửi đi)
        payload = {
       ' acctType': "'CA','SA','LN'",
       ' status': "'ACTV','DORM','MATU'",
        'tokenNo': str(tokenno),
        'lang': 'vi_VN'
        }
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        print(data)
        stkbank = str(data['data']['acctNo'])
        stkbank = str(data['data']['acctName'])

def checkGd(cokiee,tokenno):
        global token ,token , bodanglogin
        url = 'https://ebank.msb.com.vn/IBSRetail/history/byAccount.do'

        # Header của yêu cầu
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': cokiee,
            'Host': 'ebank.msb.com.vn',
            'Origin': 'https://ebank.msb.com.vn',
            # 'Referer': 'https://ebank.msb.com.vn/IBSRetail/Request?&dse_sessionId=jn5oyQ5iKwqJrOA26OoFgXv&dse_applicationId=-1&dse_pageId=4&dse_operationName=retailHomeProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start',
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Payload (dữ liệu gửi đi)
        payload = {
            # Thay đổi nội dung payload nếu cần thiết
            'queryType': 0,
        'acctNo': '19101010479737', # số tài khoản tự thay vào tôi lười
        'page': 1,
        'tokenNo': str(tokenno),
        'lang': 'vi_VN'
        }
       
        # Thực hiện yêu cầu POST
        response = requests.post(url, headers=headers, data=payload)
        print(f"{response.status_code}")
        if response.status_code !=200:
                 bodanglogin = True
                 login()
                 bodanglogin = False
                 return None
        return response.json()

def login():
            global token,chutaikhoan,stkbank,cookie
            chrome_options = Options()
            #chrome_options.add_argument("--headless") 
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=chrome_options)

            try:
            
                driver.get("https://ebank.msb.com.vn/IBSRetail/")


                time.sleep(10)

                log= True
                while log:
                  try:  
                    img_element = driver.find_element(By.CSS_SELECTOR, 'img#safecode')
    
    
                    rand_int = random.randint(1, 10000)
                    img_element.screenshot(f'data/{rand_int}img.png')
                    capchap = capcha.img(f'data/{rand_int}img.png')
                    
                    if len(capchap) < 4:
    
                        capchap = capchap + capchap[2]  
                    print(f"Giã capcha là {capchap}")    
                    def nhapdulieu_byname(name ,duliue):
                        input_element = driver.find_element(By.NAME,name)  # Tìm input bằng id
                        input_element.clear()  #
    
    
                        input_element.send_keys(duliue)
                    nhapdulieu_byname("_userName",taikhoan)    
                    nhapdulieu_byname("_passwordS",matkahu)    
                    nhapdulieu_byname("_verifyCode",capchap)    
                    login_button = driver.find_element(By.ID,"loginBtn")
                    login_button.click()
                    time.sleep(2)
                    try:
                        login = driver.find_element(By.ID, "loginBtn")
                        print("Đăng Nhập thất Bại, Login Lại")
                    except NoSuchElementException:
                        print("Đăng Nhập Thành Công msb")
                        log = False
                  except Exception as e:
                       print("Lỗi mã Cáp Cha này Login Này ", e)
                       continue      
                time.sleep(10)
               
                print("thực Thi mã Js")
                js_code = """
    return tokenService.get();  // Trả về giá trị của tokenService.get()
    """
                token = driver.execute_script(js_code)
                cookies = driver.get_cookies()
                cookie = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]) 
                
                element = driver.find_element(By.CLASS_NAME, 'msb-bank-nummber')

# Get the text from the element
                if element:
                    bank_number = element.text.strip()
                    stkbank = bank_number.replace('-', '')
                    
               # time.sleep(1000)
                element =driver.find_element(By.CLASS_NAME, 'msb-main-user-name')
                if element:
                    chutaikhoan = element.text.split()
               
                driver.close()
                driver.quit()      
            except Exception as e:
                print(f"Lỗi: {str(e)}")
@app.errorhandler(404)
def page_not_found(e):

        return """
    <html>
        <head>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f0f0;
                }
                h5 {
                    font-size: 4em;
                    color: #ff4040;
                    text-align: center;
                    margin: 0;
                    transition: transform 0.3s ease, color 0.3s ease;
                }
                h5:hover {
                    transform: scale(1.2);
                    color: #ff8000;
                }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                h5 {
                    animation: fadeIn 1s ease-in;
                }
            </style>
        </head>
        <body>
            <h5>404 <br> Bốn Không Bốn</h5>
        </body>
    </html>
    """, 404
@app.route('/api')
def api_index():
    return "hihi"
@app.route('/')
def index():
    # Lấy giá trị của tham số truy vấn 'key'
    key = request.args.get('key')
    sotin = request.args.get('adu')
    sta = request.args.get('t')
    if str(key) =="kami" and sotin != None and sta != None and bodanglogin == False:
        dulieugd =   checkGd(cookie,token)
        if dulieugd == None:
             response = jsonify({'error': "Đang Login lại",
                            'msg':'Chờ login lại'})
             return response
        status_code= 0
    
        # for index, item in enumerate(dulieugd["data"]["history"]):
        #     if item.get("remark") and str(sotin) in item["remark"]:
        #         print("Có Đơn Hàng nè Check được ")
        #         amount = item.get("amount")
        #         print(amount)
        #         if int(sta) < int(amount):
        #              status_code= 3

        #         elif    int(sta) >= int(amount)  :
        #              status_code= 2
        #              print("okeeeeeeeeeeeeeeeeeeeeeee")

        # update for Kami
        sotientrve = 0
        msgz = "No data"
        for index, item in enumerate(dulieugd["data"]["history"]):
             if item.get("remark"):
        
              remark_parts = item["remark"].split('-')
              extracted_text = next((part for part in remark_parts if sotin in part), None)


              if extracted_text and '_' in extracted_text:
                 extracted_text = extracted_text.split('_')[0]
                 if extracted_text == sotin:
   
                  amount = item.get("amount")
                #   print(f"Index: {index}")
                #   print(f"Amount: {amount}")
                #   print(f"Remark part: {remark_parts[1]}")
                  if int(sta) > int(amount):
                     status_code= 3
                     sotientrve = int(sta)
                     msgz = "chuyen tien khong du roi aaaaaaaaaa"

                  elif    int(sta) <= int(amount)  :
                     status_code= 2
                     sotientrve = int(sta)
                     msgz = "Thanh toan thanh Cong" 
                    # os.system('cls' if os.name == 'nt' else 'clear')
                     vzmsg = f'''
-------------------------------------------------------------------
Thanh Toán Thành Công đơn Hàng Với Mã GD : {sotin}

Với Số Tiền : {sta}

Tiền Chuyển Nhận Được ThựC TẾ : {amount}

iD Giao Dịch Banking MSb: {remark_parts[1]}

index GD : {index}
--------------------------------------------------------------------

'''
                     print(vzmsg)
                  break
        else:
             print("Không Có Dữ liệu Cho '", sotin)

        response = jsonify({'status': status_code,
                            'so_tien':sotientrve,
                            'DH':sotin,
                            'msg':msgz})
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
   # elif key == None or sotin == None or sta == None :
    else:
        response = jsonify({'error': "NGU Như Cặc",
                            'msg':'TOKEN , adu,t = ?'})
        response.status_code = 401
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
 

if __name__ == "__main__":
   if loog == False:
        login()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Xin chào {chutaikhoan}\n stk: {stkbank} TOken của bạn là {token}")
        loog = True
   app.run(debug=False, port=4000)
   
#    dulieugd =   checkGd(cookie,token)
#    print(f"{dulieugd}----------kami")