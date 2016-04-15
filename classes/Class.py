class ClassError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Class:

	def __init__(self, department, number, section, name, credit_hours, letter_grade = None):
	
		if not isinstance(department, basestring):
			raise ClassError("Department needs to be a string. Deparment was: " + type(department))
		if not isinstance(number, basestring):
			raise ClassError("Class number needs to be a string. Class number was: " + type(number))
		if not isinstance(section, (int, long)):
			raise ClassError("Section number needs to be an int. Section was: " + type(section))
		if not isinstance(name, basestring):
			raise ClassError("Name needs to be a string. Name was: " + type(name))
		if not isinstance(credit_hours, float):
			raise ClassError("Points total needs to be a float. Points total was: " + type(credit_hours))
		if not isinstance(letter_grade, basestring) and letter_grade is not None:
			raise ClassError("Letter grade needs to be a string. Letter grade was: " + type(name))
		
		self.department = department
		self.number = number
		self.section = section
		self.name = name
		self.credit_hours = credit_hours
		if letter_grade:
			self.letter_grade = letter_grade
			self.grade = self.convertToNumberGrade(letter_grade)
		else:
			self.letter_grade = "Current"
			self.grade = -1.0
		
		if self.grade != -1.0:
			self.credits_possible = credit_hours * 4.0
			self.grade_points = self.grade * credit_hours
		else:
			self.credits_possible = 0
			self.grade_points = 0
		
	def convertToNumberGrade(self, letter_grade):
		letter = letter_grade[:1]
		sign = letter_grade[1:].strip()
		
		if letter == 'A' or letter == 'P':
			points = 4.0
		elif letter == 'B':
			points = 3.0
		elif letter == 'C':
			points = 2.0
		elif letter == 'D':
			points = 1.0
		elif letter == 'E':
			points = 0.0
		elif letter == 'F':
			points = 0.0
		elif letter == 'W':
			points = -1.0
		else:
			raise ClassError('Grade letter not recognized! Letter was: ' + letter)
			
		if sign:
			if letter == 'B' or letter == 'C' or letter == 'D':
				if sign == '+':
					grade_change = 0.3
				elif sign == '-':
					grade_change = -0.3
			elif letter == 'A':
				if sign == '-':
					grade_change = -0.3
			else:
				raise ClassError('Grade sign not recognized! Grade was: ' + letter_grade)
		else:
			grade_change = 0
			
		points = points + grade_change
		
		return points
		
	def __str__(self):
		return_string = '  {:<6} {:<4} {:<30} {:<4} {:<2}\n'.format(self.department, self.number, self.name, self.credit_hours, self.letter_grade)
		return return_string