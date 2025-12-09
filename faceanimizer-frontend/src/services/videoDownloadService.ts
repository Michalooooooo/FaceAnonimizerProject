export async function downloadVideo(videoId: string): Promise<void> {
  try {
    const response = await fetch(`http://localhost:8000/download/${videoId}`); 

    if (!response.ok) {
      console.error("Video not found");
      return;
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = `${videoId}.mp4`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);

  } catch (error) {
    console.error("Error downloading video:", error);
  }
}
