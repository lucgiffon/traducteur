#!/usr/bin/python3

import math
import sys

def count_unigram_from_corpus(words):
	"""
	Récupère les nombres d'occurence de chaque mot.
	"""
	counted_unigrams = {}
	for word in words:
		if word not in counted_unigrams:
			counted_unigrams[word] = 1
		else:
			counted_unigrams[word] += 1
	return counted_unigrams

def prob_unigrams(counted_unigrams, number_words):
	"""
	Récupère la fréquence d'occurence de chaque mot.
	"""
	prob_unigrams = {}
	for word in counted_unigrams:
		prob_unigrams[word] = -(math.log((counted_unigrams[word] / number_words), 10))
	return prob_unigrams

def count_digrams_from_corpus(words_from_corpus, number_words):
	"""
	Récupère le nombre d'occurence de doublets de mots.
	"""
	counted_digrams = {}
	i= 1
	while i < number_words:
		if (words_from_corpus[i], words_from_corpus[i-1]) not in counted_digrams:
			counted_digrams[(words_from_corpus[i], words_from_corpus[i-1])] = 1
		else:
			counted_digrams[(words_from_corpus[i], words_from_corpus[i-1])] += 1
		i += 1
	return counted_digrams

def prob_digrams(counted_digrams, counted_unigrams):
	"""
	Récupère la fréquence d'occurence de chaque doublet.
	"""
	prob_digrams = {}
	for digram in counted_digrams:
		prob_digrams[digram] = -(math.log((counted_digrams[digram] / counted_unigrams[digram[1]]), 10))
	return prob_digrams

def display_probs(probs):
	"""
	Affiche la probabilité d'un élément
	"""
	for prob in probs:
		print(str(prob) + " -> " + str(probs[prob]))

if __name__ == "__main__":

	help = """model.py - Auteur: Luc Giffon

Utilisation:

  Programme qui prend en entrée un texte tokenizé, traduit en code, et retourne un modèle de langage avec les probabilités (exprimées en -logprob) de chaque unigramme et chaque bigramme du texte d'entrée

  python3 model.py <corpus tokenizé path> [-option]

  Attention: sys.argv est utilisé pour parser les arguments. Les arguments doivent être dans le bon ordre. De plus, les options prenant un argument doivent être utilisées avec le symbole "=" et sans espace.

Options:
  -h                    Affiche ce message d'aide
  -dprobsu              Affiche les probabilités des unigrammes
  -dprobsd              Affiche les probabilités des digrammes

  --dumpuni=<path>      Ecris les probabilités des unigrammes
  --dumpdi=<path>       Ecris les probabilités des digrammes
"""
	possible_flags = ["-h", "-dprobsu", "-dprobsd"]
	possible_options = ["--dumpuni", "--dumpdi"]

	if ("-h" in sys.argv or len(sys.argv) < 2):
		exit(help)

	corpusPath = sys.argv[1]
	flags = {}
	if (len(sys.argv) > 2):
		for flag in sys.argv[2:]:
			flag = flag.split('=')
			if flag[0] in possible_flags:
				flags[flag[0]] = True
			elif flag[0] in possible_options:
				try:
					flags[flag[0]] = flag[1]
				except:
					flags[flag[0]] = ""
			else:
				exit("\n\t/_\\ /_\\ /_\\ ERREUR: " + flag[0] + " est inconnu! /_\\ /_\\ /_\\\n\n" + help )

	words_from_corpus = []
	try:
		f = open(corpusPath, 'r')
		words_from_corpus = eval(f.read())
		f.close()
	except FileNotFoundError:
		exit("Le fichier " + corpusPath + " n'existe pas!")

	number_words = len(words_from_corpus)

	print("Calcul de la probabilité des unigrammes:",  end = " ")

	counted_unigrams = count_unigram_from_corpus(words_from_corpus)
	probs_unigram = prob_unigrams(counted_unigrams, number_words)

	if ("-dprobsu" in flags):
		print("")
		display_probs(probs_unigram)

	print("Calcul de la probabilité des unigrammes terminé")


	print("Calcul de la probabilité des digrammes:",  end = " ")
	counted_digrams = count_digrams_from_corpus(words_from_corpus, number_words)
	probs_digrams = prob_digrams(counted_digrams, counted_unigrams)

	if ("-dprobsd" in flags):
		print("")
		display_probs(probs_digrams)

	print("Calcul de la probabilité des digrammes terminé")

	if ("--dumpuni" in flags):
		if (flags["--dumpuni"] == ""):
			flags["--dumpuni"] = "unigrams"
		f = open(flags["--dumpuni"], 'w')
		f.write(str(probs_unigram))
		f.close()

	if ("--dumpdi" in flags):
		if (flags["--dumpdi"] == ""):
			flags["--dumpdi"] = "digrams"
		f = open(flags["--dumpdi"], 'w')
		f.write(str(probs_digrams))
		f.close()