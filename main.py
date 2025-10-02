from fastapi import FastAPI
from routes import users, courses, enrollments

app = FastAPI(title="EduTrack Lite API", version="1.0.0")

app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)

@app.get("/")
def root():
    return {"message": "EduTrack Lite"}
