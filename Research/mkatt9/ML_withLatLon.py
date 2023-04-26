import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
from sklearn.preprocessing import OneHotEncoder

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('202304012238291fea.csv', dtype={'postal_code': str})
assert isinstance(data, pd.DataFrame)

# Drop rows containing missing values in the relevant columns
data = data.dropna(subset=['postal_code', 'type', 'subtypes', 'category', 'rating', 'photos_count', 'latitude', 'longitude'])

# Reset the index of the data DataFrame
data.reset_index(drop=True, inplace=True)

# One-hot encode the 'type', 'subtypes', and 'category' columns
encoder = OneHotEncoder()
encoded_columns = encoder.fit_transform(data[['type', 'subtypes', 'category']])
column_names = encoder.get_feature_names_out(['type', 'subtypes', 'category'])

# Create a new DataFrame with postal_code, photo_count, and encoded type, subtypes, and category columns
encoded_columns_df = pd.DataFrame(encoded_columns.toarray(), columns=column_names, index=data.index)
X = pd.concat([data['postal_code'], data['photos_count'], encoded_columns_df], axis=1)

assert isinstance(X, pd.DataFrame)

# Create a new DataFrame with just the rating column
y = data['rating']
assert isinstance(y, pd.Series)
assert y.dtype == 'float64'

# Create a BallTree with the latitude and longitude values
tree = BallTree(data[['latitude', 'longitude']].values, leaf_size=40)

def find_best_restaurant_type(postal_code):
    postal_code = str(postal_code)  # Convert the input postal_code to a string

    if int(postal_code) < 60001 or int(postal_code) > 62999 or len(postal_code) != 5:
        print(f"Invalid postal code: {postal_code}. Please enter a valid Illinois zip code with 5 digits.")
        return None

    # Get the mean latitude and longitude of the given postal code
    postal_code_data = data[data['postal_code'] == postal_code]

    if postal_code_data.empty:
        print(f"Postal code {postal_code} not found in the dataset.")
        return None

    lat, lon = postal_code_data[['latitude', 'longitude']].mean()

    # Find the k'th nearest neighbors to the given postal code using the BallTree
    neighbors = tree.query([(lat, lon)], k=40, return_distance=False)[0]

    # Get the restaurant types, subtypes, and categories for those neighbors
    neighbor_info = data.iloc[neighbors][['type', 'subtypes', 'category']]

    # Count the occurrences of each combination
    combination_counts = neighbor_info.value_counts()

    # Return the combination with the highest count
    best_combination = combination_counts.index[0]

    # Check if any subtype matches with the best combination
    types_and_categories = [best_combination[0].lower(), best_combination[2].lower()]
    subtype_matches = [subtype.lower() for subtype in best_combination[1].split(', ')]

    # Combine all the matches and handle plural forms
    all_matches = [match[:-1] if match.endswith('s') else match for match in types_and_categories + subtype_matches]

    # Find unique matches
    unique_matches = list(set(all_matches))

    # Capitalize the first letter of each word
    formatted_matches = [match.capitalize() for match in unique_matches]

    # Print the best combination
    if len(formatted_matches) == 1:
        print(f"Zip code {postal_code}: The best restaurant type to open is '{formatted_matches[0]}'.")
    else:
        print(f"Zip code {postal_code}: The best restaurant types to open are '{', '.join(formatted_matches[:-1])} and {formatted_matches[-1]}'.")
    return best_combination


# Example usage
find_best_restaurant_type(3)
find_best_restaurant_type(62999)

# Example usage for multiple zip codes
postal_codes = [61615, 61520, 61833, 60109]
for code in postal_codes:
    find_best_restaurant_type(code)