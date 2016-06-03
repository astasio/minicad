#!/usr/bin/env python

import gio
import atk
import gtk
import cairo
import pango
import pangocairo
import os

memory='minicad.txt'

try:
	buff=file(memory,"r")
	buff.close()
except:
	buff=file(memory,"w")
	buff.close()

def func(string):
	status.push(0,string)
	if string=="move_to":
		width.hide()
		radius.hide()
		curve.hide()
		colors.hide()
	elif string=="line_to":
		width.hide()
		radius.hide()
		curve.hide()
		colors.hide()
	elif string=="arc":
		width.hide()
		radius.show()
		curve.hide()
		colors.hide()
	elif string=="curve_to" or string=="rectangle":
		width.hide()
		radius.hide()
		curve.show()
		colors.hide()
	elif string=="set_source_rgba":
		width.hide()
		radius.hide()
		curve.hide()
		colors.show()
	elif string=="set_line_width":
		width.show()
		radius.hide()
		curve.hide()
		colors.hide()		

def refresh():
	buff=file(memory,'r')
	tb=gtk.TextBuffer()
	testo=''
	for i in buff.readlines():
		testo=testo+str(i)
	tb.set_text(testo)
	textview.set_buffer(tb)
	buff.close()
	
def command():	
	tb=textview.get_buffer()
	start=tb.get_start_iter()
	end=tb.get_end_iter()
	testo=tb.get_text(start,end)
	buff=file(memory,'w')
	buff.write(testo)
	buff.close()
	screen.hide()
	screen.show()
	expose(screen,'expose_event')

def expose(widget,event):
	cr=widget.window.cairo_create()
	buff=file(memory,'r')
	for i in buff.readlines():
		try:
			exec("cr."+i)
		except:
			pass
	buff.close()

def click():
	cor=screen.get_pointer()
	buff=file(memory,'r')
	a=buff.readlines()
	buff.close()
	buff=file(memory,'w')
	try:
		a.pop()
		for i in a:
			buff.write(i)
	except:	
		pass
	func=status.get_children().__getitem__(0).get_child().get_children()[0].get_text()
	if func=="":
		func="move_to"
	elif func=="move_to":
		buff.write(func+"("+str(cor[0])+","+str(cor[1])+")\n")
	elif func=="line_to":
		buff.write(func+"("+str(cor[0])+","+str(cor[1])+")\n")
	elif func=="curve_to":
		if n1.get_text()=="0":
			n1.set_text(str(cor[0])+","+str(cor[1]))
		else:
			if n2.get_text()=="0":
				n2.set_text(str(cor[0])+","+str(cor[1]))
			else:
				buff.write("stroke()\n")
				buff.write(func+"("+n1.get_text()+","+n2.get_text()+","+str(cor[0])+","+str(cor[1])+")\n")
				n1.set_text("0")
				n2.set_text("0")
	elif func=="rectangle":
		if n1.get_text()=="0":
			n1.set_text(str(cor[0]))
			n2.set_text(str(cor[1]))
		else:
			buff.write(func+"("+n1.get_text()+","+n2.get_text()+","+str(cor[0]-int(n1.get_text()))+","+str(cor[1]-int(n2.get_text()))+")\n")
			n1.set_text("0")
			n2.set_text("0")
	elif func=="arc":
		buff.write("stroke()\n")
		buff.write(func+"("+str(cor[0])+","+str(cor[1])+","+p1.get_text().replace(",",".")+",0,6.28)\n")
	buff.write("stroke()\n")
	buff.close()
	refresh()
	screen.hide()
	screen.show()
	expose(screen,'expose_event')

def set_color():
	buff=file(memory,'a')
	buff.write("set_source_rgba("+c1.get_text().replace(",",".")+","+c2.get_text().replace(",",".")+","+c3.get_text().replace(",",".")+","+c4.get_text().replace(",",".")+")\n")
	buff.write("stroke()\n")
	buff.close()
	refresh()
	screen.hide()
	screen.show()
	expose(screen,'expose_event')

def set_line():
	buff=file(memory,'a')
	buff.write("set_line_width("+dim.get_text().replace(",",".")+")\n")	
	buff.write("stroke()\n")
	buff.close()
	refresh()
	screen.hide()
	screen.show()
	expose(screen,'expose_event')		

def stampa():
	pdfs=cairo.PDFSurface("minicad.pdf",800,400)
	cr=cairo.Context(pdfs)
	buff=file(memory,'r')
	for i in buff.readlines():
		try:
			exec("cr."+i)
		except:
			pass
	buff.close()
	pdfs.finish()
	os.system("minicad.pdf")

def exit():
	gtk.main_quit()

win= gtk.Window()
win.connect("destroy",lambda *w:exit())
win.set_title("MiniCad")
win.set_resizable(False)
vbox=gtk.VBox()
win.add(vbox)
vbox.set_homogeneous(False)

hb1=gtk.HBox()
vbox.add(hb1)

toolbar=gtk.VBox()
hb1.add(toolbar)
hb1.set_child_packing(toolbar,0,0,0,gtk.PACK_START)

