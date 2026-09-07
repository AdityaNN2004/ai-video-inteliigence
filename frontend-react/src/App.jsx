import { useRef, useState } from "react";

import Header from "./components/Header";
import VideoLibrary from "./components/VideoLibrary";
import VideoPlayer from "./components/VideoPlayer";
import VideoDetails from "./components/VideoDetails";
import VideoSummary from "./components/VideoSummary";
import { getVideoDetails } from "./services/api";
import Transcript from "./components/Transcript";
import VideoChapters from "./components/VideoChapters";
import SemanticSearch from "./components/SemanticSearch";
import VideoQA from "./components/VideoQA";
function App() {
  const [selectedVideoId, setSelectedVideoId] = useState(null);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [loadingVideo, setLoadingVideo] = useState(false);
  const [videoError, setVideoError] = useState("");
  const videoElement = useRef(null);
  const pendingSeekTime = useRef(null);

  async function handleSelectVideo(videoId, seekTime = null) {
    try {
        pendingSeekTime.current = seekTime;

        setSelectedVideoId(videoId);
        setSelectedVideo(null);
        setVideoError("");
        setLoadingVideo(true);

        const video = await getVideoDetails(videoId);

        setSelectedVideo(video);

    } catch (error) {
        console.error("Failed to load video:", error);

        setVideoError(
            error.message || "Failed to load video."
        );

    } finally {
        setLoadingVideo(false);
    }
}
function handleSearchResult(result) {
    handleSelectVideo(
        result.video_id,
        result.start_time
    );
}
  function handleSeek(seconds) {

    if (!videoElement.current) {
        return;
    }

    videoElement.current.currentTime = seconds;
    videoElement.current.play();
}

  return (
    <>
      <Header />

      <main>
        <SemanticSearch
            onResultSelect={handleSearchResult}
        />

        <VideoLibrary onSelectVideo={handleSelectVideo} />

        {loadingVideo && (
          <section className="video-loading">
            <p>Loading video...</p>
          </section>
        )}

        {videoError && (
          <section className="video-error">
            <p>{videoError}</p>
          </section>
        )}

        {selectedVideo && !loadingVideo && (
            <>
                <VideoPlayer
                    videoId={selectedVideoId}
                    videoName={selectedVideo.filename}
                    onPlayerReady={(element) => {
                        videoElement.current = element;

                        if (pendingSeekTime.current !== null) {
                            element.currentTime =
                                pendingSeekTime.current;

                            element.play();

                            pendingSeekTime.current = null;
                        }
                    }}
                />

                <VideoDetails
                    video={selectedVideo}
                />

                <VideoSummary
                    video={selectedVideo}
                />
                <VideoChapters
                    chapters={selectedVideo.chapters}
                    onSeek={handleSeek}
                />
                <VideoQA
                    videoId={selectedVideoId}
                    onSeek={handleSeek}
                />
                <Transcript
                    videoId={selectedVideoId}
                    onSeek={handleSeek}
                />
            </>
        )}
      </main>
    </>
  );
}

export default App;
