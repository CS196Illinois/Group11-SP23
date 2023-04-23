import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('202304012238291fea.csv')
assert isinstance(data, pd.DataFrame)

# Drop rows containing missing values in the relevant columns
data = data.dropna(subset=['postal_code', 'type', 'rating', 'photos_count'])

# Reset the index of the data DataFrame
data.reset_index(drop=True, inplace=True)

# Convert postal_code to numeric and drop rows with non-numeric postal codes
data['postal_code'] = pd.to_numeric(data['postal_code'], errors='coerce')
data = data.dropna(subset=['postal_code'])

# Create a function to categorize ratings into classes
def categorize_rating(rating):
    if rating <= 2.5:
        return 'low'
    elif 2.5 < rating <= 4:
        return 'medium'
    else:
        return 'high'

# Apply the categorize_rating function to the 'rating' column
data['rating'] = data['rating'].apply(categorize_rating)

assert data['type'].dtype == 'object'
assert data['rating'].dtype == 'object'
assert data['photos_count'].dtype == 'float64'
assert data['postal_code'].dtype == 'float64'


# One-hot encode the 'type' column
encoder = OneHotEncoder()
encoded_type = encoder.fit_transform(data['type'].values.reshape(-1, 1))
assert encoded_type.shape == (len(data), len(encoder.categories_[0]))

# Create a new DataFrame with postal_code, photo_count, and encoded type columns
encoded_type_df = pd.DataFrame(encoded_type.toarray(), columns=encoder.get_feature_names_out(['type']), index=data.index)
X = pd.concat([data['postal_code'].astype(int), data['photos_count'], encoded_type_df], axis=1)
X.dropna(subset=['postal_code'], inplace=True)

assert isinstance(X, pd.DataFrame)
#print(X['postal_code'])
#X.to_csv('X_dataframe.csv', index=False)
assert X['postal_code'].dtype == 'int32'

# Create a new DataFrame with just the rating column
y = data['rating']
assert isinstance(y, pd.Series)
assert y.dtype == 'object'

# Create a KNN classifier with k=5
knn = KNeighborsClassifier(n_neighbors=5)

# Fit the classifier to the data
knn.fit(X, y)

def find_best_restaurant_type(postal_code):
    assert isinstance(postal_code, int)
    
    if postal_code < 60001 or postal_code > 62999 or len(str(postal_code)) != 5:
        print(f"Invalid postal code: {postal_code}. Please enter a valid Illinois zip code with 5 digits.")
        return None

    # Create a DataFrame with the given postal code, a dummy photo_count, and the encoded 'type' column filled with zeros
    encoded_postal_code = pd.DataFrame({'postal_code': [postal_code], 'photos_count': [0]})
    encoded_postal_code = pd.concat([encoded_postal_code, pd.DataFrame(columns=encoder.get_feature_names_out(['type']), index=[0]).fillna(0)], axis=1)

    # Find the 10 nearest neighbors to the given postal code
    neighbors = knn.kneighbors([encoded_postal_code.values[0]])[1][0]

    # Get the restaurant types for those neighbors
    types = data.iloc[neighbors]['type']

    # Count the occurrences of each type
    type_counts = types.value_counts()

    # Return the type with the highest count
    best_type = type_counts.index[0]
    assert isinstance(best_type, str)
    
    print(f"Zip code {postal_code}: The best restaurant type to open is '{best_type}'.")
    return best_type

# Example usage
find_best_restaurant_type(3)
find_best_restaurant_type(62999)

# Example usage for multiple zip codes
postal_codes = [61615, 60025, 61833, 60109]
for code in postal_codes:
    find_best_restaurant_type(code)