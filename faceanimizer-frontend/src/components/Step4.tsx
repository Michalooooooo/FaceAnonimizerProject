import { Button, Center, Loader } from "@mantine/core";
import { downloadVideo } from "@/services/videoDownloadService";
import { useState } from "react";
import { anonimizeVideo } from "@/services/videoAnonymizeService";
import "../css/Step4.css"

function Step4({ onSubmit, previous, videoId, facesList, rotate }: { onSubmit: (values: any) => void, previous: (values: any) => void, videoId: string, facesList: number[], rotate: boolean }) {

    const [loading, setLoading] = useState(false);
    const [videoReady, setVideoReady] = useState(false);

    const handleAnonimize = async () => {
        setLoading(true);  // pokazujemy loader
        try {
            await anonimizeVideo(videoId, facesList, rotate);  // czekamy na zakończenie anonimizacji
            setVideoReady(true);  // odblokowujemy przycisk download
        } catch (error) {
            console.error("Error anonymizing video:", error);
            // tu możesz dodać jakiś toast lub alert o błędzie
        } finally {
            setLoading(false);  // ukrywamy loader
        }
    };

    const handleDownload = () => {
        downloadVideo(videoId);
        onSubmit({});
    };

    return (
        <>
            <center>
                <h1 style={{
                    marginLeft: "5vw",
                    marginRight: "5vw",
                    marginTop: "25vh",
                    fontWeight: "bold",
                    fontSize: "5vh",
                    color: "rgb(24, 100, 171)"
                }}>
                    Click "Anonymize your video" to anonymize and "Download your video" to download your video!
                </h1>
            </center>

            <Center>
                {!videoReady && !loading && (
                    <Button
                        onClick={handleAnonimize}
                        style={{
                            width: "35vw",
                            height: "15vh",
                            fontSize: "30px",
                            color: "rgb(24, 100, 171)",
                            margin: "5vh"
                        }}
                        variant="outline"
                    >
                        Anonymize your video
                    </Button>
                )}

                {loading && (
                    <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop: "5vh" }}>
                        <Loader color="blue" size="xl" />
                    </div>
                )}
            </Center>

            <Center>
                <Button
                    className="download-button"
                    onClick={handleDownload}
                    style={{
                        width: "35vw",
                        height: "15vh",
                        fontSize: "30px",
                        margin: "5vh"
                    }}
                    color="rgb(255, 255, 255)"
                    variant="outline"
                    disabled={!videoReady}
                >
                    Download your video
                </Button>
            </Center>

            <Center>
                <Button
                    type='button'
                    variant="light"
                    onClick={previous}
                    style={{ width: "20vw", height: "7vh", fontSize: "20px", marginBottom: "10vh" }}
                    color='rgb(24, 100, 171)'
                >
                    Previous
                </Button>
            </Center>
        </>
    );
}

export default Step4;
