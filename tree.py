from nltk.corpus import wordnet as wn
import pickle

class Node():
	def __init__(self, synset = None):
		self.wnetid = synset.pos()+str(synset.offset()).zfill(8)
		self.children = None
		self.all_categories = None
		self.root = False

	def get_synset(self):
		return wn._synset_from_pos_and_offset(str(self.wnetid[0]),int(self.wnetid[1:]))

	def add_child(self, child):
		if(not self.children):
			self.children = [child]
		else:
			self.children.append(child)

##########################################

class Imagenet():
	def __init__(self):
		print "Initialized"

	def read_wnetids(self):
		with open("./synsets.txt", 'r') as f:
			synsets = f.readlines()
		synsets_idx = [i.split()[0] for i in synsets]
		synsets_names = [i.split()[1:] for i in synsets]
		self.wnetids_idx = synsets_idx[1:1001]
		self.wnetids_names = synsets_names[1:1001]
		self.wnetids_to_synsets()

	def offset_to_synset(self, offset):
		return wn._synset_from_pos_and_offset(str(offset[0]),int(offset[1:])) 

	def synset_to_offset(self, synset):
		return synset.pos()+str(synset.offset()).zfill(8)

	def wnetids_to_synsets(self):
		all_parents = []
		self.synsets = [self.offset_to_synset(wnetid) for wnetid in self.wnetids_idx]

	def iterate_through_list(self, synsets):
		new_parents = []
		for synset_1 in synsets:
			for synset_2 in synsets:
				common = synset_1.lowest_common_hypernyms(synset_2)
				if (len(common)>1): 
					for i in common:
						if i not in new_parents:
							new_parents.append(i)
				elif(common[0] not in new_parents): new_parents.append(common[0])
		return new_parents

	def get_all_parents(self):
		self.all_parents = self.synsets

		starting_synset_list = self.synsets
		while(len(starting_synset_list)>1):
			new_list = self.iterate_through_list(starting_synset_list)
			next_elems = []
			for elem in new_list:
				if elem not in self.all_parents:
					self.all_parents.append(elem)
					next_elems.append(elem)
			starting_synset_list = next_elems

	def get_children_synsets(self, node):
		for child in node.children:
			print child.get_synset()

	def create_tree(self):
		self.all_nodes = dict()

		for synset in self.all_parents:
			if synset not in self.all_nodes:
				node = Node(synset = synset)
				self.all_nodes[synset] = node	# add 
			else:
				node = self.all_nodes[synset]

			children = synset.hyponyms()
			while(children):
				new_children = []
				for child in children:
					if(child in self.all_parents):
						# check if node exists:
						if child not in self.all_nodes:
							self.all_nodes[child] = Node(synset = child)
						node.add_child(self.all_nodes[child])	
					else:
						new_children.extend(child.hyponyms())
				children = new_children

		assert len(self.all_nodes)==len(self.all_parents)
		self.prune_tree()

	def bfs(self, root, children_to_find):
		# to do
		stack = [root]
		found_children = []
		while(stack):
			new_stack = []
			# iterate through nodes:
			for node in stack:
				# check if has children:
				if(node.children):
					# iterate through children:
					for child in node.children:
						# check if it's one you're looking for:
						if(child in children_to_find):
							if(child not in found_children): found_children.append(child)
						else: new_stack.append(child)
			stack = new_stack
		return found_children

	def bfs_subtree(self, root):
		# to do
		stack = [root]
		found_children = []
		while(stack):
			new_stack = []
			# iterate through nodes:
			for node in stack:
				# check if has children:
				if node.get_synset() in self.synsets and node.wnetid not in found_children:
					found_children.append(node.wnetid)
				if(node.children):
					# iterate through children:
					for child in node.children:
						new_stack.append(child)
			stack = new_stack
		if len(found_children)==0 :
			return None
		else:
			return found_children

	def prune_tree(self):
		children_to_prune = []
		
		for synset, node in self.all_nodes.iteritems():
			#print
			#print synset
			children_to_prune = []
			if( node.children ):
				#print len(node.children)
				for i in xrange(len(node.children)):
					all_children = node.children[:]
					all_children.pop(i)
					child = node.children[i]
					children_to_prune.extend( self.bfs(child, all_children) )
				if(len(children_to_prune)>0):
					print synset, len(children_to_prune)
					children_to_leave = []
					for child in node.children:
						if child not in children_to_prune:
							children_to_leave.append(child)
					node.children = children_to_leave
		

		pickle.dump( [value for value in self.all_nodes.itervalues()], open( "./tree_nodes.p", "wb" ) )

	def load_tree(self):
		nodes = pickle.load( open( "./tree_nodes.p", "rb" ) ) 
		self.all_nodes = dict()
		self.root_node = None
		for i in xrange(len(nodes)):
			self.all_nodes[nodes[i].get_synset()] = nodes[i]
			if(nodes[i].root == True): self.root_node = nodes[i]

	def sanity_check(self):
		print "Sanity check"					
			
		# check if nodes have either 0 (end node) or multiple children:
		for node in self.all_nodes.itervalues():
			if( node.children ):
				if( len(node.children)==1):
					print node.get_synset()
		print "TEST 1 PASSED. No unnecessary nodes"

		# all final categories (and only them) are end nodes:
		self.read_wnetids()
		for node in self.all_nodes.itervalues():
			if ( node.get_synset() not in self.synsets and not node.children):
				print "Error 1", node.get_synset()
			if(node.get_synset() in self.synsets and node.children):
				print "Error 2", node.get_synset()
		print "TEST 2 PASSED. All categories (and only them) are end nodes"

	def find_all_categories_in_each_subtree(self):
		root_node = None
		max_categories = 0
		self.read_wnetids()
		print len(self.synsets)
		print len(self.all_nodes)
		for node in self.all_nodes.itervalues():
			node.all_categories = self.bfs_subtree(node)
			if(node.all_categories):
				n = len(node.all_categories)
				if(n>max_categories):
					print node.get_synset(), n
					max_categories=n
					root_node = node
		print
		print root_node.get_synset(), max_categories
		root_node.root = True
		pickle.dump( [value for value in self.all_nodes.itervalues()], open( "./tree_nodes.p", "wb" ) )

##########################################

imagenet = Imagenet()
'''
imagenet.read_wnetids()
imagenet.get_all_parents()
imagenet.create_tree()
imagenet.prune_tree()
'''
imagenet.load_tree()
#imagenet.find_all_categories_in_each_subtree()
