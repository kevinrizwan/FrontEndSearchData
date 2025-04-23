import discord
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

CATEGORY_ID = 1093103431566245908

def load_blacklist():
    with open("blacklist.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        return [td.text.strip().lower() for td in soup.select("td:nth-of-type(2)") if td.text.strip() != "-"]

blacklist_ucp = load_blacklist()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel) and channel.category_id == CATEGORY_ID:
        await channel.send("🕵️‍♂️ Bot aktif! Membaca data...")

        async for msg in channel.history(limit=5):
            if "UCP:" in msg.content:
                ucp = msg.content.split("UCP:")[1].split()[0].lower()
                if any(b in ucp for b in blacklist_ucp):
                    await channel.send("⚠️ User ini masuk daftar blacklist!")
                else:
                    await channel.send("✅ Tidak ditemukan di blacklist.")
                break

client.run("MTA0NzA3NjM3NjMxNTk2OTU3Ng.GCuohI.NNpETZJ3ftJ8twSux_pTLohoVLM8JLbHqxeR5w")
