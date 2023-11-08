import PySimpleGUI as sg
import os
import glob
import subprocess

# check if docker daemon is running
docker_error = subprocess.run(['docker ps'], shell=True, capture_output=True, text=True).stderr
if docker_error:
    sg.popup('Warning', 'Looks like docker daemon is not running. Please start docker.', background_color='#181818', button_color='#37373C')

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
        sg.Popup('Success', 'Heatmap generation complete!', background_color='#181818', button_color='#37373C')
    except subprocess.CalledProcessError as e:
        error_message = f"Docker command failed with error: {e}"
        sg.Popup('Error', error_message, background_color='#181818', button_color='#37373C')

# Define the layout of the form
layout = [
    [sg.Text('Project folder path:', background_color='#181818', pad=(5,6.5)), sg.InputText(key='projPath', default_text='/Users/petermenzies/Projects/heatmaps/app/heatmap-app-test'), sg.FolderBrowse(target='projPath', button_color='#37373C')],
    [sg.Text('Input path:', background_color='#181818', pad=(5,6.5)), sg.InputText(key='inputPath', default_text='/Users/petermenzies/Projects/heatmaps/app/heatmap-app-test/data-in'), sg.FolderBrowse(target='inputPath', button_color='#37373C')],
    [sg.Text('Ouput path:', background_color='#181818', pad=(5,6.5)), sg.InputText(key='outputPath', default_text='/Users/petermenzies/Projects/heatmaps/app/heatmap-app-test/data-out'), sg.FolderBrowse(target='outputPath', button_color='#37373C')],
    [sg.Text('Resolution:', pad=(5,6.5), background_color='#181818'), sg.InputText(default_text='200', key='resolution')],
    [sg.Text('Area factor:', pad=(5,6.5), background_color='#181818'), sg.InputText(default_text='1', key='areaFactor')],
    [sg.Text('Unique ID field:', pad=(5,6.5), background_color='#181818'), sg.InputText(default_text='response_id', key='uniqueIdField')],
    [sg.Text('Importance field:', pad=(5,6.5), background_color='#181818'), sg.InputText(default_text='value', key='importanceField')],
    [sg.Text('All touched small:', pad=(5,6.5), background_color='#181818'), sg.InputText(default_text='true', key='allTouchedSmall')],
    [sg.Button('Submit', pad=(5,12), button_color='#37373C'), sg.Button('Cancel', pad=(5,12), button_color='#37373C')]
]

# Create the window
window = sg.Window('Generate Heatmap', layout, size=(475, 290), background_color='#181818')

# Read the form
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    projPath = values['projPath']
    inputPath = values['inputPath']
    outputPath = values['outputPath']
    resolution = values['resolution']
    areaFactor = values['areaFactor']
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

    config += '],"default": {"outPath": "/data/out","outResolution":' + resolution + ',"areaFactor":' + areaFactor + ',"uniqueIdField":"' + uniqueIdField + '","importanceField":"' + importanceField + '","logToFile": true,"allTouchedSmall":' + allTouchedSmall + ',"overwrite": true}}'

    # add config.json to project folder and run the project
    os.system(f'touch {projPath}/config.json')
    os.system(f"echo '{config}' > {projPath}/config.json")

    if __name__ == "__main__":
        run_docker_container(PATH_TO_PROJECT=projPath, INPUT_PATH=inputPath, OUTPUT_PATH=outputPath)

    os.system(f'mkdir -p {outputPath}/logs && rm {outputPath}/*txt && mv {outputPath}/*json {outputPath}/logs')

# Close the window
window.close()