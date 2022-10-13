from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import random
import numpy as np



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
for n in all_numbers:
  if n < num_samples / 2 and n < 100:
     continue
  for m in [5, 10, 20, 40]:
   if m < num_samples - n:
    print(f"Working with training set of cardinal {n}")
    if n < num_samples:
     #n1 = int(ratio * n)
     #if n1 >= len(indices1):
     #    continue
     #if n-n1 >= len(indices0):
     #    continue
     for idx_run in range(111):
        print(f"Run with index {idx_run}")
        train_indices = random.sample(indices, n)
        test_indices = [i for i in indices if i not in train_indices]
#        train_indices1 = random.sample(indices1, n1)
#        train_indices0 = random.sample(indices0, n-n1)
#        test_indices1 = [i for i in indices1 if i not in train_indices1]
#        test_indices0 = [i for i in indices0 if i not in train_indices0]
#        train_indices = train_indices1 + train_indices0
#        test_indices = test_indices1 + test_indices0
        assert len(test_indices) + len(train_indices) == num_samples
        test_indices = random.sample(test_indices, m) #(7 * len(test_indices)) // 8)
        Xtrain = [X[i] for i in train_indices]
        Ytrain = [Y[i] for i in train_indices]
        Xtest = [X[i] for i in test_indices]
        Ytest = [Y[i] for i in test_indices]
        num_good = np.sum(Ytrain)
        num_good_test = np.sum(Ytest)
        if np.sum(num_good) < len(Ytrain) / 10:
            continue
        if len(Ytrain) - np.sum(num_good) < len(Ytrain) / 10:
            continue
        if np.sum(num_good_test) < len(Ytest) / 10:
            continue
        if len(Ytest) - np.sum(num_good_test) < len(Ytest) / 10:
            continue
        if "majority" not in results:
            results["majority"] = {}
            resultso["majority"] = {}
        if n not in results["majority"]:
            results["majority"][n] = []
            resultso["majority"][n] = []
        resultso["majority"][n] += [len([y for y in Ytest if y == 1]) / len(Ytest)]
        if num_good > n / 2:
            results["majority"][n] += [len([y for y in Ytest if y == 1]) / len(Ytest)]
        else:
            results["majority"][n] += [len([y for y in Ytest if y == 0]) / len(Ytest)]
        for clf in [tree.DecisionTreeClassifier(), LogisticRegression(), MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1), svm.SVC()]:
            clf_str = str(clf)[:10] + "_" + str(len(Ytest))
            #print(f"Working with {clf_str}")
            if clf_str not in results:
                results[clf_str] = {}
                resultso[clf_str] = {}
            if n not in results[clf_str]:
                results[clf_str][n] = []
                resultso[clf_str][n] = []
            try:
                tclf = clf.fit(Xtrain, Ytrain)
                results[clf_str][n] += [tclf.score(Xtest, Ytest)]
                proba_fail = 1000000.00   # This is a lot of %.
                for u in range(len(Ytest)):
                    proba_f = tclf.predict_proba([Xtest[u]])[0][0]
                    if proba_f < proba_fail:
                        proba_fail = proba_f
                        idx = u
                resultso[clf_str][n] += [Ytest[idx]]
            except ValueError as e:
                print(f"Pb with {clf_str}: {e}")
            except AttributeError as e:
                print(f"{clf_str} does not provide probas.")
            print("Current results dict: {results}")
            print("Current resultso dict: {resultso}")
            

     for c in results:
      if n in results[c]:
        print(f"L-{pb} {n} {c} {np.sum(results[c][n]) / len(results[c][n])}")
        if len(resultso[c][n]) > 0:
           print(f"O-{pb} {n} {c} {np.sum(resultso[c][n]) / len(resultso[c][n])}")
