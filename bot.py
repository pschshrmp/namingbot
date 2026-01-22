import telebot
import os

TOKEN = "7993511767:AAEAl5IR2L5n0WTXZ5EZMT24qnOOvgUxe70"
bot = telebot.TeleBot(TOKEN)

user_files = {}  # временно храним путь к файлу

@bot.message_handler(content_types=["audio", "document"])
def handle_audio(message):
    if message.audio:
        file_id = message.audio.file_id
        original_name = message.audio.file_name
    elif message.document and message.document.file_name.endswith(".mp3"):
        file_id = message.document.file_id
        original_name = message.document.file_name
    else:
        bot.send_message(message.chat.id, "Отправь MP3 файл 🎵")
        return

    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)

    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{message.chat.id}_audio.mp3"

    with open(file_path, "wb") as f:
        f.write(downloaded)

    user_files[message.chat.id] = file_path
    bot.send_message(message.chat.id, f"Файл получен: {original_name}\n\nНапиши новое название (без .mp3)")

@bot.message_handler(func=lambda m: m.chat.id in user_files)
def rename_file(message):
    new_name = message.text.strip()
    old_path = user_files.pop(message.chat.id)

    new_path = f"temp/{new_name}.mp3"
    os.rename(old_path, new_path)

    with open(new_path, "rb") as f:
        bot.send_audio(message.chat.id, f)

    os.remove(new_path)

# ✅ Исправлено: polling должен быть в конце, вне функций
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)