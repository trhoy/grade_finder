from Class import Class, ClassError

class SemesterError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Semester:

	def __init__(self, name, year, is_current_semester, classes = None):
		self.name = name
		self.year = year
		self.is_current_semester = is_current_semester
		if not classes:
			self.classes = []
		else:
			self.classes = classes
			self.updateVariables() # Get new gpa
		self.credit_hours = 0.0
		self.credits_earned = 0.0
		self.gpa = 0.0
		
	def addClass(self, aClass):
		if not aClass:
			raise SemesterError("SemesterError: The addClass function was called with null arguement")
		else:
			self.classes.append(aClass)
			self.updateVariables()
			
	def updateVariables(self):
		hours = 0.0
		points_earned = 0.0
		
		for aClass in self.classes:
			if aClass.grade != -1.0:
				hours = hours + aClass.credit_hours
				points_earned = points_earned + aClass.grade_points
			
		self.credit_hours = hours
		self.credits_earned = points_earned
		
		if self.credit_hours != 0:
			self.gpa = round(self.credits_earned / self.credit_hours, 2)
			
	def getGPA(self):
		return self.gpa
		
	def __str__(self):
		return_string = "\n" + \
			self.name + " " + self.year + \
			"\n---------------------------" + \
			"\nCredit Hours: " + str(self.credit_hours) + \
			"\nCredits Earned: " + str(self.credits_earned) + \
			"\nGPA: " + str(self.gpa) + \
			"\n\nClasses:\n"
			
		for aClass in self.classes:
			return_string = return_string + str(aClass)
		return return_string