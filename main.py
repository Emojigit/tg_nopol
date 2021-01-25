import sys, re, logging
exit = sys.exit
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext
from telegram.ext.filters import Filters
from telegram.error import InvalidToken
from telegram import ParseMode, Update
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s[%(name)s] %(message)s")
log = logging.getLogger("MainScript")
pols = []
try:
    with open("pols.txt","r") as f:
        pols = f.readlines().copy()
except FileNotFoundError:
    log.error("No pols.txt!")
    exit(1)
alert = ""
try:
    with open("alert.txt","r") as f:
        alert = f.read()
except FileNotFoundError:
    log.error("No alert.txt!")
    exit(1)

def token():
    try:
        with open("token.txt","r") as f:
            return f.read().rstrip('\n')
    except FileNotFoundError:
        log.error("No token.txt!")
        # print("[ERROR] No token.txt!")
        exit(3)


def rawhandler(update, context):
    msg = update.message.text
    stat = 0
    for x in pols:
        if x.rstrip('\n') == "":
            continue
        if msg.find(x.rstrip('\n')) != -1:
            stat = 1
            break
    if stat == 1:
        log.info("Alerted POL! msg content: "+msg)
        update.message.reply_text(alert,parse_mode=ParseMode.MARKDOWN_V2)

def polc(update: Update, context: CallbackContext):
    log.info("Got pol command!")
    update.message.reply_text(alert,parse_mode=ParseMode.MARKDOWN_V2)

def main():
    """Start the bot."""
    tok = token()
    try:
        updater = Updater(tok, use_context=True)
        log.info("Get updater success!")
    except InvalidToken:
        log.critical("Invalid Token! Plase edit token.txt and fill in a valid token.")
        raise
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('pol', polc))
    dp.add_handler(MessageHandler(Filters.text, rawhandler))
    updater.start_polling()
    log.info("Started the bot! Use Ctrl-C to stop it.")
    updater.idle()

if __name__ == '__main__':
    main()
