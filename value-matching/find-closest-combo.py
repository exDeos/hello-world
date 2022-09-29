import logging
import itertools
logging.basicConfig(level=logging.DEBUG)

def smash_it(X,t):
    best= (t,[])
    N= len(X)
    for i in range(len(X)//2):
        left_side_attack= i+1
        right_side_attack= len(X)-i
        Q= itertools.combinations(X,left_side_attack)
        logging.info("Attack Length= {}".format(left_side_attack))
        for k in Q:
            best= check(k,best,t)
        if left_side_attack!=right_side_attack:
            logging.info("Attack Length= {}".format(right_side_attack))
            Q= itertools.combinations(X,right_side_attack)
            for k in Q:
                best= check(k,best,t)
    if len(X)%2==1:
        center_attack= (len(X)+1)//2
        logging.info("Attack Length= {}".format(center_attack))
        Q= itertools.combinations(X,right_side_attack)
        for k in Q:
            best= check(k,best,t)
    return best

def check(k,best,t):
    diff= sum(k)-t
    plug= (diff,list(k))
    if abs(plug[0])<abs(best[0]):
        logging.debug("New Best:\n  Difference: {:.2f}\n  Objects:\n    {}".format(plug[0],"\n    ".join((str(v) for v in plug[1]))))
        best= plug
    return best
