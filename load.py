"""
A Skeleton EDMC Plugin
"""
import locale
import sys

import numpy as np 

import Tkinter

this = sys.modules[__name__]
locale.setlocale(locale.LC_ALL, '')

def getDistance(x,y,z):
	p = np.array([68.84375 , 48.75 , 69.75])
	q = np.array([75.75 , 48.75 , 75.15625 ])
	r = np.array([x, y, z])

	def t(p, q, r):
		x = p-q
		return np.dot(r-q, x)/np.dot(x, x)

	def d(p, q, r):
		return np.linalg.norm(t(p, q, r)*(p-q)+q-r)

	print(d(p, q, r))


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
		jd=getDistance(entry["StarPos"][0],entry["StarPos"][1],entry["StarPos"][2])
		this.status=str(jd)

