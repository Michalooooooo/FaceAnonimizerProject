export async function uploadVideo(file: File) {
  const formData = new FormData();
  
  formData.append("file", file);

  const res = await fetch("http://localhost:8000/upload-video", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Upload failed");
  }

  const data = await res.json();

  return data.id; 
}
