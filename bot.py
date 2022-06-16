from telegram import *
import torch
from telegram.ext import *
from requests import *
from PIL import Image
import os
import Inference
from torchvision import transforms
import remedies_rice
import remedies_wheat
import text_to_speech
import translator

global count
updater = Updater(token="5212231888:AAE7Wm-esVXOpyckA2W15hhyFvKbshs1QjQ")
dispatcher = updater.dispatcher
username = ""
FIRST, SECOND = range(2)
HindiLang = "हिन्दी"
PunjLang = "ਪੰਜਾਬੀ"
EngLang = "English"
wheat = ["🌾गेहूँ🌾", "🌾ਕਣਕ🌾", "🌾wheat🌾"]
rice = ["🍚चावल🍚", "🍚ਚੌਲ🍚", "🍚rice🍚"]
lang = ""
crop = 0
fin_rice = {0: "BacterialBlight", 1: "Blast", 2: "Brownspot", 3: "Healthy", 4: "Hispa", 5: "LeafBlast", 6: "Tungro"}
fin_wheat = {0: "Healthy", 1: "leaf rust", 2: "Powdery Mildew", 3: "seedlings", 4: "Septoria", 5: "Stem Rust",
             6: "Yellow rust"}


def startCommand(update: Update, context: CallbackContext):
    global username
    username = update.message.chat_id
    # print(username)
    buttons = [[InlineKeyboardButton(HindiLang, callback_data="Hindi")],
               [InlineKeyboardButton(PunjLang, callback_data="Punjabi")],
               [InlineKeyboardButton(EngLang, callback_data="English")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                             text="🪴🪴🪴Welcome🪴🪴🪴,\n Please select your language.\nकृपया अपनी भाषा चुनें|\nਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ|")
    return FIRST


def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    global lang
    if "Hindi" in query:
        lang = "Hindi"
        buttons = [[InlineKeyboardButton(wheat[0], callback_data="wheat")],
                   [InlineKeyboardButton(rice[0], callback_data="rice")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text="आप किस फसल के बारे में जानना चाहते हैं?")

    if "Punjabi" in query:
        lang = "Punjabi"
        buttons = [[InlineKeyboardButton(wheat[1], callback_data="wheat")],
                   [InlineKeyboardButton(rice[1], callback_data="rice")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text="ਤੁਸੀਂ ਕਿਸ ਫਸਲ ਬਾਰੇ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?")

    if "English" in query:
        lang = "English"
        buttons = [[InlineKeyboardButton(wheat[2], callback_data="wheat")],
                   [InlineKeyboardButton(rice[2], callback_data="rice")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text="Which crop do you want to know about?")

    return SECOND


def send_audio(self, chat_id, audio, caption=None, duration=None, performer=None, title=None,
               reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None,
               timeout=None, thumb=None):
    """
    Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .mp3 format.
    :param chat_id:Unique identifier for the message recipient
    :param audio:Audio file to send.
    :param caption:
    :param duration:Duration of the audio in seconds
    :param performer:Performer
    :param title:Track name
    :param reply_to_message_id:If the message is a reply, ID of the original message
    :param reply_markup:
    :param parse_mode
    :param disable_notification:
    :param timeout:
:param thumb:
    :return: Message
    """
    return types.Message.de_json(
        apihelper.send_audio(self.token, chat_id, audio, caption, duration, performer, title, reply_to_message_id,
                             reply_markup, parse_mode, disable_notification, timeout, thumb))


def model_selection(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()
    # print(query)
    global lang
    global crop
    if query == "wheat":
        # print("aabc")
        # print(lang)
        crop = 1
        # print(crop)
        if lang == "Punjabi":
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਫਸਲ ਦੀਆਂ ਤਸਵੀਰਾਂ ਅਪਲੋਡ ਕਰੋ...")

        if lang == "Hindi":
            context.bot.send_message(chat_id=update.effective_chat.id, text="कृपया अपनी फसल की तस्वीरें अपलोड करें....")
        if lang == "English":
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload the images of your crops...")

    if query == "rice":
        crop = 0
        if lang == "Punjabi":
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਫਸਲ ਦੀਆਂ ਤਸਵੀਰਾਂ ਅਪਲੋਡ ਕਰੋ...")

        if lang == "Hindi":
            context.bot.send_message(chat_id=update.effective_chat.id, text="कृपया अपनी फसल की तस्वीरें अपलोड करें....")

        if lang == "English":
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload the images of your crops...")


def image_handler(update, context):
    global crop
    global lang
    global username
    file = update.message.photo[-1].get_file()
    im = file.download()
    # print(crop)
    if lang == "Hindi":
        update.message.reply_text("कृपया प्रतीक्षा करें|......")

    if lang == "Punjabi":
        update.message.reply_text("ਕ੍ਰਿਪਾ ਕਰਕੇ ਉਡੀਕ ਕਰੋ|......")

    if lang == "English":
        update.message.reply_text("Please wait....")

    if crop == 0:
        prediction = proc_rice(im)
        update.message.reply_text(fin_rice[prediction])
        # update.message.reply_text(remedies_rice.remedy(fin_rice[prediction]))
        translated_text = translator.translation(remedies_rice.remedy(fin_rice[prediction]), lang)
        update.message.reply_text(translated_text)
        text_to_speech.text_to_speech(text=translated_text, file_name=username)
        # sendAudio(username,f"{username}.mp3")
        # context.bot.sendAudio(username,f"/home/kratoes669/{username}.mp3")
        # send_audio(self, username,f"/home/kratoes669/{username}.mp3")
        context.bot.send_audio(chat_id=username, audio=open(f"/home/kratoes669/{username}.mp3", 'rb'))


    elif crop == 1:
        prediction = proc_wheat(im)
        for i in range(6):
            if prediction[i][1]>0.5:
                update.message.reply_text(prediction[i][0])
                # update.message.reply_text(remedies_wheat.remedy(fin_wheat[i]))
                translated_text = translator.translation(remedies_wheat.remedy(prediction[i][0]), lang)
                update.message.reply_text(translated_text)
                text_to_speech.text_to_speech(text=translated_text, file_name=username)
        # update.message.reply_text(fin_wheat[prediction])
        # # update.message.reply_text(remedies_rice(fin_wheat[prediction]))
        # translated_text = translator.translation(remedies_wheat.remedy(fin_wheat[prediction]), lang)

        # sendAudio(username,f"{username}.mp3")


def proc_rice(im):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = torch.load('/home/kratoes669/PycharmProjects/Crop_Saviour/rice.pt')
    path_full = os.path.join('/home/kratoes669/', im)
    img = Image.open(path_full)

    tfms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img_t = tfms(img)
    img_t = img_t.unsqueeze(0)
    img_t = img_t.to(device)
    output = model(img_t)
    prediction = int(torch.max(output.cpu().data, 1)[1].numpy())
    return prediction


def proc_wheat(im):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # model_w = torch.load('/home/kratoes669/PycharmProjects/Crop_Saviour/wheat.pt')
    path_full = os.path.join('/home/kratoes669/', im)
    pred=Inference.DiseaseClassification(filename = path_full)
    # tfms = transforms.Compose([
    #     transforms.Resize(256),
    #     transforms.CenterCrop(224),
    #     transforms.ToTensor(),
    #     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    # ])
    # img_t = tfms(img)
    # img_t = img_t.unsqueeze(0)
    # img_t = img_t.to(device)
    # output = model_w(img_t)
    # prediction = int(torch.max(output.cpu().data, 1)[1].numpy())
    return pred


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', startCommand)],
    states={
        FIRST: [CallbackQueryHandler(queryHandler)],
        SECOND: [CallbackQueryHandler(model_selection)],
    },
    fallbacks=[CommandHandler('start', startCommand)]
)

# updater.
dispatcher.add_handler(conv_handler)

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))
dispatcher.add_handler(CallbackQueryHandler(model_selection))
dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))

updater.start_polling()
