import sqlite3
import time
import pylab

class Supervise(object):
	def __init__(self):
		self.conn = sqlite3.connect('Supervise.db')
		self.cursor = self.conn.cursor()

	def InitTable(self):
		self.cursor.execute('CREATE TABLE Main (id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT, content TEXT, value INTEGER)')

	def Insert(self, date, content, value):
		self.cursor.execute('INSERT INTO Main (date,content,value) VALUES (?,?,?)', (date, content, value))

	def DeleteById(self, id):
		self.cursor.execute('DELETE FROM Main WHERE id = ?',(id,))

	def UpdateById(self, id, content, value):
		self.cursor.execute('UPDATE Main SET content=?, value=? WHERE id=?',(content, value, id))

	def ListAllByDate(self):
		for row in self.cursor.execute('SELECT * FROM Main ORDER BY date'):
			print row

	def GetDataByDate(self, date):
		return self.cursor.execute('SELECT * FROM Main WHERE date=?',(date,))

	def GetAllData(self):
		return self.cursor.execute('SELECT * FROM Main ORDER BY date')

	def saveQuit(self):
		self.conn.commit()
		self.conn.close()

	def getCurrentDate(self):
		return time.strftime('%Y-%m-%d',time.localtime(time.time()))


	def InsertInput(self):
		content = str(raw_input("Content:"))
		print 'Value Hint: 10(< 2 hours) 15:(2~3 hours) 20:(> 3 hours)'
		value = int(raw_input("Value:"))
		date = self.getCurrentDate()
		self.Insert(date, content, value)

	def UpdateInput(self):
		id = int(raw_input('ID:'))
		content = str(raw_input("Content:"))
		value = int(raw_input("Value:"))
		self.UpdateById(id,content,value)	

	def DeleteInput(self):
		id = int(raw_input("Input id please : "))
		self.DeleteById(id)

	def ListData(self):
		self.ListAllByDate()

	def StatisticGraph(self):
		Dict = {}
		for line in self.GetAllData():
			Dict[line[1]] = Dict.get(line[1], 0) + line[3]

		lx = []
		l = Dict.values()
		sumX = 0
		for x in l:
			sumX += x
			lx.append(sumX)

		pylab.xlabel('Date')
		pylab.ylabel('Value')
		pylab.title('Training Data')
		pylab.plot(lx)
		pylab.show()
	
	def getValueToday(self):
		Sum = 0
		for line in self.GetDataByDate(self.getCurrentDate()):
			Sum += line[3]
		return Sum

	def evaluate(self,real, expect):
		if real >= 2 * expect:
			print 'Excellent!'
		elif real >= 1.5 * expect:
			print 'Well done!'
		elif real >= expect:
			print 'Just Finished!'
		else:
			print 'Not yet, Try harder!'

	def checkProgress(self):
		real = self.getValueToday()
		expect = 20
		self.evaluate(real, expect)

	def commandInterface(self):
		print "Welcome back!"
		while True:
			c = raw_input("create(c) insert(i) delete(d) update(u) list(l) progress(p) statistic(s) save & quit(q) \n")
			if c == 'i':
				self.InsertInput()
			elif c == 'd':
				self.DeleteInput()
			elif c == 'c':
				self.InitTable()
			elif c == 's':
				self.StatisticGraph()
			elif c == 'l':
				self.ListData()
			elif c == 'p':
				self.checkProgress()
			elif c == 'u':
				self.UpdateInput()
			elif c == 'q':
				self.saveQuit()
				break;
			else:
				print "Wrong Input! please try again!"


if __name__ == '__main__':
	test = Supervise()
	test.commandInterface()



