from datetime import datetime
from typing import Generator
from random import gauss, choice
import json
import os


def id_generator(prefix: str = "", start_value: int = 0) -> Generator[str, None, None]:
    count: int = start_value
    while True:
        yield prefix + str(count)
        count += 1

def innitial_database(filename: str = None) -> None:
    global db
    global school_id_generator
    global course_id_generator
    global student_id_generator
    if filename and os.path.isfile(filename):
        with open(filename, "r") as file:
            db = json.loads(file.read())
            for school_id in db["schools"]:
                db["schools"][school_id]["courses"] = set(db["schools"][school_id]["courses"])
                db["schools"][school_id]["students"] = set(db["schools"][school_id]["students"])
            for student_id in db["students"]:
                db["students"][student_id]["schools"] = set(db["students"][student_id]["schools"])
                db["students"][student_id]["courses"] = set(db["students"][student_id]["courses"])
            for course_id in db["courses"]:
                db["courses"][course_id]["students"] = set(db["courses"][course_id]["students"])
    else:
        db = {
            "schools": {},
            "students": {},
            "courses": {},
            "scores": {},
            "attendance": {},
        }
    school_id_generator = id_generator("SCH", (int(sorted(db["schools"].keys())[-1].replace("SCH", "")) if db["schools"] else 0))
    course_id_generator = id_generator("C", (int(sorted(db["courses"].keys())[-1].replace("C", "")) if db["courses"] else 0))
    student_id_generator = id_generator("STU", (int(sorted(db["students"].keys())[-1].replace("STU", "")) if db["students"] else 0))

def save_database(filename: str)-> None:
    with open(filename, "w") as file:
        file.write(json.dumps(db, default=lambda o: list(o) if isinstance(o, set) else o, indent=4))
def create_school(school_name: str) -> str:
    school_id: str = next(school_id_generator)
    db["schools"][school_id] = {
        "school_id": school_id,
        "name": school_name,
        "courses": set(),
        "students": set(),
    }
    return school_id

def create_student(name: str, surname: str) -> str:
    student_id: str = next(student_id_generator)
    db["students"][student_id] = {
        "student_id": student_id,
        "name": name,
        "surname": surname,
        "schools": set(),
        "courses": set(),
    }
    return student_id

def create_course(course_name: str) -> str:
    course_id: str = next(course_id_generator)
    db["courses"][course_id] = {
        "course_id": course_id,
        "school_id": None,
        "name": course_name,
        "students": set(),
    }
    return course_id

def add_student_to_school(school_id: str, student_id: str) -> None:
    db["schools"][school_id]["students"].add(student_id)
    db["students"][student_id]["schools"].add(school_id)

def add_course_to_school(school_id: str, course_id: str) -> None:
    db["schools"][school_id]["courses"].add(course_id)
    db["courses"][course_id]["school_id"] = school_id

def add_student_to_course(course_id: str, student_id: str) -> None:
    db["courses"][course_id]["students"].add(student_id)
    db["students"][student_id]["courses"].add(course_id)

def add_score(student_id: str, course_id: str, score: int) -> None:
    if f"{student_id}-{course_id}" not in db["scores"]:
        db["scores"][f"{student_id}-{course_id}"] = []
    db["scores"][f"{student_id}-{course_id}"].append(score)

def add_attendance(student_id: str, course_id: str, date: datetime = datetime.now()) -> None:
    if f"{student_id}-{course_id}" not in db["attendance"]:
        db["attendance"][f"{student_id}-{course_id}"] = []
    db["attendance"][f"{student_id}-{course_id}"].append(date.strftime("%x"))

def get_student_all_courses_average_score(student_id: str) -> float:
    scores = [
        score 
        for course_id in db["students"][student_id]["courses"]
        for score in db["scores"][f"{student_id}-{course_id}"]
    ]
    return sum(scores) / len(scores)


