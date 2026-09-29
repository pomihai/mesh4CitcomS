#!/usr/bin/python3
from mesh4CitcomS_2_1 import *

# f = fraction between 0 and 1
# ax = axis from wich we "get"
def getLow(f, ax):
	weReturn=list()
	iNrPts=int(ax.iPoints * f)
	for i in range(iNrPts):
		weReturn.append(ax.lSteps[i])
	return weReturn

def updateLow(ax, lowList):
	for i in range(len(lowList)):
		ax.lSteps[i]=lowList[i]

def list2File(l2Spit = list(), sFName = "myTMP.dat"):
	fl = open(sFName, 'w')
	for l in l2Spit:
		fl.write(str(l) + '\n' )
	fl.close()

def mirror_me(ax):
	if (ax.sName == "nsd= 1"):
		retName="x"
	else:
		if (ax.sName == "nsd= 2"):
			retName="y"
		else:
			if (ax.sName == "nsd= 3"):
				retName="z"
	weReturn = MakeAxis('regular',	retName, ax.fStart, ax.fEnd, ax.iPoints)
	weReturn.make_lSteps()
	# myIndex=0
	for i in range(ax.iPoints-1):
		myDelta=ax.lSteps[ax.iPoints-1-i]-ax.lSteps[ax.iPoints-2-i]
		weReturn.lSteps[i+1]=weReturn.lSteps[i]+myDelta
	return weReturn

# by [pomihai] April 2026
# 
# ax	: axis
# iGap	: index of the start interval (lower coordinate of the interval has this index)
# 
# method:
# *	we make the given segment equal to it's successor.
# *	for this we spread the difference to change (+ or -) the segments left and right of iGap.
# 	=> all the segments on this axis

def smoothThisGap(ax, iGap):

	# fDelta could be positive or negative
	fDelta = ((ax.lSteps[iGap+1] - ax.lSteps[iGap]) - (ax.lSteps[iGap+2] - ax.lSteps[iGap+1]))
	# first we subtract fDelta from the length of the axis. It will be added back later.
	# 	It works the same if fDelta is positive or negative.
	for k in range(iGap, ax.iPoints - 1):
		ax.lSteps[k+1] = ax.lSteps[k+1] - fDelta

	# the length of the interval that we will "stretch" is the difference between the
	# length of the axis and the part we want to spread onto the steps: fDelta.
	# all steps of the axis will change (grow or shrink) accordingly to their original length
	# here "stretching interval" is the sum of all the mesh edges, aka "steps" on this axis
	fStretchInterval = ax.lSteps[ax.iPoints-1] - ax.fStart

	# fStretchInterval should be always positive
	# here we store a factor (quota) to stretch the steps (edges) according to their initial length
	lFraction = list()
	for k in range(ax.iPoints - 1):
		lFraction.append((ax.lSteps[k+1] - ax.lSteps[k])/fStretchInterval)

	# here we stretch the interval: each step (edge) must change by a factor of it's initial length
	# but we also have to account for the previous changes made: this is fAddedSoFar
	fAddedSoFar = 0
	for k in range(ax.iPoints - 1):
		fAddedSoFar = fAddedSoFar + lFraction[k]*fDelta
		ax.lSteps[k+1] = ax.lSteps[k+1] + fAddedSoFar 


## theta ecuator: 1.5708


#theta
start_x	= 1.453079077	  # north
end_x	= 1.688520923	  # south ~1500Km

# #fi
start_y	= 0				  # west
end_y	= 0.235441846	  # east ~1500Km

# #r
# old start_z	= 0.9004           # old bottom: this sets the depth to 634.5 Km (1-0.0996)
start_z	= 0.905038456              # bottom: this sets the depth to 605 Km (1−0.094961544)

end_z	= 1.0			 			# top: this value is set to 1. Indicates the surface of the planet


# ## new model mesh nodes configuration April 2026

nodex  = 65
nodey  = 65
nodez  = 33


zAxis = MakeAxis('liniar',	'z', start_z, end_z, nodez)
zAxis.fSlope = 1.08
zAxis.make_lSteps()

# here xAxis

xAxis = MakeAxis('gaussian',	'x', start_x, end_x, nodex)
xAxis.fWhere=0.25
xAxis.fWide=0.35
xAxis.fSteep=0.05
xAxis.make_lSteps()

xAxisOther = mirror_me(xAxis)

updateLow(xAxisOther, getLow(0.48, xAxis))
xAxis = xAxisOther

smoothThisGap(xAxis, 30)

# xAxisOther = MakeAxis('liniar',	'x', start_x, end_x, nodex)
# xAxisOther.fSlope = 0.9708
# xAxisOther.make_lSteps()

# xAxis = MakeAxis('gaussian',	'x', start_x, end_x, nodex)
# xAxis.fWhere=0.3
# xAxis.fWide=0.7
# xAxis.fSteep=0.01
# xAxis.make_lSteps()

# updateLow(xAxisOther, getLow(0.52, xAxis))
# xAxis = xAxisOther

# xAxisOther = mirror_me(xAxis)
# xAxis=xAxisOther



# Earth_Radius_meters = 6371000
# xAxis.min_max_distance((end_x - start_x) * Earth_Radius_meters, 'Km')

# list2File(xAxis.lSteps, 'x_axis_tmp2.dat')
# quit()



# here yAxis

yAxis = MakeAxis('gaussian',	'y', start_y, end_y, nodey)
yAxis.fWhere=0.25
yAxis.fWide=0.35
yAxis.fSteep=0.05
yAxis.make_lSteps()

yAxisOther = mirror_me(yAxis)

updateLow(yAxisOther, getLow(0.48, yAxis))
yAxis = yAxisOther

smoothThisGap(yAxis, 30)



# yAxisOther = MakeAxis('liniar',	'y', start_y, end_y, nodey)
# yAxisOther.fSlope = 0.9708
# yAxisOther.make_lSteps()

# yAxis = MakeAxis('gaussian',	'y', start_y, end_y, nodey)
# yAxis.fWhere=0.3
# yAxis.fWide=0.7
# yAxis.fSteep=0.01
# yAxis.make_lSteps()

# updateLow(yAxisOther, getLow(0.52, yAxis))
# yAxis = yAxisOther

# yAxisOther = mirror_me(yAxis)
# yAxis=yAxisOther

### these lines are to fiddle with the looseness or tightness of the mesh

Earth_Radius_meters = 6371000
# yAxis.min_max_distance((end_y - start_y)*Earth_Radius_meters,  'Km')
# quit()


xAxis.min_max_distance((end_x - start_x)*Earth_Radius_meters,  'Km')
yAxis.min_max_distance((end_y - start_y)*Earth_Radius_meters,  'Km')
zAxis.min_max_distance((end_z - start_z)*Earth_Radius_meters,  'Km')

quit()

# HERE lines 4 real
# HERE lines 4 real
# HERE lines 4 real

xAxis.print_nodes()
yAxis.print_nodes()
zAxis.print_nodes()
