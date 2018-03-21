#!/bin/true

IGNORE_LIST = [
    r'\.SublimeREPLHistory',
    r'after',
    r'c2u',
    r'Package Control\.cache',
    r'Projects',
    r'encoding_cache\.json',
    r'MD5:8b52288842a6f5c169180c5bbfb0a4b1', #internal
    r'MD5:bfec9aefaf7f0f9dac71e36f846fd0e7', #internal
    r'MD5:4e4311e379a8b137d5f3614924a5994a', #internal
    r'MD5:3fd11df0a86840023be0d9cc3eb99369', #internal
    r'.*crt',
    r'OverrideAudit\.status',
    r'Package Control\.(last-run|ca-bundle|ca-list|system-ca-bundle|cache|ca-certs|merged-ca-bundle|user-ca-bundle)',
    r'.*bak',
    r'MD5:643421d12b881dc433b4e187ba0b0e00',
    r'Sublimerge\.sublime-license', # For now - keep it ignored, maybe safe-copy should be used. Or leverage external apis,
    r'.*\.cache',
    r'Color Highlighter',
    r'c2u_tmp'
]

WANT_LIST = [
    r'SodaSchemes',
    r'SublimeLinter',
    r'.*\.sublime-snippet',
    r'.*\.tmTheme',
    r'ApplySyntax.ext-list',
    r'.*\.sublime-settings',
    r'close_minimap_on_multi_view\.py',
    r'.*\.sublime-keymap',
    r'print_snippet.py',
    r'Sublimerge Macros.sublime-commands',
    r'Snippets'
]