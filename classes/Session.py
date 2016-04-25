import sys
import datetime
import requests
import re
from Transcript import Transcript, TranscriptError
from Semester import Semester, SemesterError
from Class import Class, ClassError
from lxml import html

class ByuSessionError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ByuSession:

	def __init__(self, username, password):
			
			# Check to make sure all information is present
			if not username or not password:
				raise ByuSessionError("Please enter a username and password to continue.")
			
			self.username = username.lower().strip()
			self.password = password
			self.transcript = []
			self.parsed_transcript = None
			self.session = None
			self.semesters = []

	def signIn(self):
	
		sys.stdout.write("Logging in... ")
	
		session_requests = requests.session()
		
		login_url = "https://cas.byu.edu/cas/login?service=https://my.byu.edu/uPortal/Login"
		result = session_requests.get(login_url)
		
		# Must return a HTTP 200 code
		if str(result.status_code)[0] is not "2":
			raise ByuSessionError("Could not gather CAS login page. HTTP error Code: " + str(result.status_code))
		
		tree = html.fromstring(result.text)
		execution = list(set(tree.xpath("//input[@name='execution']/@value")))[0]
		lt = list(set(tree.xpath("//input[@name='lt']/@value")))[0]

		# Prepare http post data
		payload = {
			"username": self.username, 
			"password": self.password,
			"execution": execution,
			"lt": lt,
			"_eventId": "submit"
		}
		
		# Post the credentials
		result = session_requests.post(
			login_url, 
			data = payload, 
			headers = dict(referer=login_url)
		)
		
		# Must return a HTTP 200 code
		if str(result.status_code)[0] is not "2":
			raise ByuSessionError("Login failed. Please check your username and password. HTTP error Code: " + str(result.status_code))
		
		if "Unable to sign in:" in result.text:
			raise ByuSessionError("Login failed. Please check your username and password.")
		
		self.session = session_requests
		
		sys.stdout.flush()
		sys.stdout.write("Done.\n")
		
	def getTranscript(self):	
	
		sys.stdout.write("Retreiving transcript... ")
	
		if self.session is None:
			raise ByuSessionError("Please sign in first.")
			return
	
		url = 'https://y.byu.edu/ry/ae/prod/records/cgi/stdCourseWork.cgi'
		result = self.session.get(
			url, 
			headers = dict(referer = url)
		)
		
		# Must return a HTTP 200 code
		if str(result.status_code)[0] is not "2":
			raise ByuSessionError("The transcript page returned with errors. HTTP error Code: " + str(result.status_code))
		
		tree = html.fromstring(result.content)
		elem = tree.xpath("//pre/descendant-or-self::text()")
		
		for x in elem:
			self.transcript.append(x.replace("\\n", "\n"))
			
		if not self.transcript:
			raise ByuSessionError("The transcript could not be collected.\n***Please check your username and password.***")
			
		sys.stdout.flush()
		sys.stdout.write("Done.\n")
	
	def getAndParseTranscript(self):
	
		# If the transcript has not been collected yet, get it
		if not self.transcript:
			self.signIn()
			self.getTranscript()
		
		# Patterns to look for in the transcript
		semester_start_pattern = re.compile("((?:Fall|Winter|Spring|Summer)\s(?:Semester|Term)\s[0-9]{4}).*")
		current_semester_signifier = re.compile("(?:CURRENT ENROLLMENT).*")
		transfer_credits_start = re.compile("(?:YRTRM)[\S\s].*")
		end_pattern = re.compile("(?:SEM|TRN|--------------------------------------------------------------).*")
		past_class_pattern = re.compile("[\s\S]{6}(?:[0-9]{3}|[0-9]{3}[A-Z])\s+[0-9]{3}[\s\S]{42}[0-9]\.[0-9]{2}.*[A-P|W][+-]?")
		current_class_pattern = re.compile("[\s\S]{6}(?:[0-9]{3}|[0-9]{3}[A-Z])\s+[0-9]{3}[\s\S]{42}[0-9]\.[0-9]{2}")
		
		start_semester = False
		start_current_semester = False
		
		semesters = []
		recording_semester = ""
		
		# Otherwise, only get the current semester
		for line in self.transcript:
			# End of semester, current semester, and transfer credits
			if end_pattern.match(line.strip()) and start_semester:
				start_semester = False
				semesters.append(recording_semester)
				if start_current_semester:
					break;
			# Current semester sigifier
			elif current_semester_signifier.match(line):
				start_current_semester = True
			# Start of any semester
			elif semester_start_pattern.match(line):
				start_semester = True
				semester_name = line.split() # [name] Semester [year]
				recording_semester = Semester(semester_name[0], semester_name[2], start_current_semester)
			# Append class to semester
			elif start_semester:
				line = line.strip()
				if not start_current_semester:
					recording_semester.addClass(self.parsePastClass(line))
				else:
					if past_class_pattern.match(line):
						recording_semester.addClass(self.parsePastClass(line))
					else:
						recording_semester.addClass(self.parseCurrentClass(line))
						
					
		if not semesters:
			raise ByuSessionError("There are no classes listed for the selected semester.\nIf you are receiving this message in error, please try again.")
					
		self.parsed_transcript = Transcript(semesters)
		return self.parsed_transcript
		
	def getTargetSemester(self, semester_name, year):
	
		semester_name = semester_name.lower().capitalize()
		if semester_name == "Semester" or (semester_name != "All" and not year):
			raise ByuSessionError("Please enter a valid semester and year to continue.")
	
		if not self.transcript:
			self.getAndParseTranscript()
		
		# If all semesters are selected, print entire thing
		if semester_name == "All":	
			return self.parsed_transcript
		else:
			return self.parsed_transcript.getSemester(semester_name, year)
			
	def parsePastClass(self, aClass):
	
		aClass_list = self.parseClass(aClass, 2)
			
		department = aClass_list[0]
		number = aClass_list[1]
		section = aClass_list[2]
		name = aClass_list[3]
		points_total = aClass_list[4]
		grade = aClass_list[5]
			
		# Combine classes
		return Class(department, number, int(section), name, float(points_total), grade)
		
	def parseCurrentClass(self, aClass):
			
		aClass_list = self.parseClass(aClass, 1)
			
		department = aClass_list[0]
		number = aClass_list[1]
		section = aClass_list[2]
		name = aClass_list[3]
		points_total = aClass_list[4]
			
		# Combine classes
		return Class(department, number, int(section), name, float(points_total))
		
	def parseClass(self, aClass, parse_offset):
		aClass_list = aClass.split()
		
		# Check for department name in first indexes
		if not aClass_list[1][0].isdigit():
			aClass_list[0:2] = [" ".join(aClass_list[0:2])]
			
		# Merge class description
		aClass_list[3:(len(aClass_list) - parse_offset)] = [" ".join(aClass_list[3:(len(aClass_list) - parse_offset)])]
			
		return aClass_list