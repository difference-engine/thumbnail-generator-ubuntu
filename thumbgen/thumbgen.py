import os
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import Union

import click
import gi
from loguru import logger
from tqdm import tqdm

gi.require_version("GnomeDesktop", "3.0")
from gi.repository import Gio, GnomeDesktop


global factory
factory = GnomeDesktop.DesktopThumbnailFactory()
logger.remove()
logger.add(sys.stdout, level="INFO")


def make_thumbnail(fpath: Path) -> bool:
    mtime = os.path.getmtime(fpath)
    # Use Gio to determine the URI and mime type
    f = Gio.file_new_for_path(str(fpath))
    uri = f.get_uri()
    info = f.query_info("standard::content-type", Gio.FileQueryInfoFlags.NONE, None)
    mime_type = info.get_content_type()

    if factory.lookup(uri, mtime) is not None:
        logger.debug(f"FRESH       {uri}")
        return False

    if not factory.can_thumbnail(uri, mime_type, mtime):
        logger.debug(f"UNSUPPORTED {uri}")
        return False

    thumbnail = factory.generate_thumbnail(uri, mime_type)
    if thumbnail is None:
        logger.debug(f"ERROR       {uri}")
        return False

    logger.debug(f"OK          {uri}")
    factory.save_thumbnail(thumbnail, uri, mtime)
    return True


def thumbnail_folder(*, dir_path: Union[str, Path], workers: int):
    all_images = get_all_images(dir_path=dir_path)
    with Pool(processes=workers) as p:
        list(tqdm(p.imap(make_thumbnail, all_images), total=len(all_images)))


def get_all_images(*, dir_path):
    check_valid_directory(dir_path=dir_path)
    img_suffixes = [".jpg", ".jpeg", ".png"]
    all_files = Path(dir_path).rglob("*")
    all_images = [fpath for fpath in all_files if fpath.suffix in img_suffixes]
    print(f"Found {len(all_images)} images in the directory: {dir_path.resolve()}")
    return all_images


def check_valid_directory(*, dir_path):
    if not (Path(dir_path).exists() and Path(dir_path).is_dir()):
        raise ValueError(f"{dir_path} doesn't exists or isn't a valid directory")


@logger.catch()
@click.command()
@click.option(
    "-d", "--img_dirs", help='directories to recursively generate thumbnails seperated by space, eg: "dir1/dir2 dir3"'
)
@click.option("-w", "--workers", default=1, help="no of cpus to use for processing")
def main(img_dirs, workers):
    img_dirs = [Path(img_dir) for img_dir in img_dirs.split()]
    for img_dir in img_dirs:
        thumbnail_folder(dir_path=img_dir, workers=int(workers))
    print("Thumbnail Generation Completed!")


if __name__ == "__main__":
    main()
