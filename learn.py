from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import random
import numpy as np

s = np.random.randint(5000)
def short(x):
    x = np.array(x).reshape((4, 64, 64))
    y = np.zeros((4,64,64))
    for u in range(4):
        for v in range(64):
            for w in range(64):
                y[u][v // 8][w // 8] += x[u][v][w]
    return y.flatten()

def multishort(x):
    return [short(x_) for x_ in x]

Y = [1] * len(good) + [0] * len(bad)
X = good + bad

num_samples = len(X)
indices = list(range(num_samples))
indices1 = [i for i in indices if Y[i] == 1]
indices0 = [i for i in indices if Y[i] == 0]
ratio = len(indices1) / len(indices)
results = {}
resultso = {}
all_numbers = sorted([5, 10, 15, 20, 30, 40, 60, 80, 100, 120, 140, 160], reverse=True)#, 40, 80, 160, 320]
all_numbers = sorted([5, 10, 15, 20, 30, 150], reverse=True)#, 40, 80, 160, 320]
for n in all_numbers:
  if n < num_samples / 2 and n < 100:
     continue
  if n < num_samples:
     #n1 = int(ratio * n)
     #if n1 >= len(indices1):
     #    continue
     #if n-n1 >= len(indices0):
     #    continue
   for idx_run in range(27):
    print(f"Run with index {idx_run}")
    train_indices = random.sample(indices, n)
    Xtrain = [X[i] for i in train_indices]
    Ytrain = [Y[i] for i in train_indices]
    ptest_indices = [i for i in indices if i not in train_indices]
    for clf in [tree.DecisionTreeClassifier(), LogisticRegression(), MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1), svm.SVC()]:
      try:
          tclf = clf.fit(multishort(Xtrain), Ytrain)
      except ValueError as e:
          print(f"Pb with {clf_str}: {e}")
          continue
      clf_st = str(clf)[:10]
      if clf_st not in results:
          results[clf_st] = {}
      if n not in results[clf_st]:
          results[clf_st][n] = []
       
#        train_indices1 = random.sample(indices1, n1)
#        train_indices0 = random.sample(indices0, n-n1)
#        test_indices1 = [i for i in indices1 if i not in train_indices1]
#        test_indices0 = [i for i in indices0 if i not in train_indices0]
#        train_indices = train_indices1 + train_indices0
#        test_indices = test_indices1 + test_indices0
      assert len(ptest_indices) + len(train_indices) == num_samples
      for m in [2, 3, 4, 5, 6, 7]: #, 10, 15, 20, 40]:
       if m < num_samples - n:
        print(f"Working with training set of cardinal {n} and ts {m}")
        test_indices = random.sample(ptest_indices, m) #(7 * len(test_indices)) // 8)
        Xtest = [X[i] for i in test_indices]
        Ytest = [Y[i] for i in test_indices]
        results[clf_st][n] += [tclf.score(multishort(Xtest), Ytest)]
        clf_str = str(clf)[:10] + "_" + str(len(Ytest))
        if clf_str not in resultso:
          resultso[clf_str] = {}
        if n not in resultso[clf_str]:
          resultso[clf_str][n] = []
        num_good = np.sum(Ytrain)
        num_good_test = np.sum(Ytest)
        if np.sum(num_good) < len(Ytrain) / 10:
            print("not enough good train")
            continue
        if len(Ytrain) - np.sum(num_good) < len(Ytrain) / 10:
            print("not enough bad train")
            continue
        if np.sum(num_good_test) < len(Ytest) / 10:
            print("not enough good test")
            continue
        if len(Ytest) - np.sum(num_good_test) < len(Ytest) / 10:
            print("not enough bad test")
            continue
        if "majority" not in results:
            results["majority"] = {}
        if n not in results["majority"]:
            results["majority"][n] = []
        if "majority" not in resultso:
            resultso["majority"] = {}
        if n not in resultso["majority"]:
            resultso["majority"][n] = []
        resultso["majority"][n] += [len([y for y in Ytest if y == 1]) / len(Ytest)]
        if num_good > n / 2:
            results["majority"][n] += [len([y for y in Ytest if y == 1]) / len(Ytest)]
        else:
            results["majority"][n] += [len([y for y in Ytest if y == 0]) / len(Ytest)]
        if True:
            #print(f"Working with {clf_str}")
            try:
                proba_fail = 1000000.00   # This is a lot of %.
                for u in range(len(Ytest)):
                    proba_f = tclf.predict_proba([short(Xtest[u])])[0][0]
                    if proba_f < proba_fail:
                        proba_fail = proba_f
                        idx = u
                resultso[clf_str][n] += [Ytest[idx]]
            except ValueError as e:
                print(f"Pb with {clf_str}: {e}")
            except AttributeError as e:
                print(f"{clf_str} does not provide probas.")
            #print(f"Current results dict: {results}")
            #print(f"Current resultso dict: {resultso}")
            

  for c in results:
    if n in results[c]:
      print(f"L-{pb}{s} {n} {c} {np.sum(results[c][n]) / len(results[c][n])}")
  for c in resultso:
    if n in resultso[c]:
      if len(resultso[c][n]) > 0:
        print(f"O-{pb}{s} {n} {c} {np.sum(resultso[c][n]) / len(resultso[c][n])}")
