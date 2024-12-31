import      os
import      time
import      asyncio
import      discord
from        log             import      load_logged_files, log_file_info, save_data_to_json, File
from        dotenv          import      load_dotenv
from        discord.ext     import      commands
from        os              import      listdir
from        os.path         import      isfile, join

load_dotenv()
TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])  # Add your channel ID in .env (NOT SERVER ID)

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='/', intents=intents)

logged_files = load_logged_files()
existing_file_hashes = {file_info['hash'] for file_info in logged_files}
ignore_files = set()

async def upload_file_to_channel(file_path):
    print(f"Detected new file: {file_path}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            file_size = File.calculate_file_size(file_path)
            if file_size > 25000000: # Discord has 25MB file limit for non-Nitro users
                print(f'File {file_path} exceeds file size limit')
                ignore_files.add(file_path)
                return False
            
            with open(file_path, 'rb') as file:
                # bot.loop.create_task(channel.send(file=discord.File(file, filename=os.path.basename(file_path))))
                await channel.send(file=discord.File(file, filename=os.path.basename(file_path)))
                print(f'File {file_path} uploaded successfully')
                return True
        except Exception as e:
            print(f'Error uploading file {file_path}: {e}')
            return False

@bot.event
async def on_ready():
    running = True
    print(f'Logged in as {bot.user}')
    print('Bot is running, press Ctrl+C to quit')

    folder_path = r'upload' # Path to folder

    try:
        while running:
            files = [f'{folder_path}/{f}' for f in listdir(folder_path) if isfile(join(folder_path, f))]
            for file in files:
                if file in ignore_files:
                    continue
                file_hash = File.get_file_hash(file)
                if file_hash not in existing_file_hashes:
                    status = await upload_file_to_channel(file)
                    if status:
                        logged_files.append({
                            'name': os.path.basename(file),
                            'hash': file_hash,
                            'size': File.calculate_file_size(file)
                        })
                        existing_file_hashes.add(file_hash)
                        save_data_to_json('db.json', logged_files)
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print('Exiting...')
        running=False

# Run the bot
if TOKEN and CHANNEL_ID:
    bot.run(TOKEN)