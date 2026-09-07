import { useState } from "react";

import { askVideoQuestion } from "../services/api";


function formatTimestamp(seconds) {
    if (seconds === undefined || seconds === null) {
        return "00:00";
    }

    const totalSeconds = Math.floor(seconds);

    const minutes = Math.floor(totalSeconds / 60);
    const remainingSeconds = totalSeconds % 60;

    return `${String(minutes).padStart(2, "0")}:${String(
        remainingSeconds
    ).padStart(2, "0")}`;
}


function VideoQA({ videoId, onSeek }) {

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [sources, setSources] = useState([]);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    async function handleAsk(event) {

        event.preventDefault();

        const trimmedQuestion = question.trim();

        if (!trimmedQuestion || !videoId) {
            return;
        }

        try {

            setLoading(true);
            setError("");
            setAnswer("");
            setSources([]);

            const data = await askVideoQuestion(
                videoId,
                trimmedQuestion
            );

            setAnswer(data.answer || "");
            setSources(data.sources || []);

        } catch (error) {

            console.error(
                "Video Q&A failed:",
                error
            );

            setError(
                error.message ||
                "Failed to answer the question."
            );

        } finally {

            setLoading(false);

        }
    }


    return (
        <section className="video-qa">

            <div className="section-header">
                <h2>Ask AI</h2>
            </div>


            <form
                className="qa-form"
                onSubmit={handleAsk}
            >

                <input
                    type="text"
                    value={question}
                    onChange={(event) =>
                        setQuestion(event.target.value)
                    }
                    placeholder="Ask a question about this video..."
                    disabled={loading}
                />

                <button
                    type="submit"
                    disabled={loading || !question.trim()}
                >
                    {loading
                        ? "Thinking..."
                        : "Ask AI"}
                </button>

            </form>


            {error && (
                <p className="qa-error">
                    {error}
                </p>
            )}


            {answer && (
                <div className="qa-answer">

                    <h3>Answer</h3>

                    <p>{answer}</p>

                </div>
            )}


            {sources.length > 0 && (
                <div className="qa-sources">

                    <h3>Sources</h3>

                    <div className="qa-source-list">

                        {sources.map((source, index) => (

                            <button
                                key={`${source.start_time}-${index}`}
                                className="qa-source"
                                onClick={() =>
                                    onSeek(source.start_time)
                                }
                            >

                                <div className="qa-source-header">

                                    <span>
                                        {formatTimestamp(
                                            source.start_time
                                        )}
                                    </span>

                                    {source.similarity !== undefined && (
                                        <span>
                                            Score:{" "}
                                            {source.similarity.toFixed(2)}
                                        </span>
                                    )}

                                </div>

                                <p>
                                    {source.text}
                                </p>

                            </button>

                        ))}

                    </div>

                </div>
            )}

        </section>
    );
}


export default VideoQA;