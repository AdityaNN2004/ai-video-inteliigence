import { useRef, useState } from "react";

import Header from "./components/Header";
import VideoLibrary from "./components/VideoLibrary";
import VideoPlayer from "./components/VideoPlayer";
import VideoDetails from "./components/VideoDetails";
import VideoSummary from "./components/VideoSummary";
import { getVideoDetails } from "./services/api";
import Transcript from "./components/Transcript";
import VideoChapters from "./components/VideoChapters";
// import SemanticSearch from "./components/SemanticSearch";
function App() {
  const [selectedVideoId, setSelectedVideoId] = useState(null);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [loadingVideo, setLoadingVideo] = useState(false);
  const [videoError, setVideoError] = useState("");
  const videoElement = useRef(null);
  const [pendingSeekTime, setPendingSeekTime] = useState(null);

  async function handleSelectVideo(videoId) {
    try {
      setSelectedVideoId(videoId);
      setSelectedVideo(null);
      setVideoError("");
      setLoadingVideo(true);

      const video = await getVideoDetails(videoId);

      setSelectedVideo(video);
    } catch (error) {
      console.error("Failed to load video:", error);

      setVideoError(error.message || "Failed to load video.");
    } finally {
      setLoadingVideo(false);
    }
  }
// async function handleSearchResult(result) {

//     try {

//         setSelectedVideoId(result.video_id);
//         setSelectedVideo(null);
//         setVideoError("");
//         setLoadingVideo(true);

//         const video = await getVideoDetails(
//             result.video_id
//         );

//         setSelectedVideo(video);

//         // Store the timestamp that should be played
//         setPendingSeekTime(result.start_time);

//     } catch (error) {

//         console.error(
//             "Failed to open search result:",
//             error
//         );

//         setVideoError(
//             error.message ||
//             "Failed to open search result."
//         );

//     } finally {

//         setLoadingVideo(false);
//     }
// }
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
        {/* <SemanticSearch
            onResultSelect={handleSearchResult}
        /> */}

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

                      if (pendingSeekTime !== null) {

                          element.currentTime = pendingSeekTime;

                          setPendingSeekTime(null);
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
