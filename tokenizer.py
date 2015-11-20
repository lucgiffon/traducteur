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
    index_last_word_saved = 0
    id_unknown = -1
    code_unknown = {}

    if len(corpus) > 0:

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
                        if last_word != 0:
                            words_from_corpus.append(last_word)
                            index_last_word_saved = index_last_word
                        elif "-i" in flags:
                            pass
                        else:
                            words_from_corpus.append(id_unknown)
                            code_unknown[id_unknown] = corpus[index_last_word_saved + 1:index_char].strip()
                            id_unknown -= 1
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
                    words_from_corpus.append(id_unknown)
                    code_unknown[id_unknown] = corpus[index_last_word_saved + 1:index_char].strip()
                    id_unknown -= 1
                subtree = tree
                index_char += 1
    return (words_from_corpus, code_unknown)

def displayWordsOfCorpus(words_from_corpus, codeToMot, unknown):
    for word in words_from_corpus:
        try:
            print(str(word) + " -> " + codeToMot[word])
        except:
            if type(word) == str:
                print("ok ->" + word)
            else:
                print(str(word) + " -> " + unknown[word])
            continue



if __name__ == "__main__":
    help = """tokenizer.py - Auteur: Luc Giffon

Utilisation:
  Programme qui prend en entrée un texte et un lexique avec code et qui retourne le texte tokenizé selon le lexique, avec les mots remplacés par des codes.

  python3 tokenize.py <lexique path> | --loadtree=<path> <corpus path> | --text=<texte> [-option]

  Attention: sys.argv est utilisé pour parser les arguments. Les arguments doivent être dans le bon ordre. De plus, les options prenant un argument doivent être utilisées avec le symbole "=" et sans espace.

Options:
  -h                    Affiche ce message d'aide
  -dtree                Affiche l'arbre lexicographique
  -dcorpus              Affiche les mots du corpus
  -i                    Ignore les mots inconnus

  --dumpunknowns=<path> Ecris les codes des mots inconnus du corpus
  --dumptree=<path>     Ecris l'arbre lexicographique
  --dumpcorpus=<path>   Ecris les codes des mots du corpus
"""
    possible_flags = ["-h", "-dtree", "-dcorpus", "-i"]
    possible_options = ["--dumptree", "--dumpcorpus", "--dumpunknowns"]

    if ("-h" in sys.argv or len(sys.argv) < 3):
        exit(help)

    lexiquePath = None
    treePath = None
    if len(sys.argv[1].split('=')) == 1:
        lexiquePath = sys.argv[1]
    else:
        treePath = sys.argv[1].split('=')[1]

    corpus = None
    corpusPath = None
    if len(sys.argv[2].split('=')) == 1:
        corpusPath = sys.argv[2]
    else:
        corpus = sys.argv[2].split('=')[1]

    flags = {}
    if (len(sys.argv) > 3):
        for flag in sys.argv[3:]:
            flag = flag.split('=')
            if flag[0] in possible_flags:
                flags[flag[0]] = True
            elif flag[0] in possible_options:
                try:
                    flags[flag[0]] = flag[1]
                except IndexError:
                    flags[flag[0]] = ""

            else:
                exit("\n\t/_\\ /_\\ /_\\ ERREUR: " + flag[0] + " est inconnu! /_\\ /_\\ /_\\\n\n" + help )

    if lexiquePath is not None:
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
    else:
        print("Récupération de l'arbre lexicographique:", end = " ")
        try:
            f = open(treePath, 'r')
            tree = eval(f.read())
            f.close()
            print("Arbre lexicographique récupéré")
        except FileNotFoundError:
            exit("Le fichier " + treePath + " n'existe pas!")

        print("Récupération du code lexical:", end = " ")
        try:
            f = open(treePath + "_code", 'r')
            codeToMot = eval(f.read())
            f.close()
            print("Code lexical récupéré")
        except FileNotFoundError:
            exit("Le fichier " + treePath + "_code" + " n'existe pas!")


    print("Lecture du corpus:", end = " ")
    if corpus is None:
        corpus = open_corpus(corpusPath)

    (knowns, unknowns) = analyse_corpus(corpus, tree, flags)
    words_from_corpus = ["START"] + knowns + ["STOP"]

    if ("-dcorpus" in flags):
        print("")
        displayWordsOfCorpus(words_from_corpus, codeToMot, unknowns)
    print("Lecture du corpus terminée")

    if ("--dumptree" in flags):
        if (flags["--dumptree"] == ""):
            flags["--dumptree"] = "tree"
        f = open(flags["--dumptree"], 'w')
        f.write(str(tree))
        f.close()
        f = open(flags["--dumptree"] + "_code", 'w')
        f.write(str(codeToMot))
        f.close()

    if ("--dumpcorpus" in flags):
        if (flags["--dumpcorpus"] == ""):
            flags["--dumpcorpus"] = "tokenized"
        f = open(flags["--dumpcorpus"], 'w')
        f.write(str(words_from_corpus))
        f.close()

    if ("--dumpunknowns" in flags):
        if (flags["--dumpunknowns"] == ""):
            flags["--dumpunknowns"] = "unknowns"
        f = open(flags["--dumpunknowns"], 'w')
        f.write(str(unknowns))
        f.close()
