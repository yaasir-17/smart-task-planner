# Smart Task Planner

## Video Demo

https://youtu.be/qFCgEgrQ7uQ

## Description

Smart Task Planner is a web-based productivity application that helps users organize and manage their daily tasks. The application allows users to create tasks, assign priorities, set deadlines, track completion status, and receive recommendations on which task should be completed next.

The project was built using Flask, SQLite, HTML, Bootstrap, and Jinja. It was created as a personal productivity tool and as a way to apply concepts learned through CS50, including web development, databases, user authentication, session management, and dynamic content rendering.

Unlike a basic to-do list, Smart Task Planner attempts to help users decide what to work on next. Tasks are automatically sorted and a recommended task is generated based on priority and due date. The dashboard also provides statistics about total, pending, completed, and overdue tasks, giving users a quick overview of their progress.

---

## Features

* User registration and login system
* Password hashing for secure storage
* Add new tasks with due dates and priorities
* Edit existing tasks
* Mark tasks as completed
* Delete tasks
* Search tasks by title
* Sort tasks by priority or due date
* Automatic overdue detection
* Dashboard statistics
* Recommended next task system
* Responsive Bootstrap user interface

---

## File Structure

### app.py

This file contains the entire Flask backend of the application.

Its responsibilities include:

* Creating and configuring the Flask application
* Managing user sessions
* Connecting to the SQLite database
* Handling user authentication
* Processing form submissions
* Performing database queries
* Generating task recommendations
* Calculating dashboard statistics
* Rendering templates

The routes implemented are:

* `/` – Dashboard page
* `/register` – User registration
* `/login` – User login
* `/logout` – User logout
* `/add` – Add task
* `/complete` – Mark task as completed
* `/delete` – Delete task
* `/edit` – Edit task

The dashboard route is the core of the application. It retrieves tasks, applies search and sorting options, calculates statistics, and determines the recommended task based on priority and deadline.

---

### templates/layout.html

This file serves as the base template for all pages.

It contains:

* HTML boilerplate
* Bootstrap integration
* Navigation bar
* Common page layout

Using a layout template avoids repeating the same HTML code in every page and makes the application easier to maintain.

---

### templates/login.html

This template displays the login form.

It allows users to:

* Enter username
* Enter password
* View authentication error messages

The page extends the base layout template and focuses solely on user login.

---

### templates/register.html

This template displays the registration form.

It allows users to:

* Create a username
* Create a password
* Confirm password
* View validation errors

The page ensures users can create an account before accessing task management features.

---

### templates/dashboard.html

This is the main page of the application and contains most of the user-facing functionality.

The dashboard includes:

* Current date display
* Task creation form
* Task statistics cards
* Recommended next task section
* Search functionality
* Sorting options
* Task table
* Task actions

The task table displays:

* Title
* Due date
* Priority level
* Status
* Available actions

Overdue tasks are visually highlighted so users can identify them quickly.

---

### templates/edit.html

This template allows users to modify existing tasks.

Users can update:

* Task title
* Due date
* Priority

The form is pre-filled with the current task information, making edits convenient.

---

## Database Design

The project uses SQLite because it is lightweight, easy to set up, and sufficient for a personal productivity application.

The database contains two tables.

### users

Stores user account information.

Columns:

* id
* username
* hash

Passwords are never stored directly. Instead, Werkzeug's password hashing functions are used to store secure password hashes.

### tasks

Stores task information.

Columns:

* id
* user_id
* title
* due_date
* priority
* completed

The user_id column links each task to a specific user.

---

## Design Choices

### Why Flask?

I chose Flask because it is lightweight, beginner-friendly, and was the framework used throughout CS50. Flask provided enough flexibility to implement authentication, database interactions, and routing without introducing unnecessary complexity.

### Why SQLite?

SQLite was selected because the project does not require a large-scale database system. It is easy to integrate with Flask and requires no separate server setup.

### Why Use Priority Levels Instead of Categories?

Initially, I considered implementing task categories such as Academic, Personal, and Work. However, categories alone do not help users decide what should be completed first.

Priority levels directly support scheduling decisions and integrate naturally with the recommendation system.

### Why Implement a Recommended Task System?

Many task management applications simply display a list of tasks and leave the decision-making process entirely to the user.

I wanted Smart Task Planner to provide guidance rather than just storage. The recommendation system automatically selects the most important pending task by considering priority and due date, helping users focus on the next action they should take.

### Why Include Dashboard Statistics?

A long list of tasks can be difficult to interpret quickly.

Displaying total, pending, completed, and overdue task counts gives users an immediate overview of their productivity and progress.

### Why Use Bootstrap?

Bootstrap allowed the interface to become responsive and visually appealing without requiring large amounts of custom CSS.

This made development faster while ensuring consistency across different screen sizes.

---

## Challenges Faced

One of the main challenges was determining how to rank tasks for recommendation.

A simple approach would be to sort only by due date. However, this would sometimes prioritize unimportant tasks that happen to be due soon.

Sorting first by priority and then by due date provided a more balanced solution.

Another challenge was implementing search and sorting simultaneously. The application needed to preserve search results while still applying the selected sorting method, which required multiple query paths in the dashboard route.

---

## Future Improvements

Possible future improvements include:

* Recurring tasks
* Task categories and tags
* Calendar view
* Dark mode
* Email reminders
* Task completion streaks
* Data visualization charts
* Estimated completion times
* Advanced recommendation algorithms

---

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* Bootstrap 5
* Jinja2
* Werkzeug Security

---

## Author

Yaasir
