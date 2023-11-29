eel.expose(updateFileCount);

function updateFileCount(result) {
    const fileCount = result.count;
    document.getElementById('fileCount').innerText = `${fileCount}`;

}


eel.expose(dirName);

function dirName(result) {

    const dirName = result.name;

    document.getElementById('dirName').innerText = `${dirName}`;

}


eel.expose(progress);

function progress(result) {

    const loadingbar = result.loadin;

    document.getElementById('loadingbarjs').innerText = `${loadingbar}`;

}


function getPathToFile() {
    eel.pythonFunction();
};

function selectDirectory() {
    eel.select_directory();
};

function convert_selected_files() {
    eel.convert_selected_files();
};


