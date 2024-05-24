import requests
from bs4 import BeautifulSoup
import streamlit as st

# Define a function to fetch job IDs from the LinkedIn job postings page
def fetch_job_ids(url):
    response = requests.get(url)
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    page_jobs = list_soup.find_all('li')
    id_list = []
    for job in page_jobs:
        base_card_div = job.find('div', {'class': "base-card"})
        if base_card_div:
            job_id = base_card_div.get('data-entity-urn').split(':')[3]
            id_list.append(job_id)
    return id_list

# Define a function to fetch job details using job ID
def fetch_job_details(job_id):
    job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    job_response = requests.get(job_url)
    job_soup = BeautifulSoup(job_response.text, "html.parser")
    job_post = {}

    company_name_tag = job_soup.find('a', {'class': 'topcard__org-name-link topcard__flavor--black-link'})
    position_name_tag = job_soup.find('h2', {'class': 'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title'})
    apply_link_tag = job_soup.find('a', {'class': 'topcard__link'})
    job_level_tag = job_soup.find('span', {'class': "description__job-criteria-text description__job-criteria-text--criteria"})

    if company_name_tag:
        job_post['company_name'] = company_name_tag.text.strip()
    if position_name_tag:
        job_post['position_name'] = position_name_tag.text
    if apply_link_tag:
        job_post['apply_link'] = apply_link_tag['href']
    if job_level_tag:
        job_post['job_level'] = job_level_tag.text.strip()

    return job_post

# Define the main function to fetch and display job alerts
def main(url):
    # Fetch job IDs
    job_ids = fetch_job_ids(url)

    # Fetch job details
    job_list = []
    for job_id in job_ids[:10]:  # Fetch only the top 7 jobs
        job_details = fetch_job_details(job_id)
        job_list.append(job_details)

    # Format the job listings for display
    job_alerts = []
    for job in job_list:
        if 'company_name' in job and 'position_name' in job and 'apply_link' in job:
            alert = f"{job['company_name']} - {job['position_name']} ({job['job_level']})\nApply here: {job['apply_link']}\n"
            job_alerts.append(alert)

    job_alert_text ="Day X of Job Postings: Helping Job Seekers Find Opportunities!"
    job_alert_text += "\n 📢 Job Openings Alert! 📢\nExciting opportunities for Data Scientists, Business Analysts, and Data Analysts with 0-2 years of experience!\n\n"
    job_alert_text += "\n".join(job_alerts)
    job_alert_text += "\n Follow For More Daily Job Updates 😊"
    job_alert_text += "\n"
    job_alert_text += "\n#JobAlert #Jobs #DataScientist #DataAnalyst #BusinessAnalyst #Freshers #CareerOpportunities #HiringNow #lookingforjob #candidatesearch #job #joboppurtunity #jobs #hiring #recruitment #jobsearch #jobseekers #employment #jobopportunities #graduates #hr #recruiting #applynow  #talentacquisition"

    return job_alert_text

# Streamlit display
st.title("Job Alerts")

# Take URL as input from the user
url = st.text_input("Enter the URL for job postings", "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0")

# Fetch and display job alerts
job_alert_text = main(url)
st.text_area("Job Openings Alert", job_alert_text,height=600)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Running Streamlit app")
