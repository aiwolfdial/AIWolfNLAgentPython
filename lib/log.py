import multiprocessing.sharedctypes
import os
import logging
import logging.handlers
import multiprocessing
import configparser
import datetime
from typing import Optional, Callable
from . import util

class LogInfo():

	format = '%Y-%m-%d-%H-%M-%S-%f'
	encode = "utf-8"

	def __init__(self) -> None:
		self.__game_start_time:str = multiprocessing.sharedctypes.Array('c',100)
		self.__log_num:int = multiprocessing.Value('i',0)
		self.__log_times_num:int = multiprocessing.Value('i',0)
		self.__log_prepare_done_num:int = multiprocessing.Value('i',0)
	
	@property
	def game_start_time(self) -> str:
		return self.__game_start_time.value.decode()
	
	@game_start_time.setter
	def game_start_time(self, time:datetime.datetime) -> Optional[ValueError]:

		if type(time) is not datetime.datetime:
			raise ValueError("time must be a datetime type")
		
		self.__game_start_time.value = bytes(time.strftime(LogInfo.format),LogInfo.encode)
	
	@property
	def log_num(self) -> int:
		return self.__log_num.value
	
	def increment_log_num(self) -> None:
		self.__log_num.value += 1

	@property
	def log_times_num(self) -> int:
		return self.__log_times_num.value
	
	@log_times_num.setter
	def log_times_num(self, times:int) -> Optional[ValueError]:

		if type(times) is not int:
			raise ValueError("times must be a int type")
		
		self.__log_times_num.value = times
	
	@property
	def log_prepare_done_num(self) -> int:
		return self.__log_prepare_done_num.value
	
	def increment_log_prepare_done_num(self) -> None:
		self.__log_prepare_done_num.value += 1
	
	def reset_params(self) -> None:
		self.log_times_num = 0
		self.__log_prepare_done_num.value = 0

class Log():

	encode_format:str = "utf-8"

	def __init__(self, log_path:str, log_name:str):
		# set logger
		self.logger = logging.getLogger(log_name)
		self.logger.setLevel(logging.DEBUG)
		self.log_handler = logging.FileHandler(log_path, mode="w", encoding=Log.encode_format)
		self.logger.addHandler(self.log_handler)
		self.log_fmt = logging.Formatter("%(message)s")
		self.log_handler.setFormatter(self.log_fmt)
	
	def debug(self, message:str) -> None:
		self.logger.debug(message)

	def info(self, message:str) -> None:
		self.logger.info(message)
	
	def warning(self, message:str) -> None:
		self.logger.warning(message)
	
	def error(self, message:str) -> None:
		self.logger.error(message)
	
	def exception(self, message:str) -> None:
		self.logger.exception(message)
	
	def critical(self, message:str) -> None:
		self.logger.critical(message)
	
	def close(self) -> None:
		self.logger.removeHandler(self.log_handler)
		self.log_handler.close()
		logging.shutdown()

class AgentLog(Log):

	header_format = "-------------{header}-------------"
	small_header_format = "-------{header}-------"
	custom_response = "--------------{custom} RESPONSE--------------"

	def __init__(self, inifile:configparser.ConfigParser, agent_name:str, log_info:LogInfo):
		# load log inifile
		log_inifile = util.check_config(config_path=inifile.get("filePath","log_inifile"))
		log_inifile.read(inifile.get("filePath","log_inifile"),"UTF-8")

		# set log path
		current_time = datetime.datetime.now()

		if log_info.log_num%inifile.getint("agent","num") == 0:
			log_info.game_start_time = current_time
		else:
			current_time = datetime.datetime.strptime(log_info.game_start_time, LogInfo.format)

		log_info.increment_log_num()

		self.log_dir_path = log_inifile.get("log","storage_path")
		self.log_month_day_dir = self.log_dir_path + os.sep + current_time.strftime('%m-%d')

		if log_info.log_times_num == 0:
			dir_num:int = len(util.get_directories(path=self.log_month_day_dir)) + 1
			log_info.log_times_num = dir_num
		else:
			dir_num:int = log_info.log_times_num

		self.log_times = self.log_month_day_dir + os.sep + str(dir_num)
		self.log_file_path = self.log_times + os.sep + current_time.strftime('%H-%M-%S-%f') + "_" + agent_name + ".log"

		# load [log] flags
		self.log_flag_dict = {}	# key: func_name , value: flag
		self.log_flag_dict["get_info"] = log_inifile.getboolean("log","get_info")
		self.log_flag_dict["initialize"] = log_inifile.getboolean("log","initialize")
		self.log_flag_dict["talk"] = log_inifile.getboolean("log","talk")
		self.log_flag_dict["vote"] = log_inifile.getboolean("log","vote")

		# prepare
		self.prepare_log_dir()

		super().__init__(log_path=self.log_file_path, log_name=agent_name)

		log_info.increment_log_prepare_done_num()

		if log_info.log_prepare_done_num%inifile.getint("agent","num") == 0: log_info.reset_params()

	def print_header_decorator(func:Callable):

		def _wrapper(self,*args, **keywords):

			# check write or not
			if not self.log_flag_dict.get(func.__name__, True):
				print(func.__name__)
				return

			if keywords.get("header") != None:
				# print custom header
				self.info(AgentLog.header_format.format(header=keywords.get("header")))
			else:
				# print func name as header
				self.info(AgentLog.header_format.format(header=func.__name__))

			# execute function
			result = func(self, *args, **keywords)

			return result

		return _wrapper
	
	def prepare_log_dir(self) -> None:
		# if log directory is not exist: make log directory
		util.make_directory(directory_path=self.log_dir_path)
		
		# if log directory is not exist: make log directory
		util.make_directory(directory_path=self.log_month_day_dir)	

		util.make_directory(directory_path=self.log_times)
	
	@print_header_decorator
	def get_info(self, get_info:map, request:str) -> None:
		"""
			print information get from server
		"""

		self.info(get_info)
		self.info("Request:" + request)
	
	@print_header_decorator
	def initialize(self, role:str) -> None:
		"""
			print initialize log (role)
		"""

		self.info("ROLE:" + role)
	
	@print_header_decorator
	def talk(self, comment:str) -> None:
		"""
			print talk log
		"""

		self.info(message=comment)

	@print_header_decorator
	def vote(self, vote_target:int) -> None:
		"""
			print vote log
		"""

		self.info(f"Vote: " + util.index_to_agent_format(agent_index=vote_target))

	@print_header_decorator
	def divine(self, divine_target:int) -> None:
		"""
			print divine log
		"""

		self.info(f"Divine: " + util.index_to_agent_format(agent_index=divine_target))
	
	@print_header_decorator
	def divine_result(self, divine_result:dict) -> None:

		self.info(divine_result)
	
	@print_header_decorator
	def attack(self, attack_target:int) -> None:
		"""
			print attack log
		"""

		self.info(f"Attack: " + util.index_to_agent_format(agent_index=attack_target))
	
	@print_header_decorator
	def daily_finish(self) -> None:
		"""
			print daily finish log
		"""