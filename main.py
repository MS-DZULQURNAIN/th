import os, time
from display_progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from pyromod import listen
from env import BOT_TOKEN, API_ID, API_HASH, thumb, FSUB, BOT_NAME, CHANNEL_ID


Bot = Client(
    "Thumb-Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hi {}, I am video thumbnail changer Bot.

Send a video/file to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/soebb/thumb-change-bot'),
        ]]
    )

@Bot.on_message(filters.incoming & filters.private, group=-1)
async def fsub(bot, message):
  if not FSUB:
    return True
  try:
    await bot.get_chat_member(FSUB, message.from_user.id)
  except UserNotParticipant:
    if FSUB.startswith("-100"):
      link = await bot.export_chat_invite_link(FSUB)
    else:
      link = f"https://t.me/{FSUB}"
    tfsub = f"👋Halo {message.from_user.mention}\n\nSebelum menggunakan {BOT_NAME} kamu harus subscribe atau join channel dibawah ini jika sudah klik coba lagi💡"
    bfsub = InlineKeyboardMarkup([
                                  [InlineKeyboardButton(text="Join Channel", url=link),],
                                  [InlineKeyboardButton(text="Coba lagi", url=f"https://t.me/{bot.username}?start={message.command[1]}")]
                                ])
    await message.reply_text(tfsub, reply_markup=bfsub)
    await message.stop_propagation()


@Bot.on_message(filters.command(["start"]))
async def start(bot, message):
    text = START_TXT.format(message.from_user.mention, BOT_NAME)
    reply_markup = START_BTN
    await message.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    id = f'{message.from_user.id}'
    tag = f'{message.from_user.first_name}](tg://user?id={message.from_user.id})'
    await bot.send_message(int(CHANNEL_ID), f"**#BOT_START**\n\n{tag} MEMULAI BOT🔥\nUser id : `{id}`")




@Bot.on_message(filters.private & (filters.video | filters.document))
async def thumb_change(bot, m):
    global thumb
    msg = await m.reply("`Downloading..`", parse_mode='md')
    c_time = time.time()
    file_dl_path = await bot.download_media(message=m, progress=progress_for_pyrogram, progress_args=("Downloading file..", msg, c_time))
    await msg.delete()
    answer = await bot.ask(m.chat.id,'Now send the thumbnail' + ' or /keep to keep the previous thumb' if thumb else '', filters=filters.photo | filters.text)
    if answer.photo:
        try:
            os.remove(thumb)
        except:
            pass
        thumb = await bot.download_media(message=answer.photo)
    msg = await m.reply("`Uploading..`", parse_mode='md')
    c_time = time.time()
    if m.document:
        await bot.send_document(chat_id=m.chat.id, document=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    elif m.video:
        await bot.send_video(chat_id=m.chat.id, video=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    await msg.delete()
    os.remove(file_dl_path)


print("THUMBNAIL BOT BERHASIL DIAKTIFKAN 🔥🔥🔥")
print("by @MSDZULQRNN t.me/MSPR0JECT | t.me/envSample")
Bot.run()
