from flask import Flask, request
import telebot
import os

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return "Magic Chess Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        
        if text == '/start':
            bot.send_message(chat_id, "မဂ်လာပါ! Magic Chess GOGO ခန့်မှန်းရေး Bot မှကြိုဆိုပါတယ်။\n\n/predict - နောက်ယှဉ်ရမယ့်ပြိုင်ဘက်ကိုခန့်မှန်းပေးမယ်")
        
        elif text == '/predict':
            bot.send_message(chat_id, "ကစားသမား ၇ ယောက်ရဲ့ နာမည်တွေကို ကော်မာခံပြီး ရိုက်ထည့်ပါ။\nဥပမာ: ZawGyi, MgMg, SuSu, KyawKyaw, AyeAye, PhyoPhyo, Thida")
    
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
