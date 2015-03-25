#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from FileTmpl import filetmpl


def list_templates():
    files = glob.glob(filetmpl.USER_TEMPLATE_PATH + '/**')
    templates = {}
    for file in files:
        with open(file, 'r') as f:
            line = f.readline()
            if line.startswith('# FileTmpl: '):
                line = line.split(' ')
                _type = ' '.join(line[2:]).strip('\n')
                if _type not in templates:
                    templates[_type] = []
            templates[_type].append(
                {'name': os.path.basename(file), 'path': file})
    return templates


def flat_templates():
    tpls = list_templates()
    flat = []
    paths = []
    for _type in tpls:
        for tpl in tpls[_type]:
            flat.append('{}: {}'.format(_type, tpl['name']))
            paths.append(tpl['path'])
    return flat, paths


def read_template(path):
    with open(path) as f:
        return ''.join(f.readlines()[1:])
    return ''
