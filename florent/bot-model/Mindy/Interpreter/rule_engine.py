from ..Nlp import tools as nlt
from ..Graph.basics import Node,NodeList,Graph
from ..Graph.neo4j_graph import PersistentGraph
import json
import traceback
import datetime

main_graph = False


def pdate(timestamp):
    string = datetime.datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return string

def load_rules(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
    return data


def set_main_graph(mg):
    global main_graph
    main_graph = mg


context = {}


def get_user_context(user_id):
    if user_id in context:
        context_user = context[user_id]
    else:
        context[user_id] = {}
        context_user = context[user_id]
    return context_user


def set_user_context(user_context, user_id):
    context[user_id] = user_context


def clean_context(user_id):
    context[user_id] = {}


def get_debug_info(sent):
    sent_objects = nlt.get_objects_clean(sent)
    s = ""
    debug_info = []
    for x in sent_objects:
        s = s + x + ","
    debug_info.append("objects = " + s)
    return debug_info


def partial_match(obj, sent_object):
    tokens1 = nlt.tokenize(obj.lower())
    tokens2 = nlt.tokenize(sent_object.lower())
    obj_last = tokens1[-1]
    sent_last = tokens2[-1]
    return obj_last == sent_last


def partial_match_sent(obj, sent_object):

    return (sent_object.lower()).endswith(obj.lower())



def ci_match(obj, obj_lst):
    is_in_list = False
    matched_obj = ""
    for x in obj_lst:
        if partial_match_sent(obj, x):  # x.lower() == obj.lower():
            is_in_list = True
            matched_obj = x
    return is_in_list, matched_obj


def match_objects(rule_objects, sent_objects):
    matched = True
    unmatched_sent_objects = list(sent_objects)
    #sent_objects = [x.lower() for x in sent_objects]
    matched_objects = {}

    #match exact objects
    for x in rule_objects:
        #if (ci_match(x,sent_objects)) and not x.istitle() :
        ismatch,mobj = ci_match(x,sent_objects)
        if (not (ismatch)) and (not x.istitle()) :
            matched = False

        else:
            if ismatch:
                unmatched_sent_objects.remove(mobj)

   #match objects with unbound variables
    for x in rule_objects:
        if x.istitle():
            #print ("ubount1")
            if len(unmatched_sent_objects) > 0:
                matched_objects["$" + x] = unmatched_sent_objects[0]
                #print (x + " = " + str(matched_objects["$" + x]))

               # print  x, matched_objects[x]
                unmatched_sent_objects.remove(unmatched_sent_objects[0])
            else:
                matched = False

    return (matched, matched_objects)


def pattern_replace(template, bound_vars):
    for x in bound_vars:
        template = template.replace(str(x), str(bound_vars[x]))
    return template


def gen_answer_template(answer_template, bound_vars):
    tokens = answer_template.split(" ")
    new_tokens = []
    #print (bound_vars)
    for x in tokens:
        if  x in bound_vars:
           # print(bound_vars[x])
            new_tokens.append(str(bound_vars[x]))
        else:
            new_tokens.append(x)
    return " ".join(new_tokens)

def match(match_statements,sent, graph_data):

    proc = True
    action_vars = {}
    for statement in match_statements:
        act = statement.split("<-")
        if len(act) > 1:
            act_statement = act[1]
        else:
            act_statement = act[0]
        try:
            result = eval(act_statement)
            if len(act)>1:
                action_vars[act[0].strip()] = (result)
        except Exception as inst:
       #    print(type(inst))
        #   print(inst.args)
         #  print(inst)
          # traceback.print_exc()
           proc=False

    return (proc,action_vars)


def check_rule(rule, sent, objects, graph_vars):
    conditions = rule["conditions"]
    checked = True
    bound_vars = {}
    #print "check"
    if "verbs" in conditions:
        #print "1"
        cond_verbs = conditions['verbs']
        sent_verbs = nlt.get_verbs(sent)
        for x in cond_verbs:
            if not x in sent_verbs:
                checked = False
    #print (objects)
    if "objects" in conditions:
        #print "2"
        ismatched, matched = (match_objects(conditions['objects'], objects))
        checked = checked and ismatched
        bound_vars.update(matched)

    if "intent" in conditions:
        #print "3"
        sent_intent, sent_qtype = nlt.question_type_heur(sent)
        cond_intent = conditions['intent']
        if cond_intent != sent_intent:
            checked = False

    if "question_type" in conditions:
            #print "4"
            sent_intent, sent_qtype = nlt.question_type_heur(sent)
            cond_intent = conditions['question_type']
            if cond_intent != sent_qtype:
                checked = False

    if "pattern" in conditions:
            #print "4"
            if not nlt.match_pattern_words(sent, conditions["pattern"]):
                checked = False

    if "match" in conditions and checked:
        #print "5"
        #print "found match"
        mproc, newvars = match(conditions["match"], sent, graph_vars)
        if not mproc:
            checked = False
        else:
            bound_vars.update(newvars)
           # print bound_vars

    return (checked, bound_vars)


def add_context(rule, user_id):
  if "store" in rule:
    store_data = rule['store']
    context = get_user_context(user_id)
    new_context = {}
   # print ("ho")
    for vartype in store_data:
        if vartype in context:
            cont_var_type = context[vartype]
            data = store_data[vartype]
            cont_var_type.update(data)
            new_context[vartype] = cont_var_type
        else:
            new_context[vartype] = set(store_data[vartype])
            #print (new_context)
    #print (new_context)
    set_user_context(new_context, user_id)


def process_action(actions, current_vars):
    action_vars = {}
    for action in actions:
        act = action.split("<-")
        if len(act) > 1:
            act_statement = act[1]
        else:
            act_statement = act[0]
        try:
          #  print act_statement
            var = eval(pattern_replace(act_statement, current_vars))
            if len(act) > 1:
                action_vars[act[0].strip()] = var
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            traceback.print_exc()
    #print action_vars
    return action_vars


def get_reply(rules, sent, user_id, graph_vars={}):
    answer = ""
    proc = False
    objects = nlt.get_objects_clean(sent)
    graph_vars.update(nlt.get_statement_data(sent))
    new_vars={}

    for rule in rules:
        #print "rule in rules"
        match, bound_vars = check_rule(rule, sent, objects, graph_vars)
        if match:
            #print "match"
            #process action statements
            if "action" in rule:
                #print "one two"
                new_vars = process_action(rule["action"], bound_vars)
                #print new_vars
                bound_vars.update(new_vars)
            if "answer" in rule:
                #print "one two three"
                clean_context(user_id)
                answer = gen_answer_template(rule["answer"], bound_vars)
                break
            add_context(rule, user_id)
            proc = True

    if not proc:
        local_context = get_user_context(user_id)
        #print "not proc"
      #print ("current" + str(local_context))
        if len(local_context) > 0:
            objects = objects + list(local_context['objects'])
            #print "dlina nanana"
            for rule in rules:
                match, bound_vars = check_rule(rule, sent, objects)
                if match:
                    #print "if match"
                    if "answer" in rule:
                        answer = gen_answer_template(rule["answer"], bound_vars)
                    clean_context(user_id)
                    add_context(rule, user_id)
                    proc = True


    return answer, new_vars


