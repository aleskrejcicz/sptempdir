import json
from pkg_resources import parse_version

try:
	from urllib2 import urlopen
except ImportError:
	from urllib.request import urlopen

from sptempdir import __git_url__


def is_version_in_github(version):
	tag_url = '{url}/tree/v{version}'.format(url=__git_url__, version=version)
	try:
		resp = urlopen(tag_url)
	except Exception as e:
		pass
	else:
		if resp.code == 200:
			return True
	return False


def get_latest_tag_version(name):
	url = "https://pypi.python.org/pypi/{}/json".format(name)
	resp = urlopen(url).read().decode()
	json_load = json.loads(resp)
	sorted_versions = sorted(json_load["releases"], key=parse_version)
	return sorted_versions[::-1][0]  # reverse list and get first arg


latest_tag_version = get_latest_tag_version("sptempdir")
if not is_version_in_github(latest_tag_version):
	raise Exception("Version {lv} is not in github.com".format(lv=latest_tag_version))
