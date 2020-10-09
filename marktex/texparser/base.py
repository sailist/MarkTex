from typing import Union, Dict, List, Callable, Any


def regist_decoder(val: Dict[Any, Callable], type_=None):
    def wrap(func):
        val[type_] = func
        return func

    return wrap


registed_env_decoder = {

}

registed_line_decoder = {

}

registed_token_decoder = {

}

registed_line_xml_decoder = {

}

sign_to_tex = {

}
import os

with open(os.path.join(os.path.dirname(__file__), 'sign_to_tex.txt'), 'r', encoding='utf-8') as r:
    for line in r:
        res = line.strip().split(' ')
        if len(res) == 1:
            res.append('unknown')
        l, r = res

        sign_to_tex[l] = r
