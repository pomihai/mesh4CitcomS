#!/usr/bin/python3
# program written by [pomihai]
# start: 26.01.2024
# use: create a 3D mesh file coord.dat to use in CitcomS geodinamical code.
# 2.0 variant this time use classes

# start imports
import math
#end imports

class axis:
	def __init__(self, sName = 'axis',	fStart = 1.0, fEnd = 2.0, iPoints = 3):
		self.sName = sName
		self.fStart = fStart
		self.fEnd = fEnd
		self.iPoints = iPoints
		# iPoints checking is made in buildSteps()
		self.buildSteps()
	def buildSteps(self):
		# since we will use all inputs we check here if all values are correct
		self.input_checks()

		# call of the function that makes the lSteps list
		# this function will bw overloaded to add different "flavors"
		self.make_lSteps()
	def make_lSteps(self):
		# make note that checks are made in "caller" function buildSteps

		# this calculates the steps used for a regular mesh.
		# the steps are all equal
		tmp_var = 1.0 * self.fEnd - 1.0 * self.fStart
		tmp_step = tmp_var / (self.iPoints - 1.0)
		my_steps = list()
		my_steps.append(self.fStart)
		tmp_curr_step = self.fStart
		for i in range(self.iPoints - 2):
			tmp_curr_step += tmp_step
			my_steps.append(tmp_curr_step)
		my_steps.append(self.fEnd)
		self.lSteps = my_steps

	def input_checks(self):
		# start checks
		self.myCheckPositiveValue(self.fStart, 'fStart', False, 'float', 'starting point')
		self.myCheckPositiveValue(self.fEnd, 'fEnd', False, 'float', 'ending point')
		self.myCheckPositiveValue(self.iPoints, 'iPoints', True, 'int', 'number of points')
		self.check_iPoints()
		self.check_start_end()
		# end checks

	def check_start_end(self):
		def start_endOK(fStart,  fEnd): # this function checks if "ends" are ok: start < end
			if fEnd <= fStart: return False
			return True
		if not start_endOK(self.fStart,  self.fEnd): self.myRaiseErr(self, 0)

	def check_iPoints(self):
		def iPointsOK(iP): # this function checks if "iPoints" is of form 2**n+1
			my_test = iP - 1
			while my_test > 1 and (my_test % 2 == 0):	my_test /= 2
			if my_test > 1: return False
			return True
		if not iPointsOK(self.iPoints): self.myRaiseErr(1)

	def myCheckPositiveValue(self, value = 1.0, name = 'a_value', strict = False, type = 'float',  text = 'this value:'):
		if (value >= 0 and not strict) or (value > 0 and strict): return
		error_text = 'Axis: %s; %s '
		if type == 'float': error_text += '%f'
		elif type == 'int': error_text += '%i'
		error_text += ' is not '
		if strict : error_text += 'strictly '
		error_text += 'positive.'
		raise RuntimeError( error_text % (self.sName, text, value))

	def myRaiseErr(self, iErrNumber):
		sErr = ''
		if iErrNumber == 0:
			raise RuntimeError( \
				'Axis: %s start %i and end %i give negative length: %i' \
				% (self.sName, self.fStart, self.fEnd, self.fStart - self.fEnd))
		elif iErrNumber == 1:
			raise RuntimeError( \
				'Axis: %s number of points: %i not of the form 2^n + 1! ' % (self.sName, self.iPoints) + \
				'Consider changing it to the correct form.' )
		elif iErrNumber == 2:
			raise RuntimeError( \
				'Axis: %s: source: function min_max_distance() implemented lenght units to transform to, are \'m\' & \'Km\' so far.\n' % (self.sName) + \
				'Consider changing the length unit to be one of them.' )
		else:
			raise RuntimeError( \
				'Axis: %s untreated error number: %i.' \
				% (self.sName, iErrNumber))
	# This function prints the contents of the lSteps list, each value on a separate line.
	# Each line is numbered and there is some header containing the name.
	# This oputput is useful to create a "coord.dat" file and use it with CitcomS code
	def print_nodes(self):
		def write_a_value(number_list, my_Index):
			if my_Index <= len(number_list):
				print ('%i\t%.8f' % (my_Index, number_list[my_Index - 1]))
				write_a_value(number_list, my_Index + 1)
			return
		print ('%s' % self.sName)
		write_a_value(self.lSteps, 1)
		return
	def min_max_distance(self, fLength_Meters, sOutput = 'Km'):
		if sOutput not in ['m',  'Km']: self.myRaiseErr(2)
		max = 0
		min = self.fEnd - self.fStart
		min_index = 0
		max_index = 0
		# fStart and fEnd are in radians
		# we need a factor to transform the distance in meters
		fFactor_Rad2Meter = fLength_Meters / min
		for i in range(len(self.lSteps) - 1):
			dist = self.lSteps[i + 1] - self.lSteps[i]
			if dist > max :
				max = dist
				max_index = i+1
			if dist < min :
				min = dist
				min_index = i+1
		if sOutput == 'Km': fFactor_Rad2Meter = fFactor_Rad2Meter / 1000
		min = min * fFactor_Rad2Meter
		max = max * fFactor_Rad2Meter
		print ('Axis: %s; Maximum distance: %.8f %s node index: %d Minimum distance: %.8f %s node index: %d' % \
			(self.sName, max, sOutput, max_index, min, sOutput, min_index))
		return

