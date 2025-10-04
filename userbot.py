import asyncio
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession  # Import StringSession

# Replace with your own values
API_ID = '20284828'
API_HASH = 'a980ba25306901d5c9b899414d6a9ab7'
SESSION = '1BVtsOJwBu3l4UDFyABwF7glfM2kGOoY_Yesl-WX0NMpEM88V6YS9HKAzZLlXgYGZuNDNflzGP4RdVI0jgu3KSfILQ_N8eEoGuSp9Z4SoceoxngwA3JlSdjlE8b-eFPQ0RutlVSC488zdK6ck_HaN8OEc-AmNjT5yGslk6t5MPWc7C0gO_vwHQSDV6bkprNkrRRHCP58NMM-urh-WOSF7vgUbKGhenNCVj9SBiV3VmeBftHjEU0FyGPL-Z1caNTP5sMnZQkM9FqvyVrk6gJU4k6MVkkW5TFcXnmkkaydzXUe7jtRv4s_AH7OEVzrN4ybqYrHiXDj9J8qbEnXI_Km3rMkfQrVd7ig='  # File or string session name
GROUP_ID = -1001887313554  # Replace with your group/channel ID

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

async def ban_channels_in_voicechat():
    while True:
        try:
            # Get list of participants in voice chat
            result = await client(functions.phone.GetGroupCallParticipantsRequest(
                call=types.InputGroupCall(
                    id=20284828,  # Use actual voice chat id, fetchable via Telethon
                    access_hash=123456789  # Replace with actual access hash
                ),
                limit=100
            ))

            for participant in result.participants:
                # If joined via channel (has 'channel_id')
                if getattr(participant, 'channel_id', None):
                    channel_id = participant.channel_id
                    try:
                        await client.kick_participant(GROUP_ID, channel_id)
                        print(f'Banned channel {channel_id}')
                    except Exception as e:
                        print(f'Error banning channel: {e}')
            await asyncio.sleep(1)
        except Exception as e:
            print('Error scanning voice chat:', e)
            await asyncio.sleep(5)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Userbot started.')

async def main():
    await client.start()
    print("Userbot running...")
    await ban_channels_in_voicechat()

if __name__ == '__main__':
    asyncio.run(main())
