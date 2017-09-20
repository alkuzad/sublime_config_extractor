#!/usr/bin/env python

import re
import argparse
from collections import namedtuple
import hashlib
from functools import partial
import os
import platform
import shutil
import logging

import six

from .lists import IGNORE_LIST, WANT_LIST # YYY repackage to setuptools and change to absolute import

FORMAT = '[%(asctime)-15s %(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)

LOGGER = logging.getLogger('SublimeCopy')
LOGGER.setLevel(logging.INFO)

# Original is original string passed as rule
# callback is callback function that will be called with original string to determine rule match
# type can be "ignore" or "keep"
Rule = namedtuple("FileRule", ('original', 'callback', 'type'))

class UserFileFinder(object):

    def __init__(self, want_list, ignore_list):
        self.path = self.get_user_folder()
        self.rules = []
        self.want_list = want_list
        self.ignore_list = ignore_list
        self.build_rules_list()

    @staticmethod
    def get_user_folder():
        if platform.system() == 'Windows':
            LOGGER.info("detected os: windows")
            if os.environ.get('APPDATA') is None:
                raise RuntimeError("No APPDATA information - check environment vars")
            return os.path.abspath(os.path.join(os.environ['APPDATA'], r'Sublime Text 3\\Packages\\User'))
        else: # fuck Apple
            LOGGER.info("detected os: linux")
            return os.path.expanduser('~/.config/sublime-text-3/Packages/User')

    @staticmethod
    def md5_check(md5string, filename):
        md5_hash = hashlib.new('md5')
        md5_hash.update(six.u(filename).encode('utf-8'))
        return md5string == md5_hash.hexdigest()

    @staticmethod
    def generate_regexp_check(regexp):
        regexp = "^{}$".format(regexp)
        return re.compile(regexp)

    def _parse_rules(self, rules_list, rule_type):
        for rule in rules_list:
            if rule.startswith('MD5:'):
                LOGGER.debug('generated MD5 rule from: %s', rule)
                self.rules.append(Rule(rule, partial(self.md5_check, rule[4:]), rule_type))
            else:
                LOGGER.debug('generated Regexp rule from: %s', rule)
                self.rules.append(Rule(rule, self.generate_regexp_check(rule).match, rule_type))

    def build_rules_list(self):
        self._parse_rules(self.ignore_list, 'ignore')
        self._parse_rules(self.want_list, 'keep')

    def find_files(self):
        files_to_copy = []
        for fil in os.listdir(self.path):
            matched = False
            for rule in self.rules:
                if rule.callback(fil):
                    matched = True
                    if rule.type == 'keep':
                        yield os.path.abspath(os.path.join(self.path, fil))
                    break
            if not matched:
                LOGGER.warning('file does not match to any rule: %s', fil)
        return files_to_copy

def dir_exists_or_create(path):
    if not os.path.exists(path):
        LOGGER.info("creating output dir: %s", path)
        os.makedirs(path)
    elif not os.path.isdir(path):
        raise ValueError("Path is not dir: {}".format(path))
    return os.path.realpath(path)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('copy_dir', type=dir_exists_or_create)
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def copy_files(files, dest_path):
    for file_to_copy in files:
        if os.path.isdir(file_to_copy):
            dest =  os.path.join(dest_path, os.path.basename(file_to_copy))
            if os.path.exists(dest):
                shutil.rmtree(dest)
                LOGGER.debug('removed old directory: %s', dest)
            shutil.copytree(file_to_copy, dest)
            LOGGER.debug('copied directory: %s', dest)
        else:
            shutil.copy2(file_to_copy, dest_path)
            LOGGER.debug('copied file: %s', file_to_copy)
def main():
    args = parse_args()
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    finder = UserFileFinder(WANT_LIST, IGNORE_LIST)
    copy_files(finder.find_files(), args.copy_dir)

if __name__ == '__main__':
    main()