class agLinAxis(axis):
	def __init__(self, sName = 'aLax', fStart = 1.0, fEnd = 2.0, iPoints = 3, \
				 fSlope = 1.2):
		self.fSlope = fSlope
		axis.__init__(self, sName, fStart, fEnd, iPoints)

	def make_lSteps(self):
		# make note that checks are made in "caller"  function buildSteps

		# this calculates the steps used for a liniar aglomerated axis.

		# fSlope gives an error if it's 1.0
		# lucky for us we have an alternative already in place
		# which does exactly what fSlope = 1 would require ;)
		if self.fSlope == 1.0:
			axis.make_lSteps(self)
			return

		## def first_step:
		tmp_var = 1.0 * self.fEnd - 1.0 * self.fStart # length
		tmp_step=tmp_var*(self.fSlope-1)/(math.pow(self.fSlope,1-self.iPoints)\
			* ( math.pow(self.fSlope, self.iPoints) - self.fSlope))
		my_steps = list()
		my_steps.append(self.fStart)
		tmp_curr_end = self.fStart
		for i in range(self.iPoints - 2):
			tmp_curr_end += tmp_step
			my_steps.append(tmp_curr_end)
			tmp_step /= self.fSlope
		my_steps.append(self.fEnd)
		self.lSteps = my_steps


