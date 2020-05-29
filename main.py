import logging
from telegram.ext import Updater, CommandHandler
import RPi.GPIO as GPIO

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

device_dict = {"livingroom":31, "bedroom":36, "kitchen":33, "bathroom":38 ,"attic":40}

def start(update, context):
    update.message.reply_text('Hi!, run /help to view the commands')

def list_devices(update, context):
    out_str = ""
    for a in device_dict:
        out_str+=a+'\n' 
    update.message.reply_text("Your devices are :" +'\n'+out_str)     


def help(update, context):
    update.message.reply_text('''commands:
/switchon your_device  : start the switch on process
/switchoff your_device : start the switch off process
/listdevices           : list out all available devices
        ''')
def switchon(update, context):
    param = " ".join(context.args)
    if param == "all":
        for i in device_dict:
            if i != "all":
                GPIO.output(device_dict[i], GPIO.HIGH)
    else:
        out = device_dict[param]
        GPIO.output(out, GPIO.HIGH)

def switchoff(update, context):
    param = " ".join(context.args)
    if param == "all":
        for i in device_dict:
            if i != "all":
                GPIO.output(device_dict[i], GPIO.LOW)
    else:
        out = device_dict[param]
        GPIO.output(out, GPIO.LOW)



def main_func():
    GPIO.setwarnings(False)  
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setup(40, GPIO.OUT)
    
    updater = Updater("Your API Key", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("listdevices", list_devices))
    dp.add_handler(CommandHandler("switchon", switchon))
    dp.add_handler(CommandHandler("switchoff", switchoff))
    updater.start_polling()
    updater.idle()


main_func()
