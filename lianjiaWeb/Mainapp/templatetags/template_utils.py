import pypinyin
from django import template
import re

register = template.Library()

@register.simple_tag
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


@register.simple_tag
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)

@register.simple_tag
def deletestr(arg1, arg2):
    print(1111)
    print(arg1)
    print(arg2)
    print(re.sub(arg2,'',arg1))
    print(111)
    return re.sub(arg2,'',arg1)