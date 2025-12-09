export async function anonimizeVideo(
    videoId: string,
    facesList: number[],
    rotate: boolean 
): Promise<boolean> {
    try {
        const response = await fetch(`http://localhost:8000/anonimize-video/${videoId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                faces_list: facesList ?? [],
                rotate: rotate ?? false
            }),
        });

        if (!response.ok) {
            console.error("Anonimizacja nie powiodła się");
            return false;
        }

        const data = await response.json();
        if (data.status === "ok") {
            console.log("Anonimizacja zakończona");
            return true;
        } else {
            console.error("Anonimizacja nie powiodła się:", data);
            return false;
        }
    } catch (error) {
        console.error("Błąd anonimizacji:", error);
        return false;
    }
}
