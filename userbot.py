import asyncio
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# Replace with your own values
API_ID = '20284828'
API_HASH = 'a980ba25306901d5c9b899414d6a9ab7'
SESSION = 'VtsOJwBu3l4UDFyABwF7glfM2kGOoY_Yesl-WX0NMpEM88V6YS9HKAzZLlXgYGZuNDNflzGP4RdVI0jgu3KSfILQ_N8eEoGuSp9Z4SoceoxngwA3JlSdjlE8b-eFPQ0RutlVSC488zdK6ck_HaN8OEc-AmNjT5yGslk6t5MPWc7C0gO_vwHQSDV6bkprNkrRRHCP58NMM-urh-WOSF7vgUbKGhenNCVj9SBiV3VmeBftHjEU0FyGPL-Z1caNTP5sMnZQkM9FqvyVrk6gJU4k6MVkkW5TFcXnmkkaydzXUe7jtRv4s_AH7OEVzrN4ybqYrHiXDj9J8qbEnXI_Km3rMkfQrVd7ig='
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
