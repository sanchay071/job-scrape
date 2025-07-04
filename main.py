from job import extract, transform, load, create_database

if __name__ == "__main__":
    html = extract()
    job_list = transform(html)
    df = load(job_list)
    print(df)  # Display the DataFrame with job listings
    df_db = create_database(df)  # Create the database with the job listings
    print(df_db)