from flask import Flask, render_template, request
from job import extract, transform, load, create_database
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    df_html = None
    if request.method == "POST":
        # get user input
        
        job_location = request.form.get('location')
        search_term = request.form.get('job_title')
        
        html = extract(job_location, search_term)
        job_list = transform(html)
        df = load(job_list)
        df_db = create_database(df)  # Create the database with the job listings
        df_db['link'] = df_db['link'].apply(lambda url:f'<a href="{url}" target = "_blank">Apply</a>' if pd.notnull(url) else None)
        df_db.rename(columns={'link' : 'Apply'}, inplace=True)  # Rename the 'link' column to 'Apply'
        df_html = df_db.to_html(classes ='table', index=False, escape=False)
    
    return render_template('home.html', table=df_html)

if __name__ == "__main__":
    app.run(debug=True)
    