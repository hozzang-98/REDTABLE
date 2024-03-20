def precision_k(gt, predict, k=10):

    intersection = list(set(gt) & set(predict[:k]))

    return len(intersection) / k

def rel_k(gt, predict, k=10):

    return 1 if predict[k-1] in gt else 0

def evaluate_map(gt, predict, k=10):
    
    ap = 0
    for i in range(1, min(k, len(gt)) + 1):
        
        ap += precision_k(gt, predict, i) * rel_k(gt, predict, i)

    return ap / min(k, len(gt))

def evaluate_recall(gt, predict, k=10):

    intersection = list(set(gt) & set(predict))

    return min(len(intersection) / min(k, len(gt)),1.0)


def tag_based_precision_k(gt, predict, k=10):
    
    count = 0 
    for pred in predict[:k]:

        if pred in set(gt):

            count += 1

    return count / k

def tag_based_rel_k(gt, predict, k=10):

    return 1 if predict[k-1] in gt else 0

def tag_based_evaluate_map(gt, predict, k=10):
    
    ap = 0
    for i in range(1, min(k, len(gt)) + 1):
        
        ap += tag_based_precision_k(gt, predict, i) * tag_based_rel_k(gt, predict, i)

    return ap / min(k, len(gt))

def tag_based_evaluate_recall(gt, predict, k=10):

    count = 0

    for pred in predict:

        if pred in set(gt):

            count += 1

    return min(count / min(k, len(gt)),1.0)