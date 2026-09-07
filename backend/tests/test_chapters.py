from app.services.chapters import generate_video_chapters


segments = [
    {
        "start": 0,
        "end": 30,
        "text": "Today we are discussing whether Java is still worth learning in the age of AI."
    },
    {
        "start": 30,
        "end": 90,
        "text": "Companies are looking for engineers who can solve backend engineering problems."
    },
    {
        "start": 300,
        "end": 360,
        "text": "Java remains popular because companies value reliability and large enterprise systems."
    },
    {
        "start": 600,
        "end": 680,
        "text": "The recommended learning path includes Java fundamentals, Spring Boot and real projects."
    },
    {
        "start": 900,
        "end": 980,
        "text": "Developers should use AI as a learning tool rather than relying on it to replace their thinking."
    }
]


chapters = generate_video_chapters(
    segments=segments,
    duration=1200
)

print("\n==============================")
print("AI CHAPTERS")
print("==============================")

for chapter in chapters["chapters"]:
    print(
        f"{chapter['start_time']:.0f}s - "
        f"{chapter['end_time']:.0f}s | "
        f"{chapter['title']}"
    )
    print(f"  {chapter['summary']}")