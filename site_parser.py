import requests
from bs4 import BeautifulSoup
import json
from time import sleep

SITE_CONFIG = "HENDERSON" # "HENDERSON" или "SDVOR"

#########################################
### Строительный двор (пагинации нет) ###
#########################################

URL_SDVOR = "https://www.sdvor.com/moscow/category/krovlja-i-fasad-9050"
PRODUCT_TAG_SDVOR = {"tag": "div", "class_name": "product"}
PRODUCT_NAME_TAG_SDVOR = {"tag": "a", "class_name": "product-name"}
PRODUCT_PRICE_TAG_SDVOR = {"tag": "span", "class_name": "main"}
PAGES_SDVOR = {}


SDVOR_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'qrator_jsid=1729514747.185.StdffyEJKF27qRjQ-78kj82vl0sbigoo1mt16e1kp042md6ai; ASP.NET_SessionId=quf3mnbgh2wv50wxhoi4pfsr; hpuid=02238c8386cc19ef8dffb9d0b7425a1d; SRV_HAYAS=node01; UtcTos=-300; _gcl_au=1.1.439828285.1729514675; _ym_uid=1729514675821061146; _ym_d=1729514675; _ga=GA1.1.915096271.1729514675; flocktory-uuid=6245582c-48d2-4386-8320-d68c23e0d71e-2; _ym_visorc=w; _ym_isad=2; tmr_lvid=6ef528f6930eb94ab7dcd4f186fd39c9; tmr_lvidTS=1729514676716; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; ssaid=3b0413f0-8faa-11ef-986a-03944c7a57cf; domain_sid=u9W9rXtTgLyLDwt1Mho1N%3A1729514676995; mindboxDeviceUUID=9543b01f-7254-4990-97ff-5e7e75a66bce; directCrm-session=%7B%22deviceGuid%22%3A%229543b01f-7254-4990-97ff-5e7e75a66bce%22%7D; popCity=1; adrdel=1729514691889; adrcid=A2G7oGDk08RpmquaIUDQB4w; acs_3=%7B%22hash%22%3A%225c916bd2c1ace501cfd5%22%2C%22nextSyncTime%22%3A1729601091969%2C%22syncLog%22%3A%7B%22224%22%3A1729514691969%2C%221228%22%3A1729514691969%2C%221230%22%3A1729514691969%7D%7D; __tld__=null; tmr_detect=0%7C1729514694001; _ga_KXLLKH0F95=GS1.1.1729514675.1.1.1729514910.59.0.0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'sec-ch-ua': 'Google Chrome;v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
}


##################################
### Henderson (пагинация есть) ###
##################################

URL_HENDERSON = "https://henderson.ru/catalog/shirts/"
PRODUCT_TAG_HENDERSON = {"tag": "div", "class_name": "card-product__info"}
PRODUCT_NAME_TAG_HENDERSON = {"tag": "a", "class_name": "card-product__name-link"}
PRODUCT_PRICE_TAG_HENDERSON = {"tag": "div", "class_name": "card-product__price"}
PAGES_HENDERSON = {"tag": "a", "class_name": "pagination-page"}
SHORT_URL_HENDERSON = "https://henderson.ru/"

HENDERSON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "hpuid=02238c8386cc19ef8dffb9d0b7425a1d; _gcl_au=1.1.439828285.1729514675; _ym_uid=1729514675821061146; _ym_d=1729514675; _ga=GA1.1.915096271.1729514675; flocktory-uuid=6245582c-48d2-4386-8320-d68c23e0d71e-2; tmr_lvid=6ef528f6930eb94ab7dcd4f186fd39c9; tmr_lvidTS=1729514676716; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; ssaid=3b0413f0-8faa-11ef-986a-03944c7a57cf; popCity=1; adrcid=A2G7oGDk08RpmquaIUDQB4w; qrator_jsr=1729785438.597.8Xc3Iq86gvOHiPzi-gtfuf2i98n6krqntblee2scltl6fs3ve-00; qrator_jsid=1729785438.597.8Xc3Iq86gvOHiPzi-teel496ooicvlch1j3rskj1ooge8cerg; ASP.NET_SessionId=fkxvknojlbdq0cqb1jagincn; SRV_HAYAS=node12; UtcTos=-300; _ym_isad=2; _ym_visorc=b; domain_sid=u9W9rXtTgLyLDwt1Mho1N%3A1729785368270; acs_3=%7B%22hash%22%3A%225c916bd2c1ace501cfd5%22%2C%22nextSyncTime%22%3A1729871768274%2C%22syncLog%22%3A%7B%22224%22%3A1729785368274%2C%221228%22%3A1729785368274%2C%221230%22%3A1729785368274%7D%7D; adrdel=1729785368685; tmr_detect=0%7C1729785373829; mindboxDeviceUUID=9543b01f-7254-4990-97ff-5e7e75a66bce; directCrm-session=%7B%22deviceGuid%22%3A%229543b01f-7254-4990-97ff-5e7e75a66bce%22%7D; __tld__=null; _ga_KXLLKH0F95=GS1.1.1729785367.3.1.1729785417.10.0.0",
    "Host": "henderson.ru",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
}

