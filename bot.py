import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import configparser
from main import generate_and_save_colored_image

config = configparser.ConfigParser()
config.read("config.ini")

token = config.get("base", "token")
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 215368688)
upload = vk_api.VkUpload(vk_session)


def send_message(recipient_id, text, attachment=None):
    vk_session.method("messages.send", {
        "chat_id": recipient_id,
        "message": text,
        "attachment": attachment,
        "random_id": 0
    })


def create_attachment(sender_id):
    image = upload.photo_messages("pictures/" + str(sender_id) + ".png")
    owner_id = image[0]['owner_id']
    photo_id = image[0]['id']
    access_key = image[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment


def message_handler(message_text: str, chat_id: int, sender_id: int):
    if "пиво" in message_text:
        send_message(chat_id, "пиво)🍻")
    if message_text == "!цвет":
        color_name = generate_and_save_colored_image(sender_id)["color_name"]
        attachment = create_attachment(sender_id)
        send_message(chat_id, f"[id{sender_id}|Браток], цвет твоего пива - {color_name}", attachment)
    if message_text == "помощь":
        send_message(chat_id, "!цвет: узнать цвет своего пива")


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            chat_id = event.chat_id
            sender_id = event.object.message["from_id"]
            message_text = event.object.message["text"].lower()
            message_handler(message_text, chat_id, sender_id)


if __name__ == "__main__":
    main()
