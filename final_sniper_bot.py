
import requests
import time

TOKEN = "7628017221:AAF9vsP99Bwc8IQhrOWaaCUumFy-hWcjGnQ"
CHAT_ID = "492998632"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def get_current_price(symbol="KCS-USDT"):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"
    try:
        res = requests.get(url).json()
        return float(res['data']['price'])
    except:
        return None

def send_boom_alert(symbol, entry, sl):
    current_price = get_current_price(symbol)
    if current_price is None:
        send_message("تعذر جلب السعر الحالي.")
        return

    tp1 = round(entry * 1.03, 4)
    tp2 = round(entry * 1.05, 4)
    tp3 = round(entry * 1.07, 4)

    message = f"""
🚨 اشارة BOOM جديدة

العملة: {symbol}
نقطة الدخول: {entry} USDT
السعر الحالي: {current_price} USDT
وقف الخسارة: {sl} USDT

الأهداف:
1 - {tp1} USDT (+3%)
2 - {tp2} USDT (+5%)
3 - {tp3} USDT (+7%)

طريقة الخروج:
- خروج جزئي عند أول هدف
- تفعيل Trailing Stop بعد الهدف الثاني
    """
    send_message(message)

# تشغيل كل ساعة (كمثال)
if __name__ == "__main__":
    while True:
        send_boom_alert("KCS-USDT", 10.5, 10.2)
        time.sleep(3600)
