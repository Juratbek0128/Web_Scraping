import sqlite3
import requests
from bs4 import BeautifulSoup  # HTML uchun

# 1. baza yaratish
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()  # SQL
# yaratish
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT(500),
        creator TEXT(500),  
        address TEXT(500),  
        date TEXT
    )
    """
)
conn.commit()

# 2. Saytdan ma'lumotlarni olish
url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []
job_id = 1  # id uchhun

for job in soup.find_all("div", class_="card-content"):
    job_title = job.find("h2", class_="title").text.strip()
    creator = job.find("h3", class_="company").text.strip()
    address = job.find("p", class_="location").text.strip()
    date = job.find("time")["datetime"]

    # Ma'lumotlarni ro'yxatga qo'shadi
    jobs.append((job_id, job_title, creator, address, date))
    job_id += 1  # ID ni oshiradi

# 3. Ma'lumotlarni bazaga qo'shish
if jobs:
    cursor.executemany(
        """
        INSERT INTO jobs (id, job_title, creator, address, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        jobs,
    )
    conn.commit()  # tasdiqlaydi

# 4. display uchun
cursor.execute("SELECT id, job_title, creator, address, date FROM jobs")
for job in cursor.fetchall():
    print(
        f"ID: {job[0]}, Job Title: {job[1]}, Creator: {job[2]}, Address: {job[3]}, Date: {job[4]}"
    )
conn.close()
