import os
import telebot
from src.data import connection as conn
from sqlalchemy.sql import select
from datetime import datetime

token = os.getenv('TOKEN')
bot = telebot.TeleBot('5734830398:AAGoAWzEuZ9YdSXaEda5tmz3MW2UT95hhkc')


@bot.message_handler(commands=['hi'])
def hi(message):
    bot.reply_to(message, "Wellcome to use mrt bot! \nPlease select train line: r, g, b")


def crowd_request(message):
    request = message.text.split()
    if request[0].lower() in "rgb":
        return True

@bot.message_handler(func=crowd_request)
def crowd(message):
    select_c1 = """select density from crowd where carriage_id = 1 order by timestamp desc limit 1;"""
    select_c2 = """select density from crowd where carriage_id = 2 order by timestamp desc limit 1;"""
    select_c3 = """select density from crowd where carriage_id = 3 order by timestamp desc limit 1;"""
    crowd_c1 = conn.execute(select_c1).fetchall()[0][0]
    crowd_c2 = conn.execute(select_c2).fetchall()[0][0]
    crowd_c3 = conn.execute(select_c3).fetchall()[0][0]

    print(crowd_c1)

    resp = f'The crowdedness of next train is: \n carriage1:{crowd_c1}/40  \n carriage2:{crowd_c2}/40 \n carriage3:{crowd_c3}/40'

    bot.send_message(message.chat.id, resp)


@bot.message_handler(commands=['crowd'])
def hello(message):
    resp = f'The crowdedness in this cabin is{data_operation.count_crowd()}/40'
    bot.send_message(message.chat.id, resp)




bot.polling()