COOKIES = {
    '__Secure-ext_xcid': '478fd30523b7b26831a34e5fc4720bb3',
    '__Secure-user-id': '0',
    '__Secure-ab-group': '71',
    'cf_clearance': 'T5_.YUTh.707vMLqxBxj0ENpGwViPalg.g5uqaLTUCo-1706203545-1-AVue6hSHqn2WcQuhT7MgidCCWpYwvzvE/uito/Ewi5OZSGQba4u7ctjyOw2UrMVEiEeuPQrLacCfLdnHXNPJf0w=',
    'cf_clearance': 'gBHs0vHo0ybJ6Y9yAvWaSXjx_Wl4O1VHu6SttLJ7SSo-1715793372-1.0.1.1-djVNNet34MngWG6TQEqGReSIfYtXYkhEbEhYjw0jSbMiSxXAnPqWQesWkCXm7v94mNU.77rt6ofgKUzrt74diQ',
    '__Secure-ETC': 'a69261a3747192909854f6b7812cfc92',
    '__Secure-refresh-token': '6.0.L__h-9ZLQHyEeiaBuChMAQ.71.AVU7WJIdEPGFwSQiE4DYbb2_qv-d9GVohvEh0UQWpHg54UTgkEO3Jmqh7IRcn9NC1w..20241010171747.dIaBdn_Ci-ePfwHaPxZgfDINclem7lfS5b7q78vxay0.11c232def13e57206',
    '__Secure-access-token': '6.0.L__h-9ZLQHyEeiaBuChMAQ.71.AVU7WJIdEPGFwSQiE4DYbb2_qv-d9GVohvEh0UQWpHg54UTgkEO3Jmqh7IRcn9NC1w..20241010171747._XnhfRYuxlak_q3gepFoVYmJnDBf8jb08PCbQOKF1No.1a3165811cbbf5cb1',
    'xcid': '18ee78acc75ada67bccfab486aa9f26a',
    'ADDRESSBOOKBAR_WEB_CLARIFICATION': '1728573469',
    'rfuid': 'NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMDQ0MjEyNTc2LC0xLC0xMTI5MzU3NTU4LFczc2libUZ0WlNJNklsQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMWxJRkJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFwZFcwZ1VFUkdJRlpwWlhkbGNpSXNJbVJsYzJOeWFYQjBhVzl1SWpvaVVHOXlkR0ZpYkdVZ1JHOWpkVzFsYm5RZ1JtOXliV0YwSWl3aWJXbHRaVlI1Y0dWeklqcGJleUowZVhCbElqb2lZWEJ3YkdsallYUnBiMjR2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZTeDdJblI1Y0dVaU9pSjBaWGgwTDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMWRmU3g3SW01aGJXVWlPaUpOYVdOeWIzTnZablFnUldSblpTQlFSRVlnVm1sbGQyVnlJaXdpWkdWelkzSnBjSFJwYjI0aU9pSlFiM0owWVdKc1pTQkViMk4xYldWdWRDQkdiM0p0WVhRaUxDSnRhVzFsVkhsd1pYTWlPbHQ3SW5SNWNHVWlPaUpoY0hCc2FXTmhkR2x2Ymk5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlMSHNpZEhsd1pTSTZJblJsZUhRdmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmVjE5TEhzaWJtRnRaU0k2SWxkbFlrdHBkQ0JpZFdsc2RDMXBiaUJRUkVZaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMWQsV3lKeWRTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVjJsdU16SWdOUzR3SUNoWGFXNWtiM2R6SUU1VUlERXdMakE3SUZkcGJqWTBPeUI0TmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNall1TUM0d0xqQWdXV0ZDY205M2MyVnlMekkwTGpjdU1DNHdJRk5oWm1GeWFTODFNemN1TXpZZ01qQXdNekF4TURjZ1RXOTZhV3hzWVE9PSxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmU3dpYVRFNGJpSTZlMzE5TENKNVlXNWtaWGdpT25zaWJXVmthV0VpT250OUxDSnlaV0ZrWVdKcGJHbDBlU0k2ZTMwc0ltNWxkWEp2UVhOemFYTjBZVzUwSWpwN0ltOXVVR0ZuWlVOb1lXNW5aV1FpT250OUxDSnZiazVsZFhKdlFYTnphWE4wWVc1MFQzQmxibVZrU1c1VGNHeHBkRlpwWlhkTllYbGlaVU5vWVc1blpXUWlPbnQ5ZlN3aWNIVmliR2xqUm1WaGRIVnlaU0k2ZXlKVWRYSmliMEZ3Y0ZOMFlYUmxJanA3SWtoQlUxOUNSVlJVUlZKZlZrVlNVMGxQVGlJNkltaGhjMEpsZEhSbGNsWmxjbk5wYjI0aUxDSkpUbDlRVWs5SFVrVlRVeUk2SW1sdVVISnZaM0psYzNNaUxDSkpUbE5VUVV4TVFWUkpUMDVmUlZKU1QxSWlPaUpwYm5OMFlXeHNZWFJwYjI1RmNuSnZjaUlzSWs1QlZrbEhRVlJKVDA1ZlZFOWZWVTVMVGs5WFRsOUJVRkJNU1VOQlZFbFBUaUk2SW01aGRtbG5ZWFJwYjI1VWIxVnVhMjV2ZDI1QmNIQnNhV05oZEdsdmJpSXNJazVQVkY5SlRsTlVRVXhNUlVRaU9pSnViM1JKYm5OMFlXeHNaV1FpTENKU1JVRkVXVjlHVDFKZlZWTkZJam9pY21WaFpIbEdiM0pWYzJVaWZYMTlmUT09LDY1LDUyMTA1MTkxMSwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDExNjQyNDY5NTksMTI=',
    'abt_data': '7.2-pxROF22NJd0x5n3QLsD6AlmWSulY_r_8yH3o9DCvIOE7bq3hEzd0a9mQvZd7A3IOWcPOWF8yt5rAfl79IEn41cAtxqrS7B_hKd1KHmV8F-dAcVBJQ9muEuhEXDTtzOwS1zzLpGHldb11rCder_f0I0pOs7Eb4WdzeSm4siR-DEQOyKv88wy0-FPqsuKTGz9vcdorT9_peGJGRfShbBDWqjmEDLPdOIMYutFJkXKDXyCwLp6GA6Wfrc2TQRBGVU02RbaUAg_42-9jHns4vq-oLpz7l6k3CKtCL0abGpo48k5Dx5OsvFutKBg70xehbMzhVW7DKfNdjzZPF1b7Cw9pxHZ3ZG5sV4W0IzMQ9u7f47gJZ0hLPkJDPSSfSUNf3fYp96PgIm1I9UxR2f4-FBktu_yzooisrXXT-X_4I5lWkkK9pgl_meljmJ9qo-tTnAgvT49WkqQTczF_4EM_VQiO2zBZNQl9Hq6hAV1T1unkL0PCPIS5ZCgTQZNvcJDBFGVW_IWUtNJ-sBAAU',
}

