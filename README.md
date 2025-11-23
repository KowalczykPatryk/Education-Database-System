# Education-Database-System
This project implements a lightweight in-memory education database system using Python dictionaries as the primary data storage mechanism. It supports creating and managing schools, courses, students, scores, and attendance, with automatic ID generation and optional JSON persistence.

The system emulates a structured database while respecting the constraint of using only Python dictionaries as the storage backend. It also includes a data generator that fills the database with example schools, courses, and students, and assigns random scores and attendance using Gaussian distribution.

Although implemented purely with dictionaries, the design takes inspiration from relational database principles, such as entity tables, foreign-key-like references, and many-to-many relationships.

The project deliberately avoids traditional object-oriented programming to showcase how a non-OOP, data-oriented design can remain structured, maintainable, and expressive.

---

## Features
### Core Functionality
- Create and manage:
  - Schools
  - Students
  - Courses
- Track many-to-many relationships:
  - Students in schools
  - Students enrolled in courses
- Record:
  - Scores for each student in each course
  - Attendance instances stored by date
### Additional Capabilities
- Automatic unique ID generation using prefix-based generators.
- JSON file persistence with support for converting non-serializable data structures (sets).
- Loading previously saved JSON data and restoring sets from serialized lists.
- Statistical operations:
  - Student’s average score across all courses
  - Student’s average score for a specific course
  - Total attendance for specific course
  - Retrieval of students with at least one failing score
### Random Data Generation
The __main__ block demonstrates:
- Sample dataset creation
- Random assignment of scores using Gaussian distribution
- Random attendance generation
- Random simulation of failing scores

---

### Entities
- Schools:
  - `school_id`, `name`, `courses`, `students`
- Students:
  - `student_id`, `name`, `surname`, `schools`, `courses`
- Courses:
  - `course_id`, `school_id`, `name`, `students`
 
### ID Generation
The system uses generator functions to produce unique, incremental IDs with specific prefixes:
- Schools: `SCH0`, `SCH1`, ...
- Students: `STU0`, `STU1`, ...
- Courses: `C0`, `C1`, ...
When loading from JSON, ID generators automatically resume from the highest existing ID.

### Persistence
#### Saving the Database
The `save_database()` function converts sets to lists and writes JSON to a file.
#### Loading the Database
The `innitial_database()` function:
- Loads JSON if the file exists
- Restores sets from lists
- Initializes the global database if the file does not exist

### Key Functions
#### Creation
- `create_school(name)`
- `create_student(name, surname)`
- `create_course(name)`
#### Association
- `add_student_to_school(school_id, student_id)`
- `add_course_to_school(school_id, course_id)`
- `add_student_to_course(course_id, student_id)`
#### Records
- `add_score(student_id, course_id, score)`
- `add_attendance(student_id, course_id, date)`
#### Queries and Statistics
- `get_student_course_average_score(student_id, course_id)`
- `get_student_all_courses_average_score(student_id)`
- `get_student_total_attendance(student_id, course_id)`
- `get_students_with_failing_score()`

### Future Improvements
Several enhancements are planned for this project:
#### Graphical User Interface (GUI)
A complete GUI built using Tkinter, allowing interactive:
- Browsing of schools, students, and courses with proper user privileges
- Adding new entities through forms
- Viewing scores and attendance in table-like widgets
- Real-time statistics and reports
This interface will make the system usable without modifying the Python code directly.
#### Additional Planned Features
- Input validation and error handling
- Export of reports (CSV or PDF)
- More advanced filtering and search functionality
- Improved modular structure or optional OOP refactor (classes/dataclasses)
