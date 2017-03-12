#encoding=utf-8
import re
import sys

def LongToInt(value):# 由于int+int超出范围后自动转为long型，通过这个转回来  
	if isinstance(value, int):  
		return int(value)  
	else:  					         
		return int(value & sys.maxint)  	
def LeftShiftInt(number, step):# 由于左移可能自动转为long型，通过这个转回来
 	if isinstance((number << step), long):
		return int((number << step) - 0x200000000L)
	else:
		return int(number << step)  
def getOldGTK(skey):
	a = 5381
	for i in range(0, len(skey)):
		a = a + LeftShiftInt(a, 5) + ord(skey[i])
		a = LongToInt(a)					
	return a & 0x7fffffff

def getNewGTK(p_skey, skey, rv2): 
	b = p_skey or skey or rv2			
	a = 5381 
	for i in range(0, len(b)): 	
		a = a + LeftShiftInt(a, 5) + ord(b[i])  	
		a = LongToInt(a)  				
	a = str(a & 0x7fffffff)
	return a 
def getKeys(cookieStr):	
	if re.search(r'p_skey=(?P<p_skey>[^;]*)', cookieStr):  	            
		p_skey = re.search(r'p_skey=(?P<p_skey>[^;]*)', cookieStr).group('p_skey')  		      
	else:  	
		p_skey = None  		
	if re.search(r'skey=(?P<skey>[^;]*)', cookieStr):  			
		skey = re.search(r'skey=(?P<skey>[^;]*)', cookieStr).group('skey')  	
	else:  
		skey = None  
	if re.search(r'rv2=(?P<rv2>[^;]*)', cookieStr):  
		rv2 = re.search(r'rv2=(?P<rv2>[^;]*)', cookieStr).group('rv2')  					
	else:  	
		rv2 = None														
	return p_skey,skey,rv2
