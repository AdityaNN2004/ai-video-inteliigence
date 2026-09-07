function VideoCard({ video, onSelect }) {

    const metadata = video.metadata || {};

    return (
        <div className="video-card">

            <div className="video-card-info">

                <h3>{video.filename}</h3>

                <p>
                    Duration:{" "}
                    {metadata.duration !== undefined
                        ? `${metadata.duration.toFixed(1)}s`
                        : "N/A"}
                </p>

                <p>
                    Resolution:{" "}
                    {metadata.width && metadata.height
                        ? `${metadata.width} × ${metadata.height}`
                        : "N/A"}
                </p>

                <p>
                    FPS:{" "}
                    {metadata.fps !== undefined
                        ? metadata.fps
                        : "N/A"}
                </p>

                <p>
                    Status: {video.status}
                </p>

            </div>

            <button
                onClick={() => onSelect(video.video_id)}
            >
                Open Video
            </button>

        </div>
    );
}

export default VideoCard;