import ctypes

testlib = ctypes.CDLL('./cfunctions/testlib.so')
testlib.myprint()

