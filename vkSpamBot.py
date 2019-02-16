import vk_api
import random
import time
import requests
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask


ANTICAPTCHA_KEY = "HERE_IS_THE_KEY"


def makeImage(url):
    f = open('test', 'wb')
    f.write(requests.get(url).content)
    f.close()
    k = open('test', 'rb')
    return k


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция.
    """

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def captcha_handler2(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    captcha_fp = makeImage(captcha.get_url())
    client = AnticaptchaClient(ANTICAPTCHA_KEY)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    return captcha.try_again(job.get_captcha_text())


def main():

    login = "HERE_IS_YOUR_LOGIN"
    password = "HERE_IS_THE_PASS"
    vk_session = vk_api.VkApi(
        login, password,
        captcha_handler=captcha_handler2,  # функция для обработки капчи
        auth_handler=auth_handler  # функция для обработки двухфакторной аутентификации
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    message_new = "SpamLord xD"
    i = 0
    # YOU CAN DO SPAM WHATEVER YOU WANT, COZ VK_API GOT A LOT STUFF TO DO
    while True:
        try:
            time.sleep(0.5)
            vk.wall.createComment(owner_id=-"ID_THERE", post_id="POST_THERE", message="MESS", v='5.85')
            print(("#" * i) + "Sending responses")
            i += 1
        except vk_api.exceptions.Captcha:
            i = 0
            rand = random.randint(0, 1)
            print("#Sleeping for " + str(rand) + " seconds")
            time.sleep(rand)


if __name__ == '__main__':
    main()
