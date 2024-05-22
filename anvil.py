import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to fetch job IDs from the LinkedIn job postings page
def fetch_job_ids(url):
    response = requests.get(url)
    list_data = response.text
    list_soup = BeautifulSoup(list_data, "html.parser")
    job_cards = list_soup.find_all('div', {'class': 'base-card'})
    id_list = []

    for job_card in job_cards:
        job_id = job_card.get('data-entity-urn')
        if job_id:
            job_id = job_id.split(':')[-1]
            id_list.append(job_id)

    return id_list

# Function to fetch job details using job ID
def fetch_job_details(job_id):
    job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    job_response = requests.get(job_url, headers=headers)
    
    if job_response.status_code == 200:
        job_data = job_response.json()
        job_post = {}

        company_name = job_data.get('companyName')
        position_name = job_data.get('title')
        apply_link = job_data.get('applyLink')
        job_level = job_data.get('jobLevel')

        if company_name:
            job_post['company_name'] = company_name
        if position_name:
            job_post['position_name'] = position_name
        if apply_link:
            job_post['apply_link'] = apply_link
        if job_level:
            job_post['job_level'] = job_level

        return job_post
    else:
        return None

# Main function to fetch and display job alerts
def main(url):
    # Fetch job IDs
    job_ids = fetch_job_ids(url)

    # Fetch job details
    job_list = []
    for job_id in job_ids[:10]:  # Fetch only the top 10 jobs
        job_details = fetch_job_details(job_id)
        if job_details:
            job_list.append(job_details)

    # Format the job listings for display
    job_alerts = []
    for job in job_list:
        if 'company_name' in job and 'position_name' in job and 'apply_link' in job:
            alert = f"{job['company_name']} - {job['position_name']} ({job['job_level']})\nApply here: {job['apply_link']}\n"
            job_alerts.append(alert)

    job_alert_text = "Day X of Job Postings: Helping Job Seekers Find Opportunities!"
    job_alert_text += "\n 📢 Job Openings Alert! 📢\nExciting opportunities for Data Scientists, Business Analysts, and Data Analysts with 0-2 years of experience!\n\n"
    job_alert_text += "\n".join(job_alerts)
    job_alert_text += "\n Follow For More Daily Job Updates 😊"
    job_alert_text += "\n"
    job_alert_text += "\n#JobAlert #Jobs #DataScientist #DataAnalyst #BusinessAnalyst #Freshers #CareerOpportunities #HiringNow #lookingforjob #candidatesearch #job #jobopportunity #jobs #hiring #recruitment #jobsearch #jobseekers #employment #jobopportunities #graduates #hr #recruiting #applynow #talentacquisition"

    return job_alert_text

# Streamlit display
st.title("Job Alerts")

# Text input for URL
url_input = st.text_input("Enter LinkedIn job search URL")

if url_input:
    job_alert_text = main(url_input)
    st.text_area("Job Openings Alert", job_alert_text, height=600)
else:
    st.write("Please enter a LinkedIn job search URL to get job alerts.")
