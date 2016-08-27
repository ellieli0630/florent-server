from practnlptools.tools import Annotator
import nltk as nl
import re
import datetime
import dateparser
import time as t

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
    # if len(units) > 0:
    #     print "units", units
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
    # print "chunks", chunks
    for chunk in chunks:
        if chunk[0] == 'get' and chunk[1] == 'B-NP':
            # print chunk
            pos = chunks.index(chunk)
            chunks.remove(chunk)
            chunk = ('get', 'S-VP')
            # print chunk
            chunks.insert(pos, chunk)
        if len(chunks) == 2 and chunk[1] == 'E-NP':
            # print chunk
            item = chunk[0]
            pos = chunks.index(chunk)
            chunks.remove(chunk)
            chunk = (item, 'S-NP')
            # print chunk
            chunks.insert(pos, chunk)
    #pos = nl.pos_tag(nl.word_tokenize(sent))

    # print "chunks", chunks
    grammar = "NP:{<S-NP>}\n{<B-NP><E-NP>}\n{<B-NP><I-NP>*<E-NP>}"

    cp = nl.RegexpParser(grammar)
    tree = cp.parse(chunks)
    units = to_elements(tree)
    # print "units", units

    return (units, chunks)


def rectifier(sent):
    # print sent
    sent = sent.lower()
    sent = sent.replace("how many", "how")
    sent = sent.replace("how much", "how")
    #    sent = sent.replace("what", "")
    sent = sent.replace("the ", " ")
    sent = sent.replace("yea", "yes")
    sent = sent.replace("sure", "yes")
    sent = sent.replace("tell me", "yes")
    sent = sent.replace("i'd love to", "yes")
    sent = sent.replace("show more", "more")
    sent = sent.replace("show", "get")
    sent = sent.replace("what about", "get")
    # print "rectifier sent", sent

    return sent


#extracts objects found inside text
def get_objects_clean(sent):
    units, chuncks = get_objects(rectifier(sent))
    return [x[1] for x in units]


def date2timestamp(date_string):

    dt = dateparser.parse(date_string)
    timestamp = int(t.mktime(dt.timetuple()))
    return timestamp


def timestamp2date(timestamp):
    string = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return string


def get_statement_data(sent):

    sent=sent.replace("'","\"")
    quotes = re.findall('["]([^"]+)["]', sent)
    if len(quotes)>0:
        sent=sent.replace(quotes[0], " ")
    numbers = re.findall('[0-9]{1,4}', sent)
    phone_numbers = re.findall('([0-9]?\W{0,2}([2-9][0-8][0-9])\W{0,2}([0-9][0-9]{2})\W{0,2}([0-9]{4}))', sent)
    date = re.findall('([\d]{1,2}[-./][\d]{2}[-./](20|19)[\d]{2})', sent)
    time = re.findall('([\d]{1,2}[:][\d]{2}\s{0,2}(pm|am))', sent)
    email = re.findall('[a-z0-9]+[_a-z0-9\.-]*[a-z0-9]+@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})', sent, re.I)
    var = {}
    var["date"] = [x[0] for x in date]
    var["time"] = [x[0] for x in time]

    if len(var["date"]) == len(var["time"]):
        var["datetime"] = []
        for i in range(0, len(var["date"])):
            var["datetime"].append(date2timestamp(var["date"][i] + " " + var["time"][i]))
    else:
        if len(var["date"]) == 1 and (len(var["time"]) > 1):
            var["datetime"] = []
            for i in range(0, len(var["time"])):
                var["datetime"].append(date2timestamp(var["date"][0] + " " + var["time"][i]))

    #print var["datetime"]

    if len(numbers) > 0:
        var["number"] = numbers[0]
    if len(quotes) > 0:
        var["quote"] = quotes[0]
    if len(phone_numbers) > 0:
        var["phone"] = phone_numbers[0][0].strip()
    if len(email) > 0:
        var["email"] = email[0]

    if "|" in sent:
        vars2 = sent.split("|")[1]
        vars2 = vars2.split("=")
        try:
            dta =  date2timestamp(vars2[1].strip())
            var[vars2[0].strip()] = dta
        except:
            var[vars2[0].strip()] = vars2[1].strip()

    #print "vars" + str(var)
     #   print vars2[0],vars2[1]
    #print  (var, sent)

    return (var, sent)



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






