

from pyrogram import filters

from DaisyX.modules.helper_funcs.chat_status import user_admin
from DaisyX.services.pyrogram import pbot as app


@app.on_message(filters.command("ss") & ~filters.private & ~filters.edited)
@admins_only
async def take_ss(_, message):
    if len(message.command) != 2:
        await message.reply_text("Give A Url To Fetch Screenshot.")
        return
    url = message.text.split(None, 1)[1]
    m = await message.reply_text("**Taking Screenshot...**")
    await m.edit("**Uploading Screenshot...**")
    try:
        await message.reply_photo(
            photo=f"https://webshot.amanoteam.com/print?q={url}",
            caption=f"Screenshot of {url}",
        )
    except TypeError:
        await m.edit("No Such Website.")
        return
    await m.delete()
