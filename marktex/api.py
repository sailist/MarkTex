from typing import List
from marktex.util import config
import os
from marktex.markast.environments import parse_env, format_parent
from marktex.markast.environments import Environ
from marktex.markast.lines import parse_lines, Line
from marktex.markast.tokens import parse_tokens, Token


class Parser:
    def __init__(self):
        from marktex.util import cache, config
        cache.clear()

    def parse_md_ast_from_lines(self, lines: List[str]):
        ast = parse_env(lines)
        parse_lines(ast)
        parse_tokens(ast)
        return ast

    def parse_md_ast_from_file(self, file: str, new_config=True):
        if new_config:
            from marktex.util import config
            import os
            config.change_to_input_dir(os.path.dirname(file))

        with open(file, 'r', encoding='utf-8') as r:
            lines = r.readlines()
            return self.parse_md_ast_from_lines(lines)

    def parse_md_ast_from_string(self, line: str):
        return self.parse_md_ast_from_lines([line])

    def print_ast(self, ast: List[Environ]):
        for env in ast:
            print(env)

    def ast_to_texdoc(self, ast: List[Environ],
                      templete=None):
        from marktex.texparser import texparser

        return texparser.decode_ast(ast, templete)

    def parse_md_to_tex_from_file(self,
                                  file: str,
                                  output_dir,
                                  cacheimg_dir,
                                  templete):
        config.change_to_input_dir(os.path.dirname(file), output_dir, cacheimg_dir)
        ast = self.parse_md_ast_from_file(file, False)
        return self.ast_to_texdoc(ast, templete)


def convert(*input_files, output_dir=None, cacheimg_dir=None, templete=None):
    if not isinstance(output_dir, list):
        output_dir = [output_dir] * len(input_files)
    if not isinstance(cacheimg_dir, list):
        cacheimg_dir = [cacheimg_dir] * len(input_files)

    for file, opt_dir, cache_dir in zip(input_files, output_dir, cacheimg_dir):
        bfn = os.path.basename(file)
        pre, _ = os.path.splitext(bfn)
        parser = Parser()
        doc = parser.parse_md_to_tex_from_file(file, opt_dir, cache_dir, templete)

        opt_fn = os.path.join(config.output_dir, pre)
        doc.generate_tex(opt_fn)
        print('{} converted to {}.tex'.format(file, opt_fn))


def run_example():
    os.getcwd()
    base = os.path.join(os.path.dirname(__file__), 'example')
    fs = os.listdir(base)
    fs = [os.path.join(base, f) for f in fs]
    convert(*fs, output_dir=os.path.join(os.getcwd(), 'outputs'))
