import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('static/csv_files/data.csv')

# Select relevant features and drop missing values
features = ['masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage', 'Size', 'Made In','gender']
df = df.dropna(subset=features + ['id', 'productDisplayName'])

# Combine features into a single string for each product
def combine_features(row):
    return ' '.join(str(row[feature]) for feature in features)

df['combined_features'] = df.apply(combine_features, axis=1)

# Vectorize the combined feature strings using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['combined_features'])

# Create mappings
product_vectors = dict(zip(df['id'], tfidf_matrix))
product_names = dict(zip(df['id'], df['productDisplayName']))

def recommend_products(past_product_ids, top_n=5):
    # Get TF-IDF vectors of purchased products
    vectors = [product_vectors[pid] for pid in past_product_ids if pid in product_vectors]

    if not vectors:
        print("No valid product IDs found in history.")
        return []

    # Create user profile by averaging TF-IDF vectors
    user_profile = np.mean(np.vstack([v.toarray() for v in vectors]), axis=0).reshape(1, -1)

    # Compute cosine similarity between user profile and all products
    similarities = cosine_similarity(user_profile, tfidf_matrix)[0]

    # Filter out already purchased items
    candidate_indices = df.index[~df['id'].isin(past_product_ids)]
    scored_candidates = [(df.iloc[i]['id'], similarities[i]) for i in candidate_indices]

    # Sort and return top N
    top_matches = sorted(scored_candidates, key=lambda x: x[1], reverse=True)[:top_n]
    return [(pid, product_names[pid], score) for pid, score in top_matches]

# 🔍 Example usage
if __name__ == "__main__":
    
    product_id = [15970]  

    recommendations = recommend_products(product_id)

    print("Top Recommendations:")
    for pid, name, score in recommendations:
        print(f"🛍️ {name} (ID: {pid}) - Similarity: {score:.4f}")
