import telebot
import openai
import time
import pandas as pd
from config import apiKeyTelegram, apiKeyOpenAI

bot = telebot.TeleBot(apiKeyTelegram)
openai.api_key = apiKeyOpenAI

queue = []


@bot.message_handler(func=lambda message: True)
def generate_reply(message):
    queue.append(message)
    botMessage = bot.reply_to(message, "...")
    botMessage2 = ''
    isBotMessage2Visable = False
    lastVal = ''
    maxChars = 3000
    while True:
        if queue[0] == message:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens=2048,
                temperature=0.5,
                stream=True,
                messages=[
                    {"role": "system",
                     "content": "Тебя зовут WafleGPT или Вафля и ты создана двумя мирэашниками Колей и Ваней"},
                    {"role": "user", "content": "Привет, как твои делишки"},
                    {"role": "assistant", "content": "Привет, у меня всё здорово"},
                    {"role": "user", "content": message.text},
                ]
            )

            collected_messages = []
            counter = 0
            for chunk in response:
                counter += 1
                chunk_message = chunk['choices'][0]['delta']
                collected_messages.append(chunk_message)

                if counter >= 150:
                    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
                    if full_reply_content != '':
                        if len(full_reply_content) < maxChars:
                            bot.edit_message_text(full_reply_content, botMessage.chat.id, botMessage.message_id)
                        else:
                            if isBotMessage2Visable:
                                bot.edit_message_text(
                                    full_reply_content[maxChars:], botMessage2.chat.id, botMessage2.message_id)
                            else:
                                bot.edit_message_text(
                                    full_reply_content[
                                    :maxChars] + "\n\nДальнейшие строки перенесены в другое сообщение",
                                    botMessage.chat.id, botMessage.message_id)
                                botMessage2 = bot.reply_to(botMessage, full_reply_content[maxChars:])
                                isBotMessage2Visable = True

                        counter = 0

            full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
            if full_reply_content != '':
                if len(full_reply_content) < maxChars:
                    bot.edit_message_text(full_reply_content, botMessage.chat.id, botMessage.message_id)
                else:
                    if isBotMessage2Visable:
                        bot.edit_message_text(
                            full_reply_content[maxChars:], botMessage2.chat.id, botMessage2.message_id)
                    else:
                        bot.edit_message_text(
                            full_reply_content[:maxChars] + "\n\nДальнейшие строки перенесены в другое сообщение",
                            botMessage.chat.id, botMessage.message_id)
                        botMessage2 = bot.reply_to(botMessage, full_reply_content[maxChars:])
                        isBotMessage2Visable = True

            queue.remove(message)
            break
        else:
            if str(queue.index(message)) != lastVal:
                bot.edit_message_text("Вы " + str(queue.index(message)) + " в очереди", botMessage.chat.id,
                                      botMessage.message_id)
                lastVal = str(queue.index(message))

        time.sleep(5)


bot.infinity_polling(none_stop=True, interval=0, timeout=30)
