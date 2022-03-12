# -*- coding: utf-8 -*-
"""
Control variables for report production for S&P/TSX Market Breadth
This file is intended to be used to store the strategy, calc_date and other
variable so that this can be called into any report script.

"""
global strategy, calc_date

strategy = 'global'
calc_date = '2022-03-04'
title = f'{strategy}_market_performance_{calc_date}.pdf'
background_color = '#6149EB'
line_color = '#eba549'

image_file = f'global_market_performance_{calc_date}.png'
