from collections import OrderedDict

def replace_multiple_word(my_sentence, replace_words):
    for i, j in replace_words.items():
        my_sentence = my_sentence.replace(i, j)
    return my_sentence

replace_words = OrderedDict([("\xe0", "LOL"), ("dog", "INU"), ("duck", "AHIRU")])
mySentence = "This is my cat and this is my dog and THIS is my duck."
new_sentence = replace_multiple_word(mySentence, replace_words)
print(new_sentence)


