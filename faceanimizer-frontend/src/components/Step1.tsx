import { useState } from "react";
import FileUploader from "./FileUploader";
import { Button, Center } from "@mantine/core";
import "../css/Step1.css"
import { uploadVideo } from "@/services/videoUploadService";

function Step1({ onSubmit, onUpload }: { onSubmit: () => void, onUpload: (id: string) => void }) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    const handleVideoUpload = async () => {
        if (!selectedFile) return;

        try {
            const id = await uploadVideo(selectedFile);
            onUpload(id);
            console.log("ID wideo: ", id);
        } catch (err) {
            console.error(err);
        }
    }

    return (
        <div>
            <center>
                <h1 style={{ fontWeight: "bold", fontSize: "50px", color: "rgb(24, 100, 171)", marginTop: "10vh" }}
                >Upload a video to get started</h1>
            </center>
            <FileUploader file={selectedFile} onFileSelect={setSelectedFile} />
            <Center>
                <Button
                    className='next-button'
                    onClick={() => {
                        onSubmit();
                        handleVideoUpload();
                    }}
                    style={{ width: "200px", height: "50px", fontSize: "20px" }}
                    disabled={selectedFile === null}
                > Next </Button>
            </Center>
        </div>
    );
}

export default Step1;
