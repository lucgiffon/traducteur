#!/usr/bin/python3

import math
import sys

def calc_smooth_perplexity(sequence, probs_unigrams, probs_digrams):
	"""Calcule la perplexité du modèle

	:param sequence:
	:param probs_unigrams:
	:param probs_digrams:
	:return:
	"""
	sum_probs = 0
	length_sequence = len(sequence)
	i = 1
	while i < length_sequence:
		if (sequence[i], sequence[i-1]) in probs_digrams:
			sum_probs += probs_digrams[(sequence[i], sequence[i-1])]
		elif sequence[i] in probs_unigrams:
			sum_probs += probs_unigrams[sequence[i]] + 5
		else:
			sum_probs += 20
		i += 1
	return (sum_probs / (length_sequence))

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
  -u                    Calcule la perplexité pour le modèle unigramme
  -d                    Calcule la perplexité pour le modèle digramme

  --dumperp=<path>      Ecris la perplexité de la séquence
  --dcode=<path>        Affiche le code de la séquence avec ses mots suivant une table du code
"""
	possible_flags = ["-h", "-u", "-d"]
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
	if ("-d" in flags or "-u" not in flags):
		print("Chargement des probabilités des digrammes")
		try:
			f = open(probs_digrams_path)
			try:
				probs_digrams = eval(f.read())
			except SyntaxError:
				exit("Le fichier " + probs_digrams_path + " est invalide et ne peut pas être utilisé comme modèle.")
			f.close()
		except FileNotFoundError:
			exit("Le fichier " + probs_digrams_path + " n'existe pas!")
		print("Probabilités des digrammes chargées")

	probs_unigrams = {}
	if ("-u" in flags or "-d" not in flags):
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


	print("Calcul de la perplexité de la séquence:", end = " ")
	perplexite = calc_smooth_perplexity(sequence, probs_unigrams, probs_digrams)
	print("Perplexité = " + str(perplexite))

	if ("--dumperp" in flags):
		if (flags["--dumperp"] == ""):
			flags["--dumperp"] = "perplexity"
		f = open(flags["--dumperp"], 'w')
		f.write(str(perplexite))
		f.close()