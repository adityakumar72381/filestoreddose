import requests
import random
import string
from config import MESSAGES, SHORTNERS
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from pyrogram.errors.pyromod import ListenerTimeout
from helper.helper_func import force_sub

# ✅ In-memory cache
shortened_urls_cache = {}

# ✅ per-user shortener rotation cache
user_shortner_cache = {}

def generate_random_alphanumeric():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

def get_short(url, client, user_id=None):

    shortner_enabled = getattr(client, 'shortner_enabled', True)
    if not shortner_enabled:
        return url, 0

    # cache
    if url in shortened_urls_cache:
        return shortened_urls_cache[url], 0

    try:
        if not SHORTNERS:
            print("[Shortener Error] SHORTNERS not configured")
            return url, 0

        total = len(SHORTNERS)

        # 🔥 starting index (per-user rotation)
        if user_id:
            start_index = user_shortner_cache.get(user_id, 0)
            user_shortner_cache[user_id] = (start_index + 1) % total
        else:
            start_index = 0

        # 🔥 FAILOVER LOOP
        for i in range(total):
            index = (start_index + i) % total
            selected = SHORTNERS[index]

            if "url" not in selected or "api" not in selected:
                continue

            short_url = selected["url"]
            short_api = selected["api"]

            try:
                alias = generate_random_alphanumeric()
                api_url = f"https://{short_url}/api?api={short_api}&url={url}&alias={alias}"

                response = requests.get(api_url, timeout=8)
                rjson = response.json()

                if rjson.get("status") == "success" and response.status_code == 200:
                    short_link = rjson.get("shortenedUrl", url)
                    shortened_urls_cache[url] = short_link
                    return short_link, index  # ✅ success

                else:
                    print(f"[Shortener Failed] {short_url} → {rjson}")

            except Exception as e:
                print(f"[Shortener Error] {short_url} → {e}")

        # ❌ if all shorteners fail
        print("[Shortener Error] All shorteners failed")

    except Exception as e:
        print(f"[Shortener Fatal Error] {e}")

    return url, 0

#===============================================================#

@Client.on_message(filters.command('shortner') & filters.private)
async def shortner_command(client: Client, message: Message):
    await shortner_panel(client, message)

#===============================================================#

async def shortner_panel(client, query_or_message):
    shortner_enabled = getattr(client, 'shortner_enabled', True)
    enabled_text = "✓ ᴇɴᴀʙʟᴇᴅ" if shortner_enabled else "✗ ᴅɪsᴀʙʟᴇᴅ"

    msg = f"""<blockquote>✦ 𝗦𝗛𝗢𝗥𝗧𝗡𝗘𝗥 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
**ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:**
<blockquote>›› ꜱʜᴏʀᴛɴᴇʀ ꜱᴛᴀᴛᴜꜱ: {enabled_text}</blockquote>
"""

    # 🔥 Show all shortners
    for i, s in enumerate(SHORTNERS, start=1):
        url = s.get("url")
        api = s.get("api")
        tutorial = s.get("tutorial")

        # check working
        if shortner_enabled:
            try:
                test = requests.get(
                    f"https://{url}/api?api={api}&url=https://google.com&alias=test",
                    timeout=5
                )
                status = "✓ ᴡᴏʀᴋɪɴɢ" if test.status_code == 200 else "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
            except:
                status = "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
        else:
            status = "✗ ᴅɪsᴀʙʟᴇᴅ"

        msg += f"""
<blockquote>
#shortner{i}
›› ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ: `{url}`
›› ꜱʜᴏʀᴛɴᴇʀ ᴀᴘɪ: `{api[:25]}...`
›› ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ: `{tutorial}`
›› ꜱᴛᴀᴛᴜꜱ: {status}
</blockquote>
"""

    msg += "\n<blockquote>≡ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴꜰɪɢᴜʀᴇ ʏᴏᴜʀ ꜱʜᴏʀᴛɴᴇʀ ꜱᴇᴛᴛɪɴɢꜱ!</blockquote>"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('• ᴛᴇꜱᴛ ꜱʜᴏʀᴛɴᴇʀ •', 'choose_test')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ', 'settings')]
    ])

    image_url = MESSAGES.get("SHORT")

    if hasattr(query_or_message, 'message'):
        await query_or_message.message.edit_media(
            media=InputMediaPhoto(media=image_url, caption=msg),
            reply_markup=reply_markup
        )
    else:
        await query_or_message.reply_photo(photo=image_url, caption=msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^shortner$"))
async def shortner_callback(client, query):
    if not query.from_user.id in client.admins:
        return await query.answer('❌ ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ!', show_alert=True)
    await query.answer()
    await shortner_panel(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^choose_test$"))
async def choose_test(client, query: CallbackQuery):

    buttons = []
    for i in range(len(SHORTNERS)):
        buttons.append([InlineKeyboardButton(f"Test Shortner {i+1}", callback_data=f"test_{i}")])

    buttons.append([InlineKeyboardButton("◂ Back", callback_data="shortner")])

    await query.message.edit_text(
        "**Select shortner to test:**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

#===============================================================#

@Client.on_callback_query(filters.regex(r"^test_(\d+)$"))
async def test_shortner(client: Client, query: CallbackQuery):

    index = int(query.data.split("_")[1])

    if index >= len(SHORTNERS):
        return await query.answer("Invalid shortner", show_alert=True)

    s = SHORTNERS[index]
    url = s["url"]
    api = s["api"]

    await query.message.edit_text(f"🔄 Testing Shortner {index+1}...")

    try:
        test_url = "https://google.com"
        alias = generate_random_alphanumeric()

        api_url = f"https://{url}/api?api={api}&url={test_url}&alias={alias}"
        response = requests.get(api_url, timeout=10)
        rjson = response.json()

        if rjson.get("status") == "success":
            short_link = rjson.get("shortenedUrl", "")
            msg = f"""✅ SUCCESS

URL: `{url}`
Short Link: `{short_link}`"""
        else:
            msg = f"""❌ FAILED

URL: `{url}`
Error: `{rjson.get("message")}`"""

    except Exception as e:
        msg = f"""❌ ERROR

URL: `{url}`
Error: `{str(e)}`"""

    await query.message.edit_text(
        msg,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◂ Back", callback_data="shortner")]])
    )
