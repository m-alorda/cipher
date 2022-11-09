#!/usr/bin/env python
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
import uuid
import string

import fire
import cv2

from image_utils import (
    load_image,
    concat_images_horizontally,
    concat_images_vertically,
)


NUMERIC_CYPHER_MAP = {
    "a": "11",
    "b": "21",
    "c": "31",
    "d": "41",
    "e": "51",
    "f": "12",
    "g": "22",
    "h": "32",
    "i": "42",
    "j": "52",
    "k": "13",
    "l": "23",
    "m": "33",
    "n": "43",
    "ñ": "53",
    "o": "14",
    "p": "24",
    "q": "13",
    "r": "34",
    "s": "44",
    "t": "54",
    "u": "15",
    "v": "22",
    "w": "25",
    "x": "35",
    "y": "45",
    "z": "55",
}


class Cipher:
    """Allows encrypting text using different known algorithms"""

    def caesar(
        self,
        plain_text: str,
        shift: int = 5,
    ) -> str:
        """Ciphers plain_text using a caesar cipher

        This cipher is case sensitive.
        Non letter characters will not be ciphered.
        """

        alphabet = string.ascii_lowercase
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]
        caesar_cipher_map = {
            original_character: ciphered_character
            for original_character, ciphered_character in zip(
                alphabet, shifted_alphabet
            )
        }

        def cipher(char: str) -> str:
            ciphered_char = caesar_cipher_map.get(char.lower(), char)
            return ciphered_char if char.islower() else ciphered_char.upper()

        return "".join(cipher(char) for char in plain_text)

    def numeric(
        self,
        plain_text: str,
    ) -> str:
        """Ciphers plain_text using a numeric cipher

        This cipher is case insensitive.
        Non letter characters will not be ciphered.
        """

        def cipher(char: str) -> str:
            return NUMERIC_CYPHER_MAP.get(char.lower(), char)

        def cipher_line(line: str) -> str:
            return " ".join(cipher(char) for char in line)

        return "\n".join(cipher_line(line) for line in plain_text.split("\n"))

    def symbolic(
        self,
        plain_text: str,
        tab_size: int = 4,
    ) -> Path:
        """Ciphers plain_text using a symbolic cipher

        This cipher is case insensitive.
        Only letter characters and whitespace are supported.
        """
        symbolic_image_map = {
            char: load_image(f"{char}.png") for char in string.ascii_lowercase
        }
        symbolic_image_map[" "] = load_image("whitespace.png")
        supported_image_chars = set(symbolic_image_map.keys())
        supported_image_chars.add("\r")
        supported_image_chars.add("\n")
        supported_image_chars.add("\t")

        def cipher(char: str) -> cv2.Mat:
            if char == "\r":
                return concat_images_horizontally(
                    tuple(symbolic_image_map[" "] for _ in range(tab_size))
                )
            return symbolic_image_map[char.lower()]

        def cipher_line(line: str) -> cv2.Mat:
            if line == "":
                return symbolic_image_map[" "]
            return concat_images_horizontally(tuple(cipher(char) for char in line))

        for char in plain_text:
            if char.lower() not in supported_image_chars:
                raise ValueError(
                    f"Unsupported character: {char}. "
                    f"Valid characters are: {symbolic_image_map.keys()}"
                )

        result_image = concat_images_vertically(
            tuple(
                cipher_line(line) for line in plain_text.replace("\r", "").split("\n")
            )
        )

        output_path = Path(f"encripted_message_{uuid.uuid4()}.png").resolve()
        cv2.imwrite(str(output_path.absolute()), result_image)
        return output_path


if __name__ == "__main__":
    fire.Fire(Cipher)