if SITE_CONFIG == "HENDERSON":
    HEADERS = HENDERSON_HEADERS
    URL = URL_HENDERSON
    PRODUCT_TAG = PRODUCT_TAG_HENDERSON
    PRODUCT_NAME_TAG = PRODUCT_NAME_TAG_HENDERSON
    PRODUCT_PRICE_TAG = PRODUCT_PRICE_TAG_HENDERSON
    PAGES = PAGES_HENDERSON
    SHORT_URL = SHORT_URL_HENDERSON
else:
    HEADERS = SDVOR_HEADERS
    URL = URL_SDVOR
    PRODUCT_TAG = PRODUCT_TAG_SDVOR
    PRODUCT_NAME_TAG = PRODUCT_NAME_TAG_SDVOR
    PRODUCT_PRICE_TAG = PRODUCT_PRICE_TAG_SDVOR
    PAGES = PAGES_SDVOR



def get_products(url):
    all_products = []
    page = 1
    response = requests.get(url, headers=HEADERS, cookies=COOKIES)
    soup = BeautifulSoup(response.text, 'lxml')
    if PAGES:
        pages = soup.find_all(PAGES['tag'], class_=PAGES['class_name'])
    
    while True:
        if PAGES:
            print(f"Обработка страницы {page}")
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        if response.status_code != 200:
            print(f"Ошибка: статус код {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        products = soup.find_all(PRODUCT_TAG["tag"], class_=PRODUCT_TAG["class_name"])
        
        if not products:
            print("Товары не найдены на странице.")
            break
        for product in products:
            name_elem = product.find(PRODUCT_NAME_TAG['tag'], class_=PRODUCT_NAME_TAG['class_name'])
            price_elem = product.find(PRODUCT_PRICE_TAG['tag'], class_=PRODUCT_PRICE_TAG['class_name'])
            
            name = name_elem.text.strip() if name_elem else 'Нет названия'
            price = price_elem.text.strip() if price_elem else 'Нет цены'
            
            all_products.append({"name": name, "price": price})
        
        print(f"Собрано товаров: {len(all_products)}")
        
        if PAGES:
            url = SHORT_URL + pages[page-1]['href']
            page += 1
            if page > len(pages):
                break
            sleep(1)  # Задержка между запросами
        else:
            break
    
    return all_products

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    products = get_products(URL)
    filename = f"{SITE_CONFIG}_products.json"
    save_to_json(products, filename)
    print(f"Всего собрано товаров: {len(products)}")
    print(f"Данные сохранены в файл {filename}")
