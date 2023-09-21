class Command():
	initialize = "INITIALIZE"
	name = "NAME"
	role = "ROLE"
	daily_initialize = "DAILY_INITIALIZE"
	daily_finish = "DAILY_FINISH"
	talk = "TALK"
	vote = "VOTE"
	whisper = "WHISPER"
	finish = "FINISH"

	def is_initialize(request:str) -> bool:
		return request == Command.initialize
	
	def is_name(request:str) -> bool:
		return request == Command.name
	
	def is_role(request:str) -> bool:
		return request == Command.role
	
	def is_daily_initialize(request:str) -> bool:
		return request == Command.daily_initialize
	
	def is_daily_finish(request:str) -> bool:
		return request == Command.daily_finish
	
	def is_talk(request:str) -> bool:
		return request == Command.talk
	
	def is_vote(request:str) -> bool:
		return request == Command.vote
	
	def is_whisper(request:str) -> bool:
		return request == Command.whisper
	
	def is_finish(request:str) -> bool:
		return request == Command.finish