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

    # ✅ cache fix (store index also)
    if url in shortened_urls_cache:
        return shortened_urls_cache[url]

    try:
        if not SHORTNERS:
            print("[Shortener Error] SHORTNERS not configured")
            return url, 0

        total = len(SHORTNERS)

        # 🔥 per-user rotation
        if user_id:
            start_index = user_shortner_cache.get(user_id, 0)
            user_shortner_cache[user_id] = (start_index + 1) % total
        else:
            start_index = 0

        async with httpx.AsyncClient() as client_http:

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

                    response = await client_http.get(api_url, timeout=8)

                    try:
                        rjson = response.json()
                    except:
                        print(f"[Invalid JSON] {short_url}")
                        continue

                    if rjson.get("status") == "success" and response.status_code == 200:
                        short_link = rjson.get("shortenedUrl", url)

                        # ✅ store both link + index
                        shortened_urls_cache[url] = (short_link, index)

                        return short_link, index

                    else:
                        print(f"[Shortener Failed] {short_url} → {rjson}")

                except Exception as e:
                    print(f"[Shortener Error] {short_url} → {e}")

        print("[Shortener Error] All shorteners failed")

    except Exception as e:
        print(f"[Shortener Fatal Error] {e}")

    return url, 0

#===============================================================#

@Client.on_message(filters.command('shortner') & filters.private)
async def shortner_command(client: Client, message: Message):

    # ✅ admin + owner restriction
    if message.from_user.id != OWNER_ID and message.from_user.id not in ADMINS:
        return await message.reply("❌ Only admins can use this.")

    await shortner_panel(client, message)

#===============================================================#

async def check_shortner_status(client_http, s, enabled):
    url = s.get("url")
    api = s.get("api")

    if not enabled:
        return "✗ ᴅɪsᴀʙʟᴇᴅ"

    try:
        test = await client_http.get(
            f"https://{url}/api?api={api}&url=https://google.com&alias=test",
            timeout=5
        )
        return "✓ ᴡᴏʀᴋɪɴɢ" if test.status_code == 200 else "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"
    except:
        return "✗ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ"

#===============================================================#

async def shortner_panel(client, query_or_message):

    shortner_enabled = getattr(client, 'shortner_enabled', True)
    enabled_text = "✓ ᴇɴᴀʙʟᴇᴅ" if shortner_enabled else "✗ ᴅɪsᴀʙʟᴇᴅ"

    msg = f"""<blockquote>✦ 𝗦𝗛𝗢𝗥𝗧𝗡𝗘𝗥 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</blockquote>
**ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢꜱ:**
<blockquote>›› ꜱʜᴏʀᴛɴᴇʀ ꜱᴛᴀᴛᴜꜱ: {enabled_text}</blockquote>
"""

    async with httpx.AsyncClient() as client_http:

        # ✅ parallel calls
        tasks = [check_shortner_status(client_http, s, shortner_enabled) for s in SHORTNERS]
        statuses = await asyncio.gather(*tasks)

    for i, (s, status) in enumerate(zip(SHORTNERS, statuses), start=1):
        url = s.get("url")
        api = s.get("api")
        tutorial = s.get("tutorial")

        msg += f"""
<blockquote>
#shortner{i}
›› ꜱʜᴏʀᴛɴᴇʀ ᴜʀʟ: `{url}`
›› ꜱʜᴏʀᴛɴᴇʀ ᴀᴘɪ: `****{api[-6:]}`
›› ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ: `{tutorial}`
›› ꜱᴛᴀᴛᴜꜱ: {status}
</blockquote>
"""

    msg += "\n<blockquote>≡ ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ</blockquote>"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('• ᴛᴇꜱᴛ ꜱʜᴏʀᴛɴᴇʀ •', 'choose_test')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings')]
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

    async with httpx.AsyncClient() as client_http:
        try:
            alias = generate_random_alphanumeric()
            api_url = f"https://{url}/api?api={api}&url=https://google.com&alias={alias}"

            response = await client_http.get(api_url, timeout=10)

            try:
                rjson = response.json()
            except:
                return await query.message.edit_text("❌ Invalid JSON response")

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
