const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("resumeFile");

dropZone.addEventListener("click", () => {
    fileInput.click();
});

dropZone.addEventListener("dragover", e => {
    e.preventDefault();
});

dropZone.addEventListener("drop", e => {
    e.preventDefault();

    fileInput.files = e.dataTransfer.files;
});