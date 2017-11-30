import telegram

bot = telegram.Bot(token='481861352:AAHC418jtyRpkSh1TLFGvk97xqHOVHX6MN0')

response = bot.getUpdates()
for message in response:
    print(message)