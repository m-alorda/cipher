"""               Copyright 2022 m-alorda

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from pathlib import Path

import cv2


SCRIPT_DIR = Path(__file__).resolve().parent
SYMBOLS_DIR = SCRIPT_DIR / "symbols"


def load_image(
    filename: str,
) -> cv2.Mat:
    """Loads the given image from resources"""

    file_path = SYMBOLS_DIR / filename
    return cv2.imread(str(file_path))


def concat_images_vertically(
    images: tuple[cv2.Mat, ...],
) -> cv2.Mat:
    """Concatenates the given images vertically in the given order

    Images are padded to the width of the largest image.
    """
    result_width = max(image.shape[1] for image in images)
    padded_images = tuple(
        _pad_image_to_the_right(
            image,
            desired_width=result_width,
        )
        for image in images
    )
    return cv2.vconcat(padded_images)


def _pad_image_to_the_right(image: cv2.Mat, desired_width: int) -> cv2.Mat:
    num_pixels_to_pad = desired_width - image.shape[1]
    return cv2.copyMakeBorder(
        image,
        top=0,
        bottom=0,
        left=0,
        right=num_pixels_to_pad,
        borderType=cv2.BORDER_REPLICATE,
    )


def concat_images_horizontally(
    images: tuple[cv2.Mat, ...],
    interpolation_type: int = cv2.INTER_CUBIC,
) -> cv2.Mat:
    """Concatenates the given images horizontally in the given order

    Images are resized to the height of the smallest image.

    Interpolation_type is the interpolation algorithm to use to resize images.
    """
    result_height = min(image.shape[0] for image in images)
    resized_images = tuple(
        _resize_image(
            image,
            result_height,
            interpolation_type,
        )
        for image in images
    )
    return cv2.hconcat(resized_images)


def _calculate_new_width(
    current_width: int,
    current_height: int,
    new_height: int,
) -> int:
    reshape_ratio = new_height / current_height
    return int(current_width * reshape_ratio)


def _resize_image(
    image: cv2.Mat,
    new_height: int,
    interpolation_type: int,
) -> cv2.Mat:
    return cv2.resize(
        src=image,
        dsize=(
            _calculate_new_width(
                current_width=image.shape[1],
                current_height=image.shape[0],
                new_height=new_height,
            ),
            new_height,
        ),
        interpolation=interpolation_type,
    )
