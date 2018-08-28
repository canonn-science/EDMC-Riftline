"""
A Skeleton EDMC Plugin
"""
import locale
import sys
import math

import Tkinter

this = sys.modules[__name__]
locale.setlocale(locale.LC_ALL, '')

RIEDQUAT=(68.84375, 48.75, 69.75)
REORTE=(75.75, 48.75, 75.15625)


def dot(a, b):
	return sum([a[i]*b[i] for i in range(3)])


def getNearest(x,y,z):
        # gets the coordinates of the nearest point on a line extending through Riedquat and Reorte
        r = RIEDQUAT
        q = REORTE
        p = (x, y, z)

        # avoid divide by zero if the x,y,z is one of the end points
        if (str(r) == str(p)):
                return r
        if (str(r) == str(q)):
                return r
        # https://math.stackexchange.com/questions/1521128/given-a-line-and-a-point-in-3d-how-to-find-the-closest-point-on-the-line
        # find the magnitude along the line at the closestpoint
        # t=(r-q).(q-p)/(r-q).(r-q)
        # that can be used in the formula g=q+t^(r.q) to derive the
        # point g on the line that is closest to point p.

        # define variables for r-q and q-p
        rq = tuple([r[i]-q[i] for i in range(3)])
        qp = tuple([p[i]-q[i] for i in range(3)])

        # this gets the distance along the line of the nearest point
        t=dot(rq,qp)/dot(rq,rq)
        # This calculates the coordinates of the nearest point
        g=tuple([q[i]+(t*r[i]-t*q[i]) for i in range(3)])

        return g

def getDistance(x,y,z):
        # gets the distance to a line extending through Riedquat and Reorte
        p=(x,y,z)
        g=getNearest(x,y,z)

        return math.sqrt(sum(tuple([math.pow(p[i]-g[i],2)  for i in range(3)])))


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

