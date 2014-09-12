from collections import defaultdict
import shelve, gc

class IndexBuilder:
	def __init__ (self):
		self.index = defaultdict(lambda:defaultdict(list))
		gc.disable()
		return

	def build_index(self, file_id, word_list):
		for pos in xrange(0,len(word_list)):
			self.index[word_list[pos]][file_id].append(pos)
		return

	def write_index(self, file_location):
		file_dict = shelve.open(file_location)
		for key,value in self.index.iteritems():
			file_dict[key.encode('utf-8')] = value
		file_dict.close()

	def delete_index(self):
		del self.index
		gc.collect()

	def get_index(self):
		return self.index