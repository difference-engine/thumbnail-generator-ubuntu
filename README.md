# Thumbgen

Pre-generates thumbnails for 'Gnome Files' formerly known as nautilus. This is useful if you have a lot of files which you want to glance over but you have to wait for them to load as you scroll.
Supports **Python 3.5+** and any Linux distro using Gnome Desktop 3.

## Basic Usage
```
# generating thumbnails for two directories
thumbgen -d directory1/directory1_1 directory2

# Pulling up the help
thumbgen --help
```

## Command Line Options
| short | long          | Description                                                                                         |
|-------|---------------|-----------------------------------------------------------------------------------------------------|
| -d    | --img_dirs    | directories to recursively generate thumbnails seperated by space, eg: "dir1/dir2 dir3"  [required] |
| -w    | --workers     | no of cpus to use for processing                                                                    |
| -i    | --only_images | Whether to only look for images to be thumbnailed                                                   |
| -r    | --recursive   | Whether to recursively look for files                                                               |
|       | --help        | CLI help                                                                                            |


## Installation

Install PyGObject pre-requisites for your OS from [here](https://pygobject.readthedocs.io/en/latest/getting_started.html). For Ubuntu/Debian:

```
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0
```

Then install Thumbgen using:
```
pip install thumbgen
```
