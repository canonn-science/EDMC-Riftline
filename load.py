"""
A Skeleton EDMC Plugin
"""
import locale
import sys


import Tkinter

this = sys.modules[__name__]
locale.setlocale(locale.LC_ALL, '')

def dot(a, b):
	return sum([a[i]*b[i] for i in range(3)])

def norm(a):
	return sum([a[i]**2 for i in range(3)])**0.5

def getDistance(x,y,z):
	#The Rift Line is a line that passes through Riedquat and Reorte
	#So hard coding the coords here
	p = (68.84375, 48.75, 69.75)
	q = (75.75, 48.75, 75.15625)
	r = (x, y, z)
    
	def t(p, q, r):
		a = tuple([r[i]-q[i] for i in range(3)])
		b = tuple([p[i]-q[i] for i in range(3)])
		return dot(a, b)/dot(b, b)
    
	def d(p, q, r):
		k = t(p, q, r)
		a = tuple([k*(p[i]-q[i]) for i in range(3)])
		b = tuple([a[i]+q[i] for i in range(3)])
		c = tuple([b[i]-r[i] for i in range(3)])
		return norm(c)
    
	return d(p, q, r)




def plugin_start():
    """
    Start this plugin
    :return: Plugin name
    """
    return 'EDMC-Riftline'


def plugin_app(parent):
    """
    Return a TK Widget for the EDMC main window.
    :param parent:
    :return:
    """
    label = Tkinter.Label(parent, text="Riftline:")
    this.status = Tkinter.Label(parent, anchor=Tkinter.W, text="Waiting for Jump")
    this.total_bounty = 0
    return label, this.status


def journal_entry(cmdr, system, station, entry):
    
    if entry['event'] == 'FSDJump':
		jd=getDistance(float(entry["StarPos"][0]),float(entry["StarPos"][1]),float(entry["StarPos"][2]))
		this.status["text"]=str(round(jd,1))+"ly"

