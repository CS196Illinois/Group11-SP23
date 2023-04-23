import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('202304012238291fea.csv')
assert isinstance(data, pd.DataFrame)

# Drop rows containing missing values in the relevant columns
data = data.dropna(subset=['postal_code', 'type', 'subtypes', 'category', 'rating', 'photos_count'])

# Reset the index of the data DataFrame
data.reset_index(drop=True, inplace=True)

# Convert postal_code to numeric and drop rows with non-numeric postal codes
data['postal_code'] = pd.to_numeric(data['postal_code'], errors='coerce')
data = data.dropna(subset=['postal_code'])

# One-hot encode the 'type', 'subtypes', and 'category' columns
encoder = OneHotEncoder()
encoded_columns = encoder.fit_transform(data[['type', 'subtypes', 'category']])
column_names = encoder.get_feature_names_out(['type', 'subtypes', 'category'])

# Create a new DataFrame with postal_code, photo_count, and encoded type, subtypes, and category columns
encoded_columns_df = pd.DataFrame(encoded_columns.toarray(), columns=column_names, index=data.index)
X = pd.concat([data['postal_code'].astype(int), data['photos_count'], encoded_columns_df], axis=1)
X.dropna(subset=['postal_code'], inplace=True)

assert isinstance(X, pd.DataFrame)
assert X['postal_code'].dtype == 'int32'

# Create a new DataFrame with just the rating column
y = data['rating']
assert isinstance(y, pd.Series)
assert y.dtype == 'float64'

# Create a KNN regressor with k=5
knn = KNeighborsRegressor(n_neighbors=5)

# Fit the regressor to the data
knn.fit(X, y)

def find_best_restaurant_type(postal_code):
    assert isinstance(postal_code, int)

    if postal_code < 60001 or postal_code > 62999 or len(str(postal_code)) != 5:
        print(f"Invalid postal code: {postal_code}. Please enter a valid Illinois zip code with 5 digits.")
        return None

    # Create a DataFrame with the given postal code, a dummy photo_count, and the encoded columns filled with zeros
    encoded_postal_code = pd.DataFrame({'postal_code': [postal_code], 'photos_count': [0]})
    encoded_postal_code = pd.concat([encoded_postal_code, pd.DataFrame(columns=column_names, index=[0]).fillna(0)], axis=1)

    # Find the 10 nearest neighbors to the given postal code
    neighbors = knn.kneighbors([encoded_postal_code.values[0]])[1][0]

    # Get the restaurant types, subtypes, and categories for those neighbors
    neighbor_info = data.iloc[neighbors][['type', 'subtypes', 'category']]

    # Count the occurrences of each combination
    combination_counts = neighbor_info.value_counts()

    # Return the combination with the highest count
    best_combination = combination_counts.index[0]

    # Check if any subtype matches with the best combination
    types_and_categories = [best_combination[0], best_combination[2]]
    subtype_matches = [subtype for subtype in best_combination[1] if subtype in types_and_categories]

    # Print the best combination
    if subtype_matches:
        print(f"Zip code {postal_code}: The best restaurant type to open is '{best_combination[0]}' with subtypes '{', '.join(subtype_matches)}' and category '{best_combination[2]}'.")
    else:
        print(f"Zip code {postal_code}: The best restaurant type to open is '{best_combination[0]}' with category '{best_combination[2]}'.")
    return best_combination

# Example usage
find_best_restaurant_type(3)
find_best_restaurant_type(62999)

# Example usage for multiple zip codes
postal_codes = [61615, 60025, 61833, 60109]
for code in postal_codes:
    find_best_restaurant_type(code)