from tvDatafeed import TvDatafeed, Interval
import ta
from telegram import Bot
import schedule
import time

BOT_TOKEN = "8568034921:AAGmxegwUnkTYwRGOTnm2uYUhTDyhQuK3T0"
CHAT_ID = "8334695382"

bot = Bot(token=BOT_TOKEN)
tv = TvDatafeed()

pairs = ["EURUSD", "GBPUSD"]

def analyze():
    for symbol in pairs:

        df = tv.get_hist(symbol=symbol,
                         exchange='FX_IDC',
                         interval=Interval.in_1_minute,
                         n_bars=200)

        df['ema20'] = ta.trend.ema_indicator(df['close'], 20)
        df['ema50'] = ta.trend.ema_indicator(df['close'], 50)
        df['rsi'] = ta.momentum.rsi(df['close'], 14)

        last = df.iloc[-1]

        score = 0
        direction = None

        if last['ema20'] > last['ema50']:
            direction = "BUY"
            score += 50
        elif last['ema20'] < last['ema50']:
            direction = "SELL"
            score += 50

        if 40 < last['rsi'] < 60:
            score += 20

        if score >= 70:

            message = f"""
🚨 SIGNAL ALERT

Pair: {symbol}
Direction: {direction}
Expiry: 3 Minutes
Confidence: High

Trade safe ⚠️
"""

            bot.send_message(chat_id=CHAT_ID, text=message)

schedule.every(60).seconds.do(analyze)

while True:
    schedule.run_pending()
    time.sleep(1)
