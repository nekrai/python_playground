import pandas as pd

data = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)
feature_cols = ['TV', 'radio', 'newspaper']
X = data[feature_cols]
y = data.sales


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
print(y_test)


from sklearn.linear_model import LinearRegression
clf = LinearRegression()

clf.fit(X_train, y_train)

predictions = clf.predict(X=X_test)
print(predictions)


from sklearn.metrics import mean_squared_error
print(mean_squared_error(y_test, predictions))
