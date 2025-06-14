from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests

TELEGRAM_TOKEN = "7628017221:AAF9vsP99Bwc8IQhrOWaaCUumFy-hWcjGnQ"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في بوت تتبع الأسعار في KuCoin.\n\nاكتب الأمر بالشكل:\n\nprice BTC-USDT"
    )

# أمر تلقائي لقراءة أي رسالة فيها كلمة "price"
async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    if message.lower().startswith("price"):
        try:
            _, symbol = message.split(" ", 1)
            url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol.upper()}"
            response = requests.get(url).json()

            if 'data' in response:
                price = response['data']['price']
                await update.message.reply_text(f"💰 سعر {symbol.upper()} الآن: {price} USDT")
            else:
                await update.message.reply_text("❌ لم أتمكن من جلب السعر. تحقق من الرمز.")

        except Exception as e:
            await update.message.reply_text("❌ هناك مشكلة في معالجة الأمر. تأكد من الصيغة: price BTC-USDT")

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price))
    print("✅ Bot is running...")
    app.run_polling()
