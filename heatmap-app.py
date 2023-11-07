import PySimpleGUI as sg
import os
import glob
import subprocess

# check if docker daemon is running
docker_error = subprocess.run(['docker ps'], shell=True, capture_output=True, text=True).stderr
if docker_error:
    print('\n** Looks like docker daemon is not running. Please start docker. **\n')

def run_docker_container(PATH_TO_PROJECT, INPUT_PATH, OUTPUT_PATH):
    docker_command = f"""
    set -x
    docker run -it \
        -v "{PATH_TO_PROJECT}":/projects/current \
        -v "{INPUT_PATH}":/data/in \
        -v "{OUTPUT_PATH}":/data/out \
        seasketch/heatmap:latest \
        bash -c "/work/scripts/gen_heatmap /projects/current/config.json"
    """
    try:
        subprocess.run(docker_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Docker command failed with error: {e}")

# Define the layout of the form
layout = [
    [sg.Text('Project folder path:'), sg.InputText(key='projPath'), sg.FolderBrowse(target='projPath')],
    [sg.Text('Input path:'), sg.InputText(key='inputPath'), sg.FolderBrowse(target='inputPath')],
    [sg.Text('Ouput path:'), sg.InputText(key='outputPath'), sg.FolderBrowse(target='outputPath')],
    [sg.Text('Resolution:'), sg.InputText(default_text='200', key='resolution')],
    [sg.Text('Unique ID field:'), sg.InputText(default_text='response_id', key='uniqueIdField')],
    [sg.Text('Importance field:'), sg.InputText(default_text='value', key='importanceField')],
    [sg.Text('All touched small:'), sg.InputText(default_text='true', key='allTouchedSmall')],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

# Create the window
window = sg.Window('User Input Form', layout, size=(475, 210))

# Read the form
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    projPath = values['projPath']
    inputPath = values['inputPath']
    outputPath = values['outputPath']
    resolution = values['resolution']
    uniqueIdField = values['uniqueIdField']
    importanceField = values['importanceField']
    allTouchedSmall = values['allTouchedSmall']

    # generate config.json
    config = ''
    config += '{"runs": ['

    shps = []
    extensions = ['*.shp', '*.fgb', '*json']

    for ext in extensions:
        files = glob.glob(inputPath + '/' + ext)
        shps.extend(files)

    for i in range(0, len(shps)):
        
        shp = os.path.basename(shps[i])

        if i < len(shps)-1:
            config += f'{{"infile": "/data/in/{shp}"}},'
        else:
            config += f'{{"infile": "/data/in/{shp}"}}'

    config += '],"default": {"outPath": "/data/out","outResolution":' + resolution + f',"areaFactor": 1,"uniqueIdField":"' + uniqueIdField + f'","importanceField":"' + importanceField + '","logToFile": true,"allTouchedSmall":' + allTouchedSmall + ',"overwrite": true}}'

    # add config.json to project folder and run the project
    os.system(f'touch {projPath}/config.json')
    os.system(f"echo '{config}' > {projPath}/config.json")

    if __name__ == "__main__":
        run_docker_container(PATH_TO_PROJECT=projPath, INPUT_PATH=inputPath, OUTPUT_PATH=outputPath)

    os.system(f'mkdir -p {outputPath}/logs && rm {outputPath}/*txt && mv {outputPath}/*json {outputPath}/logs')

# Close the window
window.close()