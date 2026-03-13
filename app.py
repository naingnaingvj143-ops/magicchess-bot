import telebot
from telebot import types
import os
from flask import Flask
import threading

# Bot Token
TOKEN = "8696380329:AAEF-2jNWen-AsANOozyD6mb9nzVMqGNzRs"
bot = telebot.TeleBot(TOKEN)
user_status = {}

server = Flask(__name__)

@server.route("/")
def index():
    return "Bot is running!", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Magic Chess Bot (Cloud) အဆင်သင့်ဖြစ်ပါပြီ။\n/predict ကို နှိပ်ပါ။")

@bot.message_handler(commands=['predict'])
def ask_players(message):
    msg = bot.send_message(message.chat.id, "နာမည် ၇ ခုကို ကော်မာ (,) ခံပြီး ပို့ပေးပါ။")
    bot.register_next_step_handler(msg, process_prediction)

def process_prediction(message):
    try:
        players = [name.strip() for name in message.text.split(',')]
        user_status[message.chat.id] = {'players': players, 'index': 0}
        show_prediction(message.chat.id, message.message_id, is_new=True)
    except:
        bot.reply_to(message, "မှားယွင်းနေပါတယ်။ /predict ကို ပြန်နှိပ်ပါ။")

def show_prediction(chat_id, message_id, is_new=False):
    status = user_status.get(chat_id)
    if not status: return
    players = status['players']
    idx = status['index']
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⏭️ Next Player (အစဉ်လိုက်)", callback_data="next_step"))
    text = f"🔮 **Magic Chess ခန့်မှန်းချက်**\n\nယခုပြိုင်ဘက်: **{players[idx]}**"
    if is_new:
        bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "next_step")
def callback_next(call):
    chat_id = call.message.chat.id
    if chat_id in user_status:
        user_status[chat_id]['index'] = (user_status[chat_id]['index'] + 1) % len(user_status[chat_id]['players'])
        show_prediction(chat_id, call.message.message_id)

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
    
