import asyncio
import httpx
import random
import string
from config import MESSAGES, SHORTNERS, OWNER_ID, ADMINS
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from helper.helper_func import force_sub

# ✅ In-memory cache (store link + index)
shortened_urls_cache = {}

# ✅ per-user shortener rotation cache
user_shortner_cache = {}

def generate_random_alphanumeric():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

#===============================================================#

async def get_short(url, client, user_id=None):
    shortner_enabled = getattr(client, 'shortner_enabled', True)
    if not shortner_enabled:
        return url, 0

    if url in shortened_urls_cache:
        return shortened_urls_cache[url]

    try:
        if not SHORTNERS:
            return url, 0

        total = len(SHORTNERS)
        if user_id:
            start_index = user_shortner_cache.get(user_id, 0)
            user_shortner_cache[user_id] = (start_index + 1) % total
        else:
            start_index = 0

        async with httpx.AsyncClient() as client_http:
            for i in range(total):
                index = (start_index + i) % total
                selected = SHORTNERS[index]
                short_url = selected["url"]
                short_api = selected["api"]

                try:
                    alias = generate_random_alphanumeric()
                    api_url = f"https://{short_url}/api?api={short_api}&url={url}&alias={alias}"
                    response = await client_http.get(api_url, timeout=8)
                    rjson = response.json()

                    if rjson.get("status") == "success" and response.status_code == 200:
                        short_link = rjson.get("shortenedUrl", url)
                        shortened_urls_cache[url] = (short_link, index)
                        return short_link, index
                except:
                    continue
    except:
        pass
    return url, 0

#===============================================================#

@Client.on_message(filters.command('shortner') & filters.private)
async def shortner_command(client: Client, message: Message):
    if message.from_user.id != OWNER_ID and message.from_user.id not in ADMINS:
        return await message.reply("❌ Only admins can use this.")
    await shortner_panel(client, message)

@Client.on_callback_query(filters.regex("^shortner$"))
async def shortner_callback(client: Client, query: CallbackQuery):
    if query.from_user.id != OWNER_ID and query.from_user.id not in ADMINS:
        return await query.answer("❌ Admin only!", show_alert=True)
    await query.answer()
    await shortner_panel(client, query)

@Client.on_callback_query(filters.regex("^toggle_shortner$"))
async def toggle_shortner_callback(client: Client, query: CallbackQuery):
    if query.from_user.id != OWNER_ID and query.from_user.id not in ADMINS:
        return await query.answer("❌ Admin only!", show_alert=True)
    
    # Toggle the status
    current = getattr(client, 'shortner_enabled', True)
    client.shortner_enabled = not current
    
    status_text = "ENABLED ✅" if client.shortner_enabled else "DISABLED ❌"
    await query.answer(f"Shortener is now {status_text}", show_alert=False)
    await shortner_panel(client, query)

#===============================================================#

async def check_shortner_status(client_http, s, enabled):
    if not enabled:
        return "✗ ᴅɪsᴀʙʟᴇᴅ"
    try:
        test = await client_http.get(
            f"https://{s.get('url')}/api?api={s.get('api')}&url=https://google.com&alias=test{random.randint(1,999)}",
            timeout=5
        )
        return "✓ ᴡᴏʀᴋɪɴɢ" if test.status_code == 200 else "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
    except:
        return "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"

#===============================================================#

async def shortner_panel(client, query_or_message):
    shortner_enabled = getattr(client, 'shortner_enabled', True)
    
    # UI Formatting
    enabled_text = "✅ ᴇɴᴀʙʟᴇᴅ" if shortner_enabled else "❌ ᴅɪsᴀʙʟᴇᴅ"
    toggle_btn_text = "ᴛᴜʀɴ ᴏғғ 🔴" if shortner_enabled else "ᴛᴜʀɴ ᴏɴ 🟢"

    msg = f"""<blockquote>✦ 𝗦𝗛𝗢𝗥𝗧𝗡𝗘𝗥 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
**ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:**
<blockquote>›› ꜱʜᴏʀᴛɴᴇʀ ꜱᴛᴀᴛᴜꜱ: {enabled_text}</blockquote>
"""

    async with httpx.AsyncClient() as client_http:
        tasks = [check_shortner_status(client_http, s, shortner_enabled) for s in SHORTNERS]
        statuses = await asyncio.gather(*tasks)

    for i, (s, status) in enumerate(zip(SHORTNERS, statuses), start=1):
        msg += f"""
<blockquote>
#shortner{i}
›› ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ: `{s.get("url")}`
›› ꜱʜᴏʀᴛɴᴇʀ ᴀᴘɪ: `****{s.get("api")[-6:]}`
›› ꜱᴛᴀᴛᴜꜱ: {status}
</blockquote>
"""

    msg += "\n<blockquote>≡ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ</blockquote>"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(toggle_btn_text, 'toggle_shortner')],
        [InlineKeyboardButton('• ᴛᴇꜱᴛ ꜱʜᴏʀᴛɴᴇʀ •', 'choose_test')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
    ])

    image_url = MESSAGES.get("SHORT")

    # If it's a callback, edit the current message
    if isinstance(query_or_message, CallbackQuery):
        await query_or_message.message.edit_media(
            media=InputMediaPhoto(media=image_url, caption=msg),
            reply_markup=reply_markup
        )
    # If it's a command, send a new photo message
    else:
        await query_or_message.reply_photo(photo=image_url, caption=msg, reply_markup=reply_markup)

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
    s = SHORTNERS[index]
    
    await query.message.edit_text(f"🔄 Testing Shortner {index+1} ({s['url']})...")

    async with httpx.AsyncClient() as client_http:
        try:
            api_url = f"https://{s['url']}/api?api={s['api']}&url=https://google.com&alias=test{generate_random_alphanumeric()}"
            response = await client_http.get(api_url, timeout=10)
            rjson = response.json()

            if rjson.get("status") == "success":
                msg = f"✅ **SUCCESS**\n\nURL: `{s['url']}`\nShort Link: `{rjson.get('shortenedUrl')}`"
            else:
                msg = f"❌ **FAILED**\n\nURL: `{s['url']}`\nError: `{rjson.get('message')}`"
        except Exception as e:
            msg = f"❌ **ERROR**\n\nURL: `{s['url']}`\nError: `{str(e)}`"

    await query.message.edit_text(
        msg,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◂ Back", callback_data="shortner")]])
    )
    
