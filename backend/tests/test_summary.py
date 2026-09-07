from app.services.summarization import generate_video_summary


transcript = """
Today we are discussing REST APIs.

A REST API allows different applications to communicate
with each other using HTTP.

The most common HTTP methods are GET, POST, PUT and DELETE.

GET is generally used to retrieve data, while POST is used
to create new resources.

REST APIs are commonly used in modern web applications.
"""


summary = generate_video_summary(transcript)

print("\n==============================")
print("AI SUMMARY")
print("==============================")
print(summary)