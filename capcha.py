import cv2
import pytesseract


def img(path):
        try:
                         image_path = str(path)
                         img = cv2.imread(image_path)

                         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                         blur = cv2.medianBlur(gray, 3)
                         thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                         custom_config = r'--oem 3 --psm 6 outputbase digits'
                         text = pytesseract.image_to_string(thresh, config=custom_config)
                         print(f"Chữ số nhận dạng từ ảnh: {text.strip()}")
                         return str(text.strip())
        except Exception as e:
                print(e)
