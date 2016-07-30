from Tkinter import *
from PIL import Image
import tkFileDialog
import os
import ttk
import numpy as np 
import math 


gbase = 0
cnt = 0 
gtup = (0,0,0,0,0,0)

def clearbox(newwin , root , e1 , e2 , e3 , e4):
	global cnt
	global gbase
	global gtup
	cnt = cnt + 1
	baseYear = int(e1.get())
	currentYear = int(e2.get())
	if cnt == 1:
		gbase = baseYear
	base = e3.get()
	cur = e4.geometryt()
	ft = get_base_tuple(base , currentYear , baseYear)
	if cnt == 1:
		gtup = ft
	result = get_result(res)
	with open("features.txt" , "a") as features:
		features.write(','.join(str(s) for s in ft) + '\n')
	with open("results.txt" , "a") as results:
		results.write(','.join(str(s) for s in result) + '\n')	
	e1.delete(0,END)
	e2.delete(0,END)
	e3.delete(0,END)
	e4.delete(0,END)
	newwin.destroy()



def cls(newwin , root , e1 , e2 , e3 , e4):
	global cnt
	global gbase
	global gtup
	cnt = cnt + 1 
	baseYear = int(e1.get())
	currentYear = int(e2.get())
	if cnt == 1:
		gbase = baseYear
	base = e3.get()
	cur = e4.get()
	ft = get_base_tuple(base , currentYear , baseYear)
	result = get_result(cur)
	if cnt == 1:
		gtup = ft
	# print ft
	# print result

	with open("features.txt" , "a") as features:
		features.write(','.join(str(s) for s in ft) + '\n')
	with open("results.txt" , "a") as results:
		results.write(','.join(str(s) for s in result) + '\n')	
	e1.delete(0,END)
	e2.delete(0,END)
	e3.delete(0,END)
	e4.delete(0,END)
	newwin.destroy()
	root.destroy()


def ask(root,e1,e2,e3,e4):
	
	if (e1.get() == '' or e2.get() == '' or e3.get() == '' or e4.get() == ''):
		print 'Please fill complete Info\n'
		return 

	done = False
	newwin = Tk()
	newwin.title("want more ? ")
	newwin.geometry("400x400")
	askby = Button(newwin , text = "Yes" , command = lambda : clearbox(newwin , root , e1 , e2 , e3 , e4) )
	askbn = Button(newwin , text = "No" , command = lambda : cls(newwin , root ,e1 , e2 , e3 , e4))
	askby.grid(row = 0 , column = 0)
	askbn.grid(row = 0 , column = 2)
	newwin.mainloop()



def get_result(path):
	im = Image.open(path) # path of base image
	pix = im.load()
	(width, height) =im.size #Get the width and hight of the image for iterating over
	water = 0  #blue
	vegetation = 0  #green
	soil = 0 #red
	buildup = 0 #black
	tot = 0 
	leave = 0 
	for x in range(width):
	    for y in range(height):
	    	# if(pix[x,y][0]+ pix[x,y][1] + pix[x,y][2] == 17):
	    	# 	print pix[x,y]
	    	# 	break 
	    	if pix[x,y][0] > 150:
	    		soil = soil + 1
	    	elif pix[x,y][1] > 150:
	    		vegetation = vegetation + 1 
	    	elif pix[x,y][2] > 150:
	    		water = water + 1
	    	elif (pix[x,y][0] < 40 or pix[x,y][1] < 40 or pix[x,y][2] < 40):
	    		buildup = buildup + 1 
	    	else:
	    		leave = leave + 1

	tot = width*height - leave
	# print tot
	# print leave
	soil = ((1.0*soil)/ (tot*1.0) )*100.0
	water = ((1.0*water)/ (tot*1.0) )*100.0
	vegetation = ((1.0*vegetation)/ (tot*1.0) )*100.0
	buildup = ((1.0*buildup)/ (tot*1.0) )*100.0

	return (soil , vegetation , water , buildup)

def get_base_tuple(path , currentyear , baseyear):
	im = Image.open(path) # path of base image
	pix = im.load()
	(width, height) =im.size #Get the width and hight of the image for iterating over
	water = 0  #blue
	vegetation = 0  #green
	soil = 0 #red
	buildup = 0 #black
	tot = 0 
	leave = 0 
	for x in range(width):
	    for y in range(height):
	    	if pix[x,y][0] > 150:
	    		soil = soil + 1
	    	elif pix[x,y][1] > 150:
	    		vegetation = vegetation + 1 
	    	elif pix[x,y][2] > 150:
	    		water = water + 1
	    	elif (pix[x,y][0] < 40 or pix[x,y][1] < 40 or pix[x,y][2] < 40):
	    		buildup = buildup + 1 
	    	else:
	    		leave = leave + 1

	tot = width*height - leave
	soil = ((1.0*soil)/ (tot*1.0) )*100.0
	water = ((1.0*water)/ (tot*1.0) )*100.0
	vegetation = ((1.0*vegetation)/ (tot*1.0) )*100.0
	buildup = ((1.0*buildup)/ (tot*1.0) )*100.0
	
	assert currentyear >= baseyear

	return (1 , soil , vegetation , water , buildup , currentyear - baseyear) 



