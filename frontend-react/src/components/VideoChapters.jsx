function formatTimestamp(seconds) {
    if (seconds === undefined || seconds === null) {
        return "00:00";
    }

    const totalSeconds = Math.floor(seconds);

    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor(
        (totalSeconds % 3600) / 60
    );
    const remainingSeconds = totalSeconds % 60;

    if (hours > 0) {
        return `${String(hours).padStart(2, "0")}:${String(
            minutes
        ).padStart(2, "0")}:${String(
            remainingSeconds
        ).padStart(2, "0")}`;
    }

    return `${String(minutes).padStart(2, "0")}:${String(
        remainingSeconds
    ).padStart(2, "0")}`;
}


function VideoChapters({ chapters, onSeek }) {

    if (!chapters || chapters.length === 0) {
        return null;
    }


    return (
        <section className="video-chapters">

            <h2>AI Chapters</h2>

            <div className="chapter-list">

                {chapters.map((chapter, index) => (

                    <button
                        key={`${chapter.start_time}-${index}`}
                        className="chapter-item"
                        onClick={() =>
                            onSeek(chapter.start_time)
                        }
                    >

                        <span className="chapter-time">
                            {formatTimestamp(
                                chapter.start_time
                            )}
                        </span>

                        <div className="chapter-content">

                            <strong>
                                {chapter.title}
                            </strong>

                            <p>
                                {chapter.summary}
                            </p>

                        </div>

                    </button>

                ))}

            </div>

        </section>
    );
}


export default VideoChapters;