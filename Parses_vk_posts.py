import json
import os
import requests

token = "12c1364a9d426d4c3a654bd1d279e4953df572a80f4b9aed00b4e3c9f2cd8de242dd3c3630368e0d0546c"
group_name="azbukaxaypa"
def get_wall_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.81"
    req = requests.get(url)
    src = req.json()

    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)

    # сохраняем данные в json файл, чтобы видеть структуру
    with open(f"{group_name}/{group_name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    """Проверка, если файла не существует, значит это первый
    парсинг группы(отправляем все новые посты). Иначе начинаем
    проверку и отправляем только новые посты."""
    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("Файла с ID постов не существует, создаём файл!")

        with open(f"{group_name}/exist_posts_{group_name}.txt", "w") as file:
            for item in fresh_posts_id:
                file.write(str(item) + "\n")

        # извлекаем данные из постов
        for post in posts:
            #Сохраняем фотки
            def download_img(url, post_id, group_name):
                res = requests.get(url)

                # создаем папку group_name/files
                if not os.path.exists(f"{group_name}/files"):
                    os.mkdir(f"{group_name}/files")

                with open(f"{group_name}/files/{post_id}.jpg", "wb") as img_file:
                    img_file.write(res.content)
            #пробкем извелкать ссылку с фото
            try:
                post_id = post["id"]
                print(f"{post_id}")
                if "attachments" in post:
                    post = post["attachments"]

                    photo_quality = {
                    "m": 0,
                    "o": 1,
                    "p": 2,
                    "q": 3,
                    "r": 4,
                    "s": 5,
                    "w": 6,
                    "x": 7,
                    "y": 8,
                    "z": 9
                    }
                    if len(post) == 1:
                        # забираем фото
                        i=0
                        if post[0]["type"] == "photo":
                            for pq in photo_quality:
                                if pq in post[0]["photo"]["sizes"][i]["type"]:
                                    post_photo = post[0]["photo"]["sizes"][photo_quality[pq]]["url"]
                                    print(f"Фото с расширением {pq}")
                                    print(post_photo)
                                    download_img(post_photo, post_id, group_name)
                                    i+=1
                                    break
                    elif post[0]["type"] == "video":
                        print("Видео пост")
            except Exception:
                print("Сори")




def main():
    get_wall_posts(group_name)


if __name__ == '__main__':
    main()