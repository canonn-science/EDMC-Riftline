"""
A Skeleton EDMC Plugin
"""
import locale
import sys
import math
import threading
import requests
import json
import l10n
from l10n import Locale

import Tkinter
from urllib import quote_plus

this = sys.modules[__name__]
locale.setlocale(locale.LC_ALL, '')

RIEDQUAT=(68.84375, 48.75, 69.75)
REORTE=(75.75, 48.75, 75.15625)
SOL=(0,0,0)
ZURARA=(-9529.4375,-64.5,-7428.4375)

def stringFromNumber(a,b):
	return Locale.stringFromNumber(a,b)

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
			displayRift(self.system,float(s["coords"]["x"]),float(s["coords"]["y"]),float(s["coords"]["z"]))
			#debug(self.payload,2)
		#except:
		#	print("[RiftLine] Issue posting message " + str(sys.exc_info()[0]))

class Traffic(threading.Thread):
	def __init__(self, system):
		threading.Thread.__init__(self)
		self.system = system

	def run(self):
		#try:
			
			url="https://www.edsm.net/api-system-v1/traffic?systemName="+quote_plus(self.system)
			r=requests.get(url)
			s =  r.json()
			this.traffic.grid()
			this.traffic["text"]="Traffic: {} ships".format(stringFromNumber(s["traffic"]["total"],0))	
			print s
			
		
class SphereSystems(threading.Thread):
	def __init__(self, centre,system):
		threading.Thread.__init__(self)
		self.system = system
		self.centre = centre

	def getList(self,c,radius):
		x,y,z=c
		url="https://www.edsm.net/api-v1/sphere-systems?showCoordinates=1&minRadius=0&radius={}&x={}&y={}&z={}"
		r=requests.get(url.format(radius,x,y,z))
		s =  r.json()
		return s
		
	def getDensity(self,c,radius,systems):	
		x,y,z=c
		#using Sol as the reference density to 100%
		DSOL=8260
		VSOL=(4/3)*math.pi*pow(100,3)
		
		#get the sample volume and get a scale factor
		v=(4/3)*math.pi*pow(radius,3)
		scale=VSOL/v
		print "scale {}".format(scale)		
		denom=DSOL/scale
		print "Denonimator {}".format(denom)	
		print "round(({}/{})*100,1)".format(systems,denom)
		return round((systems/denom)*100,0)
		
	def run(self):
		#try:
		
			# get a list of systems
			systems=self.getList(self.centre,100)
			
			# we might not be in range of the centre so need to make an extra call
			# could optimise this by checking distance.
			local=len(self.getList(self.system,20))		
					
			# after grabbing the list of sites we need to rotate and translate them
			# then find the closest site to the nc with a positive x and negative x
			# if they can be found then put them on the map if we wanted but at over 800 systems that would be naughty
			
			#get the density and compare
			d=self.getDensity(self.centre,100,len(systems))
			print "density: {}%".format(d)
			d=self.getDensity(self.system,20,local)
			print "density: {}%".format(d)
			
			#this.denlocal.grid()
			#this.denarea.grid()
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
        # gets the distance between two systems
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
    imagepath=this.plugin_dir+'\\images\\{}'
      
    this.RADAR_PANEL = Tkinter.PhotoImage(file = imagepath.format("circle_panel.gif"))
    this.RADAR_SCREEN = Tkinter.PhotoImage(file = imagepath.format("radar_panel.gif"))
    this.TEXT_LOGO = Tkinter.PhotoImage(file = imagepath.format("text_panel_logo.gif"))
    this.TEXT_PANEL = Tkinter.PhotoImage(file = imagepath.format("text_panel.gif"))
    this.SHIP = Tkinter.PhotoImage(file = imagepath.format("ship.gif"))
	
    #this.radar_frame=Tkinter.Canvas(this.container)
	
    #this.ship = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location",image=this.SHIP)		
    #this.ship.place(x=0, y=0, relwidth=1, relheight=1)	
    this.radar_screen = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location", image=this.RADAR_SCREEN)
    this.radar_screen.grid(row=0,column=0, sticky=Tkinter.W)
	
	
	
    this.text_panel = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location", image=this.TEXT_LOGO)
    this.text_panel.grid(row=0,column=1, sticky=Tkinter.W)
   
    this.infopanel=Tkinter.Frame(this.container)
    this.infopanel.columnconfigure(1, weight=1)
    this.infopanel.place(x=180, y=15)		
	
    this.status = Tkinter.Label(this.infopanel, anchor=Tkinter.W, text="Waiting for location")
    this.status.grid(row=0,column=0, sticky=Tkinter.W)
    this.dsol=Tkinter.Label(this.infopanel, anchor=Tkinter.W)
    this.dsol.grid(row=1,column=0, sticky=Tkinter.W)
    this.zurara=Tkinter.Label(this.infopanel, anchor=Tkinter.W)
    this.zurara.grid(row=2,column=0, sticky=Tkinter.W)
    this.reidquat=Tkinter.Label(this.infopanel, anchor=Tkinter.W)
    this.reidquat.grid(row=3,column=0, sticky=Tkinter.W)
    this.reorte=Tkinter.Label(this.infopanel, anchor=Tkinter.W)
    this.reorte.grid(row=4,column=0, sticky=Tkinter.W)
    this.traffic=Tkinter.Label(this.infopanel, anchor=Tkinter.W)
    this.traffic.grid(row=5,column=0, sticky=Tkinter.W)
    this.denlocal=Tkinter.Label(this.infopanel, anchor=Tkinter.W)	
    this.denlocal.grid(row=6,column=0, sticky=Tkinter.W)
    this.denarea=Tkinter.Label(this.infopanel, anchor=Tkinter.W)
    this.denarea.grid(row=7,column=0, sticky=Tkinter.W)
		
    this.dsol.grid_remove()
    this.zurara.grid_remove()
    this.reidquat.grid_remove()
    this.reorte.grid_remove()
    this.denlocal.grid_remove()
    this.denarea.grid_remove()
    this.traffic.grid_remove()
   
    #this.radar_panel = Tkinter.Label(this.radar_frame, anchor=Tkinter.W, text="Waiting for location", image=this.RADAR_PANEL)
    #this.radar_panel.pack()
    
    #this.status.place(x=0, y=0,width=155,height=150)		
    #this.radar_panel.place(x=0, y=0,width=155,height=150)		
    #this.status.place(x=0, y=0, relwidth=199, relheight=199)			
    
    this.ship = Tkinter.Label(this.container, anchor=Tkinter.W, text="Waiting for location",image=this.SHIP)		
    rx,ry=getRadialCoords((0,0,0),0)
    this.ship.place(x=rx, y=ry)		
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
	
	if d > 88:
		d = 88
		
	#get the angle of rotation
	radians=math.atan2(z,y)
	#rotate by by distance
	d = d*0.75
	(yy,xx) = (d*math.cos(radians),d*math.sin(radians))
	
	

	return round(xx+75,0),round(yy+75,0)
	
