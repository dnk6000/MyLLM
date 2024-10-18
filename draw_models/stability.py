import requests

import config

def get_image(prompt: str, fname: str) -> None:
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {config.STABILITY_API_KEY}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "jpeg",
        },
    )

    if response.status_code == 200:
        with open(fname, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))

def get_test_fname() -> str:
    return f"{config.DATA_FOLDER}\\story_title2.png"

if __name__ == "__main__":
    promt = ("A beautiful woman stands confidently in a modern, bustling city. She is wearing stylish leather clothing, "
             "giving her a sleek and futuristic look. Augmented reality glasses rest on her face, overlaying holographic "
             "data and vibrant visuals in the air around her. The cityscape behind her is detailed with tall "
             "skyscrapers, glowing neon signs, and digital billboards. The overall atmosphere is vivid and rich in "
             "color, with bright, juicy hues highlighting the woman's appearance and the advanced technology "
             "surrounding her.")
    get_image(promt, f"{config.DATA_FOLDER}\\story.jpg")

