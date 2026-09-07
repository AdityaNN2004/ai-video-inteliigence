import { useEffect, useState } from "react";

import { getVideos } from "../services/api";
import VideoCard from "./VideoCard";


const PAGE_SIZE = 10;


function VideoLibrary({ onSelectVideo }) {

    const [videos, setVideos] = useState([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        let cancelled = false;

        async function fetchVideos() {

            try {

                setLoading(true);
                setError("");

                const skip = (page - 1) * PAGE_SIZE;

                const data = await getVideos(
                    skip,
                    PAGE_SIZE
                );

                if (!cancelled) {
                    setVideos(data);
                    setLoading(false);
                }

            } catch (error) {

                console.error(
                    "Failed to load videos:",
                    error
                );

                if (!cancelled) {

                    setError(
                        error.message ||
                        "Failed to load videos."
                    );

                    setLoading(false);
                }
            }
        }

        fetchVideos();

        return () => {
            cancelled = true;
        };

    }, [page]);


    function handlePrevious() {

        if (page > 1) {
            setPage(page - 1);
        }
    }


    function handleNext() {

        if (videos.length === PAGE_SIZE) {
            setPage(page + 1);
        }
    }


    if (loading) {
        return (
            <section>
                <h2>Video Library</h2>
                <p>Loading videos...</p>
            </section>
        );
    }


    if (error) {
        return (
            <section>
                <h2>Video Library</h2>

                <p>{error}</p>

                <button
                    onClick={() => setPage(page)}
                >
                    Retry
                </button>
            </section>
        );
    }


    return (
        <section className="video-library">

            <div className="section-header">

                <h2>Video Library</h2>

            </div>


            {videos.length === 0 ? (
                <p>No videos found.</p>
            ) : (
                <div className="video-grid">

                    {videos.map((video) => (

                        <VideoCard
                            key={video.video_id}
                            video={video}
                            onSelect={onSelectVideo}
                        />

                    ))}

                </div>
            )}


            <div className="pagination">

                <button
                    onClick={handlePrevious}
                    disabled={page === 1}
                >
                    Previous
                </button>


                <span>
                    Page {page}
                </span>


                <button
                    onClick={handleNext}
                    disabled={videos.length < PAGE_SIZE}
                >
                    Next
                </button>

            </div>

        </section>
    );
}


export default VideoLibrary;