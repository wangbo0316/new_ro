import os
import sys


MAIN_PATH = os.getcwd()
STATIC_PATH = MAIN_PATH + '\\static'
sys.path.append(MAIN_PATH + '\\script')
sys.path.append(MAIN_PATH + '\\static')
sys.path.append(MAIN_PATH + '\\ui')

DEFAULT_OPEN_PATH = "D:\\Data"