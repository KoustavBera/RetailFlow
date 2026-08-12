import pandas as pd

df = pd.read_csv("data/raw/online_retail_II.csv")

print(df.head(5))
print(f"Total rows:{len(df)}")
print(f"rows with negative quantity /(returns/ cancellations) : {(df['Quantity']<0).sum()}")
print(f"rows  with missing customerId  : {df['Customer ID'].isna().sum()}")
print(f"Duplicate rows : {df.duplicated().sum()}")
print(f"Distinct countries : {df['Country'].nunique()}")
print(f"Data error( price < 0) : {(df['Price']<0).sum()}")

