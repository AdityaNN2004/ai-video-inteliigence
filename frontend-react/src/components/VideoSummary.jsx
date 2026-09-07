function VideoSummary({ video }) {

    if (!video || !video.summary_data) {
        return null;
    }

    const summary = video.summary_data;


    return (
        <section className="video-summary">

            <h2>AI Summary</h2>

            {summary.summary && (
                <div className="summary-section">

                    <h3>Summary</h3>

                    <p>{summary.summary}</p>

                </div>
            )}


            {summary.key_points &&
                summary.key_points.length > 0 && (
                    <div className="summary-section">

                        <h3>Key Points</h3>

                        <ul>

                            {summary.key_points.map(
                                (point, index) => (
                                    <li key={index}>
                                        {point}
                                    </li>
                                )
                            )}

                        </ul>

                    </div>
                )}


            {summary.topics &&
                summary.topics.length > 0 && (
                    <div className="summary-section">

                        <h3>Topics</h3>

                        <div className="topic-list">

                            {summary.topics.map(
                                (topic, index) => (
                                    <span
                                        key={index}
                                        className="topic-tag"
                                    >
                                        {topic}
                                    </span>
                                )
                            )}

                        </div>

                    </div>
                )}

        </section>
    );
}


export default VideoSummary;