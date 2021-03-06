#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mal_readline
import printer
import reader
from core import ns
from env import Env
from mal_types import *


def READ(s: str) -> MalType:
    return reader.read_str(s)


def eval_ast(ast: MalType, env: Env):
    if isinstance(ast, MalSymbol):
        return env.get(ast)
    elif isinstance(ast, MalList):
        return MalList(EVAL(child, env) for child in ast)
    else:
        return ast


def EVAL(ast: MalType, env: Env) -> MalType:
    while True:
        if isinstance(ast, MalVector):
            return MalVector(EVAL(member, env) for member in ast)
        if isinstance(ast, MalHashmap):
            return MalHashmap([ast[0], EVAL(ast[1], env)])
        if not isinstance(ast, MalList):  # not a list
            return eval_ast(ast, env)

        if isinstance(ast, MalList):
            if len(ast) == 0:  # an empty list
                return ast
            else:  # a list
                if ast[0] == 'def!':
                    return env.set(ast[1], EVAL(ast[2], env))
                elif ast[0] == 'let*':
                    let_env = Env(outer=env)
                    param1 = iter(ast[1])
                    for symbol, value in zip(param1, param1):
                        let_env.set(symbol, EVAL(value, env=let_env))
                    # return EVAL(ast[2], env=let_env)
                    ast, env = ast[2], let_env
                    continue
                elif ast[0] == 'do':
                    # value = nil
                    # for element in ast[1:]:
                    #     value = EVAL(element, env)
                    # return value
                    for ele in ast[1:-1]:
                        eval_ast(ele, env)
                    ast = ast[-1]
                    continue
                elif ast[0] == 'if':
                    cond = EVAL(ast[1], env)
                    if cond != nil and MalBool(cond):
                        # return EVAL(ast[2], env)
                        ast = ast[2]
                        continue
                    elif len(ast) == 4:
                        # return EVAL(ast[3], env)
                        ast = ast[3]
                        continue
                    else:
                        return nil
                elif ast[0] == 'fn*':
                    return MalFunction(ast=ast[2], params=ast[1], env=env,
                                       eval_fn=EVAL)
                else:
                    f, *args = eval_ast(ast, env)
                    if isinstance(f, MalFunction):
                        env = Env(binds=f.params, exprs=args, outer=f.env)
                        ast = f.ast
                        continue
                    else:
                        return f(*args)


def PRINT(exp: MalType) -> str:
    return printer.pr_str(exp, print_readably=True)


repl_env = Env(ns)


def rep(s: str) -> str:
    return PRINT(
        EVAL(
            READ(s),
            env=repl_env
        )
    )


rep("(def! not (fn* (a) (if a false true)))")


def main():
    while True:
        try:
            print(rep(mal_readline.readline('user> ')))
        except (KeyboardInterrupt, EOFError):
            break
            # except Exception as e:
            #     print('Error: ', e)


if __name__ == '__main__':
    main()
