#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pypandoc


with open('../../README.md', 'r') as load_file:
	filtred_text = []
	icons_dict = {}
	md_text = load_file.read()
	for line in md_text.splitlines():
		m = re.search(r'https://img.shields.io/', line)
		if m:
			for i, l in enumerate(line.split(' ')):
				lm = re.search(r'(https:.*\.svg)', l)
				ltext = r'.. image:: {svg_image}'.format(svg_image=lm.group(1))
				itext = r'TemplateFooterLineN{}'.format(i)
				icons_dict[itext] = ltext
				filtred_text.append(itext + "\n")
		else:
			filtred_text.append(line)

	clean_text = []
	rst_text = pypandoc.convert_text('\n'.join(filtred_text), 'rst', format='md')
	for line in rst_text.splitlines():
		if line.startswith(tuple(icons_dict.keys())):
			clean_text.append(icons_dict.get(line))
		else:
			clean_text.append(line)

	rst_text_clean = '\n'.join(clean_text)

	with open('../../PYPI_README.rst', 'wb') as f:
		f.write(rst_text_clean.encode('utf-8'))
