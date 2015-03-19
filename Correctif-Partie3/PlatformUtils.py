# -*- coding: utf-8 -*-

import sys

class PlatformUtils:
	MAC_OS	=	'darwin'
	@staticmethod
	def getLeftButton():
		"""
			Return the index of the left click button depending on the operating system
		"""
		return 1
	@staticmethod
	def getRightButton():
		"""
			Return the index of the right click button depending on the operating system
		"""
		return 2 if(sys.platform == PlatformUtils.MAC_OS)else 3
