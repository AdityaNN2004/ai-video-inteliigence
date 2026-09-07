import { useEffect, useState } from "react";

import { getTranscript } from "../services/api";


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


function Transcript({ videoId, onSeek }) {

    const [segments, setSegments] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    useEffect(() => {

        let cancelled = false;

        async function loadTranscript() {

            try {

                setLoading(true);
                setError("");

                const data = await getTranscript(videoId);

                if (!cancelled) {
                    setSegments(data.segments || []);
                    setLoading(false);
                }

            } catch (error) {

                console.error(
                    "Failed to load transcript:",
                    error
                );

                if (!cancelled) {

                    setError(
                        error.message ||
                        "Failed to load transcript."
                    );

                    setLoading(false);
                }
            }
        }

        loadTranscript();

        return () => {
            cancelled = true;
        };

    }, [videoId]);


    if (loading) {
        return (
            <section className="transcript">
                <h2>Transcript</h2>
                <p>Loading transcript...</p>
            </section>
        );
    }


    if (error) {
        return (
            <section className="transcript">
                <h2>Transcript</h2>
                <p>{error}</p>
            </section>
        );
    }


    if (segments.length === 0) {
        return (
            <section className="transcript">
                <h2>Transcript</h2>
                <p>No transcript available.</p>
            </section>
        );
    }


    return (
        <section className="transcript">

            <h2>Transcript</h2>

            <div className="transcript-list">

                {segments.map((segment) => (

                    <button
                        key={`${segment.start_time}-${segment.end_time}`}
                        className="transcript-segment"
                        onClick={() =>
                            onSeek(segment.start_time)
                        }
                    >

                        <span className="transcript-time">
                            {formatTimestamp(
                                segment.start_time
                            )}
                        </span>

                        <span className="transcript-text">
                            {segment.text}
                        </span>

                    </button>

                ))}

            </div>

        </section>
    );
}


export default Transcript;