# fWide is how wide is the area that will be agglomerated measured in percents from the entire length
class agGaussAxis(axis):
	def __init__(self, sName = 'aGax', fStart = 1.0, fEnd = 2.0, iPoints = 17, \
				 fWhere = 60.0/100.0,  fWide = 30.0/100.0, fSteep = 0.1):
		self.fWhere = fWhere
		self.fWide = fWide
		self.fSteep = fSteep
		axis.__init__(self, sName, fStart, fEnd, iPoints)

	def make_lSteps(self):
		# first we make a "dummy" solution with iPoints and indefinite length
		# after we obtain the dummy we will scale it to the real value
		def list_wide(my_list): return my_list[len(my_list) - 1] - my_list[0]
		def dummy_try(fWhere, fWide, iPoints, fSteep = 10.0/100.0):
			top_value = 5
			a = top_value - top_value * fSteep 			#a = 4.5
			# fSteep is a proportion between a and top_value.
			# in this instance fSteep is 10%, meaning that top_value-a/top_value = 10/100

			my_fStart = 0.0
			my_fEnd = 50.0
			fLength = my_fEnd - my_fStart
			def gauss_pct(top_value, f_a,  f_b, f_c, f_x):
				return top_value-f_a*math.exp(-(math.pow((f_x-f_b),2))/(2*math.pow(f_c,2)))
			g_intervals = list()
			d_list = list()
			tmp_step = fLength / iPoints
			b = fLength * fWhere
			# here we refine b to be in the middle of a interval
			end_interval = 0
			while end_interval < b : end_interval += tmp_step
			start_interval = end_interval - tmp_step
			b = (end_interval + start_interval) / 2.0
			# b is refined
			c = fLength * fWide
			step = 0
			left_steps = iPoints - 1
			while step < start_interval:
				g_intervals.append(gauss_pct(top_value, a, b, c, step))
				step += tmp_step
				left_steps -= 1
			left_intervals = list()
			for interval in reversed(g_intervals) :
				if left_steps > 0 :
					left_intervals.append(interval)
					left_steps -= 1
				else : break
			while left_steps > 0 :
				left_intervals.append(g_intervals[0])
				left_steps -= 1
			g_intervals = g_intervals + left_intervals
			tmp_next_insert = 0
			d_list.append(tmp_next_insert)
			for interval in g_intervals :
				tmp_next_insert += interval
				d_list.append(tmp_next_insert)
			return d_list
		# this function scales the dummy_list by a given factor
#		def scaled_sol (dummy_list, fFactor, fStart, fEnd):
		def scaled_sol (dummy_list, fStart, fEnd):
			def add_float2list(my_float, my_list):
			# this function adds the same float to each element of the list
				def my_add (one_element): return one_element + my_float
				return list(map(my_add, my_list))
			def make_scaled_list(dummy_list, fFactor):
				sc_list = list()
				for interval in dummy_list:
					scaled_interval = (interval * fFactor)
					sc_list.append(scaled_interval)
				return sc_list
			dummy_length = list_wide(dummy_list)
			fLength = fEnd - fStart
			fFactor = fLength / dummy_length
			scaled_sol = make_scaled_list(dummy_list, fFactor)
			result_length = list_wide(scaled_sol)
			new_fFactor = fLength / result_length
			while math.fabs(1.0 - new_fFactor) > math.pow(10, -4):
				scaled_sol = make_scaled_list(scaled_sol, new_fFactor)
				result_length = list_wide(scaled_sol)
				new_fFactor = fLength / result_length
			scaled_sol = add_float2list(fStart,  scaled_sol)
			return scaled_sol

		# first we make the dummy
		dummy_list = dummy_try(self.fWhere, self.fWide, self.iPoints, self.fSteep)
		dummy_wide = list_wide(dummy_list)
		#we scale it to the actual length
		s_sol = scaled_sol(dummy_list, self.fStart, self.fEnd)
		self.lSteps = s_sol

def MakeAxis(axtype, direction, start, end, nodes):
	if		direction == 'x': newname = 'nsd= 1'
	elif	direction == 'y': newname = 'nsd= 2'
	elif	direction == 'z': newname = 'nsd= 3'
	else:
		raise RuntimeError( \
			'Axis direction: %s; not implemented. Must be one of: "x", "y", "z"' % direction )
		return

	if		axtype == 'regular':	tmp_axis = axis(sName = newname, fStart = start, fEnd = end, iPoints = nodes)
	elif	axtype == 'liniar':		tmp_axis = agLinAxis(sName = newname, fStart = start, fEnd = end, iPoints = nodes)
	elif	axtype == 'gaussian':	tmp_axis = agGaussAxis(sName = newname, fStart = start, fEnd = end, iPoints = nodes, fSteep = 0.1)
	else:
		raise RuntimeError( \
			'Axis type: axtype: %s; not implemented. Must be one of: "regular", "liniar", "gaussian"' % axtype )
		return
	tmp_axis.type = axtype
	return tmp_axis
