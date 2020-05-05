"""This module provides functions for identifying unknown visages."""

import face_recognition as fr
from PIL import Image, ImageDraw, ImageFont
import os


def files_in_directory(directory, extensions=None):
    """
    Returns a list of files in a directory.

    :param directory: A directory path.
    :param extensions: A list of file extensions. Only files with extensions in
        this list will be returned. Defaults to None.
    :return: A list of file paths for the files in the given directory.
    """
    files = []
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            name, extension = os.path.splitext(filename)
            if extensions is None or extension in extensions:
                files.append(file)
    return files


def visage_encodings(visage_files):
    """
    Returns encodings for each visage in the given images.

    :param visage_files: A list of file paths to images containing visages.
    :return: A list of encodings for each visage in the given images.
    """
    encodings = []
    for file in visage_files:
        image = fr.load_image_file(file)
        encodings.append(fr.face_encodings(image)[0])
    return encodings


def identify(known_visages_directory, unknown_visages_file):
    """
    Identifies visages in an image and returns an image with the visages
    outlined and labeled.

    :param known_visages_directory: A path to a directory with images of
        known visages. The image filenames are used as labels for identified
        visages.
    :param unknown_visages_file: A file path to an image containing unknown
        visages.
    :return: An image with the unknown visages outlined and labeled.
    """
    known_visage_files = files_in_directory(known_visages_directory, [".jpg", ".png"])
    known_visage_encodings = visage_encodings(known_visage_files)
    known_visage_labels = [os.path.splitext(os.path.basename(file))[0] for file in known_visage_files]

    unknown_visages_image = fr.load_image_file(unknown_visages_file)
    unknown_visage_locations = fr.face_locations(unknown_visages_image)
    unknown_visage_encodings = fr.face_encodings(unknown_visages_image, unknown_visage_locations)

    identified_visages_image = Image.fromarray(unknown_visages_image)
    identified_visages_draw = ImageDraw.Draw(identified_visages_image)

    font = ImageFont.truetype("cour.ttf", 20)
    text_fill_color = "white"
    text_outline_color = "black"
    visage_outline_color = "black"

    for (top, right, bottom, left), unknown_visage_encoding in zip(unknown_visage_locations, unknown_visage_encodings):
        hits = fr.compare_faces(known_visage_encodings, unknown_visage_encoding)
        label = ""

        if True in hits:
            first_hit_index = hits.index(True)
            label = known_visage_labels[first_hit_index]

        # Visage outline
        identified_visages_draw.rectangle(((left, top), (right, bottom)), outline=visage_outline_color, width=8)

        text_width, text_height = identified_visages_draw.textsize(label)
        text_x, text_y = left, top - text_height - 10

        # Label outline
        identified_visages_draw.text((text_x - 1, text_y - 1), label, fill=text_outline_color, font=font)
        identified_visages_draw.text((text_x + 1, text_y - 1), label, fill=text_outline_color, font=font)
        identified_visages_draw.text((text_x - 1, text_y + 1), label, fill=text_outline_color, font=font)
        identified_visages_draw.text((text_x + 1, text_y + 1), label, fill=text_outline_color, font=font)

        # Label
        identified_visages_draw.text((text_x, text_y), label, fill=text_fill_color, font=font)

    del identified_visages_draw
    return identified_visages_image
