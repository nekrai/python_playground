from sklearn import tree

labels_s = {
    'Orange': 0,
    'Apple': 1
}

labels_n = {
    0: 'Orange',
    1: 'Apple'
}

features = [[140, 1], [130, 1], [150, 0], [170, 0]]
labels = [labels_s['Apple'], labels_s['Apple'], labels_s['Orange'], labels_s['Orange']]

clf = tree.DecisionTreeClassifier()

clf.fit(features, labels)
print(labels_n[clf.predict([[160, 0]])[0]])
