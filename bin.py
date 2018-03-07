# coding:utf-8

from core import run,parse_conf
from conf import hosts


if __name__ == '__main__':
    parse_conf(hosts)
    run()