move=gtk.Button()
move.set_label("Move")
move.connect("clicked",lambda *w: func("move_to"))
line=gtk.Button()
line.set_label("Line")
line.connect("clicked",lambda *w: func("line_to"))
arc=gtk.Button()
arc.set_label("Curve")
arc.connect("clicked",lambda *w: func("curve_to"))
rect=gtk.Button()
rect.set_label("Rectangle")
rect.connect("clicked",lambda *w: func("rectangle"))
ring=gtk.Button()
ring.set_label("Circle")
ring.connect("clicked",lambda *w: func("arc"))
color=gtk.Button()
color.set_label("Color")
color.connect("clicked",lambda *w: func("set_source_rgba"))
dimline=gtk.Button()
dimline.set_label("Line Bold")
dimline.connect("clicked",lambda *w: func("set_line_width"))
printer=gtk.Button()
printer.set_label("Print")
printer.connect("clicked",lambda *w: stampa())
toolbar.add(move)
toolbar.add(line)
toolbar.add(arc)
toolbar.add(rect)
toolbar.add(ring)
toolbar.add(color)
toolbar.add(dimline)
toolbar.add(printer)

v2=gtk.VBox()
hb1.add(v2)

screen=gtk.DrawingArea()
screen.set_events(gtk.gdk.BUTTON_PRESS_MASK)
screen.set_size_request(800,400)
v2.add(screen)	
v2.set_child_packing(screen,expand=False,fill=False, padding=0,pack_type=gtk.PACK_START)
screen.connect('expose_event',expose)
screen.connect("button_press_event",lambda *w: click())
screen.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse("#aaa"))

scroll2=gtk.ScrolledWindow()
scroll2.set_size_request(800,200)
v2.add(scroll2)
textview=gtk.TextView()
scroll2.add(textview)

put=gtk.Button('Invio')
v2.add(put)
v2.set_child_packing(put,expand=False,fill=False, padding=0,pack_type=gtk.PACK_START)
put.connect('clicked',lambda *w: command())


hb=gtk.HBox()
vbox.add(hb)
vbox.set_child_packing(hb,expand=0,fill=0, padding=10,pack_type=gtk.PACK_START)

radius=gtk.HBox()
hb.add(radius)
hb.set_child_packing(radius,0,0,0,gtk.PACK_START)
p1=gtk.SpinButton()
p1.set_digits(1)
adj=gtk.Adjustment(0,0,1000,0.1,0,0)
p1.set_adjustment(adj)
radius.add(p1)
radius.set_child_packing(p1,0,0,0,gtk.PACK_START)
lbl_r=gtk.Label("Set Radius")
radius.add(lbl_r)
radius.set_child_packing(lbl_r,0,0,0,gtk.PACK_START)

curve=gtk.HBox()
hb.add(curve)
hb.set_child_packing(curve,0,0,0,gtk.PACK_START)
n1=gtk.Label("0")
curve.add(n1)
curve.set_child_packing(n1,0,0,10,gtk.PACK_START)
n2=gtk.Label("0")
curve.add(n2)
curve.set_child_packing(n2,0,0,10,gtk.PACK_START)

colors=gtk.HBox()
hb.add(colors)
hb.set_child_packing(colors,0,0,0,gtk.PACK_START)
lbl=gtk.Label("Red")
colors.add(lbl)
colors.set_child_packing(lbl,0,0,5,gtk.PACK_START)
c1=gtk.SpinButton()
c1.set_digits(1)
adj=gtk.Adjustment(0,0,1,0.1,0,0)
c1.set_adjustment(adj)
colors.add(c1)
colors.set_child_packing(c1,0,0,5,gtk.PACK_START)
lbl=gtk.Label("Green")
colors.add(lbl)
colors.set_child_packing(lbl,0,0,5,gtk.PACK_START)
c2=gtk.SpinButton()
c2.set_digits(1)
adj=gtk.Adjustment(0,0,1,0.1,0,0)
c2.set_adjustment(adj)
colors.add(c2)
colors.set_child_packing(c2,0,0,5,gtk.PACK_START)
lbl=gtk.Label("Blue")
colors.add(lbl)
colors.set_child_packing(lbl,0,0,5,gtk.PACK_START)
c3=gtk.SpinButton()
c3.set_digits(1)
adj=gtk.Adjustment(0,0,1,0.1,0,0)
c3.set_adjustment(adj)
colors.add(c3)
colors.set_child_packing(c3,0,0,5,gtk.PACK_START)
lbl=gtk.Label("Alpha")
colors.add(lbl)
colors.set_child_packing(lbl,0,0,5,gtk.PACK_START)
c4=gtk.SpinButton()
c4.set_digits(1)
adj=gtk.Adjustment(1,0,1,0.1,0,0)
c4.set_adjustment(adj)
colors.add(c4)
colors.set_child_packing(c4,0,0,5,gtk.PACK_START)
set=gtk.Button("Set Color")
colors.add(set)
set.connect("clicked",lambda *w: set_color())
colors.set_child_packing(set,0,0,5,gtk.PACK_START)

width=gtk.HBox()
hb.add(width)
hb.set_child_packing(width,0,0,0,gtk.PACK_START)
dim=gtk.SpinButton()
dim.set_digits(1)
adj=gtk.Adjustment(0,0,100,0.1,0,0)
dim.set_adjustment(adj)
width.add(dim)
width.set_child_packing(dim,0,0,0,gtk.PACK_START)
set2=gtk.Button("Set Line Bold")
width.add(set2)
set2.connect("clicked",lambda *w: set_line())
width.set_child_packing(set2,0,0,0,gtk.PACK_START)

status=gtk.Statusbar()
vbox.add(status)
vbox.set_child_packing(status,expand=False,fill=False, padding=0,pack_type=gtk.PACK_END)
refresh()

win.show_all()
radius.hide()
curve.hide()
colors.hide()
width.hide()

gtk.main()
