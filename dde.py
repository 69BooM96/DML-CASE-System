import os
import sys
import json
import string
import random
import numpy as np
from collections import Counter


class DDE:
	unicode_types = json.load(open("utf.json", "r"))
	def __init__(self, lkey=2, layers=8):
		self.lkey = lkey
		self.layers = layers
		self.matrix_I = []
		self.matrix_O = []
		self.matrix_R = {}

		self.auth_key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

	def gen_pointers(self):
		self.lkey

	def gen_matrix(self, types=None):
		dmt = None
		if types is not None: dmt = [self.unicode_types[m] for m in types]
		else: dmt = self.unicode_types

		for lindex in range(self.layers):
			self.matrix_I.append({})
			self.matrix_O.append({})

			for mt in dmt:
				for index in range(mt["s"], mt["e"]):
					rkey = self.gen_keys(self.lkey)

					sb = chr(index)

					if rkey not in self.matrix_O[lindex]:
						self.matrix_I[lindex][sb] = rkey
						self.matrix_O[lindex][rkey] = sb
					else:
						for i in range(0x10000):
							big = i.to_bytes(self.lkey, 'big')
							little = i.to_bytes(self.lkey, 'little')

							if big not in self.matrix_O[lindex]:
								self.matrix_I[lindex][sb] = big
								self.matrix_O[lindex][big] = sb
								break

							if little not in self.matrix_O[lindex]:
								self.matrix_I[lindex][sb] = little
								self.matrix_O[lindex][little] = sb
								break

	def update_matrix(self, data):
		for i in data:
			...

	def live_decode(self, data, mn=None):
		res = []
		map_key = {}

		old_sb = ""
		if mn is None:
			for i in data:
				for lindex in range(self.layers):
					sb = self.matrix_O[lindex].get(i)
					if sb is None and lindex == self.layers-1:
						map_key[old_sb] = i
					else:
						old_sb = sb
						res.append(sb)
		else:
			

		return res, map_key

	def live_encode(self, data, mn=None):
		res = []
		map_key = {}
		update_keys = {}
		sb_count = Counter(data)
		self.matrix_R = self.matrix_I.copy()

		for up_key in sb_count:
			update_keys[up_key] = [sb_count[up_key], random.randint(1, sb_count[up_key])]

		if mn is None:
			for i in data:
				res.append(self.matrix_I[mn][i])

				if update_keys[i][0] == update_keys[i][1]: 
					res.append(self.gen_keys(self.lkey))
					update_keys[i][0] = -1
				else: update_keys[i][0] = update_keys[i][0] - 1
		else:
			for i in data:
				res.append(self.matrix_I[mn][i])

				if update_keys[i][0] == update_keys[i][1]: 
					res.append(self.gen_keys(self.lkey))
					update_keys[i][0] = -1
				else: update_keys[i][0] = update_keys[i][0] - 1

		print("########", len(update_keys))
		return res

	def static_decode(self, data, mn):
		return [self.matrix_O[mn].get(i) for i in data]

	def static_encode(self, data, mn):
		return [self.matrix_I[mn].get(i) for i in data]

	def load_matrix(self, data):
		...

	def dump_matrix(self, data):
		...

	def load_mdata(self, data):
		return [data[i:i+self.lkey] for i in range(0, len(data), self.lkey)]

	def dump_mdata(self, data):
		return b''.join(data)

	def analyzer(self, text):
		data = set()
		for char in text:
			ch = ord(char)
			for index, i in enumerate(self.unicode_types):
				if i["s"] <= ch <= i["e"]: data.add(index)
		return data

	def gen_keys(self, length):
		return os.urandom(length)

	def gen_auth_key(self):
		random.shuffle(self.auth_key)
		return self.auth_key

	def get_i_matrix(self):
		return self.matrix_I

	def get_o_matrix(self):
		return self.matrix_O

if __name__ == "__main__":
	sess = DDE()

	text = open("test.text", "r").read()


	an = sess.analyzer(text)
	sess.gen_matrix(an)
	d0 = sess.live_encode(text)
	print(d0, "\n")
	d1 = sess.dump_mdata(d0)
	print(d1, "\n")
	d2 = sess.load_mdata(d1)
	print(d2, "\n")
	d3 = sess.live_decode(d2)
	print(d3, "\n")

	tex = ""
	for n in d3[0]:
		if n is not None: tex+=n
	print(tex)

	print("==============")
	print(len(d1), len(text.encode()))
	print('''text'''.encode())