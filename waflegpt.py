# import telebot
from telebot.async_telebot import AsyncTeleBot
import openai
import time
import logging
import asyncio

# from config import *
# import workcsv

bot = AsyncTeleBot('key')  # telebot.TeleBot

tokens = ['token1', 'token2', 'token3', 'token4'] # openai tokens

queue = {}

logging.basicConfig(filename="waflegpt.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.WARNING)
names = ["@WafleGPTBot", "WafleGPT", "waflegpt", "Waflegpt", "Wafle", "Wafl", "wafle", "wafl", "Вафля", "Вафл", "вафля",
         "вафл"]


@bot.message_handler(func=lambda message: (
        "wafl" in message.text.lower() or "вафл" in message.text.lower()) if message.chat.type != "private" else True)
async def WafleGPT(message):
    if message.chat.id in queue:
        queue[message.chat.id].append(message)
    else:
        queue[message.chat.id] = [message]

    botMessage = await bot.reply_to(message, "(1/1)Подключение...▋")
    botMessage2 = ''
    isBotMessage2Visable = False
    lastVal = ''
    maxChars = 3000
    maxCharsAll = 6000
    prevFullReplyContent = ""
    userMessageOpenAI = str(message.text)
    for n in names:
        if n in userMessageOpenAI:
            userMessageOpenAI = userMessageOpenAI.replace(n, "")
    while True:
        if queue[message.chat.id][0] == message:
            try:
                # workcsv.write_data(message.from_user.id, 'user', message.text)
                response = None
                for i in range(len(tokens)):
                    try:
                        openai.api_key = tokens[i]
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            max_tokens=2048,
                            temperature=0.5,
                            stream=True,
                            timeout=15,
                            messages=[
                                {"role": "system",
                                 "content": "Тебя зовут по-разному: Wafle или Wafl или WafleGPT или Вафл или Вафля"},
                                {"role": "user", "content": userMessageOpenAI}
                            ]
                        )
                        tokens.insert(0, tokens.pop(i))
                        break
                    except Exception as e:
                        print(e)
                        await bot.edit_message_text("({}/{})Подключение...▋".format(i + 2, i + 2), botMessage.chat.id,
                                                    botMessage.message_id)

                collected_messages = []
                counter = 0
                for chunk in response:
                    counter += 1
                    chunk_message = chunk['choices'][0]['delta']
                    collected_messages.append(chunk_message)

                    if counter >= 150:
                        full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
                        if full_reply_content.strip() != '' and full_reply_content.strip() != prevFullReplyContent.strip():
                            if len(full_reply_content) < maxChars:
                                await bot.edit_message_text(full_reply_content + "▋", botMessage.chat.id,
                                                            botMessage.message_id)
                            else:
                                if isBotMessage2Visable:
                                    await bot.edit_message_text(
                                        full_reply_content[maxChars:maxCharsAll] + "▋", botMessage2.chat.id,
                                        botMessage2.message_id)
                                else:
                                    await bot.edit_message_text(
                                        full_reply_content[
                                        :maxChars] + "\n\nДальнейшие строки перенесены в другое сообщение",
                                        botMessage.chat.id, botMessage.message_id)
                                    botMessage2 = await bot.reply_to(botMessage,
                                                                     full_reply_content[maxChars:maxCharsAll] + "▋")
                                    isBotMessage2Visable = True

                            prevFullReplyContent = full_reply_content
                            counter = 0

                full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
                # workcsv.write_data(message.from_user.id, 'assistant', full_reply_content)
                if full_reply_content.strip() != '' and full_reply_content.strip() != prevFullReplyContent.strip():
                    if len(full_reply_content) < maxChars:
                        await bot.edit_message_text(full_reply_content, botMessage.chat.id, botMessage.message_id)
                    else:
                        if isBotMessage2Visable:
                            await bot.edit_message_text(
                                full_reply_content[maxChars:maxCharsAll], botMessage2.chat.id, botMessage2.message_id)
                        else:
                            await bot.edit_message_text(
                                full_reply_content[:maxChars] + "\n\nДальнейшие строки перенесены в другое сообщение",
                                botMessage.chat.id, botMessage.message_id)
                            botMessage2 = await bot.reply_to(botMessage, full_reply_content[maxChars:maxCharsAll])
                            isBotMessage2Visable = True

            except Exception as e:
                await bot.reply_to(botMessage if botMessage2 == '' else botMessage2, str(e))

            queue[message.chat.id].remove(message)
            break
        else:
            if str(queue[message.chat.id].index(message)) != lastVal:
                await bot.edit_message_text("Вы " + str(queue[message.chat.id].index(message)) + " в очереди",
                                            botMessage.chat.id,
                                            botMessage.message_id)
                lastVal = str(queue[message.chat.id].index(message))

        time.sleep(2)


asyncio.run(bot.infinity_polling(interval=0, timeout=30))
