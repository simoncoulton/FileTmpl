#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sublime
import sublime_plugin
from FileTmpl import filetmpl
from FileTmpl.filetmpl import log, SIDEBAR_MENU, MAIN_MENU
from FileTmpl import filetmpl_templates as templates


def new_template_from_path(path):
    window = sublime.active_window()
    window.new_file()
    content = templates.read_template(path)
    window.active_view().run_command('insert_snippet', {'contents': content})


class CreateTemplateCommand(sublime_plugin.TextCommand):

    def run(self, edit, paths, path):
        new_template_from_path(path)


class ReloadTemplateMenuCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        refresh_menu()


class NewFileFromTemplateCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.find_templates()
        self.show_quick_panel(self.templates, self.template_selected)

    def find_templates(self):
        self.templates, self.template_paths = templates.flat_templates()
        return self.templates

    def show_quick_panel(self, options, done):
        sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

    def template_selected(self, selected_index):
        if selected_index != -1:
            new_template_from_path(self.template_paths[selected_index])


class OpenInFinderCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None, parameters=None, file=None):
        print(file)
        arg = ['open', '-R', file]
        subprocess.Popen(arg)


SIDEBAR_MENU_CONTENT = '''
[
    {{ "caption": "-" }},
    {{
        "caption": "New File from Template...",
        "children":
        [
            {children}
            {{ "caption": "-" }},
            {{
                "caption": "Reload Templates",
                "command": "reload_template_menu"
            }}
        ]
    }}
]
'''

MAIN_MENU_CONTENT = '''
[
    {{
        "caption": "File",
        "mnemonic": "F",
        "id": "file",
        "children": [{{
            "caption": "-"
        }}, {{
        "caption": "New File from Template...",
        "children":
        [
            {children}
            {{ "caption": "-" }},
            {{
                "caption": "Reload Templates",
                "command": "reload_template_menu"
            }}
        ]
    }}]
    }},
    {{
        "caption": "Preferences",
        "mnemonic": "n",
        "id": "preferences",
        "children":
        [{{
            "caption": "Package Settings",
            "mnemonic": "P",
            "id": "package-settings",
            "children": 
            [{{
                "caption": "FileTmpl",
                "children": 
                [{{
                    "command": "open_in_finder",
                    "args": {{
                        "file": "${{packages}}/User/FileTmpl"
                    }},
                    "caption": "Manage Templates"
                }}]
            }}]
        }}]
    }}
]
'''

MENU_ITEM = '''
{{
    "caption": "{}",
    "children":
    [
        {children}
    ]
}}
'''

CHILD_MENU_ITEM = '''
{{
    "id": "{}",
    "caption": "{}",
    "command": "create_template",
    "args": {{"paths": [], "path": "{}"}}
}}
'''


class MenuUpdater(object):
    name = None
    menu_path = None

    def __init__(self, name="..."):
        self.name = name

    def update_menu(self, menu_name, menus):
        menu = os.path.join(os.path.dirname(__file__), menu_name)
        with open(menu, 'w', encoding='utf-8') as f:
            f.write(menus)

    def remove_menu(self, menu_name):
        if os.path.exists(self.menu_path):
            menu = os.path.join(self.menu_path, menu_name)
            if os.path.exists(menu):
                os.remove(menu)

    @property
    def menu_items(self):
        tpls = templates.list_templates()
        s = sorted(tpls.keys())
        items = []
        for key in s:
            key_tpls = tpls[key]
            children = [
                CHILD_MENU_ITEM.format(
                    t['name'], t['name'], t['path']) for t in key_tpls]
            items.append(MENU_ITEM.format(key, children=','.join(children)))
        return items

    def main(self):
        self.update_menu(
            MAIN_MENU,
            MAIN_MENU_CONTENT.format(children=','.join(self.menu_items) + ',')
        )

    def sidebar(self):
        self.update_menu(
            SIDEBAR_MENU,
            SIDEBAR_MENU_CONTENT.format(children=','.join(self.menu_items) + ',')
        )


def update_menu():
    updater = MenuUpdater()
    updater.sidebar()
    updater.main()
    log('Updated menu.')


def refresh_menu():
    update_menu()
    settings = filetmpl.load_settings()
    settings.clear_on_change('reload_menu')
    settings.add_on_change('reload_menu', refresh_menu)


def plugin_loaded():
    refresh_menu()
