from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telethon import TelegramClient, sync
from pyrogram import *
from telebot import *
import telebot
import logging
from .models import *
import xlwt
import datetime


logger = telebot.logger
# https://ok-business.herokuapp.com/register 
# https://api.telegram.org/bot5438036163:AAEZVa8ils-KkBQn6pxw-QboPEdttz9Mows/setWebhook?url=https://okk-business.herokuapp.com/register/api/
bot = telebot.TeleBot("5438036163:AAEZVa8ils-KkBQn6pxw-QboPEdttz9Mows") 
# bot = telebot.TeleBot("5030280895:AAEhFHbB1DpjesuvuAK8UG-YP-1TJqyulRg") #test token

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url Page")
    elif request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def greeting(message):  
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Ro'yxatdan o'tish")
    markup.add(btn1)
    if len(BotUser.objects.filter(user_id=message.from_user.id)) == 0:
        bot_user = BotUser.objects.create(
            user_id=message.from_user.id,
            first_name=message.from_user.username,
            permission='candidate',
            )
        bot_user.save()
        bot.send_message(message.from_user.id,
                  f'Assalomu alaykum {message.from_user.username}.\nBotga xush kelibsiz.\nBu yerda siz OK Business Group kompaniyasida ishlash uchun ariza qoldirishingi mumkin.',reply_markup=markup)
    elif len(BotUser.objects.filter(user_id=message.from_user.id, permission='candidate')) > 0:
        # print(BotUser.objects.filter(user_id=message.from_user.id, permission='candidate'))
        bot.send_message(message.from_user.id,
                  f'Assalomu alaykum {message.from_user.username}.\nBotga xush kelibsiz.\nBu yerda siz OK Business Group kompaniyasida ishlash uchun ariza qoldirishingi mumkin.',reply_markup=markup)
    else:     
        bot_user = BotUser.objects.get(user_id=message.from_user.id)   
        if bot_user.permission == "admin":
            admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_excel = types.KeyboardButton("Excelga import qilish")
            admin.add(btn_excel)
            bot.send_message(message.from_user.id, f"Salom {message.from_user.first_name}.\nBu yerda siz mavjud arizalarni yuklab olishingiz mumkin.", reply_markup=admin)
    
    
