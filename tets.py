import httpx


with  httpx.Client(http2=True) as client:
                kami = client.post("https://ebank.msb.com.vn/IBSRetail/Request")
                print(kami.status_code)
                if kami.status_code == 302:
                    print(kami.headers.get('Location'))