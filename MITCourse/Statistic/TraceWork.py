#TracekWork.py

import pylab

class TraceWork(object):

	def __init__(self, filename):
		self.filename = filename
		self.data = self.GetDataFromFile()



	# read date from file
	# return a list of lines in the file

	def GetDataFromFile(self):
		try:
			traceFile = open(self.filename, 'r')
			try:
				allLines = [ line.rstrip() for line in traceFile.readlines() ]
			except:
				print "[TraceError]failed to read from %s" %self.filename
			finally:
				traceFile.close()
		except:
			print "[TraceError]failed to open %s" %self.filename

		lines = []
		for line in allLines:
			if len(line) == 0:
				continue
			lines.append(line)

		return lines


	def SaveDataToFile(self):
		try:
			f = open(self.filename, 'w')
			try:
				data = "\n".join(self.data)
				f.write(data)
			except:
				print "[TraceError]failed to save %s" %self.filename
			finally:
				f.close()
		except:
			print "[TraceError]failed to open %s" %self.filename

	def listData(self):
		for i in self.data:
			print i

	def Insert(self, date = '20121729', content = 'MIT6.00SC_L1', points = '10'):
		info = date + '|' + content + '|' + points
		self.data.append(info)

	def InsertInput(self):
		date = str(raw_input("Date:"))
		content = str(raw_input("Content:"))
		points = str(raw_input("Points:"))
		self.Insert(date, content, points)
		
	def DeleteInput(self):
		date = str(raw_input("Which date do you want check?"))
		index = []
		for i in range(len(self.data)):
			if date in self.data[i]:
				index.append(i)
		for i in index:
			print "{0}  {1}".format(i, self.data[i])
		if index != []:
			j = int(raw_input('which one will be deleted?'))
			if j not in index:
				print "Wrong Index!"
			else:
				self.data.pop(j)
		else:
			print "Fail to find records!"
			

	def DrawCurve(self):
		d = {}
		x = []
		y = []
		z = []
		for info in self.data:
			if info == '':
				break
			singleList = info.split('|')
			element = int(singleList[0].replace(' ',''))
			points = int(singleList[2])
			if element not in d.keys():
				d[element] = points
			else:
				d[element] += points

		for i in range(20121001, 20121031):
			x.append(i)
			if i in d.keys():
				y.append(d[i])
			else:
				y.append(0)

		z = y[:]
		for i in range(len(y)):
			for j in range(i):
				z[i] += y[j] 
		pylab.xlabel('Date')
		pylab.ylabel('Total Points')
		pylab.title('Training Data')
		pylab.plot(x,z)
		pylab.show()


	def MainFunction(self):
		print "Welcome to my work track, please enter command:"

		while True:
			c = raw_input("insert(i) delete(d) list(l) curve(c) exit(e) \n")
			if c == 'i':
				self.InsertInput()
			elif c == 'd':
				self.DeleteInput()
			elif c == 'l':
				self.listData()
			elif c == 'c':
				self.DrawCurve()
			elif c == 'e':
				self.SaveDataToFile()
				break;
			else:
				print "Wrong Input! please try again!"





if __name__ == "__main__":
	trace = TraceWork('TraceWork.txt')
	trace.MainFunction()

