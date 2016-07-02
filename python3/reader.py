#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import List

from mal_types import *

Token = str


class Reader:
    """a simple stateful object stores the tokens and a position."""

    def __init__(self, tokens):
        """
        :type tokens: List[Token]
        """
        self.tokens = tokens
        self.position = 0

    def next(self) -> Token:
        """Returns the token at the current position and increments the
        position.
        """
        value = self.peek()
        self.position += 1
        return value

    def peek(self) -> Token:
        """Returns the token at the current position.
        """
        try:
            token = self.tokens[self.position]
        except IndexError:
            raise IndexError('No more tokens')
        else:
            return token


def read_str(line_str: str) -> MalType:
    """Convert string to an MAL data structure."""
    tokens = tokenizer(line_str)
    reader = Reader(tokens)
    return read_form(reader)


def tokenizer(s):
    """Takes a single string and return a list of all the tokens (strings)
    in it.
    """
    mal_pattern = re.compile(r"""
    [\s,]*      # matches whitespaces or commas. this is not captured
    (~@        # captures special two-characters
    | [\[\]{}()'`~\^@]        # any special single character
    | "(?:\\.|[^\\"])*"      # starts capturing at a double-quote and strops
                            # at next double-quote unless it was proceeded
                            # by a backslash in which case it includes it
                            # until next double-quote
    | ;.*        # any sequence of characters starting with ;
    | [^\s\[\]{}('"`,;)]*    # a sequence of zero or more non special characters
    )""", re.VERBOSE)
    return re.findall(mal_pattern, s)


def read_form(reader):
    """Peek at the first token in the Reader object and switch on the first
    character of that token.

    :type reader: Reader
    :return: a mal data type
    :rtype: MalType
    """
    token = reader.peek()
    # TODO: handle more types to pass the test

    if token == '':
        pass
    elif token == '(':
        reader.next()
        return read_list(reader)
    else:
        value = read_atom(reader)
        reader.next()
        return value


def read_list(reader: Reader) -> MalList:
    """Returns a list of values."""
    results = MalList()
    while True:
        token = reader.peek()
        if token == '':  # EOF
            # raise ValueError('illegal string')
            break
        elif token[0] == ')':
            reader.next()
            break
        else:
            results.append(read_form(reader))
    return results


def read_atom(reader: Reader) -> MalType:
    """Look at the contents of the token and return the appropriate scalar
    (simple/single) data type value.
    """
    token = reader.peek()
    # Number type
    try:
        return MalNumber(token)
    except ValueError:
        pass

    if token[0] == token[-1] == '"':
        s = MalString(token)
        s = s.replace('\\"', r'"')
        s = s.replace('\\n', '\n')
        s = s.replace('\\\\', '\\')
        return s

    # catch all as Symbol type
    try:
        return MalSymbol(token)
    except ValueError:
        pass