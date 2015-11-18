#!/usr/bin/python3

import math
import sys

def perplexity(sequence, probs):
	sum_probs = 0
	length_sequence = len(sequence)
	i = 1
	while i < length_sequence:
		sum_probs += probs[(sequence[i], sequence[i-1])]
		i += 1
	return (sum_probs / (length_sequence + 1))

def smooth_prob_digrams(d_probs_digrams, d_probs_unigrams):
	coefficient = [0.9, 0.09, 0.01]
	smooth_probs_digrams = {}
	for digram in d_probs_digrams:
		smooth_probs_digrams[digram] = (coefficient[0] * d_probs_digrams[digram] +
										coefficient[1] * d_probs_unigrams[digram[0]] +
										coefficient[2])
	return smooth_probs_digrams

def display_probs(probs):
	"""
	Affiche la probabilité d'un élément
	"""
	for prob in probs:
		print(str(prob) + " -> " + str(probs[prob]))

def displayWordsOfCorpus(words_from_corpus, codeToMot):
	for word in words_from_corpus:
		try:
			print(str(word) + " -> " + codeToMot[word])
		except:
			print(word)
			continue

if __name__ == "__main__":

	help = """perplexity.py - Auteur: Luc Giffon

  Programme qui prend en entrée un modèle de langage calculé avec le programme précédent et un texte (tokenizé + code) et retourne la valeur de perplexité du modèle sur ce texte.

Utilisation:

  python3 perplexity.py <texte tokenizé path> | --sequence=<sequence> <modèle digrammes> <modèle unigrammes> [-option]

  Attention: sys.argv est utilisé pour parser les arguments. Les arguments doivent être dans le bon ordre. De plus, les options prenant un argument doivent être utilisées avec le symbole "=" et sans espace.
  Une la séquence doit être formatée comme [1,2,3] et non pas [1, 2, 3].

Options:
  -h                    Affiche ce message d'aide
  -dperp                Affiche les probabilités des unigrammes

  --dumperp=<path>      Ecris la perplexité de la séquence
  --dcode=<path>        Ecris le code de la séquence avec ses mots suivant une table du code
"""
	possible_flags = ["-h", "-dperp"]
	possible_options = ["--dumperp", "--dcode"]

	if ("-h" in sys.argv or len(sys.argv) < 3):
		exit(help)

	sequencePath = None
	sequence = None
	if len(sys.argv[1].split('=')) == 1:
		sequencePath = sys.argv[1]
	else:
		try:
			sequence = eval(sys.argv[1].split('=')[1])
		except SyntaxError:
			exit("Format de séquence invalide: " + sys.argv[1].split('=')[1])

	probs_digrams_path = sys.argv[2]
	probs_unigrams_path = sys.argv[3]

	flags = {}
	if (len(sys.argv) > 4):
		for flag in sys.argv[4:]:
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

	if sequence is None:
		sequence = []
		print("Chargement de la séquence:", end = " ")
		try:
			f = open(sequencePath, 'r')
			try:
				sequence = eval(f.read())
			except:
				exit("Le fichier " + sequencePath + " est invalide et ne peut pas être utilisé comme texte.")
			f.close()
		except FileNotFoundError:
			exit("Le fichier " + sequencePath + " n'existe pas!")

	if "--dcode" in flags:
		f = open(flags["--dcode"], 'r')
		try:
			codeToMot = eval(f.read())
		except SyntaxError:
			exit("Le fichier " + flags["--dcode"] + " est invalide et ne peut pas être utilisé comme table de décodage.")
		f.close()
		displayWordsOfCorpus(sequence, codeToMot)
	print("Séquence chargée")

	probs_digrams = {}
	print("Chargement des probabilités des digrammes")
	try:
		f = open(probs_digrams_path)
		try:
			probs_digrams = eval(f.read())
		except SyntaxError:
			exit("Le fichier " + probs_digrams_path + " est invalide et ne peut pas être utilisé comme modèle.")
		f.close()
	except FileNotFoundError:
		exit("Le fichier " + probs_digrams_Path + " n'existe pas!")
	print("Probabilités des digrammes chargées")

	probs_unigrams = {}
	print("Chargement des probabilités des unigrammes")
	try:
		f = open(probs_unigrams_path)
		try:
			probs_unigrams = eval(f.read())
		except SyntaxError:
			exit("Le fichier " + probs_unigrams_path + " est invalide et ne peut pas être utilisé comme modèle.")
		f.close()
	except FileNotFoundError:
		exit("Le fichier " + probs_unigrams_path + " n'existe pas!")
	print("Probabilités des unigrammes chargées")




	if False:
	# --- probabilité d'une séquence --- #

		#~ print("Probabilité d'une séquence:")
		sequence_fr = "Marie-Antoinette"
		#~ words_from_sequence_fr = analyse_corpus(sequence_fr, tree_fr)
		#~ print("Sequence française: " + str(words_from_sequence_fr))

		#~ perplexite_fr = perplexity(words_from_sequence_fr, probs_digrams_fr)
		#~ print("Perplexité de la séquence française: " + str(perplexite_fr))

		#~ smooth_prob_digrams_fr = smooth_prob_digrams(probs_digrams_fr, probs_unigram_fr)
		#~ smooth_perplexite_fr = perplexity(words_from_sequence_fr, smooth_prob_digrams)
		#~ print("Smooth_perplexité de la séquence française: " + str(smooth_perplexite_fr))
		#~ print("")


		sequence_en = "Marie-Antoinette"
		#~ words_nom_sequence_en = analyse_corpus(sequence_en, tree_en)
		#~ print("Sequence Anglaise: " + str(words_enom_sequence_en))

		#~ perplexite_en = perplexity(words_nom_sequence_en, probs_digrams_en)
		#~ print("Perplexité de la séquence anglaise: " + str(perplexite_en))

		#~ smooth_prob_digrams_en = smooth_prob_digrams(probs_digrams_en, probs_unigram_en)
		#~ smooth_perplexite_en = perplexity(words_nom_sequence_en, smooth_prob_digrams)
		#~ print("Smooth_perplexité de la séquence anglaise: " + str(smooth_perplexite_en))
		#~ print("")

		#~ print("")
