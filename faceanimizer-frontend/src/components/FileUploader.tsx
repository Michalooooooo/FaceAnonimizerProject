import "../css/FileUploader.css";

type FileUploaderProps = {
    file: File | null;
    onFileSelect: (file: File | null) => void;
};

function FileUploader({ file, onFileSelect }: FileUploaderProps) {
    const fileName = file ? file.name : "Select your video!";

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const newFile = e.target.files?.[0] ?? null;
        onFileSelect(newFile); // przekazanie pliku do rodzica
    };

    return (
        <div className="file-input-container">
            <label className="file-input-label">
                <span className="file-name">{fileName}</span>
                <input className="file-input" type="file" onChange={handleFileChange} />
            </label>
        </div>
    );
}

export default FileUploader;
