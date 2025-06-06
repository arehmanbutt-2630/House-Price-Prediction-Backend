import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

data = {
    "square_footage": [800, 1200, 1500, 1800, 2000, 2200, 2400, 2600],
    "bedrooms": [2, 3, 3, 4, 4, 5, 4, 5],
    "price": [150000, 200000, 250000, 300000, 320000, 360000, 380000, 400000],
}
df = pd.DataFrame(data)

# Train model
X = df[["square_footage", "bedrooms"]]
y = df["price"]
model = LinearRegression()
model.fit(X, y)

# Save model
with open("house_price_model.pkl", "wb") as f:
    pickle.dump(model, f)
