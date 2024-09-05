from abc import abstractmethod


class BaseView:
	def __init__(self):
		pass

	@abstractmethod
	def display(self):
		pass