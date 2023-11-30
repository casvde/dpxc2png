

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
    const cpu = result.cpu;
    const ram = result.ram;

    document.getElementById('loadingbarjs').innerText = `${loadingbar}`;
    document.getElementById('cpu').innerText = `${cpu}`;
    document.getElementById('ram').innerText = `${ram}`;
}




function get_path_to_file() {
    eel.pythonFunction();
};

function selectDirectory() {
    eel.select_directory();
};

function convert_selected_files() {
    eel.convert_selected_files();
};





