from nltk.tokenize import regexp_tokenize
import nltk
import numpy as np
import os
import sys
import random
from collections import Counter
from collections import defaultdict


def unique(lst):
    x = np.array(lst)
    return np.unique(x)


def markov_chains(b):
    dw = defaultdict(dict)
    freq_counter = Counter(b)
    for elem in b:
        head = elem[0] + " " + elem[1]
        tail = elem[2]
        n = freq_counter[elem]
        dw[head][tail] = n
    return dw


def prediction(word, dictionary):
    max_counter = 0
    next_word = ""
    for i in dictionary[word]:
        if dictionary[word][i] > max_counter:
            max_counter = dictionary[word][i]
            next_word = i
    return next_word


def get_tails_and_weights(dictionary):
    tails = list()
    weights = list()
    for i in dictionary:
        tails.append(i)
        weights.append(dictionary[i])
    return tails, weights


def good_head(word):
    punctuation_marks = [",", ".", "!", "?"]
    word = word.split()[0]
    return True if word[len(word) - 1] not in punctuation_marks and word[0].isupper() else False


def main():
    end_marks = [".", "?", "!"]
    if sys.platform.startswith('win32'):
        file_name = os.path.basename(input())
        file_path = os.getcwd() + "\\test\\" + file_name
    else:
        file_path = os.getcwd() + "/" + input()
    corpus = open(file_path, "r", encoding="utf-8")
    tokens = regexp_tokenize(corpus.read(), "[^ \t\n\r\f\v]+")
    # all_tokens = len(tokens)
    # unique_tokens = len(unique(tokens))
    trigrams = list(nltk.trigrams(tokens))
    dictionary = markov_chains(trigrams)
    heads = [i for i in dictionary if good_head(i)]
    sentences = list()

    for _ in range(10):
        random.seed()
        rand_word = "none"
        sentence = list()
        counter = 0

        while True:
            if len(sentence) == 0:
                rand_word = random.choice(heads)
                sentence.append(rand_word)
            tails, weights = get_tails_and_weights(dictionary[rand_word])
            next_word = random.choices(tails, weights=weights, k=1)[0]
            sentence.append(next_word)
            if len(sentence) >= 4 and next_word[len(next_word) - 1] in end_marks:
                break
            # sentence.append(prediction(rand_word, dictionary))
            rand_word = rand_word.split()[1] + " " + next_word
            counter += 1
            if counter > 100:
                sentence = list()
        sentences.append(" ".join(sentence))

    for i in range(10):
        print(sentences[i])

    '''
    print("Number of bigrams:", len(bigrams))
    print(f"Corpus statistics\n"
         f"All tokens: {all_tokens}\n"
         f"Unique tokens: {unique_tokens}")

    while True:
        ui = input()
        if ui == "exit":
            break
        if ui.isdigit() or ui[1:].isdigit():
            ui = int(ui)
            if ui <= all_tokens:
                print(f"Head: { bigrams[ui][0]} Tail: { bigrams[ui][1]}")
            else:
                print("Index Error. Please input an integer that is in range of the corpus.")
        elif isinstance(ui, str):
            dictionary = markov_chains(bigrams)
            if ui in dictionary:
                print(f"Head: {ui}")
                for i in dictionary[ui]:
                    print(f"Tail: {i} Count: {dictionary[ui][i]}")
            else:
                print(f"Head: {ui}")
                print("The requested word is not in the model. Please input another word.")
        else:
            print("Type Error. Please input an integer")
    '''


if __name__ == "__main__":
    main()
