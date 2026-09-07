const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request(endpoint, options = {}) {
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        options
    );

    if (!response.ok) {
    let message = "API request failed";

    try {
        const data = await response.json();

        if (data.detail) {
            message =
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail);
        }
    } catch {
        // Response was not JSON
    }

    throw new Error(message);
}

    return response.json();
}

export async function getVideos(skip = 0, limit = 10) {
    return request(
        `/api/videos?skip=${skip}&limit=${limit}`
    );
}

export async function getVideoDetails(videoId) {
    return request(
        `/api/videos/${videoId}/details`
    );
}

export async function getTranscript(videoId) {
    return request(
        `/api/videos/${videoId}/transcript`
    );
}

export async function semanticSearch(query, limit = 10) {
    return request(
        `/api/videos/semantic-search?q=${encodeURIComponent(query)}&limit=${limit}`
    );
}

export async function askVideoQuestion(videoId, question) {
    return request(
        `/api/videos/${videoId}/ask`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question
            })
        }
    );
}

export function getVideoFileUrl(videoId) {
    return `${API_BASE_URL}/api/videos/${videoId}/file`;
}

export { API_BASE_URL };