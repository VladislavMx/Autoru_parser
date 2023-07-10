import requests #Библиотека для запроса
import telebot
from telegram import InputMediaPhoto
import numpy

global price, cars_amnt

bot = telebot.TeleBot("")

@bot.message_handler(content_types=['text'])
def start_function(message):
    if message.text == "/start":
        open('Save_auto.txt', 'w').close()
        bot.send_message(message.from_user.id, "Max price:")
    bot.register_next_step_handler(message, cars_amount)

def cars_amount(message):
    global price
    price = int(message.text)
    message = bot.send_message(message.from_user.id, "Amount of cars:")
    bot.register_next_step_handler(message, pars_autoru)

def pars_autoru(message):
    print(1)
    cars_amnt = int(message.text)
    a = 1 #Переменная для перехода по страницам
    while a <= (cars_amnt//38)+1: #Всего 99 страниц на сайте
        #Объявление переменных как глобальные
        global  Price_rub,img, Model_auto, Marka_info
        URL = 'https://auto.ru/-/ajax/desktop/listing/' #URL на который будет отправлен запрос

        #Параметры запроса
        PARAMS = {
             'catalog_filter' : [{"mark": "NISSAN"}],
             'section': "all",
             'category': "cars",
             'sort': "fresh_relevance_1-desc",
             'page': a,
             'price_to': price
            }
        #Заголовки страницы
        HEADERS = {
            'Accept': '',
            'Accept-Encoding': '',
            'Accept-Language': '',
            'Connection': '',
            'Content-Length': '',
            'content-type': '',
            'Cookie': '',
            'Host': '',
            'origin': '',
            'Referer': '',
            'User-Agent': '',
            'x-client-app-version': '',
            'x-client-date': '',
            'x-csrf-token': '',
            'x-page-request-id': '',
            'x-requested-with': ""
        }

        response = requests.post(URL, json=PARAMS, headers=HEADERS) #Делаем post запрос на url
        data = response.json()['offers'] #Переменная data хранит полученные объявления

        if cars_amnt > len(data):

            return "no cars found"

        img_url = []
        i = 0 #Переменная для перехода по объявлениям
        while i <= cars_amnt - 1: #len(data)-1 это количество пришедших объявлений

            #Цена в рублях, евро и долларах
            try: Price_rub = 'Цена: ' + str(data[i]['price_info']['RUR']) + '₽'
            except: Price_rub = 'Not price rub'

            #Картинки автомобиля
            #Возвращается несколько фото, мы их добавляем в словарь img_url
            for img in data[i]['state']['image_urls']:
                img_url.append(img['sizes']['1200x900'])

            #Название автомобиля
            try: Model_info = 'Модель автомобиля: ' + str(data[i]['vehicle_info']['model_info']['name'])
            except: Model_info = 'Not model info'

            #Марка автомобиля
            try: Marka_info = 'Марка автомобиля: ' + str(data[i]['vehicle_info']['mark_info']['name'])
            except: Marka_info = 'Not marka info'

            link_img = [] #Переменная для ссылок
            for link_img_0 in img_url: #Перебираем ссылки из словаря img_url, и записываем их в одну переменную текстом
                link_img += str(link_img_0) + '\n'

            #Переменная в которую всё записываем
            text = Model_info + "\n" + Marka_info +"\n" + Price_rub + "\n"

            bot.send_photo(message.from_user.id, "https:"+img_url[0], caption=text)
            img_url = []
            i += 1 #Увеличиваем переменную перехода по объявлениям на 1
        print('Page: ' + str(a)) #Выводим сообщение, какая страница записалась
        a += 1 #Увеличиваем переменную страницы сайта на 1
    print('Successfully') #Выводим информацию об успешном выполнении


bot.polling(none_stop=True, interval=0)