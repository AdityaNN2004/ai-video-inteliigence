import { useState } from "react";

import { semanticSearch } from "../services/api";


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


function SemanticSearch({ onResultSelect }) {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    async function handleSearch(event) {

        event.preventDefault();

        const trimmedQuery = query.trim();

        if (!trimmedQuery) {
            return;
        }

        try {

            setLoading(true);
            setError("");
            setResults([]);

            const data = await semanticSearch(
                trimmedQuery,
                10
            );

            setResults(data);

        } catch (error) {

            console.error(
                "Semantic search failed:",
                error
            );

            setError(
                error.message ||
                "Semantic search failed."
            );

        } finally {

            setLoading(false);
        }
    }


    return (
        <section className="semantic-search">

            <div className="section-header">
                <h2>Semantic Search</h2>
            </div>


            <form
                className="search-form"
                onSubmit={handleSearch}
            >

                <input
                    type="text"
                    value={query}
                    onChange={(event) =>
                        setQuery(event.target.value)
                    }
                    placeholder="Search your videos..."
                />

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading ? "Searching..." : "Search"}
                </button>

            </form>


            {error && (
                <p className="search-error">
                    {error}
                </p>
            )}


            {!loading &&
                !error &&
                query &&
                results.length === 0 && (
                    <p className="search-empty">
                        No relevant results found.
                    </p>
                )}


            {results.length > 0 && (
                <div className="search-results">

                    {results.map((result, index) => (

                        <button
                            key={`${result.video_id}-${result.start_time}-${index}`}
                            className="search-result"
                            onClick={() =>
                                onResultSelect(result)
                            }
                        >

                            <div className="search-result-header">

                                <strong>
                                    {result.filename}
                                </strong>

                                <span>
                                    {formatTimestamp(
                                        result.start_time
                                    )}
                                </span>

                            </div>


                            <p>
                                {result.text}
                            </p>

                        </button>

                    ))}

                </div>
            )}

        </section>
    );
}


export default SemanticSearch;