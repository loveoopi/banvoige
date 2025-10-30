import asyncio
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# Replace with your own values
API_ID = '20284828'
API_HASH = 'a980ba25306901d5c9b899414d6a9ab7'
SESSION = '1AZWarzQBu4V96UbXa7P0MI18a9nPTo4KHjM81vU7Rb7uw5sWofeN-RdANmiqIN3PuqN1sSsLkMxU-yp1nJrzKwVChE117DVV5prb5HbmeOgJo56c7HpQp1S7lV5ShvboZ1U7ETJkt5f3od1RSkQf3XuipNyMLo18KXQO0l2VySIz6ZBuq19rJLOk_428SdLVzkWA-8uHFO_xbtJxfXzSuufwuwWjMcZIXpefh7bKuReyDMlz_zqZc-ocBs1emTEvkLtuWpcnK1TsfLCW6X0wvdXTPIbJxunNt2VzC9sVKxz7dSnzWzWccpyLMiJpWFGx1yNliLszcS26grTnBLoPZY7Hr7taHJg='
GROUP_ID = -1002601964685

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def get_active_voice_chat():
    """Get the active voice chat in the group"""
    try:
        entity = await client.get_entity(GROUP_ID)
        full_chat = await client(functions.channels.GetFullChannelRequest(channel=entity))
        if hasattr(full_chat.full_chat, 'call') and full_chat.full_chat.call:
            return full_chat.full_chat.call
        return None
    except Exception as e:
        print(f"Error getting voice chat: {e}")
        return None

async def ban_channels_in_voicechat():
    while True:
        try:
            # Get active voice chat
            voice_chat = await get_active_voice_chat()
            if not voice_chat:
                print("No active voice chat found")
                await asyncio.sleep(10)
                continue

            # Get participants
            result = await client(functions.phone.GetGroupParticipantsRequest(
                call=voice_chat,
                ids=[],
                sources=[],
                offset='',
                limit=100
            ))

            banned_count = 0
            for participant in result.participants:
                # Check if participant is a channel
                if hasattr(participant, 'peer') and hasattr(participant.peer, 'channel_id'):
                    channel_id = participant.peer.channel_id
                    try:
                        # Ban the channel
                        await client.edit_permissions(
                            GROUP_ID,
                            channel_id,
                            view_messages=False
                        )
                        print(f'Banned channel {channel_id}')
                        banned_count += 1
                    except Exception as e:
                        print(f'Error banning channel {channel_id}: {e}')

            if banned_count > 0:
                print(f"Banned {banned_count} channels from voice chat")
            
            await asyncio.sleep(5)  # Check every 5 seconds

        except Exception as e:
            print('Error scanning voice chat:', e)
            await asyncio.sleep(10)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Userbot started. Monitoring voice chat for channels...')

@client.on(events.NewMessage(pattern='/status'))
async def status(event):
    voice_chat = await get_active_voice_chat()
    if voice_chat:
        await event.respond('Voice chat monitoring is active!')
    else:
        await event.respond('No active voice chat found.')

async def main():
    try:
        await client.start()
        print("Userbot started successfully!")
        print("Monitoring voice chat for channels...")
        await ban_channels_in_voicechat()
    except Exception as e:
        print(f"Failed to start: {e}")
        # If session is invalid, you'll need to create a new one
        print("The session string might be invalid. Please generate a new one.")

if __name__ == '__main__':
    asyncio.run(main())
