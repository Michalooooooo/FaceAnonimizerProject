

export const handleUpload = async (file: File) => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed!');
        }

        const data = await response.json();
        console.log('Update success: ', data);
    } catch (error) {
        console.error(error);
    }
};