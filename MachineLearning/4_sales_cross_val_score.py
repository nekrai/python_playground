import pandas as pd

data = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)
feature_cols = ['TV', 'radio', 'newspaper']
X = data[feature_cols]
y = data.sales


from sklearn.linear_model import LinearRegression
lm = LinearRegression()


from sklearn.model_selection import cross_val_score
scores = cross_val_score(lm, X, y, cv=10, scoring='neg_mean_squared_error')
print(-scores)


