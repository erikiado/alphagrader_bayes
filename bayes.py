import fileinput
import json
import re


# class BayesNet(object):

#     def __init__(self):
#         self.nodes = {}
    # bayes = BayesNet()
    # lines = list(map(lambda x: x.strip(), lines))


def read_input():
    step = 0
    lines = []
    net = {}
    queries = []

    for line in fileinput.input():
        lines.append(line.strip())
    
    
    for line in lines:
        if line and line[0] != '#':
            if line[0] == '[':
                step += 1
                continue
            if step == 1:
                net = { node.strip():{} for node in line.split(',')}
            elif step == 2:
                event, prob = line.split('=')
                event, prob = event.strip(), float(prob.strip())
                if '|' in event:
                    prior, cond = event.split('|')
                    conds = [ c.strip() for c in cond.split(',')]
                    net[prior[1:]]['parents'] = list(map(lambda x: x[1:], conds))
                    net[prior[1:]]['root'] = False
                    for c in conds:
                        if 'childs' not in net[c[1:]].keys():
                            net[c[1:]]['childs'] = []
                        if prior[1:] not in net[c[1:]]['childs']:
                            net[c[1:]]['childs'].append(prior[1:])
                    net[prior[1:]][ (prior + '|' + ','.join(conds)) ] = prob
                else:
                    net[event[1:]]['root'] = True
                    if '+' in event:
                        net[event[1:]][event] = prob
                        net[event[1:]][event.replace('+','-')] = 1 - prob
                    else:
                        net[event[1:]][event] = prob
                        net[event[1:]][event.replace('-','+')] = 1 - prob
            elif step == 3:
                queries.append(line.strip())
    return net,queries


def main():
    answers = []
    net, qs = read_input()
    print(json.dumps(net,indent=2))    
    
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
    
    for a in answers: print(a)


if __name__ == '__main__':
    main()