def displayDistance(d):
	if d <= 100:
		sd=" = " +str(round(jd,1))+ "ly"
	else:
		sd=" > 100ly"
	this.status["text"]="d(Centre)"+sd
	
def displayRift(system,x,y,z):
	jd=getRiftDistance(x,y,z)
	#nc = NearestCoordinates
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
	
	this.dsol.grid()
	this.dsol["text"]="d(Sol) = {}ly".format(stringFromNumber(round(getDistance(SOL,(x,y,z)),0),0))
	this.zurara.grid()
	this.zurara["text"]="d(Zurara) = {}ly".format(stringFromNumber(round(getDistance(ZURARA,(x,y,z)),0),0))
	this.reorte.grid()
	this.reorte["text"]="d(Reorte) = {}ly".format(stringFromNumber(round(getDistance(REORTE,(x,y,z)),0),0))	
	this.reidquat.grid()
	this.reidquat["text"]="d(Riedquat) = {}ly".format(stringFromNumber(round(getDistance(RIEDQUAT,(x,y,z)),0),0))	
	
	this.ship.place(x=rx, y=ry)		
	SphereSystems(nc,(x,y,z)).start()
	Traffic(system).start()
	
	this.text_panel["image"] = this.TEXT_PANEL
	displayDistance(jd)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    
	if entry['event'] in ['StartUp', 'Location', 'FSDJump']:
		displayRift(system,float(entry["StarPos"][0]),float(entry["StarPos"][1]),float(entry["StarPos"][2]))

def cmdr_data(data):
	CmdrData(data["lastSystem"]["name"]).start()