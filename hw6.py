import unittest

def kwiq(word, filename, num = 3):
    '''Find "many-grams" with a special word in the text
    The function search the word and returns it with other 3 words before and
    after this word if it's possible.

    Args:
        word: a word you look for in text
        filename: txt file with a text using for a search
        num: a number of words on the each side of the special word; 3 by default.

    Returns:
        a list of contexts with the special word  
    '''

    arr = []
    file_txt = open(filename, 'r', encoding = 'utf-8-sig').read().split()
    for numb, words in enumerate(file_txt):
        clear_w = words.strip('.,!?;:').lower()
        if clear_w == word:
            arr.append([' '.join(file_txt[numb - num:numb]),words, ' '.join(file_txt[numb + 1:numb + num + 1])])
            
    return arr

def to_table(table):
    """
    transorm words into the kwic format
    Args:
       table: a list of lists
    Returns:
        a special line
    """
    if not table:
        return ''
    maxlenght = max([len(row[0]) for row in table])
    lenght = max([len(row[1]) for row in table])
    result = ''
    for row in table:
        result += row[0] + ' ' * (maxlenght - len(row[0]) + 3) + row[1] + ' ' \
                  *(lenght - len(row[1]) + 3) + row[2] + '\n'
    return result


class Tester(unittest.TestCase):
    def one(self):
        self.assertEqual(kwiq('hi','text.txt'),
                         [['what"s up', 'hi', 'it is me']])
        
    def no_one(self):
        self.assertEqual(kwiq('boss','text.txt'),[])


print(to_table(kwiq('great','text.txt')))
unittest.main()