@bot.message_handler(func=lambda message: True)
def register(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Ro'yxatdan o'tish")
    markup.add(btn1)
    ads_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    ads_1 = types.KeyboardButton("OLX")
    ads_2 = types.KeyboardButton("Telegram")
    ads_3 = types.KeyboardButton("Instagram")
    ads_4 = types.KeyboardButton("Facebook")
    ads_5 = types.KeyboardButton("Boshqa")
    ads_markup.add(ads_1, ads_2, ads_3, ads_4, ads_5)
    if message.text == 'Ro\'yxatdan o\'tish':
        if len(Candidate.objects.filter(user_id=message.from_user.id)) == 0:
            client = Candidate.objects.create(
                user_id=message.from_user.id,
                fullname=message.from_user.first_name)
            client.step = 1
            client.on_process = True
            client.save()
            bot.send_message(message.from_user.id, "Qaysi e'lon orqali bizni topdingiz?", reply_markup=ads_markup)
        else:
            bot.send_message(message.from_user.id, "Siz allaqachon ro'yxatdan o'tgansiz.")
    elif message.text == "Excelga import qilish":
        b = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Faylni yuklash.", url="https://ok-business.herokuapp.com/register/excel")
        b.add(btn)
        bot.send_message(message.from_user.id, "Excel faylni yuklash uchun quyidagi tugmani bosing.", reply_markup=b)
        
    elif message.text == 'Orqaga ↩️':
        client = Candidate.objects.filter(user_id=message.from_user.id, on_process=True).last()
        client.step -= 1
        client.save()
        cancel_func(message)
    elif message.text == 'Bekor qilish 🚫':
        client = Candidate.objects.filter(user_id=message.from_user.id, on_process=True).last()
        client.delete()
        bot.send_message(message.from_user.id,
                         "*Sizning arizangiz bekor qilindi.*\n", parse_mode="Markdown", reply_markup=markup)
    elif message.text == "Tasdiqlash✅":
        client = Candidate.objects.filter(user_id=message.from_user.id, on_process=True).last()
        client.on_process = False
        filled_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        client.filled_date = filled_date
        client.save()
        bot.send_message(message.from_user.id, "Ro'yxatdan muvaffaqiyatli o'tdingiz. Ma'lumotlaringizni o'rganib chiqib, mas'ul xodim sizga aloqaga chiqadi.", reply_markup=markup)

    else:
        client = Candidate.objects.filter(user_id=message.from_user.id, on_process=True).last()
        secondary = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Orqaga ↩️')
        btn2 = types.KeyboardButton('Bekor qilish 🚫')
        secondary.add(btn1, btn2)

        if client.step == 1:
            client.ads_type = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Familiya, Ism va Sharifingizni to'liq holatda kiriting.", reply_markup=secondary)
        elif client.step == 2:
            client.fullname = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, 'Necha yoshdasiz?', reply_markup=secondary)
        elif client.step == 3:
            if str(message.text).isdigit():
                client.age = message.text
                client.step += 1
                client.save()
                bot.send_message(message.from_user.id, "Telefon raqamingizni 9xxxxxxxx ko'rinishda kiriting.", reply_markup=secondary)
            else:
                bot.send_message(message.from_user.id, 'Iltimos, yoshingizni faqat raqamlarda kiriting.', reply_markup=secondary)
        elif client.step == 4:
            if str(message.text).isdigit():
                client.contact_number = message.text
                client.step += 1
                client.save()
                bot.send_message(message.from_user.id, 'Ayni paytdagi yashash manzilingizni kiriting.', reply_markup=secondary)
            else:
                bot.send_message(message.from_user.id, "Iltimos, to'g'ri ma'lumot kiriting.", reply_markup=secondary)
                bot.send_message(message.from_user.id, "Telefon raqamingizni 9xxxxxxxx ko'rinishda kiriting.", reply_markup=secondary)
        elif client.step == 5:
            client.address = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Ma'lumotingiz turini kiriting. (Oliy, o'rta va h.k.)", reply_markup=secondary)
        elif client.step == 6:
            client.education = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Ilk mablag'ingizni necha yoshda ishlab topgansiz?", reply_markup=secondary)
        elif client.step == 7:
            if str(message.text).isdigit():
                client.first_salary = message.text
                client.step += 1
                client.save()
                bot.send_message(message.from_user.id, 'Avvalgi ish joyingizni kiriting.', reply_markup=secondary)
            else:
                bot.send_message(message.from_user.id, "Iltimos, yoshingizni faqat raqamlarda kiriting.", reply_markup=secondary)
        elif client.step == 8:
            client.ex_workplace = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Ishdan bo'sh vaqtingizni nimalar bilan shug'ullanasiz?", reply_markup=secondary)
        elif client.step == 9:
            client.leisure_activities = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, 'Hayotingizda nima bilan faxrlanasiz, ehtiyojlardan ortiq nimalar qilgansiz?', reply_markup=secondary)
        elif client.step == 10:
            client.achievements = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Avvalgi ish joyingizdagi maoshingiz qancha bo'lgan?", reply_markup=secondary)
        elif client.step == 11:
            if str(message.text).isdigit():
                client.ex_salary = message.text
                client.step += 1
                client.save()
                bot.send_message(message.from_user.id, 'Qanacha maoshlik ish izlayapsiz?', reply_markup=secondary)
            else:
                bot.send_message(message.from_user.id, "Iltimos, to'g'ri ma'lumot kiriting.", reply_markup=secondary)
                bot.send_message(message.from_user.id, "Avvalgi ish joyingizdagi maoshingiz qancha bo'lgan? (faqat raqamlarda kiriting.)", reply_markup=secondary)
        elif client.step == 12:
            if str(message.text).isdigit():
                client.expected_salary = message.text
                client.step += 1
                client.save()
                bot.send_message(message.from_user.id, 'Qancha maoshdan boshlashga tayyorsiz?', reply_markup=secondary)
            else:
                bot.send_message(message.from_user.id, "Iltimos, to'g'ri ma'lumot kiriting.", reply_markup=secondary)
                bot.send_message(message.from_user.id, "Qanacha maoshlik ish izlayapsiz? (faqat raqamlarda kiriting.)", reply_markup=secondary)

        elif client.step == 13:
            if str(message.text).isdigit():
                client.start_salary = message.text
                client.step += 1
                client.save()
                bot.send_message(message.from_user.id, "Nima deb o'ylaysiz, kompaniya nima uchun pul to'laydi?", reply_markup=secondary)
            else:
                bot.send_message(message.from_user.id, "Iltimos, to'g'ri ma'lumot kiriting.", reply_markup=secondary)
                bot.send_message(message.from_user.id, "Qancha maoshdan boshlashga tayyorsiz? (faqat raqamlarda kiriting.)", reply_markup=secondary)
        elif client.step == 14:
            client.salary_factor = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Aytingchi, qanday xodimni eng zo'r kadr deyish mumkin?", reply_markup=secondary)
        elif client.step == 15:
            client.best_employee = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, 'Oilaviy holatingiz qanday? (Turmush qurgan/qurmagan, birga yashaymiz va h.k.)', reply_markup=secondary)
        elif client.step == 16:
            client.marital_status = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Kitob o'qiysizmi, aga o'qisangiz, qaysi kitoblarni.", reply_markup=secondary)
        elif client.step == 17:
            client.book = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, 'Zararli odatlaringiz bormi?', reply_markup=secondary)
        elif client.step == 18:
            client.bad_habit = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, 'Avvalgi ishingizda qanday yuqori natijalarga erishgansiz va buni kim tasdiqlay oladi? (ularning ismlari va telefon raqamini kiriting.)', reply_markup=secondary)
        elif client.step == 19:
            client.work_achievements = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, 'Qanchalik tez boshlay olasiz?', reply_markup=secondary)
        elif client.step == 20:
            markup_confirm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton("Tasdiqlash✅")
            btn2 = types.KeyboardButton("Bekor qilish 🚫")
            markup_confirm.add(btn1, btn2)
            client.ready_to_start = message.text
            client.step += 1
            client.save()
            bot.send_message(message.from_user.id, "Ro'yxatdan o'tish yakunlandi.")
            bot.send_message(message.from_user.id, "Iltimos, ma'lumotlaringiz to'g'riligini tekshirib chiqing.")
            bot.send_message(message.from_user.id, f"Bizni qaysi manba orqali topdingiz: {client.ads_type}\nFISH: {client.fullname}\nYoshi: {client.age}\nTelefon raqami: {client.contact_number}\nYashash manzili: {client.address}\nMa'lumotingiz: {client.education}\nIlk mablag'ingizni ishlab topgan yoshingiz: {client.first_salary}\nAvvalgi ish joyi: {client.ex_workplace}\nIshdan tashqari mashg'ulotlari: {client.leisure_activities}\nHayotingizda nimalar bilan faxrlanasiz, ehtiyojlardan ortiq nimalar qilgansiz: {client.achievements}\nAvvalgi ish joyingizdagi maoshingiz: {client.ex_salary}\nQancha maoshli ish izlayapsiz: {client.expected_salary}\nQancha maoshdan boshlashga tayyorsiz: {client.start_salary}\nNima deb o'ylaysiz kompaniya nima uchun pul to'laydi: {client.salary_factor}\nAytingchi qanday xodimni eng zo'r kadr deyish mumkin: {client.best_employee}\nOilaviy holatingiz qanday: {client.marital_status}\nKitob o'qiysizmi: {client.book}\nZararli odatlaringiz bormi: {client.bad_habit}\nAvvalgi ishingizda qanday yuqori natijalarga erishgansiz: {client.work_achievements}\nQanchalik tez ish boshlay olasiz: {client.ready_to_start}", reply_markup=markup_confirm)


