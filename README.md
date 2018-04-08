# Sublime Settings extractor

Python2/3 script to extract sublime settings from `Packages/User` folder (Win/Linux) to given directory. This directory can be used to backup Sublime configuration and packages (packages will be reinstalled on new machine)

`Packages/User` includes your ST3 license and propably other "not safe" files so this approach is better that just syncing this folder through cloud. 

# Configuration

This package has `lists.py` file with two lists: `WANT_LIST` and `IGNORE_LIST`. Both of them has top-level paths from sublime settings folder defined. `WANT_LIST` is list of paths that should be copied, `IGNORE_LIST` - paths that should not. If file is not on one of this lists - script will issue warning and path won't be copied. By default this lists follow PackageControl backup instructions https://packagecontrol.io/docs/syncing.

# Usage

```
usage: sublime_settings_extractor.py [-h] [-v] copy_dir

positional arguments:
  copy_dir

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose
```

Example:
`python sublime_settings_extractor.py conf_backup -v`

