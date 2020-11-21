#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 常量类
Desc : 
"""

import sys


class const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__.keys():  # 判断 常量名是否存在 存在抛出异常
            raise self.ConstError("can't change const.%s" % name)
        if not name.isupper():  # 判断 常量名是否全为大写 非全部大写抛出异常
            raise self.ConstCaseError("const name '%s' is not all uppercase " % name)
        self.__dict__[name] = value  # 满足上述条件 进行赋值操作


sys.modules[__name__] = const()