def get_student_course_average_score(student_id: str, course_id: str) -> float:
    return sum(db["scores"][f"{student_id}-{course_id}"]) / len(db["scores"][f"{student_id}-{course_id}"])

def get_student_total_attendance(student_id: str, course_id: str) -> int:
    return len(db["attendance"][f"{student_id}-{course_id}"])

def get_students_with_failing_score() -> list:
    def has_failing_score(student_id):
        for course_id in db["students"][student_id]["courses"]:
            if any(score < 50 for score in db["scores"][f"{student_id}-{course_id}"]):
                return True
        return False
    return list(filter(has_failing_score, db["students"]))


if __name__ == "__main__":
    innitial_database("education_database.json")

    schools_id = []
    courses_id = []
    students_id = []

    schools_id.append(create_school("Cape Cod Academy"))
    schools_id.append(create_school("Sandwich High School"))

    courses_id.append(create_course("Mathematics"))
    courses_id.append(create_course("Physics"))
    courses_id.append(create_course("History"))
    courses_id.append(create_course("Computer Science"))
    courses_id.append(create_course("Art"))
    courses_id.append(create_course("Geography"))

    students_id.append(create_student("Olivia", "Brown"))
    students_id.append(create_student("Ava", "Smith"))
    students_id.append(create_student("Charlotte", "Johnson"))
    students_id.append(create_student("Emma", "Williams"))
    students_id.append(create_student("Evelyn", "Jones"))
    students_id.append(create_student("Isabella", "Garcia"))
    students_id.append(create_student("James", "Miller"))
    students_id.append(create_student("Mia", "Davis"))
    students_id.append(create_student("Sophia", "Rodriguez"))
    students_id.append(create_student("Amelia", "Martinez"))
    students_id.append(create_student("Daniel", "Hernandez"))
    students_id.append(create_student("Eliana", "Lopez"))
    students_id.append(create_student("Jack", "Gonzalez"))
    students_id.append(create_student("Liam", "Wilson"))
    students_id.append(create_student("Luna", "Anderson"))
    students_id.append(create_student("Noah", "Thomas"))
    students_id.append(create_student("Theodore", "Taylor"))
    students_id.append(create_student("Aurora", "Moore"))
    students_id.append(create_student("Ellie", "Jackson"))
    students_id.append(create_student("John", "Martin"))

    add_course_to_school(schools_id[0], courses_id[0])
    add_course_to_school(schools_id[0], courses_id[1])
    add_course_to_school(schools_id[0], courses_id[2])
    add_course_to_school(schools_id[1], courses_id[3])
    add_course_to_school(schools_id[1], courses_id[4])
    add_course_to_school(schools_id[1], courses_id[5])   

    for i in range(10):
        add_student_to_course(courses_id[0], students_id[i])
        add_student_to_course(courses_id[1], students_id[i])
        add_student_to_course(courses_id[2], students_id[i])
        add_student_to_course(courses_id[3], students_id[10+i])
        add_student_to_course(courses_id[4], students_id[10+i])
        add_student_to_course(courses_id[5], students_id[10+i])
        for j in range(3):
            for _ in  range(12):
                if choice(9*[True]+[False]):
                    add_score(students_id[i], courses_id[j], gauss(90,3))
                    add_attendance(students_id[i], courses_id[j])
                else:
                    add_score(students_id[i], courses_id[j], 0)
                if choice(9*[True]+[False]):
                    add_score(students_id[10+i], courses_id[3+j], gauss(90,3))
                    add_attendance(students_id[10+i], courses_id[3+j])
                else:
                    add_score(students_id[i], courses_id[j], 0)
    save_database("education_database.json")

    print("Students that failed:",get_students_with_failing_score())
    print(f"Student's id: {students_id[0]}, average score in course {courses_id[1]}: {get_student_course_average_score(students_id[0], courses_id[1]):.2f} and attendance: {get_student_total_attendance(students_id[0], courses_id[1])}, average score in all courses: {get_student_all_courses_average_score(students_id[0]):.2f}")
