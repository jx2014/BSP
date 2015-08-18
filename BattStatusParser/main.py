from BatteryStatusParser import BSP

#testLog = r"C:\Users\jxue\Documents\RMA\RMA 35491\Net_Mgr_Logs\Scenario2_BBU_0p25V.txt"
#testLog = r"C:\Users\jxue\Documents\RMA\RMA 35491\Net_Mgr_Logs\Scenario2b_BBU_2p5V.txt"
#testLog = r"C:\Users\jxue\Documents\RMA\RMA 35491\Net_Mgr_Logs\Scenario1_BBU_4P05v.txt"
testLog = r"\\o9020-9kbqx12\temp\Battery_Status_Logs\REL_REF.txt"

test = BSP(testLog)

test.FileNames()

#test.Test()

ipv6 = "fe80::213:50ff:fe11:e000"
macID = "00:13:50:ff:fe:11:e0:00"
macID2 = "001350fffe11e000"
NoneSense1 = "001350fffe11e00k0asd"
NoneSense2 = "001350"
NoneSense3 = "001350fff"

#for i in [ipv6, macID, macID2, NoneSense1, NoneSense2, NoneSense3]:
#    print test.ConvIpMac(i)


test.OutputFunc(testLog)
# print next(test.YieldLine(testLog))
# print next(test.YieldLine(testLog))
# print next(test.YieldLine(testLog))
# print next(test.YieldLine(testLog))




#########
# 
# def logger(func):
#     def inner(*args, **kwargs):
#         print "Arguments: %s, %s" % (args, kwargs)
#         return func(*args, **kwargs)
#     return inner
# 
# @logger
# def fool(x, y=1):
#     return x * y

# 
# 
# 
# class Coordinate(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#     
#     def __repr__(self):
#         return "Coord: " + str(self.__dict__)
#     
# def add(a, b):
#     return Coordinate(a.x + b.x,  a.y + b.y)
# 
# def sub(a, b):
#     return Coordinate(a.x - b.x,  a.y - b.y)
# 
# one = Coordinate(100, 200)
# two = Coordinate(300, 200)
# 
# add(one, two)
# 
# 
# def wrapper(func):
#     def checker(a, b):
#         if a.x < 0 or a.y < 0:
#             a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
#         if b.x < 0 or b.y < 0:
#             b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
#         ret = func(a, b)
#         if ret.x < 0 or ret.y < 0:
#             ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
#         return ret
#     return checker
# 
# 
# #########
# def outer(some_func):
#     def inner():
#         print "before some_func"
#         print some_func.func_name
#         return some_func()    
#     return inner
# 
# def foo():
#     print "this is foo"
#     
# decorated = outer(foo)
# decorated()