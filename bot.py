#(©) Codeflix_Bots

from aiohttp import web
from plugins import web_server

from pyrogram import Client
import sys
from datetime import datetime
from config import LOGGER, PORT, OWNER_ID, SHORTNERS
from helper import MongoDB

version = "v1.0.0"


class Bot(Client):
    def __init__(
        self,
        session,
        workers,
        db,
        fsub,
        token,
        admins,
        messages,
        auto_del,
        db_uri,
        db_name,
        api_id,
        api_hash,
        protect,
        disable_btn
    ):
        super().__init__(
            name=session,
            api_hash=api_hash,
            api_id=api_id,
            plugins={"root": "plugins"},
            workers=workers,
            bot_token=token
        )

        self.LOGGER = LOGGER
        self.name = session
        self.db = db
        self.fsub = fsub
        self.owner = OWNER_ID
        self.fsub_dict = {}
        self.admins = admins + [OWNER_ID] if OWNER_ID not in admins else admins
        self.messages = messages
        self.auto_del = auto_del
        self.protect = protect
        self.req_fsub = {}
        self.disable_btn = disable_btn
        self.reply_text = messages.get('REPLY', 'Do not send any useless message in the bot.')
        self.mongodb = MongoDB(db_uri, db_name)
        self.req_channels = []
        self.db_channels = {}
        self.primary_db_channel = db

        # ✅ SHORTNER SYSTEM (CONFIG BASED)
        if not SHORTNERS:
            raise ValueError("SHORTNERS config is empty")

        self.shortners = SHORTNERS
        self.shortner_enabled = True  # default, will be overridden by DB

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        #================ F-SUB =================#

        if len(self.fsub) > 0:
            for channel in self.fsub:
                try:
                    chat = await self.get_chat(channel[0])
                    name = chat.title
                    link = None

                    if not channel[1]:
                        link = chat.invite_link

                    if not link and not channel[2]:
                        chat_link = await self.create_chat_invite_link(
                            channel[0],
                            creates_join_request=channel[1]
                        )
                        link = chat_link.invite_link

                    if not channel[1]:
                        self.fsub_dict[channel[0]] = [name, link, False, 0]

                    if channel[1]:
                        self.fsub_dict[channel[0]] = [name, link, True, 0]
                        self.req_channels.append(channel[0])

                    if channel[2] > 0:
                        self.fsub_dict[channel[0]] = [name, None, channel[1], channel[2]]

                except Exception:
                    self.LOGGER(__name__, self.name).warning("Fsub error")
                    sys.exit()

        # Load dynamic fsubs
        try:
            db_fsub_channels = await self.mongodb.get_fsub_channels()

            for channel_id_str, channel_data in db_fsub_channels.items():
                channel_id = int(channel_id_str)

                if channel_id in self.fsub_dict:
                    continue

                try:
                    chat = await self.get_chat(channel_id)
                    channel_data[0] = chat.title
                    self.fsub_dict[channel_id] = channel_data

                    if channel_data[2]:
                        self.req_channels.append(channel_id)

                except:
                    await self.mongodb.remove_fsub_channel(channel_id)

        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Fsub load error: {e}")

        await self.mongodb.set_channels(self.req_channels)

        #================ DB CHANNELS =================#

        try:
            db_channels_data = await self.mongodb.get_db_channels()
            self.db_channels = {}
            self.primary_db_channel = self.db

            for channel_id_str, channel_data in db_channels_data.items():
                channel_id = int(channel_id_str)

                try:
                    chat = await self.get_chat(channel_id)
                    channel_data['name'] = chat.title
                    self.db_channels[channel_id_str] = channel_data

                    if channel_data.get('is_primary', False):
                        self.primary_db_channel = channel_id
                        self.db = channel_id

                except:
                    await self.mongodb.remove_db_channel(channel_id)

        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"DB channel error: {e}")

        #================ SHORTNER TOGGLE =================#

        try:
            settings = await self.mongodb.get_shortner_settings()
            self.shortner_enabled = settings.get('enabled', True)
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Shortner toggle load failed: {e}")
            self.shortner_enabled = True

        #================ DB CHANNEL CHECK =================#

        try:
            db_channel = await self.get_chat(self.db)
            self.db_channel = db_channel

            test = await self.send_message(
                chat_id=db_channel.id,
                text="Testing Message"
            )
            await test.delete()

        except Exception as e:
            self.LOGGER(__name__, self.name).warning(e)
            sys.exit()

        self.LOGGER(__name__, self.name).info("Bot Started!")

        #================ RESTART MESSAGE =================#

        try:
            await self.send_message(
                chat_id=self.owner,
                text="<b>Bot restarted successfully 🚀</b>"
            )
        except Exception as e:
            self.LOGGER(__name__, self.name).warning(f"Restart msg failed: {e}")

        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__, self.name).info("Bot stopped.")


#================ WEB =================#

async def web_app():
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()
