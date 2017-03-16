import fileinput
import json
import re

def calculate_network():
    # for query in qs:
    #     if '|' in query:
    #         prior, cond = query.split('|')
    #         if query in net[prior[1:]].keys():
    #             answers.append(net[prior[1:]][query])
    #         else:
    #             answers.append('falta calcular')            
    #     else:
    #         if query in net[query[1:]].keys():
    #             answers.append(net[query[1:]][query])
    #         else:
    #             answers.append('falta calcular')            
    
    
    pass

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


def main():
    answers = []

    net, qs, roots = read_input()

    calculate_network()

    print(roots)    
    print(json.dumps(net,indent=2))    
    for a in answers: print(a)


if __name__ == '__main__':
    main()
