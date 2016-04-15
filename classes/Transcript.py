class TranscriptError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Transcript:

	def __init__(self, semesters = None):
		self.total_credit_hours = 0.0
		self.total_credits_earned = 0.0
		self.total_gpa = 0.0
		self.current_semester = "There is no current sememster listed"
		
		if semesters:
			self.semesters = semesters
			self.updateVariables()
		else:
			self.semesters = []
		
	def addSemester(self, semester):
		if not semester:
			raise SemesterError("TranscriptError: The addSemester function was called with null arguement")
		else:
			self.semesters.append(semester)
			self.updateVariables()
		
	def updateVariables(self):
		hours = 0.0
		points_earned = 0.0
		
		self.findCurrentSemester()
	
		for semester in self.semesters:
			hours = hours + semester.credit_hours
			points_earned = points_earned + semester.credits_earned
			
		self.total_credit_hours = hours
		self.total_credits_earned = points_earned
		
		if self.total_credit_hours != 0:
			self.total_gpa = round(self.total_credits_earned / self.total_credit_hours, 2)
		
	def findCurrentSemester(self):
		for semester in self.semesters:
			if semester.is_current_semester:
				self.current_semester = semester
				self.semesters.remove(semester)
				break
				
	def getSemester(self, name, year):
		for semester in self.semesters:
			if semester.name == name and semester.year == year:
				"Past Semester: ", name, " ", year
				return semester
			
		if self.current_semester.name == name and self.current_semester.year == year:
			return self.current_semester
		
		# If no matching semseter was found
		return None
			
	def getGPA(self):
		return self.total_gpa
		
	def __str__(self):
	
		return_string = "\n" + \
			"***********************************\nCurrent Semester\n***********************************\n" + \
			str(self.current_semester) + \
			"\n***********************************\nPast Semesters\n***********************************\n"
		
		for semester in self.semesters:
			return_string = return_string + str(semester) + "\n"
	
		return return_string