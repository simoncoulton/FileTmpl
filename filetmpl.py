#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sublime


SETTINGS = 'FileTmpl.sublime-settings'
MENU_PATH = ''
USER_PACKAGE_PATH = os.path.join(
    sublime.packages_path(),
    'User',
    'FileTmpl')

USER_TEMPLATE_PATH = os.path.join(USER_PACKAGE_PATH, 'templates')

SIDEBAR_MENU = "Side Bar.sublime-menu"
MAIN_MENU = "Main.sublime-menu"


def load_settings():
    return sublime.load_settings(SETTINGS)


def log(msg):
    print(str(msg))


def ensure_paths():
    if not os.path.exists(USER_PACKAGE_PATH):
        os.makedirs(USER_PACKAGE_PATH)
    if not os.path.exists(USER_TEMPLATE_PATH):
        os.makedirs(USER_TEMPLATE_PATH)
    log('Created paths.')


def plugin_loaded():
    ensure_paths()
