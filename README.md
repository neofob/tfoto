# `tfoto` a simple tool to resize photos
**Summary:** *`tfoto` resizes a bunch of photos to whatever you configure in a
config file (size, sharpen...).*

### Quick use
```
$ pip install tfoto
$ tfoto --help
```

### Examples
```
$ mkvirtualenv foto
$ git clone https://github.com/neofob/tfoto
$ cd tfoto
$ mkdir -p ~/.config/image
$ cp src/tfoto/image.cfg ~/.config/image/image.cfg
...work on something
...be somewhere
$ tfoto /path/to/big_tif /path/to/camera_jpg /path/to/final_tif
```

**Note:**

	* The `-o` option--output to a directory--is not implemented yet
	* Only image files under a list of `DIRS` work for now; no recursive directory
	  traversal yet

__author__: *tuan t. pham*
