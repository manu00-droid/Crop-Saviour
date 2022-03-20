from telegram import *
import torch
from telegram.ext import * 
from requests import *
from PIL import Image
import os
from torchvision import transforms
global count
updater = Updater(token="5212231888:AAE7Wm-esVXOpyckA2W15hhyFvKbshs1QjQ")
dispatcher = updater.dispatcher

HindiLang = "हिन्दी"
PunjLang = "ਪੰਜਾਬੀ"
EngLang = "English"

fin={0:"BacterialBlight",1:"Blast",2:"Brownspot",3:"Healthy",4:"Hispa",5:"LeafBlast",6:"Tungro"}

def startCommand(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton(HindiLang, callback_data = "Hindi")], [InlineKeyboardButton(PunjLang, callback_data = "Punjabi")], [InlineKeyboardButton(EngLang, callback_data = "English")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Welcome,\n Please select your language.\nकृपया अपनी भाषा चुनें|\nਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ|")
    # buttons = [[KeyboardButton(PunjLang)], [KeyboardButton(HindiLang)]]
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome,\n Please select your language.\nकृपया अपनी भाषा चुनें|\nਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ| ", reply_markup=ReplyKeyboardMarkup(buttons))

def messageHandler(update: Update, context: CallbackContext):

    if HindiLang in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="कृपया अपनी फसल की तस्वीरें अपलोड करें")
    if PunjLang in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਫਸਲ ਦੀਆਂ ਤਸਵੀਰਾਂ ਅਪਲੋਡ ਕਰੋ")



def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    count=0

    if "Hindi" in query:
        # likes +=1
        count=1
        context.bot.send_message(chat_id=update.effective_chat.id, text="कृपया अपनी फसल की तस्वीरें अपलोड करें....")

    if "Punjabi" in query:
        # dislikes +=1
        count=2
        context.bot.send_message(chat_id=update.effective_chat.id, text="ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਫਸਲ ਦੀਆਂ ਤਸਵੀਰਾਂ ਅਪਲੋਡ ਕਰੋ...")
    
    if "English" in query:
        # dislikes +=1
        count=3
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload the images of your crops...")



def image_handler(update, context):
    # file = update.message.photo[0].file_id
    # obj = context.bot.get_file(file)
    # obj.download()
    # file = context.bot.getFile(update.message.photo[-1].file_id)
    # print ("file_id: " + str(update.message.photo.file_id))
    # file.download('image.jpg')
    file = update.message.photo[-1].get_file()
    im = file.download()
    # print(im)
    # if( count == 3):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="Pleasw wait....")
    # elif(count == 2):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="कृपया प्रतीक्षा करें|")
    #     update.message.reply_text("कृपया प्रतीक्षा करें|")
    # elif(count == 1):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="ਕ੍ਰਿਪਾ ਕਰਕੇ ਉਡੀਕ ਕਰੋ|")
    #     update.message.reply_text("ਕ੍ਰਿਪਾ ਕਰਕੇ ਉਡੀਕ ਕਰੋ|")
    # else:
    update.message.reply_text("Please wait.\n\nकृपया प्रतीक्षा करें|\n\nਕ੍ਰਿਪਾ ਕਰਕੇ ਉਡੀਕ ਕਰੋ|")
    prediction=proc(im)
    update.message.reply_text(fin[prediction])
def proc(im):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model=torch.load('/home/kratoes669/model.pt')
    model.eval()
    # device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model=model.to(device)
    path_full=os.path.join('/home/kratoes669/',im)
    print(path_full)
    img=Image.open(path_full)

    tfms=transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])
    img_t=tfms(img)
    img_t=img_t.unsqueeze(0)
    img_t=img_t.to(device)
    output=model(img_t)
    prediction = int(torch.max(output.cpu().data, 1)[1].numpy())
    # _, preds= torch.max(outputs,1)
    # lab=class_names[preds[0]]
    # print(fin[prediction])  
    return prediction
    




dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))
updater.start_polling()