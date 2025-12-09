// videoProcessingService.ts
export async function handleProcessVideo(
  videoId: string,
  formValues: Record<string, any> // przyjmujemy dowolny obiekt, np. form.values z komponentu
): Promise<Record<string, string>> {
  if (!videoId) {
    throw new Error("Brak videoId");
  }

  try {
    const res = await fetch(`http://localhost:8000/analyze-video/${videoId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formValues),
    });

    if (!res.ok) {
      throw new Error(`Processing failed: ${res.statusText}`);
    }

    const data: { faces: Record<string, string> } = await res.json();
    return data.faces;
  } catch (err) {
    console.error(err);
    throw err;
  }
}
