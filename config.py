import logging
from logging.handlers import RotatingFileHandler


#========== CORE CONFIGURATION ==========
LOG_FILE_NAME = "obsidianBots.log"
PORT = "5010"

OWNER_ID = 6128121762
ADMINS = [6497757690, 6103092779]

WORKERS = 5
SESSION = "obsidianbots"


#========== TELEGRAM API ==========
TOKEN = "12345"
API_ID = "12345"
API_HASH = "12345"

MSG_EFFECT = 5046509860389126442


#========== MULTI SHORTNERS ==========
SHORTNERS = [
    {
        "url": "linkshortify.com",
        "api": "YOUR_API_1",
        "tutorial": "https://t.me/tutorial1"
    },
    {
        "url": "shareus.io",
        "api": "YOUR_API_2",
        "tutorial": "https://t.me/tutorial2"
    }
]
# Temp Premium Settings
TEMP_PREMIUM_ENABLED = True
TEMP_PREMIUM_DURATION = 24  # in hours


#========== DATABASE CONFIGURATION ==========
DB_URI = "mongodb"
DB_NAME = "fileshare"

# Primary Database Channel
DB_CHANNEL =   # put channel id only (do not add quotes)

# Multiple Database Channels (optional)
# DB_CHANNELS = {
#     "-1002595092736": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1001234567890": {"name": "Secondary DB", "is_primary": False, "is_active": True}
# }


#========== FORCE SUBSCRIPTION ==========
# Format: [channel_id, request_enabled, timer_in_minutes]
FSUBS = [
    [-1003016571084, True, 10]
]


#========== BOT SETTINGS ==========
AUTO_DEL = 300  # Auto delete timer (seconds)

DISABLE_BTN = True
PROTECT = True


#========== MESSAGE TEMPLATES ==========
MESSAGES = {

    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote> ɪ ᴀᴍ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.</blockquote></b>",

    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",

    "ABOUT": "<b>›› ғᴏʀ ᴍᴏʀᴇ: @Obsidian_Bots\n<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/Obsidian_Bots'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>\n›› ᴏᴡɴᴇʀ: @automated_adminBOT\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>\n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>\n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>\n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @Obsidian_Bots</blockquote></b>",

    "REPLY": "<b>ꜰᴏʀ ᴍᴏʀᴇ ᴜᴘᴅᴀᴛᴇꜱ ᴊᴏɪɴ @Obsidian_Bots</b>",

    "SHORT_MSG": "<b>📊 ʜᴇʏ {first},\nɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ\n⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",

    "START_PHOTO": "https://graph.org/file/510affa3d4b6c911c12e3.jpg",
    "FSUB_PHOTO": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT_PIC": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT": "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg"
}


#========== LOGGER CONFIGURATION ==========
def LOGGER(name: str, client_name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE_NAME,
        maxBytes=50_000_000,
        backupCount=10
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
