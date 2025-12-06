#Excellent - 90,85"
#On Track- 75,60"
#At Risk -60,40"
#Failing - fail "

#should use the if/elif\else block CSV style dataset attendence and test scores for multiple students .
def classify_student(attendance_percent: float, avg_mark: float) -> str:
    if attendance_percent >= 90 and avg_mark >= 85:
        return "Excellent"
    elif attendance_percent >= 75 and avg_mark >= 60:
        return "On Track"
    elif attendance_percent >= 60 and avg_mark >= 40:
        return "At Risk"
    else:
        return "Failing"


def classify_all(students: list[dict]):
    results = []
    for s in students:
        name = s["name"]
        attendance = s["attendance"]
        marks = s["marks"]  
        avg = sum(marks) / len(marks) if marks else 0
        label = classify_student(attendance, avg)
        results.append({"name": name, "attendance": attendance, "avg": avg, "label": label})
    return results


if __name__ == "__main__":
    
    marks_list = [90, 66, 80, 93, 95]
    students = [
        {"name": "priya", "attendance": 95, "marks": marks_list},
        {"name": "chinnu", "attendance": 70, "marks": [40, 50, 60]},
    ]

    for res in classify_all(students):
        print(res)