def cancel_func(message):
    client = Candidate.objects.get(user_id=message.from_user.id, on_process=True) 
    secondary = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Orqaga ↩️')
    btn2 = types.KeyboardButton('Bekor qilish 🚫')
    secondary.add(btn1, btn2)

    ads_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    ads_1 = types.KeyboardButton("OLX")
    ads_2 = types.KeyboardButton("Telegram")
    ads_3 = types.KeyboardButton("Instagram")
    ads_4 = types.KeyboardButton("Facebook")
    ads_5 = types.KeyboardButton("Boshqa")
    ads_markup.add(ads_1, ads_2, ads_3, ads_4, ads_5)

    if client.step == 1:
        bot.send_message(message.from_user.id, "Qaysi e'lon orqali bizni topdingiz?", reply_markup=ads_markup)
    elif client.step == 2:
        bot.send_message(message.from_user.id, "Familiya, Ism va Sharifingizni to'liq holatda kiriting.", reply_markup=secondary)
    elif client.step == 3:
        bot.send_message(message.from_user.id, 'Necha yoshdasiz?', reply_markup=secondary)
    elif client.step == 4:
        bot.send_message(message.from_user.id, "Telefon raqamingizni 9xxxxxxxx ko'rinishda kiriting.", reply_markup=secondary)
    elif client.step == 5:
        bot.send_message(message.from_user.id, 'Ayni paytdagi yashash manzilingizni kiriting.', reply_markup=secondary)
    elif client.step == 6:
        bot.send_message(message.from_user.id, "Ma'lumotingiz turini kiriting. (Oliy, o'rta va h.k.)", reply_markup=secondary)
    elif client.step == 7:
        bot.send_message(message.from_user.id, "Ilk mablag'ingizni necha yoshda ishlab topgansiz?", reply_markup=secondary)
    elif client.step == 8:
        bot.send_message(message.from_user.id, 'Avvalgi ish joyingizni kiriting.', reply_markup=secondary)
    elif client.step == 9:
        bot.send_message(message.from_user.id, "Ishdan bo'sh vaqtingizni nimalar bilan shug'ullanasiz?", reply_markup=secondary)
    elif client.step == 10:
        bot.send_message(message.from_user.id, "Hayotingizda nima bilan faxrlanasiz, ehtiyojlardan ortiq nimalar qilgansiz?", reply_markup=secondary)
    elif client.step == 11:
        bot.send_message(message.from_user.id, "Avvalgi ish joyingizdagi maoshingiz qancha bo'lgan?", reply_markup=secondary)
    elif client.step == 12:
        bot.send_message(message.from_user.id, 'Qanacha maoshlik ish izlayapsiz?', reply_markup=secondary)
    elif client.step == 13:
        bot.send_message(message.from_user.id, 'Qancha maoshdan boshlashga tayyorsiz?', reply_markup=secondary)
    elif client.step == 14:
        bot.send_message(message.from_user.id, "Nima deb o'ylaysiz, kompaniya nima uchun pul to'laydi?", reply_markup=secondary)
    elif client.step == 15:
        bot.send_message(message.from_user.id, "Aytingchi, qanday xodimni eng zo'r kadr deyish mumkin?", reply_markup=secondary)
    elif client.step == 16:
        bot.send_message(message.from_user.id, 'Oilaviy holatingiz qanday? (Turmush qurgan/qurmagan, birga yashaymiz va h.k.)', reply_markup=secondary)
    elif client.step == 17:
        bot.send_message(message.from_user.id, "Kitob o'qiysizmi, aga o'qisangiz, qaysi kitoblarni.", reply_markup=secondary)
    elif client.step == 18:
        bot.send_message(message.from_user.id, 'Zararli odatlaringiz bormi?', reply_markup=secondary)
    elif client.step == 19:
        bot.send_message(message.from_user.id, 'Avvalgi ishingizda qanday yuqori natijalarga erishgansiz va buni kim tasdiqlay oladi? (ularning ismlari va telefon raqamini kiriting.)', reply_markup=secondary)
    elif client.step == 20:
        bot.send_message(message.from_user.id, 'Qanchalik tez boshlay olasiz?', reply_markup=secondary)


