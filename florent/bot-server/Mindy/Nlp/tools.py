from practnlptools.tools import Annotator
import nltk as nl
import re

annotator = Annotator()

def tokenize(string):
    tokens = nl.word_tokenize(string)
    return tokens


def match_pattern_words(sent, pattern):
    pos = [(x, x) for x in (nl.word_tokenize(sent))]
    grammar = pattern
    try:
        cp = nl.RegexpParser(grammar)
        tree = cp.parse(pos)
        units = to_elements(tree)
    except:
        units = []
    return units


def is_match_words(sent, pattern):
    units = match_pattern_words(sent, pattern)
    return len(units) > 0


def to_elements(tree):
    myNE = []
    for c in tree:
        if hasattr(c, 'label'):
            myNE.append((c.label(), ' '.join(i[0] for i in c.leaves())))
    return myNE


def get_verbs(sent):
    verbs = annotator.getAnnotations(sent)['verbs']
    return verbs


def get_objects(sent):
    chunks = annotator.getAnnotations(sent)['chunk']

  #pos = nl.pos_tag(nl.word_tokenize(sent))
    grammar = "NP:{<S-NP>}\n{<B-NP><E-NP>}\n{<B-NP><I-NP>*<E-NP>}"

    cp = nl.RegexpParser(grammar)
    tree = cp.parse(chunks)
    units = to_elements(tree)
    return (units, chunks)


def rectifier(sent):
    #sent = sent.lower()
    sent = sent.replace("how many", "how")
    sent = sent.replace("how much", "how")
#    sent = sent.replace("what", "")
    sent = sent.replace("the ", " ")

    return sent


#extracts objects found inside text
def get_objects_clean(sent):
    units, chuncks = get_objects(rectifier(sent))
    return [x[1] for x in units]


def get_statement_data(sent):
    numbers = re.findall('[0-9]{1,4}', sent)
    quotes = re.findall('(["][^"]+["])', sent)
    phone_numbers = re.findall('([0-9]?\W{1,2}([2-9][0-8][0-9])\W{1,2}([0-9][0-9]{2})\W{1,2}([0-9]{4})(\se?x?t?(\d*)))',sent)
    date = re.findall('([\d]{2}[-./][\d]{2}[-./](20|19)[\d]{2})',sent)
    time = re.findall('([\d]{2}[:][\d]{2}\s{0,2}(pm|am))',sent)
    var = {}
    var["date"] = [x[0] for x in date]
    var["time"] = [x[0] for x in time]



    if len(numbers) > 0:
        var["number"] = numbers[0]
    if len(quotes) > 0:
        var["quote"] = quotes[0]
    if len(phone_numbers) > 0:
        var["phone"] = phone_numbers[0][0]

    return var



def question_type_heur(sent):
    '''heuristic algoritm to determine question type'''

    intent = "statement"
    question_type = "none"
    sent = sent.lower()

    if "?" in sent:
        intent = "question"

    if is_match_words(sent, "QB:{<what>}"):
        question_type = "what"
        intent = "question"

    if is_match_words(sent, "QB:{<when>}"):
        question_type = "when"
        intent = "question"

    if is_match_words(sent, "QB:{<do><you>}\nQB:{<do><i>}\nQB:{<do><we>}"):
        intent = "question"
#        print "q"

    if is_match_words(sent, "QB:{<can><you>}\nQB:{<can><i>}\nQB:{<can><we>}\nQB:{<can><anyone>}"):
        intent = "question"
        #print "q"

    if is_match_words(sent, "QB:{<what><is>}\nQB:{<what><are>}"):
        question_type = "what_is"
        intent = "question"


    if is_match_words(sent, "QB:{<where>}\n"):
        question_type = "where"
        intent = "question"

    if is_match_words(sent, "QB:{<who><are>}\n{<who><is>}"):
        question_type = "who"
        intent = "question"

    if is_match_words(sent, "QB:{<how><are>}\n{<how><is>}"):
        question_type = "how"
        intent = "question"

    if is_match_words(sent, "QB:{<how><long>}"):
        question_type = "how_long"
        intent = "question"

    if is_match_words(sent, "QB:{<how><much>}\n{<what>*<number><of>}\n{<how><many>}\n{<what>*<count><of>}"):  # lint:ok
        question_type = "what_count"
        intent = "question"

    return (intent, question_type)






