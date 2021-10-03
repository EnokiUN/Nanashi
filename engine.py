
class Player:
	def __init__(self, member, stats):
		self.member = member
		self.name = member.name
		self.id = member.id
		self.hp = stats["hp"]
		self.bhp = stats["hp"]
		self.mp = 0
		self.mmp = stats["mp"]
		self.atk = stats["atk"]
		self.defence = stats["def"]
		
class Enemy:
	def __init__(self, name, stats):
		self.name = name
		self.hp = stats["hp"]
		self.bhp = stats["hp"]
		self.mp = 0
		self.mmp = stats["mp"]
		self.atk = stats["atk"]
		self.defence = stats["def"]
        