#!/usr/bin/python3

import sys
# import tree

def append_word(tree, word):
	"""ajoute un mot dans l'arbre de préfixes avec son identifiant

	tree: arbre des préfixes (type dict)
	word: mot analysé, en cours d'ajout dans l'arbre (type string)
	"""
	global id_word
	if len(word):
		char = word[0]
		if not (char in tree):
			tree[char] = [{}, 0]
			# si l'identifiant est égal à 0, aucun mot du lexique
			# ne possède cette suite de caractères
		append_word(tree[char][0], word[1:]) # recursion
		if len (word[1:]) == 0:
			tree[char][1] = id_word
			id_word += 1


def make_tree(tree, words, codeToMot):
	"""ajoute chaque mots du lexique dans l'arbre de préfixes

	tree: arbre des préfixes (type dict)
	words: liste des mots à ajouter (type list)
	"""
	for w in words:
		codeToMot[id_word] = w
		append_word(tree, w)



def display_tree(tree, indent=0):
	"""fonction d'afffichage de l'arbre des préfixes
	"""
	for c in tree.keys():
		print("-" * indent + c, end="")
		if tree[c][1] != 0:
			print("-> " + str(tree[c][1]))
		else:
			print("")
		display_tree(tree[c][0], indent + 2)


def open_lexique(path):
	"""
	Ouvre le lexique et stocke tous les mots possibles dans une liste
	"""
	try:
		words_from_lexique = []
		f = open(path, 'r')
		line = f.readline()
		while line != "":
			words_from_lexique.append(line.strip().split()[0].strip())
			line = f.readline()
		return words_from_lexique
	except:
		exit("Le fichier " + path + " n'existe pas!")


def open_corpus(path):
	"""
	Ouvre le corpus, le stocke dans une string et retourne la string.
	"""
	try:
		f = open(path, 'r')
		stream = f.read()
		return stream
	except:
		exit("Le fichier " + path + " n'existe pas!")

def analyse_corpus(corpus, tree, flags):
	"""
	Récupère les mots du corpus.
	"""
	words_from_corpus = []
	separators = [',', ';', '.', '?', '!', ':', "EOF", " ", "BOF", "\n", "\t"]
	last_word = 0
	index_last_word = 0

	if corpus[-1] not in separators:
		corpus += "."

	index_char = 0
	subtree = tree
	while index_char < len(corpus):
		char = corpus[index_char]
		if index_char < (len(corpus) - 1):
			next_char = corpus[index_char + 1]
		else:
			next_char = "EOF"
		if index_char == 0:
			previous_char = "BOF"
		else:
			previous_char = corpus[index_char - 1]
		if char in subtree: #si le préfixe a des descendants
			#~ print("known = " + char)
			if subtree[char][1] != 0 and (next_char in separators):
				#si le préfixe est une fin de mot et le caractère suivant est un separateur fort
				last_word = subtree[char][1] # on enregistre le dernier mot
				index_last_word = index_char # on enregistre la position de la fin du dernier mot
				subtree = subtree[char][0] # on avance dans l'arbre
				index_char += 1 # on avance dans le corpus


			elif subtree[char][1] != 0 and char == "'" and next_char in tree:
				words_from_corpus.append(subtree[char][1])
				last_word = 0
				index_last_word = 0
				subtree = tree
				index_char += 1

			else:
				subtree = subtree[char][0] # on avance dans l'arbre
				index_char += 1 # on avance dans le corpus



		# vérifie que l'espace n'est pas un espace de liaison (ex: pomme de terre)
		elif char == " " and "_" in subtree and next_char in subtree["_"][0]:
			#~ print("espace = " + char)
			char = "_"
			if subtree[char][1] != 0 and next_char in separators: #si le préfixe est une fin de mot
				last_word = subtree[char][1]
				index_last_word = index_char
			subtree = subtree[char][0]
			index_char += 1

		elif char in separators:
				if previous_char not in separators:
					if "-i" in flags and last_word == 0:
						pass
					else:
						words_from_corpus.append(last_word)
				index_char += 1
				#~ print("separateur = " + char)
				index_last_word = 0 # a modifier?
				last_word = 0
				subtree = tree
		else:
			#~ print("unknown = " + char, end="")
			while (index_char < len(corpus)) and (corpus[index_char] not in separators):
				index_char += 1
				#~ print(corpus[index_char], end="")
			#~ print("")
			if "-i" not in flags:
				words_from_corpus.append(0)
			subtree = tree
			index_char += 1
	return words_from_corpus

def displayWordsOfCorpus(words_from_corpus, codeToMot):
	for word in words_from_corpus:
		try:
			print(str(word) + " -> " + codeToMot[word])
		except:
			print(word)
			continue



if __name__ == "__main__":
	help = """tokenizer.py - Auteur: Luc Giffon

Utilisation:
  python3 tokenize.py <lexique path> <corpus path> [-flag]

  Attention: sys.argv est utilisé pour parser les arguments. Les arguments doivent être dans le bon ordre. De plus,
  les options prennant un argument doivent être utilisées avec le symbole "=" et sans espace.

Options:
  -h                    Affiche ce message d'aide
  -dtree                Affiche l'arbre lexicographique
  -dcorpus              Affiche les mots du corpus
  -i                    Ignore les mots inconnus

  --dumptree=<path>     Ecris l'arbre lexicographique
  --dumpcorpus=<path>   Ecris les codes des mots du corpus
"""
	possible_flags = ["-h", "-dtree", "-dcorpus", "-i"]
	possible_options = ["--dumptree", "--dumpcorpus"]

	if ("-h" in sys.argv or len(sys.argv) < 3):
		exit(help)

	lexiquePath = sys.argv[1]
	corpusPath = sys.argv[2]
	flags = {}
	if (len(sys.argv) > 3):
		for flag in sys.argv[3:]:
			flag = flag.split('=')
			if flag[0] in possible_flags:
				flags[flag[0]] = True
			elif flag[0] in possible_options:
				flags[flag[0]] = flag[1]

			else:
				exit("\n\t/_\\ /_\\ /_\\ ERREUR: " + flag[0] + " est inconnu! /_\\ /_\\ /_\\\n\n" + help )


	print("Construction de l'arbre lexicographique:", end = " ")
	words_from_lexique = open_lexique(lexiquePath)

	id_word = 1
	tree = {}
	codeToMot = {}
	make_tree(tree, words_from_lexique, codeToMot)
	if ("-dtree" in flags):
		print("")
		display_tree(tree)
	print("Arbre lexicographique construit")



	print("Lecture du corpus:", end = " ")
	corpus = open_corpus(corpusPath)
	words_from_corpus = ["START"] + analyse_corpus(corpus, tree, flags) + ["STOP"]


	if ("-dcorpus" in flags):
		print("")
		displayWordsOfCorpus(words_from_corpus, codeToMot)
	print("Lecture du corpus terminée")

	if ("--dumptree" in flags):
		f = open(flags["--dumptree"], 'w')
		f.write(str(tree))
		f.close()

	if ("--dumpcorpus" in flags):
		f = open(flags["--dumpcorpus"], 'w')
		f.write(str(words_from_corpus))
		f.close()