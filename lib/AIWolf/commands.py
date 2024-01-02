class AIWolfCommand():
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
		return request == AIWolfCommand.initialize
	
	def is_name(request:str) -> bool:
		return request == AIWolfCommand.name
	
	def is_role(request:str) -> bool:
		return request == AIWolfCommand.role
	
	def is_daily_initialize(request:str) -> bool:
		return request == AIWolfCommand.daily_initialize
	
	def is_daily_finish(request:str) -> bool:
		return request == AIWolfCommand.daily_finish
	
	def is_talk(request:str) -> bool:
		return request == AIWolfCommand.talk
	
	def is_vote(request:str) -> bool:
		return request == AIWolfCommand.vote
	
	def is_whisper(request:str) -> bool:
		return request == AIWolfCommand.whisper
	
	def is_finish(request:str) -> bool:
		return request == AIWolfCommand.finish