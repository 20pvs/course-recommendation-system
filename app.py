from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the preprocessed DataFrame
df = pickle.load(open('df.pkl', 'rb'))
popular_df = pickle.load(open('popular_df.pkl', 'rb'))
popular_df2 = pickle.load(open('popular_df2.pkl', 'rb'))
popular_df3 = pickle.load(open('popular_df3.pkl', 'rb'))

def recommend_courses_by_keyword(keyword, df, num_courses=6):
    # Filter courses based on whether their name contains the keyword
    relevant_courses = df[df['course_name'].str.contains(keyword, case=False)]
    # Sort relevant courses by ratings in descending order
    sorted_courses = relevant_courses.sort_values(by='rating', ascending=False)

    # Get top courses
    top_courses = sorted_courses.head(num_courses)
    tpc = top_courses[['course_name','course url']]
    return tpc

@app.route('/')
def index():
    return render_template('index.html',courses=popular_df)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get keyword from form input
    keyword = request.form.get('keyword')

    # Recommend courses based on keyword
    recommended_courses = recommend_courses_by_keyword(keyword, df)

    return render_template('recommend.html', keyword=keyword, courses=recommended_courses)

@app.route('/index2')
def index2():
    return render_template('index2.html',courses=popular_df2)

@app.route('/index3')
def index3():
    return render_template('index3.html',courses=popular_df3)
if __name__ == '__main__':
    app.run(debug=True)
