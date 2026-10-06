# Data Redundancy Removal System

## CodeAlpha Cloud Computing Internship - Task 1

The Data Redundancy Removal System is a cloud-based web application developed to validate incoming records and prevent duplicate data from being stored in a cloud database.

The system validates user-provided name, email, and phone number before processing the record. A SHA-256 hash is generated from normalized record information and compared with existing hashes in the database. If the same record already exists, it is rejected as duplicate data. Only validated and unique records are stored.

## Features

- User-friendly web interface
- Name, email, and phone number validation
- Duplicate data detection
- SHA-256 record fingerprinting
- Prevention of duplicate database entries
- Validation activity logging
- Cloud-based MySQL database
- Flask backend
- AWS EC2 deployment
- AWS RDS database integration
- Records viewing page

## Technology Stack

### Frontend
- HTML5
- CSS3

### Backend
- Python
- Flask

### Database
- MySQL
- Amazon RDS

### Cloud
- Amazon EC2
- Amazon RDS

### Other Technologies
- SHA-256 hashing
- Git
- GitHub
- Python-dotenv

## System Architecture

```text
                    User
                      |
                      v
              Web Browser
                      |
                      v
              AWS EC2 Instance
                      |
                      v
              Flask Application
                      |
             +--------+--------+
             |                 |
             v                 v
      Data Validation    Duplicate Detection
             |                 |
             +--------+--------+
                      |
                      v
                 SHA-256 Hash
                      |
                      v
                AWS RDS MySQL
                 /          \
                /            \
               v              v
           records      validation_logs