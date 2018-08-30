"""
A Skeleton EDMC Plugin
"""
import locale
import sys
import math
import threading
import requests

import Tkinter
from urllib import quote_plus

this = sys.modules[__name__]
locale.setlocale(locale.LC_ALL, '')

RIEDQUAT=(68.84375, 48.75, 69.75)
REORTE=(75.75, 48.75, 75.15625)


class CmdrData(threading.Thread):
	def __init__(self, system):
		threading.Thread.__init__(self)
		self.system = system

	def run(self):
		#try:
			url="https://www.edsm.net/api-v1/system?showCoordinates=1&systemName="+quote_plus(self.system)
			r=requests.get(url)
			s =  r.json()
			print s
			displayRift(float(s["coords"]["x"]),float(s["coords"]["y"]),float(s["coords"]["z"]))
			#debug(self.payload,2)
		#except:
		#	print("[RiftLine] Issue posting message " + str(sys.exc_info()[0]))

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

def getRiftDistance(x,y,z):
        # gets the distance to a line extending through Riedquat and Reorte
        p=(x,y,z)
        g=getNearest(x,y,z)

        return getDistance(p,g)
		
def getDistance(p,g):
        # gets the distance to a line extending through Riedquat and Reorte
        
        return math.sqrt(sum(tuple([math.pow(p[i]-g[i],2)  for i in range(3)])))


def translate(c,t):
	# translate coordinates c by t
	# if c and t are the same then returns 0,0,0
	return tuple([c[i]-t[i] for i in range(3)])

def plugin_start(plugin_dir):
	"""
	Start this plugin
	:return: Plugin name
	"""
	this.plugin_dir = plugin_dir
	return 'EDMC-Riftline'


def plugin_app(parent):
    """
    Return a TK Widget for the EDMC main window.
    :param parent:
    :return:
    """
    this.parent=parent
    this.pcont=Tkinter.Frame(parent)
    this.container=Tkinter.Frame(this.pcont)
    this.container.columnconfigure(3, weight=1)
    
    #label = Tkinter.Label(this.container, text="Riftline:")
    #this.status = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location")
    
    #this.ship = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location")	

    this.RADAR = Tkinter.PhotoImage(file = this.plugin_dir+'\\radar.gif')
    #this.SHIP = Tkinter.PhotoImage(file = this.plugin_dir+'\\ship.gif')
    #this.ship = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location",image=this.SHIP)		
    #this.ship.place(x=0, y=0, relwidth=1, relheight=1)	
    this.status = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location", image=this.RADAR)
    this.status.grid(row=0,column=0, sticky=Tkinter.W)
    #this.status.place(x=0, y=0, relwidth=199, relheight=199)			
    this.SHIP = Tkinter.PhotoImage(file = this.plugin_dir+'\\ship.gif')
    this.ship = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location",image=this.SHIP)		
    rx,ry=getRadialCoords((0,0,0),0)
    this.ship.place(x=97, y=97)		
    this.container.grid_remove()
    this.container.grid()
    #return label, this.status
    return (this.pcont)
	
def rotate(xyz,xz,xy):
	x,y,z=xyz
	"""Only rotate xz point around the origin (0, 0)."""
	xx = x * math.cos(xz) + z * math.sin(xz)
	zz = -x * math.sin(xz) + z * math.cos(xz)
	"""Only rotate xy point around the origin (0, 0)."""
	xxx = xx * math.cos(xy) + y * math.sin(xy)
	yy = -xx * math.sin(xy) + y * math.cos(xy)
	
	return (round(xxx,5), round(yy,5), round(zz,5))
	

	
def getRadialCoords(c,d):
	"""
		We want to position our commander on a radar
		screen so we need to limit the coordinates to
		the boundary
			
		c = coordinates
		d = distance from origin
	"""
	
	x,y,z=c
	
	if d > 100:
		d = 100
		
	#get the angle of rotation
	radians=math.atan2(z,y)
	#rotate by by distance
	(yy,xx) = (d*math.cos(radians),d*math.sin(radians))
	

	return round(xx+97,0),round(yy+97,0)
	
	
	
	
	
	
	
		
	
def displayRift(x,y,z):
	jd=getRiftDistance(x,y,z)
	nc=getNearest(x,y,z) 
	
	# We are going to translate the origin to nearest point in the line
	# So we translate a know point in the same fashion 
	tr=translate(RIEDQUAT,nc)
	
	#Next work out the angles needed to 
	xz = math.atan2(tr[2],tr[0])
	xy = math.atan2(tr[1],tr[0])
	
	cp = translate((x,y,z),nc)
	
	# then we translate one end of the line RIEDQUAT
	tr=translate(RIEDQUAT,nc)
	tq=translate(REORTE,nc)
	# to put the line on the x axis first rotate 
	# x to z then x to y
	xz = math.atan2(tr[2],tr[0])
	xy = math.atan2(tr[1],tr[0])
	
	#current position
	cp = translate((x,y,z),nc)
	
	# get on screen coordinates for cp
	rx,ry=getRadialCoords(rotate(cp,xz,xy),getDistance((0,0,0),rotate(cp,xz,xy)))
	
	this.ship.place(x=rx, y=ry)		
	
	this.status["text"]=str(round(jd,1))+"ly "

def journal_entry(cmdr, is_beta, system, station, entry, state):
    
	if entry['event'] in ['StartUp', 'Location', 'FSDJump']:
		displayRift(float(entry["StarPos"][0]),float(entry["StarPos"][1]),float(entry["StarPos"][2]))

def cmdr_data(data):
	CmdrData(data["lastSystem"]["name"]).start()