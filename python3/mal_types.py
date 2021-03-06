#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing


class MalType:
    pass


class MalList(MalType, list):
    pass


class MalNumber(MalType, int):
    pass


class MalString(MalType, str):
    pass


class MalSymbol(MalType, str):
    pass


class MalKeyword(MalType, str):
    def __init__(self, s):
        self.value = '\u200B' + s

    def __str__(self):
        return self.value[1:]

    def __eq__(self, other):
        if isinstance(other, MalKeyword):
            return self.value == other.value
        else:
            return self.value == other


class MalVector(MalType, list):
    pass


class MalHashmap(MalType, list):
    pass


class MalFunction(MalType):
    def __init__(self, ast, params, env, eval_fn):
        self.ast = ast
        self.env = env
        self.params = params
        self.fn = eval_fn

    def __call__(self, *args):
        from env import Env

        closure_env = Env(binds=self.params, exprs=args, outer=self.env)
        return self.fn(self.ast, closure_env)

    def __str__(self):
        return '#<Function>'


nil = MalSymbol('nil')


class MalBool(MalType):
    def __init__(self, v):
        if isinstance(v, MalBool):
            self.v = v.v
        else:
            self.v = 'false' if v is False else 'true'

    def __bool__(self):
        return self.v == 'true'

    def __str__(self):
        return self.v


MalArray = typing.TypeVar('MalArray', MalList, MalVector, MalHashmap)
