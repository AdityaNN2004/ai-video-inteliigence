import { useRef } from "react";

import { getVideoFileUrl } from "../services/api";


function VideoPlayer({
    videoId,
    videoName,
    onPlayerReady
}) {

    const videoRef = useRef(null);


    function handleLoadedMetadata() {

        if (onPlayerReady) {
            onPlayerReady(videoRef.current);
        }
    }


    if (!videoId) {
        return (
            <div className="video-player-empty">
                <p>Select a video to start watching.</p>
            </div>
        );
    }


    return (
        <section className="video-player-container">

            <h2>
                {videoName || "Video Player"}
            </h2>

            <video
                ref={videoRef}
                controls
                preload="metadata"
                width="100%"
                src={getVideoFileUrl(videoId)}
                onLoadedMetadata={handleLoadedMetadata}
            >
                Your browser does not support video playback.
            </video>

        </section>
    );
}


export default VideoPlayer;