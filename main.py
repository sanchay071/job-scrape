from job import extract, transform, load

if __name__ == "__main__":
    html = extract()
    job_list = transform(html)
    df = load(job_list)
    print(df)  # Display the DataFrame with job listings