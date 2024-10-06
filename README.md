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
- [x] Django Authentication
- [x] Djoser for Simple User Register/Login/Update endpoints 
- [x] Simple JWT
- [x] Update Permissions on API 
- [x] Use Postman to test out authentication endpoints
- [ ] Optional: Custom TokenPairView that includes: remaining lifespan with user that requested
- [x] Optional: Djoser Email confirmation for account activation (Django All-Auth)

### Django Emails
- [x] Set up Email Connectivty with Gmail
- [x] Make sure Activation Emails with Djoser are sent
    - [x] Passwords Reset
    - [x] Username Reset
- [x] Redirect to Front End Url

### User & Model Relationships
- [x] With Permissions, we tie users and jobs 
- [x] Emails for Login
    - [x] Custom User Model 
- [x] Users must be logged in for us to post a job to thier account 

### Work on React and our Finished Rest API 
- [ ] With all the endpoints, we need to tie our Django Backend with the React Frontend


### Refactor and Other things to add
- [x] It's good practice to Create 2 **Seperate** Serializer:
    - One for Post: Necessary fields that are required for Posting
    - One for Get: present specifc fields
    - For instance I don't need (user) and (user_link) 
        - However Post needs user while Get doesn't
 - [x] Order Jobs by most recent?
 - [x] Can the homepage Show things for our users to choose:
    - Jobs
    - Users
    - Images
- [x] API to query a specific User's post
    - If i want the queryset for user: "Thy" then it should return **ONLY** job posts by her
- [x] Custom Commands with `manage.py` to add in *testing data*
    - [x] Users 
    - [x] Job for random Users
- [x] Additional Model Fields for Job (NR --> Not Required):
    - [x] Location (City TextField and State SelectionField)
    - [x] Link (NR)
    - [x] Job Summary (NR)
- [x] Other Non Required fields:
    - [x] Salary
- [x] Create another READ serialier to showcase:
    - Status Choices 
    - State Choices