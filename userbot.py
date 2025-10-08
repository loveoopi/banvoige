import asyncio
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# Replace with your own values
API_ID = '20284828'
API_HASH = 'a980ba25306901d5c9b899414d6a9ab7'
SESSION = '1BVtsOJwBu1Uh8UnJuaO0vjgmDsqMDrqxt22ovpRMhk4HMERKaRi0v9dPGaykicbRVY2dvhoOdM8CYu3zXc1RxJcYnLY3j9LS8zQAcm946MYAOeNYJxPJSkaZsaMd6PLZv6tXMH7u6SB_wLFtmFp9SCH_Ynt7RZBBLDe-3qgbv9O4FHGewoNF-Q3BZ9ZwKGsIGJ46_9BEjX4Mpd6wdcQe14X0FJddbVn_B1mUwoS0kYeZUCnPS0ytzACHYhN3ztP2oLdLiHbHYupQh9mxcaLKVkOAagxwKhgKA0jD0T3b-zUle85Pd5HEiqe7mgJHxXnBXyb5kyLG1O1fmJR16ADMsSVT99VyCKg='
GROUP_ID = -1001887313554

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

            # Get participants - using the correct method name
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
    await client.start()
    print("Userbot running... Monitoring voice chat for channels")
    await ban_channels_in_voicechat()

if __name__ == '__main__':
    asyncio.run(main())
