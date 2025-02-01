from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, constr, validator
from typing import List, Optional
import re

app = FastAPI()

# Pydantic model for student registration
class StudentRegister(BaseModel):
    name: constr(min_length=1, max_length=50)  # Name must be between 1 and 50 characters
    email: EmailStr  # Valid email address
    age: int  # Age must be an integer
    courses: List[constr(min_length=5, max_length=30)]  # List of courses

    @validator('name')
    def validate_name(cls, name):
        if not all(c.isalpha() or c.isspace() for c in name):
            raise ValueError("Name must contain only alphabets and spaces.")
        return name

    @validator('courses')
    def check_courses(cls, courses):
        if len(courses) < 1 or len(courses) > 5:
            raise ValueError("The number of courses must be between 1 and 5.")
        if len(courses) != len(set(courses)):
            raise ValueError("Duplicate course names are not allowed.")
        return courses

# Endpoint to get student information
@app.get("/students/{student_id}")
async def get_student_info(
    student_id: int,
    include_grades: bool = Query(False),
    semester: Optional[str] = Query(None)
):
    try:
        # Validate student_id
        if not (1000 < student_id < 9999):
            raise HTTPException(status_code=422, detail="student_id must be an integer between 1001 and 9998.")
        
        # Validate semester format
        if semester and not re.match(r'^(Fall|Spring|Summer)\d{4}$', semester):
            raise HTTPException(status_code=422, detail="Semester must be in the format 'Fall2024', 'Spring2025', etc.")

        # Simulate fetching student information (mock data)
        student_info = {
            "student_id": student_id,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "grades": {"Math": "A", "Physics": "B"} if include_grades else None
        }
        
        if semester:
            student_info["semester"] = semester
        
        return student_info

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Endpoint to register a new student
@app.post("/students/register")
async def register_student(student: StudentRegister):
    try:
        # Validate age
        if student.age < 18 or student.age > 30:
            raise HTTPException(status_code=422, detail="Age must be between 18 and 30.")

        # Simulate saving the student information (mock response)
        return {
            "message": "Student registered successfully",
            "student": {
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "courses": student.courses
            }
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Pydantic model for updating email
class UpdateEmail(BaseModel):
    email: EmailStr  # Valid email address

# Endpoint to update student email
@app.put("/students/{student_id}/email")
async def update_student_email(student_id: int, email_update: UpdateEmail):
    try:
        # Validate student_id
        if not (1000 < student_id < 9999):
            raise HTTPException(status_code=422, detail="student_id must be an integer between 1001 and 9998.")
        
        # Simulate updating the student's email (mock response)
        return {
            "message": "Email updated successfully",
            "student_id": student_id,
            "new_email": email_update.email
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)