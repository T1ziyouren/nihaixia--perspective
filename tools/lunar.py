#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 公历农历转换 v1.2 — 基于 lunardate 库
# 用法: python3 lunar.py 1993-1-7
#       python3 lunar.py 1996-01-01
#       python3 lunar.py 1992-3-25

import sys
from datetime import date
from lunardate import LunarDate

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 lunar.py YYYY-MM-DD")
        print("示例: python3 lunar.py 1993-01-07")
        sys.exit(1)

    d_str = sys.argv[1]
    try:
        d = date.fromisoformat(d_str)
    except:
        print(f"日期格式错误: {d_str}")
        sys.exit(1)

    lunar = LunarDate.fromSolarDate(d.year, d.month, d.day)
    cn_num = ['','正','二','三','四','五','六','七','八','九','十','十一','腊']
    cn_day = ['','初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
              '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
              '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十']

    is_leap = getattr(lunar, 'isLeapMonth', False)
    # lunardate 0.2.x API
    leap_str = "闰" if hasattr(lunar, 'isLeapMonth') and lunar.isLeapMonth else ""

    print(f"{d_str} → 农历{lunar.year}年{leap_str}{cn_num[lunar.month]}月{cn_day[lunar.day]}")
    print(f"  数字: 年={lunar.year} 月={lunar.month} 日={lunar.day} 闰={'是' if leap_str else '否'}")
