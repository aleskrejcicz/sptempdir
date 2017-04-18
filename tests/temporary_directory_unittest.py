import sys
import re
import os
import unittest
from sptempdir import TemporaryDirectory
from tempfile import gettempdir


class SPtempdirRemoveAutoTrueOrFalse(unittest.TestCase):
	def test_tempdir_with_autodelete_true(self):
		with TemporaryDirectory(delete=True) as d:
			self.assertTrue(os.path.exists(d.name))
		self.assertFalse(os.path.exists(d.name))

	def test_tempdir_with_autodelete_false(self):
		with TemporaryDirectory(delete=False) as d:
			self.assertTrue(os.path.exists(d.name))
		self.assertTrue(os.path.exists(d.name))


class SPtempdirClassDestroyTrueOrFalse(unittest.TestCase):
	def test_tempdir_class_autodelete_true(self):
		d = TemporaryDirectory(delete=True)
		self.assertTrue(os.path.exists(d.name))
		tempdir = d.name
		del d
		self.assertFalse(os.path.exists(tempdir))

	def test_tempdir_class_autodelete_false(self):
		d = TemporaryDirectory(delete=False)
		self.assertTrue(os.path.exists(d.name))
		tempdir = d.name
		del d
		self.assertTrue(os.path.exists(tempdir))


class SPtempdirRemoveManually(unittest.TestCase):
	def test_tempdir_manually_one(self):
		d = TemporaryDirectory(delete=False)
		self.assertTrue(os.path.exists(d.name))
		d.remove()
		self.assertFalse(os.path.exists(d.name))


class SPtempdirOther(unittest.TestCase):
	def test_tempdir_remove_one(self):
		with TemporaryDirectory() as d:
			self.assertTrue(os.path.exists(d.name))
			d.remove()
			self.assertFalse(os.path.exists(d.name))

	def test_tempdir_remove_two(self):
		with TemporaryDirectory() as d:
			self.assertTrue(os.path.exists(d.name))
			d.remove()
			self.assertFalse(os.path.exists(d.name))

	def test_tempdir_dir_and_prefix_and_suffix(self):
		spec_dir_name, prefix, suffix = 'example_subdir', "prefbegin_", "_suffend"
		my_specific_dir = os.path.join(gettempdir(), spec_dir_name)
		if not os.path.exists(my_specific_dir):
			os.mkdir(my_specific_dir)
		with TemporaryDirectory(
				prefix=prefix,
				suffix=suffix,
				dir=my_specific_dir
		) as temp:
			dirs_split = temp.name.split(os.sep)
			start_index = len(dirs_split) - 2
			root_dirname, random_dirname = dirs_split[start_index:]
			self.assertTrue(start_index >= 0)
			self.assertEqual(root_dirname, spec_dir_name)
			self.assertTrue(re.match('^({p}).*({s})$'.format(p=prefix, s=suffix), random_dirname))

	def test_tempdir_cmdline_rmdir(self):
		# TODO: In future (python - windows problem testing)
		# with TemporaryDirectory() as d:
		# 	self.assertTrue(os.path.exists(d.name))
		# 	os.chmod(d.name, 0o000)
		# self.assertFalse(os.path.exists(d.name))
		pass


if __name__ == '__main__':
	sys.exit(unittest.main())