def browse(entryField , e2):
	
	if e2.get() == '':
		print 'Please Enter Year of This Image before selecting\n'
		return 

	currentYear = int(e2.get())

	root = Tk()
	root.withdraw() #use to hide tkinter window

	currdir = os.getcwd()
	tempdir = tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
	entryField.insert(0 , tempdir)


def import_data():
	from numpy import genfromtxt
	my_data = genfromtxt('features.txt', delimiter=',')
	y = genfromtxt('results.txt', delimiter=',')
	return my_data,y

def train():
	my_data , yy = import_data()
	x = np.array(my_data) 
	y = np.array(yy)

	if x.shape[0] == 1:
		xt = x[: , None]
		x = x[None , :]
		y = y[None , :]
		print 'going in\n'
	else:
		xt = x.transpose()

	print x.shape
	print xt.shape

	xinv = np.linalg.pinv( np.dot(xt , x))
	print xinv.shape # pinv(x*xt) 
	print "theta...\n"
	
	theta = np.dot(np.dot(xinv , xt) , y)
	# assert 0 
	print xinv.shape
	print 'theta shape = ' ,theta.shape
	return theta


def predict(pwin , ep ,theta):
	if(ep.get() == ''):
		print 'enter some year first.....\n'
	else:
		currentYear = int(ep.get())
		global gbase
		global gtup
		x = np.array(gtup)
		x[5] = currentYear - gbase
		ans = np.dot(x , theta)
		lsoil = Label(pwin , text = ans[0])
		lsoil.grid(row = 110 , column = 2)
		lveg = Label(pwin , text = ans[1] )
		lveg.grid(row = 130 , column = 2)
		lwater = Label(pwin , text = ans[2] )
		lwater.grid(row = 150 , column = 2)
		lbuild = Label(pwin , text = ans[3] )
		lbuild.grid(row = 170 , column = 2)



def main():
	top = Tk()

	top.title("Prediction of Land Use And  Land Cover")
	top.geometry("600x600")



	l1 = Label(top , text = "Enter Year 1 : ")
	l2 = Label(top , text = "Enter Year 2 : ")

	cnt = 0

	l1.grid(row = 50 , column = 0)
	l2.grid(row = 70 , column = 0)

	e1 = Entry(top)
	e2 = Entry(top)

	e1.grid(row = 50 , column = 1)
	e2.grid(row = 70 , column = 1)

	e3 = Entry(top)
	e4 = Entry(top)
	
	e3.grid(row = 50 , column = 5)
	e4.grid(row = 70 , column = 5)

	b1 = Button(top , text = "Select Image 1" , command = lambda: browse(e3 , e1) )
	b2 = Button(top , text = "Select Image 2" , command = lambda: browse(e4 , e2) )
	submit = Button(top , text = "Next" , command = lambda : ask(top,e1,e2,e3,e4) )

	b1.grid(row = 50 , column = 2)
	b2.grid(row = 70 , column = 2)

	submit.grid(row = 90 , column = 1)



	lbl = [0 for i in range(4)]


	top.mainloop() 
	theta = train()
	print theta
	
	print "global tup = " , gtup
	pwin = Tk()
	pwin.title("Prediction of Land Use And  Land Cover")
	pwin.geometry("600x600")
	lp = Label(pwin , text = "Enter Year to predict : ")
	lp.grid(row = 50 , column = 0)
	ep = Entry(pwin)
	ep.grid(row = 50 , column = 1)
	nextb = Button(pwin , text = "Next" , command = lambda : predict(pwin , ep , theta) )
	nextb.grid(row = 90 , column = 1)

	lsoil = Label(pwin , text = "Soil = " )
	lsoil.grid(row = 110 , column = 0)
	lveg = Label(pwin , text = "Vegetation = " )
	lveg.grid(row = 130 , column = 0)
	lwater = Label(pwin , text = "Water = " )
	lwater.grid(row = 150 , column = 0)
	lbuild = Label(pwin , text = "Buildup = " )
	lbuild.grid(row = 170 , column = 0)

	pwin.mainloop()


if __name__ == "__main__" :
	main()

