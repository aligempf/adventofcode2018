import datetime

asleep = "asleep"
awake = "awake"

class Shift:
	def __init__(self, eventTimes=[]):
		if "begins shift" in eventTimes[0]:
			self.shiftStart = eventTimes[0].split(' ')[0]
			self.ID = int(eventTimes[0].split('#')[1].split(' ')[0])
		else:
			raise Exception
		self.asleep = False
		self.startedSleeping = None
		self.sleepingTime = 0
		self.sleepingMinutes = {minute: 0 for minute in range(60)}
		for event in eventTimes[1:]:
			if "falls asleep" in event and not self.asleep:
				self.asleep = True
				self.startedSleeping = getEventTime(event)
			elif "wakes up" in event and self.asleep:
				self.asleep = False
				self.sleepingTime += (getEventTime(event) - self.startedSleeping).seconds / 60
				for minute in range(self.startedSleeping.minute, getEventTime(event).minute):
					self.sleepingMinutes[minute] += 1

	def __eq__(self, other):
		return other.ID == self.ID

	def __iadd__(self, other):
		for minute in self.sleepingMinutes:
			self.sleepingMinutes[minute] += other.sleepingMinutes[minute]
		return self

	def __isub__(self, other):
		for minute in self.sleepingMinutes:
			self.sleepingMinutes[minute] -= other.sleepingMinutes[minute]
		return self

	def __hash__(self):
		return self.ID

class Guard:
	def __init__(self, shift=None, id=None):
		if shift:
			self.ID = shift.ID
			self.sleepingTime = shift.sleepingTime
			self.sleepingMinutes = shift.sleepingMinutes
		else:
			self.ID = id
			self.sleepingTime = 0
			self.sleepingMinutes = {minute: 0 for minute in range(60)}

	def __iadd__(self, other):
		for minute in self.sleepingMinutes:
			self.sleepingMinutes[minute] += other.sleepingMinutes[minute]
			self.sleepingTime += other.sleepingMinutes[minute]
		return self

	def __str__(self):
		return str(id) + str(self.sleepingMinutes)

	def getMaxMinute(self):
		maxMinute = 0
		maxMinuteFreq = 0
		for minute in self.sleepingMinutes:
			if self.sleepingMinutes[minute] > maxMinuteFreq:

				maxMinute = minute
				maxMinuteFreq = self.sleepingMinutes[minute]
		return maxMinute


def parseInput(inputList):
	separatedInput = []
	guardShift = []
	for inputEvent in inputList:
		if "begins shift" in inputEvent and guardShift:
			separatedInput.append(guardShift)
			guardShift = []
		guardShift.append(inputEvent)
	separatedInput.append(guardShift)
	return separatedInput

def sortInput(inputList):
	return sorted(inputList, key=getEventTime)

def getEventTime(event):
	return datetime.datetime.strptime(event.split(']')[0].strip('['), "%Y-%m-%d %H:%M")

def reduceByGuard(shifts):
	guardIDs = set(shift.ID for shift in shifts)
	byGuard = set()
	for guard in guardIDs:
		currentGuard = filter(lambda a: a.ID == guard, shifts)
		guardTotal = Guard(id=guard)
		for shift in currentGuard:
			guardTotal += shift
		byGuard.add(guardTotal)
	return byGuard

def sortGuardsByTotalSleepTime(guards, reverse=True):
	return sorted(guards, key=lambda a: a.sleepingTime, reverse=reverse)
