# -*- coding: utf-8 -*-
def check_fields(fields, args):
    return False if False in [_arg in args for _arg in fields] else True
