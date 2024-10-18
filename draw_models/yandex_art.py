import requests
import random
import time
import base64

import config


def get_image(prompt: str, fname: str) -> None:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
        "Authorization": f"Bearer {config.YANDEX_IAM_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"art://{config.YANDEX_CATALOG}/yandex-art/latest",
        "generationOptions": {
            "seed": f"{random.randint(0, 1000000)}",
            "aspectRatio": {
                "widthRatio": "16",
                "heightRatio": "9"
            }
        },
        "messages": [
            {
                "weight": "1",
                "text": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        request_id = response.json()['id']
        print(request_id)

        time.sleep(25)

        headers = {"Authorization": f"Bearer {config.YANDEX_IAM_TOKEN}"}
        url = f"https://llm.api.cloud.yandex.net:443/operations/{request_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(response.json())
            image_base64 = response.json()['response']['image']
            image_data = base64.b64decode(image_base64)
            with open(fname, 'wb') as file:
                file.write(image_data)
            print("Изображение успешно сохранено как image.jpeg")
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")
    else:
        print(response.text)

if __name__ == "__main__":
    promt = ("A beautiful woman stands confidently in a modern,bustling city.She is wearing stylish leather clothing, "
             "giving her a sleek and futuristic look. Augmented reality glasses rest on her face, overlaying holographic "
             "data and vibrant visuals in the air around her. The cityscape behind her is detailed with tall "
             "skyscrapers, glowing neon signs, and digital billboards. The overall atmosphere is vivid and rich in "
             "color,with bright,juicy hues highlighting the woman's appearance and the advanced technology")
    get_image(promt, f"{config.DATA_FOLDER}\\story_yart.jpg")
