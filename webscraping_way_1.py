import sqlite3  # storage
import requests  # HTTP bilan ishlash
from bs4 import BeautifulSoup  # HTML bilan ishlash uchun


# 1-qadam
def setup_database():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute(
        """
                   create table if not exists jobs(
                       id integer,
                       job_title TEXT(500),
                       creator TEXT(500),
                       address TEXT(500),
                       date TEXT 
                   )
                   """
    )
    conn.commit()
    return conn, cursor


# 2- qadam
def scrape_jobs():
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    job_id = 1
    for job in soup.find_all("div", class_="card-content"):
        job_title = job.find("h2", class_="title").text.strip()
        creator = job.find("h3", class_="company").text.strip()
        address = job.find("p", class_="location").text.strip()
        date = job.find("time")["datetime"]
        jobs.append((job_id, job_title, creator, address, date))
        job_id += 1
    return jobs  # to'liq listni qaytarib beradi


# 3-qadam
def insert_jobs(cursor, jobs):
    cursor.executemany(
        """
        INSERT INTO jobs (id, job_title, creator, address, date)
        VALUES (?, ?, ?, ?, ?)
    """,
        jobs,
    )


# 4-qadam ko'rsatish
def display_jobs(cursor):
    cursor.execute("""select  id,job_title,creator,address,date from jobs""")
    for job in cursor.fetchall():
        print(
            f"ID: {job[0]}, Ish nomi: {job[1]}, Yaratuvchi: {job[2]}, Manzil: {job[3]}, Sana: {job[4]}"
        )


# 5-qadam main() funksiya


def main():
    conn, cursor = setup_database()
    jobs = scrape_jobs()
    insert_jobs(cursor, jobs)
    conn.commit()  # tastiqlab beradi yani run qilishni
    display_jobs(cursor)
    conn.close()


if __name__ == "__main__":
    main()
