import fileinput
import json
import copy
import re


def read_input():
    step = 0
    lines = []
    net = {}
    queries = []
    roots = []

    # Read file input and clean each line
    for line in fileinput.input():
        lines.append(line.strip())
    
    
    for line in lines:
        # Lines that are not comments
        if line and line[0] != '#':
            # Each [Title] from input change of step
            if line[0] == '[':
                step += 1
                continue
            # Input nodes
            if step == 1:
                net = { node.strip():{} for node in line.split(',')}
            # Input Probabilities and initialize graph
            elif step == 2:
                event, prob = line.split('=')
                event, prob = event.strip(), float(prob.strip())
                # If probability is conditional
                if '|' in event:
                    prior, cond = event.split('|')
                    conds = [ c.strip() for c in cond.split(',')]
                    # Add information of parents to the current node 
                    net[prior[1:]]['parents'] = list(map(lambda x: x[1:], conds))
                    # Add information of childs to the parents
                    for c in conds:
                        if 'childs' not in net[c[1:]].keys():
                            net[c[1:]]['childs'] = []
                        if prior[1:] not in net[c[1:]]['childs']:
                            net[c[1:]]['childs'].append(prior[1:])
                    # Save probability of event
                    conds.sort()
                    net[prior[1:]][ (prior + '|' + ','.join(conds)) ] = prob

                # Else probability is indepent, hence a root. Also calculate inverse probability
                # on the tables of each node
                else:
                    roots.append(event[1:])
                    if '+' in event:
                        net[event[1:]][event] = prob
                        net[event[1:]][event.replace('+','-')] = 1 - prob
                    else:
                        net[event[1:]][event] = prob
                        net[event[1:]][event.replace('-','+')] = 1 - prob
            # Input queries and clean them
            elif step == 3:
                queries.append(line.strip())
    return net, queries, roots 

# def child_snowball(ancestor, node):
#     if ancestor in node[]

def get_network_ancestors(net, roots): 
    nodes = copy.deepcopy(roots)
    visited = set()
    str_node = nodes.pop()
    node = net[str_node]
    count = 0
    # net[node]

    while len(nodes) > 0:
        if count < len(roots):
            net[str_node]['ancestors'] = []
        if 'childs' in node.keys():
            for child in node['childs']:
                if 'ancestors' not in net[child].keys():
                    net[child]['ancestors'] = []
                net[child]['ancestors'].extend(node['ancestors'])
                valid = False
                if 'parents' in net[child].keys():
                    if any([True if p in visited else False for p in net[child]['parents']]):
                        valid = True
                if str(child) not in visited:
                    valid = True
                if valid:
                    nodes.append(str(child))
        visited.add(str(node))
        str_node = nodes.pop()
        node = net[str_node]

    # for node in nodes:
        # if 'childs' in net[node].keys():
            # for child in net[root]['childs']:

    # for node in net:
    #     if 'parents' in net[node].keys():
    #         for parent in net[node]['parents']:
    #             neu_node = parent
    #             while 'parents' in net[neu_node]:
                    
    #                 pass
    #             print(parent)


# def calculate_network(net, roots): 
#     for node in net:
#         if 'parents' in net[node].keys():
#             for parent in net[node]['parents']:
#                 neu_node = parent
#                 while 'parents' in net[neu_node]:
                    
#                     pass
#                 print(parent)
#         # print(node)

# def calculate_node(net, node):
#     if 'parents' not in node.keys():
#         return 
    

    # for parent in net[node]['parents']:
    #     neu_node = parent
    # if 'parents' in net[node].keys():
    #             while 'parents' in net[neu_node]:
                    
    #                 pass
    #             print(parent)

def enumerate_algorithm(query):
    result = ''
    for q in query:
        prior,cond = q.split('|')
        print(prior,cond)

    return result

def clean_queries(qs):
    neu_qs = []
    for q in qs:
        if '|' in q:
            prior, cond = q.split('|')
            conds = [c.strip() for c in cond.split(',')]
            conds.sort()
            priors = [p.strip() for p in prior.split(',')]
            temp_priors = []
            for p in priors:
                temp_priors.append(p + '|' + ','.join(conds))
            neu_qs.append(temp_priors)
        else:
            neu_qs.append([q.strip()])
    return neu_qs

def answer_queries(net,qs):
    answers = []
    for queries in qs:
        for query in queries:
            if '|' in query:
                prior, cond = query.split('|')
                if query in net[prior[1:]].keys():
                    answers.append(net[prior[1:]][query])
                else:
                    answers.append('falta calcular')            
            else:
                if query in net[query[1:]].keys():
                    answers.append(net[query[1:]][query])
                else:
                    answers.append('falta calcular')            
    return answers


def main():

    net, qs, roots = read_input()

    # calculate_network(net,roots)

    qs = clean_queries(qs)
    answers = answer_queries(net,qs)

    # print(roots)    
    get_network_ancestors(net, roots)
    print(json.dumps(net,indent=2))    

    # print(enumerate_algorithm(qs[4]))

    # for a in answers: print(a)


if _name_ == '_main_':
    main()
