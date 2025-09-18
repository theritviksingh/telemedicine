import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # expects .env in project root

cfg = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
}

sql_statements = """
CREATE DATABASE IF NOT EXISTS telemedicine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE telemedicine;
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('patient','doctor','pharmacy','admin') DEFAULT 'patient',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT NOT NULL,
  doctor_id INT,
  start_time DATETIME,
  status VARCHAR(50),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (patient_id) REFERENCES users(id),
  FOREIGN KEY (doctor_id) REFERENCES users(id)
);
"""

conn = mysql.connector.connect(**cfg)
cursor = conn.cursor()
for stmt in sql_statements.split(';'):
    s = stmt.strip()
    if s:
        cursor.execute(s + ';')
conn.commit()
cursor.close()
conn.close()
print("Database and tables created/verified.")
