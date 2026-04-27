from __future__ import annotations

import ast
from itertools import zip_longest
from textwrap import indent

NO_DEFAULT = object()


def _extract_positional_args(
    arguments: ast.arguments,
) -> list[dict]:
    return [
        {
            'name': arg.arg,
            'type': getattr(arg.annotation, 'id', '__type__'),
            'default': (
                default.value
                if default is not NO_DEFAULT
                else default
            ),
        }
        for arg, default in zip_longest(
            reversed([*arguments.posonlyargs, *arguments.args]),
            reversed(arguments.defaults),
            fillvalue=NO_DEFAULT,
        )
        if arg.arg not in ['self', 'cls']
    ][::-1]


def _extract_star_args(
    arguments: ast.arguments,
) -> list[dict | None]:
    return [
        {
            'name': f'*{arg.arg}'
            if arg_type == 'vararg'
            else f'**{arg.arg}',
            'type': getattr(arg.annotation, 'id', '__type__'),
            'default': NO_DEFAULT,
        }
        if arg
        else None
        for arg_type in ['vararg', 'kwarg']
        for arg in [getattr(arguments, arg_type)]
    ]


def _extract_keyword_args(
    arguments: ast.arguments,
) -> list[dict]:
    return [
        {
            'name': arg.arg,
            'type': getattr(arg.annotation, 'id', '__type__'),
            'default': NO_DEFAULT
            if default is None
            else default.value,
        }
        for arg, default in zip(
            arguments.kwonlyargs, arguments.kw_defaults
        )
    ]


def extract_arguments(arguments: ast.arguments) -> tuple[dict]:
    args = _extract_positional_args(arguments)

    varargs, kwargs = _extract_star_args(arguments)
    if varargs:
        args.append(varargs)

    args.extend(_extract_keyword_args(arguments))

    if kwargs:
        args.append(kwargs)

    return tuple(args)


def extract_return_annotation(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.Name):
        return str(node.id)
    return '__return_type__'


def suggest_docstring(
    node: ast.AsyncFunctionDef | ast.FunctionDef,
) -> str:
    if args := extract_arguments(node.args):
        args = [
            f'{arg["name"]} : {arg["type"]}'
            + (
                f', default {arg["default"]}'
                if arg['default'] is not NO_DEFAULT
                else ''
            )
            + '\n    __description__'
            for arg in args
        ]
        args = ['', 'Parameters', '----------', *args]
    else:
        args = []

    returns = (
        extract_return_annotation(node.returns)
        + '\n    __description__'
    )
    return '\n'.join(
        [
            '"""',
            '___description___',
            *args,
            '',
            'Returns',
            '-------',
            returns,
            '"""',
        ]
    )


class DocstringTransformer(ast.NodeTransformer):
    def _handle_missing_docstring(
        self, node: ast.AsyncFunctionDef | ast.FunctionDef
    ) -> None:
        if ast.get_docstring(node) is None:
            suggestion = suggest_docstring(node)
            prefix = ' ' * (node.col_offset + 4)
            docstring_node = ast.Expr(
                ast.Constant(
                    indent(suggestion[3:-3] + prefix, prefix)
                )
            )

            node.body.insert(0, docstring_node)
            node = ast.fix_missing_locations(node)

        return node

    def _visit_helper(
        self, node: ast.AsyncFunctionDef | ast.FunctionDef
    ) -> ast.AsyncFunctionDef | ast.FunctionDef:
        node = self._handle_missing_docstring(node)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        return self._visit_helper(node)

    def visit_FunctionDef(
        self, node: ast.FunctionDef
    ) -> ast.FunctionDef:
        return self._visit_helper(node)


if __name__ == '__main__':
    from pathlib import Path

    file = Path(__file__)
    source_code = file.read_text()
    tree = ast.parse(source_code)

    visitor = DocstringTransformer()
    tree = visitor.visit(tree)

    Path(file.stem + '_edited' + file.suffix).write_text(
        ast.unparse(tree)
    )
