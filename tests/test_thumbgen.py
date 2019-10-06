from thumbgen import __version__
from thumbgen.thumbgen import get_all_files, get_all_images, thumbnail_folder


def test_version():
    assert __version__ == "0.1.0"


def test_get_all_files_work_correctly():
    all_files = get_all_files(dir_path="tests/fixtures/thumbnail_files")
    assert len(all_files) == 6


def test_get_all_images_work_correctly():
    all_images = get_all_images(dir_path="tests/fixtures/thumbnail_files")
    assert len(all_images) == 4


def test_thumbnail_folder_works_for_all_test_files():
    thumbnail_folder(dir_path="tests/fixtures/thumbnail_files", workers=1, only_images=False)


def test_thumbnail_folder_works_for_image_test_files():
    thumbnail_folder(dir_path="tests/fixtures/thumbnail_files", workers=1, only_images=True)
