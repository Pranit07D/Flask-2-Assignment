#Question 4. Develop a recommendation system using Flask that suggests content to users based on their preferences.

from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load and prepare data
df = pd.read_csv('data/items.csv')

# Feature extraction
tfidf = TfidfVectorizer(stop_words='english')
df['item_features'] = df['item_features'].fillna('')
tfidf_matrix = tfidf.fit_transform(df['item_features'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recommendations(item_name, cosine_sim=cosine_sim):
    idx = df.index[df['item_name'] == item_name].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 recommendations
    item_indices = [i[0] for i in sim_scores]
    return df.iloc[item_indices]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    item_name = request.form['item_name']
    recommendations = get_recommendations(item_name)
    return render_template('recommendations.html', item_name=item_name, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)