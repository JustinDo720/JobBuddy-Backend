# JobBuddy Backend

---

## Table of Contents 
1) [Project Description](#project-description)
1) [Project Tasks](#project-tasks)

---

## Project Description 

This repository contains the backend for JobBuddy, a personal job tracking dashboard designed to help users manage their job search efficiently. Built with Django Rest Framework (DRF), the backend provides the necessary API endpoints to support the features of the JobBuddy React frontend.

Key Features:
    - Job Application Management: Endpoints to add, edit, and remove job entries, including fields for job title, company name, salary, status, and more.
    - Goal Setting and Progress Tracking: Allows users to set daily goals such as applying for jobs, networking, or completing coding exercises. Progress is recorded and shared with the frontend.
    - Job Application Trends: Provides data endpoints to visualize job application trends over time, enabling integration with Chart.js or Recharts in the frontend.

The backend is designed to offer seamless integration with the React frontend, using RESTful API principles to ensure a clean, scalable, and maintainable codebase. It includes authentication and authorization mechanisms to protect user data, ensuring that job search details are securely stored.

---

## Project Tasks

### Basic Tasks
- [x] Connect MySQL DB
- [x] Tie Django with Rest Framework 

### Add a Job
- [x] Create Job Model
- [x] Job Serializer 
- [x] Create POST API to add a job
- [x] Test the API with Postman or Django Rest Framework UI
- [ ] Integrate the API with the React frontend form

### Edit a Job
- [x] Create PUT/PATCH API to edit a job
- [x] Ensure proper validation for updating job details
- [x] Test the API with Postman or Django Rest Framework UI
- [ ] Integrate the edit functionality with the React frontend

### Delete a Job
- [x] Create DELETE API to remove a job
- [x] Confirm job deletion with validation and feedback
- [x] Test the API with Postman or Django Rest Framework UI
- [ ] Integrate the delete functionality with the React frontend

### Accessing Indiviual Job 
- [x] Singly retrieve information from ONE job via ID
- [x] Work on Hyperlinking Job List with this new API 

### Set up Django Corsheader 
- [x] Install and add Corsheader to our Django Application 
- [x] Fix up `settings.py` for our REACT application to send request

### Work on Job Images 
- [x] Create a Job Image Model where one Job have any many Images
- [x] Create that POST API for uploading Images 
- [x] Create that Edit API for uploading Images 
- [x] Create Delete API as well
- [x] Update the Job Serializer to include all Images related to that job post 

### Work on Authentication 
- [ ] Django Authentication
- [ ] Djoser
- [ ] Simple JWT
- [ ] Update Permissions on API 

### User & Model Relationships
- [ ] With Permissions, we tie users and jobs 
- [ ] Users must be logged in for us to post a job to thier account 

### Work on React and our Finished Rest API 
- [ ] With all the endpoints, we need to tie our Django Backend with the React Frontend

