import requests
import configparser
from PIL import Image
from bs4 import BeautifulSoup
from colormap import rgb2hex

config = configparser.ConfigParser()
config.read("config.ini")

source_img_format = config.get("base", "source_img_format")


def generate_and_save_colored_image(user_id: int) -> Image:
    '''
    Генерирует картинку, покрашенную в индивидуальный для каждого
    пользователя цвет, а затем сохраняет в папку pictures с именем user_id.
    Цвет генерируется из user_id
        Параметры:
            image (PIL.Image) : Картинка, которую нужно покрасить
            user_id (int) : ID пользователя, которое конвертируется в цветовой код (RGB)
    '''
    source_image = Image.open("source." + source_img_format).convert("RGBA")
    color_rgb = convert_num_to_color(user_id)
    color_image = Image.new("RGBA", source_image.size, color_rgb)
    result = Image.blend(source_image, color_image, 0.5)
    result.save("pictures/" + str(user_id) + ".png")
    color_name = get_color_name(color_rgb)
    return {"image": result, "color_name": color_name}


def convert_num_to_color(num: int) -> tuple:
    '''
    Конвертирует число в кортеж с цветом в формате RGB
        Параметры:
            num (int) : Число, которое нужно конвертировать
    '''
    if num // 100 < 1:
        raise ValueError("ID is not long enough")
    num_str = str(num) # Для красоты и разборчивости в последующих строках
    a = int(len(num_str) / 3)
    color_list = [int(num_str[:a]), int(num_str[a:2*a]), int(num_str[2*a:])]
    for index, element in enumerate(color_list):
        while element > 255:
            element = element // 2
        color_list[index] = element
    return tuple(color_list)


def get_color_name(color_rgb: tuple):
    '''
    Возвращает название цвета по HEX коду с номощью парсинга сайта whatcolor.ru/color
        Параметры:
            color_rgb (tuple) : Цвет в формате RGB, название которого нужно узнать
    '''
    color_hex = rgb2hex(color_rgb[0], color_rgb[1], color_rgb[2]).replace("#", '')
    page = requests.get("https://whatcolor.ru/color/", color_hex)
    soup = BeautifulSoup(page.content, "html.parser")
    color_name = soup.find("h2", {'class': "c2-h2"}).text
    return color_name.lower()


def main():
    input_id = int(input("ID: "))
    generate_and_save_colored_image(input_id)


if __name__ == "__main__":
    main()
