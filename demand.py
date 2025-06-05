import requests
import pandas as pd

url = "https://dummyjson.com/products"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data['products'])
df.to_csv("product_data.csv", index=False)

print("Data pulled and saved as product_data.csv")

import pandas as pd

# Load the saved data
df = pd.read_csv("product_data.csv")

# Step 1: View basic info
print(df.info())
print(df.head())

# Step 2: Check for missing values
print(df.isnull().sum())

# Step 3: Keep only relevant columns
df_clean = df[['title', 'price', 'stock', 'rating', 'category']].copy()

# Step 4: Handle any missing values (if found)
df_clean.dropna(inplace=True)

# Step 5: Save cleaned data
df_clean.to_csv("cleaned_product_data.csv", index=False)
print("Cleaned data saved to cleaned_product_data.csv")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cleaned_product_data.csv")
sns.set(style="whitegrid")

# 1. Price vs Stock
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="price", y="stock", hue="category")
plt.title("Price vs Stock by Category")
plt.savefig("price_vs_stock.png")
plt.close()  # 👈 suppress plot window

# 2. Rating Distribution
plt.figure(figsize=(6, 4))
sns.histplot(df["rating"], bins=10, kde=True)
plt.title("Product Rating Distribution")
plt.savefig("rating_dist.png")
plt.close()

# 3. Average Price by Category
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x="category", y="price", estimator="mean")
plt.xticks(rotation=45)
plt.title("Average Price by Category")
plt.savefig("avg_price_by_category.png")
plt.close()


df = pd.read_csv("cleaned_product_data.csv")

# One-hot encode 'category'
df = pd.get_dummies(df, columns=["category"], drop_first=True)

# Drop unnecessary columns
df.drop(columns=["title"], inplace=True)

# Define features (X) and target (y)
X = df.drop(columns=["stock"])  # Predicting 'stock' as demand proxy
y = df["stock"]

# Save ready-to-train data
X.to_csv("features.csv", index=False)
y.to_csv("target.csv", index=False)

print("Features and target saved.")
