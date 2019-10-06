import os
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import List, Union

import click
import gi
from loguru import logger
from tqdm import tqdm

gi.require_version("GnomeDesktop", "3.0")
from gi.repository import Gio, GnomeDesktop  # isort:skip


global factory
factory = GnomeDesktop.DesktopThumbnailFactory()
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("/tmp/thumbgen.log", level="DEBUG", rotation="100 MB")


def make_thumbnail(fpath: str) -> bool:
    mtime = os.path.getmtime(fpath)
    # Use Gio to determine the URI and mime type
    f = Gio.file_new_for_path(str(fpath))
    uri = f.get_uri()
    info = f.query_info("standard::content-type", Gio.FileQueryInfoFlags.NONE, None)
    mime_type = info.get_content_type()

    if factory.lookup(uri, mtime) is not None:
        logger.debug("FRESH       {}".format(uri))
        return False

    if not factory.can_thumbnail(uri, mime_type, mtime):
        logger.debug("UNSUPPORTED {}".format(uri))
        return False

    thumbnail = factory.generate_thumbnail(uri, mime_type)
    if thumbnail is None:
        logger.debug("ERROR       {}".format(uri))
        return False

    logger.debug("OK          {}".format(uri))
    factory.save_thumbnail(thumbnail, uri, mtime)
    return True


@logger.catch()
def thumbnail_folder(*, dir_path: Union[str, Path], workers: int, only_images: bool, recursive: bool) -> None:
    all_files = get_all_files(dir_path=dir_path, recursive=recursive)
    if only_images:
        all_files = get_all_images(all_files=all_files)
    all_files = [str(fpath) for fpath in all_files]
    with Pool(processes=workers) as p:
        list(tqdm(p.imap(make_thumbnail, all_files), total=len(all_files)))


def get_all_images(*, all_files: List[Path]) -> List[Path]:
    img_suffixes = [".jpg", ".jpeg", ".png", ".gif"]
    all_images = [fpath for fpath in all_files if fpath.suffix in img_suffixes]
    print("Found {} images".format(len(all_images)))
    return all_images


def get_all_files(*, dir_path: Union[str, Path], recursive: bool) -> List[Path]:
    check_valid_directory(dir_path=dir_path)
    if recursive:
        all_files = Path(dir_path).rglob("*")
    else:
        all_files = Path(dir_path).glob("*")
    all_files = [fpath for fpath in all_files if fpath.is_file()]
    print("Found {} files in the directory: {}".format(len(all_files), Path(dir_path).resolve()))
    return all_files


def check_valid_directory(*, dir_path: Union[str, Path]) -> None:
    if not (Path(dir_path).exists() and Path(dir_path).is_dir()):
        raise ValueError("{} doesn't exists or isn't a valid directory".format(dir_path.resolve()))


@click.command()
@click.option(
    "-d", "--img_dirs", required=True, help='directories to generate thumbnails seperated by space, eg: "dir1/dir2 dir3"'
)
@click.option("-w", "--workers", default=1, help="no of cpus to use for processing")
@click.option(
    "-i", "--only_images", is_flag=True, default=False, help="Whether to only look for images to be thumbnailed"
)
@click.option("-r", "--recursive", is_flag=True, default=False, help="Whether to recursively look for files")
def main(img_dirs: str, workers: str, only_images: bool, recursive: bool) -> None:
    img_dirs = [Path(img_dir) for img_dir in img_dirs.split()]
    for img_dir in img_dirs:
        thumbnail_folder(dir_path=img_dir, workers=workers, only_images=only_images, recursive=recursive)
    print("Thumbnail Generation Completed!")


if __name__ == "__main__":
    main()
