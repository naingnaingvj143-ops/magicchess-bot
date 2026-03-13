import telebot
from telebot import types
import os
from flask import Flask
import threading

# Bot Token
TOKEN = "8696380329:AAEF-2jNWen-AsANOozyD6mb9nzVMqGNzRs"
bot = telebot.TeleBot(TOKEN)

# User တစ်ဦးချင်းစီရဲ့ အစဉ်လိုက်အခြေအနေကို မှတ်ထားရန်
user_status = {}

# Render Cloud Error မတက်စေရန် အသေးစား Web Server တစ်ခုဆောက်ခြင်း
server = Flask(__name__)

@server.route("/")
def index():
    return "Bot is running on Cloud!", 200

# /start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "မဂ်လာပါ! Magic Chess Bot (Cloud Version) ဖြစ်ပါတယ်။\n\n/predict ကို နှိပ်ပြီး နာမည် ၇ ခုကို အစဉ်လိုက်အတိုင်း ပို့ပေးပါ။")

# /predict Command
@bot.message_handler(commands=['predict'])
def ask_players(message):
    msg = bot.send_message(message.chat.id, "ကစားသမား ၇ ယောက်ရဲ့ နာမည်တွေကို အစဉ်လိုက်အတိုင်း ကော်မာ (,) ခံပြီး ပို့ပေးပါ။\nဥပမာ- Ry,Oo,Pu,Ao,Bs,Ke,Joker")
    bot.register_next_step_handler(msg, process_prediction)

def process_prediction(message):
    try:
        # နာမည်များကို ခွဲထုတ်ပြီး list ထဲထည့်ခြင်း
        players = [name.strip() for name in message.text.split(',')]
        
        if len(players) < 1:
            bot.reply_to(message, "⚠️ နာမည်များကို သေချာပြန်ထည့်ပေးပါ။")
            return
            
        # ပထမဆုံးလူကနေ စတင်ရန် index 0 သတ်မှတ်
        user_status[message.chat.id] = {'players': players, 'index': 0}
        
        # ပထမဆုံးခန့်မှန်းချက်ကို ပြသရန်
        show_prediction(message.chat.id, message.message_id, is_new=True)
    except Exception as e:
        bot.reply_to(message, "မှားယွင်းနေပါတယ်။ /predict ကို ပြန်နှိပ်ပါ။")

# ခန့်မှန်းချက်ပြသခြင်းနှင့် Next ခလုတ်ထည့်ခြင်း
def show_prediction(chat_id, message_id, is_new=False):
    status = user_status.get(chat_id)
    if not status: return

    players = status['players']
    idx = status['index']
    current_player = players[idx]
    
    markup = types.InlineKeyboardMarkup()
    next_button = types.InlineKeyboardButton("⏭️ Next Player (အစဉ်လိုက်)", callback_data="next_step")
    markup.add(next_button)
    
    text = f"🔮 **Magic Chess ခန့်မှန်းချက်**\n\nယခုယှဉ်ပြိုင်ရမည့်သူ: **{current_player}**\n\n(ကျော်လို့မရဘဲ အစဉ်လိုက် ပြသနေပါသည်)"
    
    if is_new:
        bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)

# Next ခလုတ်နှိပ်သည့်အခါ နောက်တစ်ယောက်သို့ ပြောင်းရန်
@bot.callback_query_handler(func=lambda call: call.data == "next_step")
def callback_next(call):
    chat_id = call.message.chat.id
    if chat_id in user_
