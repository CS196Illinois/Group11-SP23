import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('202304012238291fea.csv')

# Drop rows containing missing values in the relevant columns
data = data.dropna(subset=['postal_code', 'type', 'rating'])

# Convert postal_code to numeric and drop rows with non-numeric postal codes
data['postal_code'] = pd.to_numeric(data['postal_code'], errors='coerce')
data = data.dropna(subset=['postal_code'])

# One-hot encode the 'type' column
encoder = OneHotEncoder()
encoded_type = encoder.fit_transform(data['type'].values.reshape(-1, 1))

# Create a new DataFrame with postal_code and encoded type columns
X = pd.concat([data['postal_code'].astype(int), pd.DataFrame(encoded_type.toarray())], axis=1)

# Create a new DataFrame with just the rating column
y = data['rating']

# Create a KNN classifier with k=5 (you can experiment with different values of k)
knn = KNeighborsClassifier(n_neighbors=5)

# Fit the classifier to the data
knn.fit(X, y)

# Define a function that takes a postal code as input and returns the best type of restaurant to open
def find_best_restaurant_type(postal_code):
    # Create a DataFrame with the given postal code and the encoded 'type' column filled with zeros
    encoded_postal_code = pd.DataFrame({'postal_code': [postal_code]})
    encoded_postal_code = pd.concat([encoded_postal_code, pd.DataFrame(columns=encoder.get_feature_names_out(['type']), index=[0]).fillna(0)], axis=1)

    # Find the 10 nearest neighbors to the given postal code
    neighbors = knn.kneighbors([encoded_postal_code.values[0]])[1][0]

    # Get the restaurant types for those neighbors
    types = data.iloc[neighbors]['type']

    # Count the occurrences of each type
    type_counts = types.value_counts()

    # Return the type with the highest count
    return type_counts.index[0]

# Example usage
print(find_best_restaurant_type(61615))
