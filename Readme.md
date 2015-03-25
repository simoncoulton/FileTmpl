# FileTmpl

FileTmpl allows you to create some no fuss templates that can be used when creating new files. Think of them as snippets, with a little more organisation.

## Accessing your templates

There are 2 methods of accessing your templates:

1. Bring up the command palette and type `New File from Template`
2. Use the `New File from Template` option in the main/sidebar menus

## Reloading your templates

From the sidebar or main menu select `New File from Template` and then `Reload Templates`. Or restart Sublime Text, whichever is easiest for you.

## Creating a template

A template is a simple file that lives within your `Packages/User/FileTmpl/templates` directory. While it is not the same structure as a snippet, you can use snippet based logic within them. Each template must contain the following line at the top of the file to be classed as a template:

    # FileTmpl: [category]

[category] will be used within menus as a way of categorising your templates.


## Example templates

    # FileTmpl: PHP
    <?php
    namespace \${1:namespace};

    class ${2:Class}
    {}



    # FileTmpl: Python
    # -*- coding: ${1:utf-8} -*-