def export_candidates(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="arizalar.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Arizalar')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [ 
                'Biz qanday topgan',
                'FISH', 
                'Yoshi', 
                'Telefon raqami', 
                'Manzili', 
                "Ma'lumoti", 
                "Ilk maoshni ishlab topgan yoshi", 
                "Avvalgi ish joyi", 
                "Ishdan tashqari mashg'ulotlari", 
                "Yutuqlari", 
                "Avvalgi maoshi", 
                "Qancha maoshlik ish izlamoqda", 
                "Qancha maoshdan boshlay oladi", 
                "Kompaniya nima uchun pul to'laydi", 
                "Eng yaxshi xodim", 
                "Oilaviy holati", 
                "O'qiydigan kitoblari", 
                "Yomon odatlari", 
                "Ishdagi yutuqlari", 
                "Ishni qanchada boshlay oladi",
                "Ariza to'ldirgan sana"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    font_style = xlwt.XFStyle()
    rows = Candidate.objects.all().values_list(
        'ads_type',
        'fullname', 
        'age', 
        'contact_number', 
        'address',
        'education',
        'first_salary',
        'ex_workplace',
        'leisure_activities',
        'achievements',
        'ex_salary',
        'expected_salary',
        'start_salary',
        'salary_factor',
        'best_employee',
        'marital_status',
        'book',
        'bad_habit',
        'work_achievements',
        'ready_to_start',
        'filled_date'
        )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

bot.polling()
telebot.logger.setLevel(logging.DEBUG)