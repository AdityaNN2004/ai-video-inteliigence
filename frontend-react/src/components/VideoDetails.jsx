function VideoDetails({ video }) {
    if (!video) {
        return null;
    }

    const metadata = video.metadata || {};

    return (
        <section className="video-details">
            <h2>Video Details</h2>

            <div className="details-grid">

                <div>
                    <strong>Filename</strong>
                    <p>{video.filename}</p>
                </div>

                <div>
                    <strong>Duration</strong>
                    <p>
                        {metadata.duration !== undefined
                            ? `${metadata.duration.toFixed(2)} seconds`
                            : "N/A"}
                    </p>
                </div>

                <div>
                    <strong>Resolution</strong>
                    <p>
                        {metadata.width && metadata.height
                            ? `${metadata.width} × ${metadata.height}`
                            : "N/A"}
                    </p>
                </div>

                <div>
                    <strong>FPS</strong>
                    <p>
                        {metadata.fps !== undefined
                            ? metadata.fps
                            : "N/A"}
                    </p>
                </div>

                <div>
                    <strong>Video Codec</strong>
                    <p>{metadata.video_codec || "N/A"}</p>
                </div>

                <div>
                    <strong>Audio</strong>
                    <p>
                        {metadata.has_audio ? "Yes" : "No"}
                    </p>
                </div>

                <div>
                    <strong>Audio Codec</strong>
                    <p>{metadata.audio_codec || "N/A"}</p>
                </div>

                <div>
                    <strong>Status</strong>
                    <p>{video.status}</p>
                </div>

            </div>
        </section>
    );
}

export default VideoDetails;