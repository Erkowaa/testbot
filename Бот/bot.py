from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Определение состояний
REGISTER, IT_PROBLEM_SELECTION, HINTS_LEVEL_1, HINTS_LEVEL_2, HINTS_LEVEL_3, PROBLEM_DESCRIPTION, EMAIL_REQUEST, ADMIN_REPLY = range(8)

# Список отделов
departments = ['Бухгалтерия', 'Отдел кадров', 'Производственный отдел', 'Административный отдел']

# Список IT проблем
it_problems = ['Проблема с операционной системой', 'Проблема с сетью', 'Проблема с интернетом', 'Проблема с принтером', 'Требуется заведение почты и т.п.']

# Функция для начала регистрации
def start(update, context):
    user = update.message.from_user

    # Проверяем, зарегистрирован ли пользователь
    if 'department' in context.user_data:
        update.message.reply_text(f"Здравствуйте, {user.first_name}! Вы уже зарегистрированы.")
        return it_problem_selection(update, context)

    # Предлагаем пользователю зарегистрироваться
    update.message.reply_text("Добро пожаловать! Пожалуйста, введите ваше ФИО и выберите отдел из списка.",
                              reply_markup=ReplyKeyboardMarkup([departments], one_time_keyboard=True))
    return REGISTER

# Функция для обработки регистрации
def register(update, context):
    user = update.message.from_user
    department = update.message.text

    # Сохраняем информацию о пользователе
    context.user_data['department'] = department

    update.message.reply_text(f"Спасибо, {user.first_name}! Вы успешно зарегистрированы в отделе {department}.")
    return it_problem_selection(update, context)

# Функция для выбора IT проблемы
def it_problem_selection(update, context):
    update.message.reply_text("Пожалуйста, выберите IT проблему из списка.",
                              reply_markup=ReplyKeyboardMarkup([it_problems], one_time_keyboard=True))
    return HINTS_LEVEL_1

# Функция для обработки первого уровня подсказок
def hints_level_1(update, context):
    selected_problem = update.message.text

    # Проверяем выбранную проблему и отправляем подсказки первого уровня
    if selected_problem == 'Проблема с операционной системой':
        update.message.reply_text("Подсказка первого уровня: Перезагрузить компьютер. 2. Проверить подключение к электричеству. 3. Проверить кабели и соединения.")
    elif selected_problem == 'Проблема с сетью':
        update.message.reply_text("Подсказка первого уровня: Перезагрузить маршрутизатор и модем. 2. Проверить подключение кабелей и соединений. 3. Проверить настройки сетевой карты.")
    elif selected_problem == 'Проблема с интернетом':
        update.message.reply_text("Подсказка первого уровня: Проверьте подключение к провайдеру', 'Попробуйте использовать другой браузер', 'Свяжитесь с провайдером")
    elif selected_problem == 'Проблема с принтером':
        update.message.reply_text("Подсказка первого уровня: Проверьте подключение к компьютеру', 'Проверьте наличие бумаги и чернил")
    elif selected_problem == 'Требуется заведение почты и т.п.':
        update.message.reply_text("Подсказка первого уровня: Обратитесь к администратору системы', 'Проверьте настройки почтового клиента', 'Свяжитесь с отделом IT")

    update.message.reply_text("Выберите уровень подсказки: 1, 2 или 3.")
    return HINTS_LEVEL_2

# Функция для обработки второго уровня подсказок
def hints_level_2(update, context):
    selected_level = update.message.text

    # Проверяем выбранный уровень и отправляем подсказки второго уровня
    if selected_level == '1':
        update.message.reply_text("Подсказка второго уровня: ...")
    elif selected_level == '2':
        update.message.reply_text("Подсказка второго уровня: ...")
    elif selected_level == '3':
        update.message.reply_text("Ваша проблема будет передана сисадмину для дальнейшего решения.")

    update.message.reply_text("Если у вас возникли другие вопросы или проблемы, пожалуйста, выберите их из списка или опишите подробнее.")
    return PROBLEM_DESCRIPTION

