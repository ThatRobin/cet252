import os

from player_data import PlayerData
from screen import Screen
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import sys

API_URL = 'http://localhost:4001/mods'

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
os.chdir(script_dir)

def installMod():
    mod_id = input("Enter Mod ID: ")
    base_path = "mods"
    file_name = "mod.metadata"
    try:
        response = getMod(mod_id)
        data = json.loads(response.read().decode('utf-8'))["mod"]
        if data:
            temp = data.pop("json", None)
            path = os.path.join(base_path, mod_id, file_name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            
            temp = temp.replace("\\\"", "?").replace("'", "\"").replace("?", "'")
            json_array = json.loads(temp)
            print(json_array)
            for mod in json_array:
                file_path = mod.pop("path", None)
                if file_path:
                    print(f"Downloading mod file: {file_path}")
                    # Create the directory if it doesn't exist
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    # Write the JSON object to the file
                    with open(file_path, 'w') as json_file:
                        json.dump(mod, json_file, indent=4)
            print("Mod Download complete!")
        else:
            print(f"Mod with ID {mod_id} not found.")
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")

def getMod(mod_id):
    response = None
    try:
        response = urlopen(f'{API_URL}/{mod_id}')
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")
        response = e
    return response

def updateMod():
    mod_id = input("Enter Mod ID to Update: ")

    mod_data = get_mod_metadata(mod_id)
    mod_data["json"] = str(get_local_mod(mod_id))

    response = putMod(mod_id, mod_data)
    if response is not None:
        print(json.loads(response.read().decode('utf-8'))["message"])


def putMod(mod_id, mod_data):
    response = None
    try:
        req = Request(f'{API_URL}/{mod_id}', method='PUT', data=json.dumps(mod_data).encode('utf-8'),
                      headers={'Content-Type': 'application/json'})
        response = urlopen(req)
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason} ")
        response = e
    return response


def listRemoteMods():
    print("Getting All Mods:")
    print("-" * 30)
    try:
        response = urlopen(API_URL)
        mods = json.loads(response.read().decode('utf-8'))["mods"]
        print_mods(mods)
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")


def listLocalMods():
    print("Getting All Mods:")
    print("-" * 30)
    try:
        mods = []
        for root, dirs, files in os.walk("mods"):
            for file_name in files:
                if file_name == "mod.metadata":
                    file_path = os.path.join(root, file_name)
                    with open(file_path, "r") as file:
                        try:
                            json_data = json.load(file)
                            mods.append(json_data)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in file {file_path}")
        print_mods(mods)
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")


def exitGame():
    print("exiting...")


def uploadMod():
    mod_id = input("Enter Mod ID: ")
    mod_data = get_mod_metadata(mod_id)
    mod_data["json"] = str(get_local_mod(mod_id))
    print(json.loads(postMod(mod_data).read().decode('utf-8'))["message"])

def postMod(mod_data):
    response = None
    try:
        req = Request(API_URL, method='POST', data=json.dumps(mod_data).encode('utf-8'),
                      headers={'Content-Type': 'application/json'})
        response = urlopen(req)
        
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")
        response = e
    return response

def deleteMod(mod_id):
    response = None
    try:
        req = Request(f'{API_URL}/{mod_id}', method='DELETE')
        response = urlopen(req)
    except HTTPError as e:
        print(f"Error: {e.code} - {e.reason}")
        response = e
    return response

def get_local_mod(mod_id):
    json_array = []
    base_path = "mods"
    # Walk through the base directory
    for root, dirs, files in os.walk(os.path.join(base_path, mod_id)):
        for file_name in files:
            # Check if the file has a .json extension
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                # Read the JSON content from the file
                with open(file_path, 'r') as json_file:
                    json_content = json.load(json_file)

                    # Add a "path" field to the JSON object
                    json_content["path"] = file_path

                    # Append the modified JSON object to the array
                    json_array.append(json_content)
    return json_array

def get_mod_metadata(mod_id):
    base_path = "mods"
    file_name = "mod.metadata"
    with open(os.path.join(base_path, mod_id, file_name), "r") as metadata:
        data = json.load(metadata)
        return data

class TitleScreen:
    def __init__(self):
        self.character = None

    def main(self):
        choices = ["Game Name Here", "1) Start Adventure", "2) Swap Character", "3) Manage Mods", "4) Exit",
                   "What would you like to do? "]
        choicef = [None, self.startAdventure, self.characterScreen, self.manageMods, exitGame, None]
        screen = Screen(choices, choicef)
        choice = screen.display()
        if choice is not None:
            choice()

    def startAdventure(self):
        return

    def manageMods(self):
        choices = ["Mod Menu:", "1) List Currently Installed Mods", "2) List Remote Mods",
                   "3) Install Mod", "4) Upload Mod", "5) Update Mod", "6) Delete Mod",
                   "7) Exit", "What would you like to do? "]
        choicef = [None, listLocalMods, listRemoteMods, installMod, uploadMod, updateMod, self.deleteMod, self.main,
                   None]
        screen = Screen(choices, choicef)
        choice = screen.display()
        if choice == self.main:
            choice()
        else:
            self.character = choice()
            self.main()

    def characterScreen(self):
        choices = ["Character Menu:", "1) Choose existing character", "2) Create New Character",
                   "3) List Characters",
                   "4) Exit", "What would you like to do? "]
        choicef = [None, PlayerData.getCharacter, PlayerData.createCharacter, PlayerData.displayCharacterList, self.main,
                   None]
        screen = Screen(choices, choicef)
        choice = screen.display()
        if choice == self.main:
            choice()
        else:
            self.character = choice()
            self.main()

    def removeMod(self):
        mod_id = input("Enter Mod ID to Delete: ")
        delete_confirmation = input(f"Are you sure you want to delete {mod_id}? (y/n) ")
        if delete_confirmation == "n":
            self.manageMods()
        elif delete_confirmation == "y":
            print(json.loads(deleteMod(mod_id).read().decode('utf-8'))["message"])
        else:
            self.removeMod()


def print_mods(mods):
    for mod in mods:
        print_mod(mod)

def print_mod(mod):
    print(f"Mod ID: {mod['mod_id']}")
    print(f"Mod Name: {mod['mod_name']}")
    print(f"Username: {mod['username']}")
    print(f"Version: {mod['version']}")
    print("-" * 30)
