import os
import secrets

from PIL import Image
from flask import current_app


def save_profile_picture(form_picture) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext.lower()
    picture_path = os.path.join(
        current_app.root_path,
        "static",
        "profile_pics",
        picture_fn,
    )

    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    output_size = (128, 128)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn
