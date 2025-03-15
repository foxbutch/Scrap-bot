from telethon import TelegramClient, events
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

API_ID = 28434302  
API_HASH = "d01853b574668a746fe390aa65586bd5"  
SESSION_NAME = "my_session"

SOURCE_CHANNEL = -1002415631322  
  # Ensure this is correct
TARGET_GROUP = -1002492628749  # Ensure this is correct

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def fetch_old_messages():
    """Fetches old messages and forwards them to the target group."""
    logger.info("📜 Fetching old messages...")

    try:
        source = await client.get_entity(SOURCE_CHANNEL)  # Fix for private channels
        async for message in client.iter_messages(source, reverse=True):
            if message.video or message.document:
                logger.info(f"📩 Downloading old media: {message.id}...")
                file_path = await message.download_media()
                logger.info(f"✅ Media downloaded to: {file_path}")

                await client.send_file(TARGET_GROUP, file_path, caption=message.text if message.text else "")
                logger.info(f"✅ Forwarded old media message {message.id}")
            else:
                logger.info(f"ℹ️ Skipping non-media message {message.id}")
    except Exception as e:
        logger.error(f"❌ Error fetching old messages: {e}")

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def forward_new_messages(event):
    """Forwards new messages from the source channel to the target group."""
    try:
        if event.video or event.document:
            logger.info("📩 New media detected! Downloading...")
            file_path = await event.download_media()
            logger.info(f"✅ Media downloaded to: {file_path}")

            await client.send_file(TARGET_GROUP, file_path, caption=event.text if event.text else "")
            logger.info(f"✅ Forwarded new media from {SOURCE_CHANNEL} to {TARGET_GROUP}")
        else:
            logger.info("ℹ️ Ignored non-media message")
    except Exception as e:
        logger.error(f"❌ Error forwarding media: {e}")

async def main():
    await client.start()
    await fetch_old_messages()  # Fetch old messages before running the bot
    logger.info("🚀 Bot is now listening for new messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())  # Correctly handles the event loop
