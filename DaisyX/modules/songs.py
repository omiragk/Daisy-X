import os

import aiohttp
from pyrogram import filters
from pytube import YouTube
from youtubesearchpython import VideosSearch

from DaisyX import LOGGER, pbot
from DaisyX.utils.ut import get_arg


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@pbot.on_message(filters.command("song"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("Processing...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("Song not found.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")


__help__ = """
*🎧 Playing Music in Voice chats using Anna*

please add these 2 accounts to your group
 1. [Bot](https://t.me/musicandsong_play_robot)
 2. [Assistant](https://t.me/ogk_music_player)

👉 Cannot add Bot or Assistant??
    - [contact me](https://t.me/omiragk)

👉 Need any help??
    - [contact me](https://t.me/omiragk)

*👇here are the commands👇*

For all members in group

/play - reply to youtube url or song file to play song
/play <song name> - play song you requested
/search <query> - search videos on youtube with details

Group Admins only

/pause - pause song play
/resume - resume song play
/skip or /next - play next song
/end - stop music play
/joinplayer - invite assistant to your group
/leaveplayer - remove assistant from your group

🎧 Enjoy Music  😍
"""

__mod_name__ = "Music 🎧"
