# -*- coding: utf-8 -*-

# =============================================================
# Author: http://sefikail.cz
# =============================================================

import os
import errno
from random import choice
from shutil import rmtree
from tempfile import gettempdir


TMP_MAX = 10000  # Try again, max number


def notremoved(tempdir):
	from platform import system
	from subprocess import call

	if system() == "Windows":
		call(['cmd', '/c', 'rmdir', '/s', '/q', tempdir], shell=False)

	if os.path.exists(tempdir):
		return True
	return False


class TemporaryDirectoryWrapper:
	def __init__(self, tempdir, delete=True):
		self.tempdir = tempdir
		self.delete = delete
		self.rmtemp_called = False

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.rmtemp()

	def __del__(self):
		self.rmtemp()

	def rmtemp(self):
		if not self.rmtemp_called:
			self.rmtemp_called = True
			if self.delete and os.path.exists(self.tempdir):
				try:
					rmtree(self.tempdir)
				except Exception as e:
					if e.errno == errno.EACCES:
						if notremoved(self.tempdir):
							raise IOError(errno.EACCES, 'Cannot remove temporary directory "%s".' % self.tempdir)
					else:
						raise e

	@property
	def name(self):
		return self.tempdir


def generate_random_chain(length=12):
	# @formatter:off (pycharm - no formatting)
	characters = {
		'letters': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
		'digits': '0123456789'
	}
	# @formatter:on (pycharm - no formatting)

	all_chars = ''.join(str(x) for x in characters.values())  # All the characters in one variable
	rand_chars = ''.join(choice(all_chars) for x in range(length))  # Generate random characters
	return rand_chars


def TemporaryDirectory(suffix='', prefix='', dir=None, delete=True):
	if not dir or dir is None:
		dir = gettempdir()

	for i in range(TMP_MAX, 0, -1):
		tempdir = os.path.join(dir, prefix + generate_random_chain() + suffix)
		try:
			os.mkdir(tempdir)
		except OSError as e:
			if e.errno == errno.EEXIST:
				continue  # If folder exists, try again.
			else:
				raise e
		else:
			return TemporaryDirectoryWrapper(tempdir, delete)

	raise IOError(errno.EEXIST, 'Cannot create temporary directory "%s".' % tempdir)