# Функция для обработки описания проблемы
def problem_description(update, context):
    description = update.message.text
    user = update.message.from_user

    # Отправляем описание проблемы сисадмину
    admin_chat_id = '687940985'  
    admin_message = f"Пользователь {user.first_name} из отдела {context.user_data['department']} описал следующую проблему:\n\n{description}"
    context.bot.send_message(chat_id=admin_chat_id, text=admin_message)

    update.message.reply_text("Спасибо за описание проблемы. Сисадмин скоро рассмотрит вашу заявку.")
    return ConversationHandler.END

# Функция для обработки запроса на создание корпоративной почты
def email_request(update, context):
    update.message.reply_text("Пожалуйста, последовательно заполните форму для создания корпоративной почты.")
    update.message.reply_text("Введите вашу фамилию на латинице.")
    return EMAIL_REQUEST

# Функция для обработки заполнения формы для создания корпоративной почты
def process_email_request(update, context):
    user = update.message.from_user
    surname = update.message.text

    # Сохраняем фамилию пользователя
    context.user_data['surname'] = surname

    update.message.reply_text("Введите ваше имя на латинице.")
    return EMAIL_REQUEST + 1

# Функция для обработки заполнения формы для создания корпоративной почты
def process_email_request_2(update, context):
    user = update.message.from_user
    name = update.message.text

    # Сохраняем имя пользователя
    context.user_data['name'] = name

    update.message.reply_text("Введите вашу личную почту (email).")
    return EMAIL_REQUEST + 2

# Функция для обработки заполнения формы для создания корпоративной почты
def process_email_request_3(update, context):
    user = update.message.from_user
    email = update.message.text

    # Отправляем информацию о заявке на почту админа
    admin_chat_id = '687940985'  
    admin_message = f"Пользователь {user.first_name} из отдела {context.user_data['department']} запросил создание корпоративной почты с следующими данными:\n\nФамилия: {context.user_data['surname']}\nИмя: {context.user_data['name']}\nЛичная почта: {email}"
    context.bot.send_message(chat_id=admin_chat_id, text=admin_message)

    update.message.reply_text("Спасибо за заявку на создание корпоративной почты. Сисадмин скоро рассмотрит вашу заявку.")
    return ConversationHandler.END

# Функция для обработки ответа админа на заявку
def admin_reply(update, context):
    user = update.message.from_user
    reply_text = update.message.text

    # Отправляем ответ админа пользователю
    user_chat_id = '687940985'  # Замените на фактический идентификатор чата пользователя
    context.bot.send_message(chat_id=user_chat_id, text=reply_text)

    update.message.reply_text("Ответ успешно отправлен пользователю.")
    return ConversationHandler.END

# Функция для обработки команды отмены
def cancel(update, context):
    update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END

# Основная функция
def main():
    # Инициализация Telegram Bot API
    updater = Updater(token='6278627089:AAGr4lSwa8yn1QEFFtNCwOklzR5D8DGDS3E', use_context=True)  

    # Инициализация диспетчера
    dispatcher = updater.dispatcher

    # Инициализация ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REGISTER: [MessageHandler(Filters.text, register)],
            IT_PROBLEM_SELECTION: [MessageHandler(Filters.text, it_problem_selection)],
            HINTS_LEVEL_1: [MessageHandler(Filters.text, hints_level_1)],
            HINTS_LEVEL_2: [MessageHandler(Filters.text, hints_level_2)],
            PROBLEM_DESCRIPTION: [MessageHandler(Filters.text, problem_description)],
            EMAIL_REQUEST: [MessageHandler(Filters.text, process_email_request)],
            EMAIL_REQUEST + 1: [MessageHandler(Filters.text, process_email_request_2)],
            EMAIL_REQUEST + 2: [MessageHandler(Filters.text, process_email_request_3)],
            ADMIN_REPLY: [MessageHandler(Filters.text, admin_reply)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Регистрация ConversationHandler в диспетчере
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запуск основной функции
if __name__ == '__main__':
    main()
