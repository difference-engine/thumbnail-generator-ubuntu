from pathlib import Path

from thumbgen import __version__
from thumbgen.thumbgen import get_all_files, get_all_images, thumbnail_folder

THIS_DIRECTORY = Path(__file__).parent


def test_images_directory():
    return THIS_DIRECTORY / "fixtures/thumbnail_files"


def test_version():
    assert __version__ == "0.1.0"


def test_get_all_files_work_correctly():
    all_files_recursive = get_all_files(dir_path=test_images_directory(), recursive=True)
    all_files = get_all_files(dir_path=test_images_directory(), recursive=False)
    assert len(all_files_recursive) == 12
    assert len(all_files) == 6


def test_get_all_images_work_correctly():
    all_files_recursive = get_all_files(dir_path=test_images_directory(), recursive=True)
    all_files = get_all_files(dir_path=test_images_directory(), recursive=False)
    all_images = get_all_images(all_files=all_files)
    all_images_recursive = get_all_images(all_files=all_files_recursive)
    assert len(all_images) == 4
    assert len(all_images_recursive) == 8


def test_thumbnail_folder_works_for_all_test_files_recursive():
    thumbnail_folder(dir_path=test_images_directory(), workers=1, only_images=False)


def test_thumbnail_folder_works_for_image_test_files():
    thumbnail_folder(dir_path=test_images_directory(), workers=1, only_images=True)
