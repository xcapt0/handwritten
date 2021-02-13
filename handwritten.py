import os
import random
import re
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from math import ceil
from datetime import datetime
from typing import Optional, List, Union
import docx2txt


class HandWrite:
	"""Converts text into handwritten text"""
	all_pages: Optional[str] = None
	font_path: str = os.path.join(os.path.dirname(__file__), 'Cursive.ttf')

	def _add_line_break(self, text: str) -> List[List[str]]:
		"""
		Limits the number of words in a line so that it doesn't get out of the image borders

		text:
			Plain text with \n \t and so on symbols
		"""
		lines = []
		line = []
		max_width = 1170
		font = ImageFont.truetype(self.font_path, 41)

		for word in text.split(' '):
			line.append(word)
			line_width, line_height = font.getsize('  '.join(line))

			if line_width > max_width:
				line.pop()
				lines.append(line)
				line = [word]

		lines.append(line)
		return lines

	def _rotate_line(self, row: str, font: object) -> object:
		"""Rotates line. Returns Pillow object"""
		line_height = sum(font.getmetrics())
		deg = 1 + random.random()

		fontimage = Image.new('L', (font.getsize(row)[0], line_height + 5))
		ImageDraw.Draw(fontimage).text((0, 0), row, fill=255, font=font)
		fontimage = fontimage.rotate(deg, resample=Image.BICUBIC, expand=True)

		return fontimage

	def _format_text(self, text: str) -> List[List[list]]:
		"""
		Formats text into list of paragraphs for adding paragraphs in Pillow

		text:
			Plain text with \n \t and so on symbols
		"""
		lines = []
		paragraph = text.split('\n')

		for rows in paragraph:
			lines.append(self._add_line_break(rows))

		return lines

	def _pages_list(self, plain_text: str) -> List[Union[List[list], list]]:
		"""
		Gets plain text and returns a list separated into pages for rendering the images

		plain_text:
			Plain text with \n \t and so on symbols
		"""
		formatted_text = self._format_text(plain_text)

		# Converts into 1 dimensional list
		all_lines = sum(formatted_text, [])
		max_lines = 30
		num_pages = ceil(len(all_lines) / max_lines)
		# Nested list of pages, paragraphs, and lines
		pages = [all_lines[max_lines * i:max_lines * (i + 1)] for i in range(num_pages)]

		return pages

	def _save_image(self, file: object, path: str) -> None:
		"""
		Save image

		file:
			Pillow object

		path:
			File path to save jpg file
		"""
		file.save(path)

	def _render(self, lst: List[Union[List[list], list]], save_dir: str) -> None:
		"""
		Adjusts the display of text in the image. Adds a random slope and indent
		of the text, draws the text on the image, adds the file name.

		lst:
			Nested list of pages, paragraphs, and lines

		save_dir:
			Folder path to save images
		"""
		if len(lst) > 0:
			font = ImageFont.truetype(self.font_path, 42)

			# Separate by pages
			for i, page in enumerate(lst):
				y = 0
				file = Image.open(os.path.join(os.path.dirname(__file__), 'A4.png'))
				ImageDraw.Draw(file)

				# Add random angle slope for the line
				for line in page:
					x = random.randint(40, 55)
					y += random.randint(52, 55)
					row = re.sub(r'[«»]', '"', '  '.join(line))
					row = re.sub(r'[–—]', '-', row)
					rotated = self._rotate_line(row, font)
					file.paste((98, 64, 179), box=(x, y), mask=rotated)

				image_name = '{} {} {}.jpg'.format('hand', datetime.now().date(), i)

				if not save_dir:
					path = os.path.join(os.path.dirname(__file__), image_name)
				else:
					path = os.path.join(save_dir, image_name)

				self._save_image(file, path)

	def to_txt(self, path: str, edit: bool = False, random_order: bool = True,
			   save_path: Optional[str] = None) -> str:
		"""
		Extracts text from docx, doc, or txt file

		path:
			Path to open file, for example: /script_dir/file.docx

		edit:
			Saves formatted txt file. If no directory is specified, it'll be saved
			to the folder with the python file

		random_order:
			If it needs a random selection of paragraphs. If there are less than 10
			paragraphs, there is a random selection of sentences.

		save_path:
			File path to save txt file
		"""
		if os.path.getsize(path) <= 0:
			raise BaseException('Empty file')

		if re.search(r'(\.doc$)|(\.docx$)', path):
			text = docx2txt.process(path)
		elif re.search(r'\.txt$', path):
			with open(path, 'r', encoding='utf-8') as file:
				text = file.read()
		else:
			raise ValueError('Wrong file type! You can only use .doc, .docx, .txt format')

		processed_text = re.sub(r'\n+', '\n', text)

		if random_order:
			if processed_text.count('\n') < 10:
				splitted = processed_text.split('.')
			else:
				splitted = processed_text.split('\n')

			chosen = []

			# Minimum and maximum number of random paragraph or
			# number of random sentences
			min_val = round(0.2 * len(splitted))
			max_val = round(0.4 * len(splitted))
			num_paragraphs = random.randint(min_val, max_val)
			step = 1

			for i in range(0, num_paragraphs, step):
				chosen.append(splitted[i])
				step = len(splitted) // num_paragraphs

			final_text = '\n'.join(chosen)
		else:
			final_text = processed_text

		if edit:
			if not save_path:
				save_path = os.path.join(os.path.dirname(path), 'temp.txt')

			with open(save_path, 'w+', encoding='utf-8') as temp:
				temp.write(final_text)

		return final_text

	def convert_to_image(self, file_path: str, save_dir: Optional[str] = None,
						 random_order: bool = True) -> None:
		"""
		Converts docx, doc, or txt file into images with handwritten fonts

		file_path:
			Specify file path, for example: /script_dir/file.docx

		random_order:
			If it needs a random selection of paragraphs. If there are less than 10
			paragraphs, there is a random selection of sentences.

		save_dir:
			Folder path to save images
		"""
		text = self.to_txt(file_path, random_order=random_order)
		pages = self._pages_list(text)
		self._render(pages, save_dir)