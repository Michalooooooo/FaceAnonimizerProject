import { useEffect, useState } from "react";
import ImageWithId from "./ImageWithID";
import { Button, Center, Group, List } from '@mantine/core';
import { Loader } from '@mantine/core';
import "../css/Step3.css"
import { handleProcessVideo } from '@/services/videoProcessService';

function Step3({
    onSubmit,
    previous,
    videoId,
    form
}: {
    onSubmit: (values: Record<string, any>) => void; // teraz values zawiera też selectedFaces
    previous: () => void;
    videoId: string | null;
    form: Record<string, any>;
}) {

    const [images, setImages] = useState<Record<string, string>>({

    });
    const [loading, setLoading] = useState(0);
    const [selectedIds, setSelectedIds] = useState<number[]>([]);
    const [allSelected, setAllSelected] = useState(false);
    const [selectedCounter, setSelectedCounter] = useState(0);

    const handleSelect = (id: number, selected: boolean) => {
        setSelectedIds((prev) => {
            if (selected) {

                console.log("Dodano zaznaczenie ", selectedIds)
                setSelectedCounter(selectedCounter + 1)
                return [...prev, id];
            } else {
                console.log("Usunięto zaznaczenie ", selectedIds)
                setSelectedCounter(selectedCounter - 1)
                return prev.filter((item) => item !== id);
            }
        });
    };

    const selectAll = () => {
        const allIds = Object.keys(images).map((id) => Number(id));
        setSelectedIds(allIds);
        setSelectedCounter(Object.keys(images).length)
    };

    const deselectAll = () => {
        setSelectedIds([]);
        setSelectedCounter(0);
    }

    const processVideo = async () => {
        if (!videoId) return;
        try {
            console.log("Wartości formularza przed fetch:", form);
            const faces = await handleProcessVideo(videoId, form);
            setImages(faces);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(prev => prev + 1);  // <- tu funkcja aktualizująca
        }
    }
    useEffect(() => { console.log("") })

    return (
        <>
            {loading === 0 && (
                <>
                    <center>
                        <h1 style={{ fontWeight: "bold", fontSize: "50px", color: "rgb(24, 100, 171)", marginTop: "10vh" }}
                        >Press 'Process Your Video' to proceed</h1>
                    </center>
                    <Center>
                        <Button
                            type='button'
                            variant="outline"
                            onClick={() => {
                                setLoading(loading + 1);
                                processVideo();
                            }}
                            style={{ width: "20vw", height: "7vh", fontSize: "20px", margin: "20px" }}
                            color='rgb(24, 100, 171)'
                        >Process your video</Button>
                    </Center>
                </>
            )}
            {loading === 1 && (
                <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop: "5vh" }}>
                    <Loader color="blue" size="xl" />
                </div>
            )}
            {loading === 2 && (
                <>
                    <center><h1 style={{ fontWeight: "bold", fontSize: "50px", color: "rgb(24, 100, 171)" }}>Select the faces to anonymize</h1></center>
                    <Center>
                        <Button type='button' variant="outline"
                            onClick={selectedCounter === Object.keys(images).length ? (deselectAll) : (selectAll)}
                            style={{ width: "20vw", height: "7vh", fontSize: "20px" }}
                            color='rgb(24, 100, 171)'
                        >{selectedCounter === Object.keys(images).length ? ('Deselect all') : ('Select all')}</Button>
                    </Center>
                    <div style={{ display: "flex", flexWrap: "wrap" }}>
                        {Object.entries(images).map(([id, url]) => (
                            <ImageWithId
                                key={id}
                                id={Number(id)}
                                url={url}
                                selected={selectedIds.includes(Number(id))}
                                onSelect={handleSelect}
                            />
                        ))}
                    </div>
                </>
            )}
            <Group style={{ justifyContent: "space-between", marginLeft: "2vw", marginRight: "2vw", marginTop: "2vh", marginBottom: "1vh" }}>
                <Button
                    type='button'
                    variant="light"
                    onClick={previous}
                    style={{ width: "20vw", height: "7vh", fontSize: "20px", margin: "5vw" }}
                    color='rgb(24, 100, 171)'
                >Previous</Button>
                <Button
                    className="next-button"
                    onClick={() => onSubmit({ ...form, selectedFaces: selectedIds })}
                    style={{ width: "20vw", height: "7vh", fontSize: "20px" }}
                    color='rgb(24, 100, 171)'
                    disabled={selectedCounter === 0}
                >
                    Next
                </Button>
            </Group>
        </>
    );
}

export default Step3;