![image](https://github.com/kcpgilbert/HeatIslandHero/assets/120534381/20c6ff61-b377-458c-bb22-fd3fdb1826a8)

# HeatIslandHero

HeatIslandHero is a website that allows users to search for urban heat island impact and sensitivity data accross census tracts in Los Angeles County. This data will be displayed both on a map and in list format to the user. HeatIslandHero also searches the relevant census tracts for buildings that are good candidates for the addition of green roofs in the area and displays these to the users. 

## Collaborators

This project was created at the AECtech Hackathon 2023 in Los Angeles by the following collaborators. 
![image](https://github.com/kcpgilbert/HeatIslandHero/assets/120534381/36d63d0d-efc9-4133-8212-3c82ab302d07)

## System Overview
![image](https://github.com/kcpgilbert/HeatIslandHero/assets/120534381/c7bac068-b0f9-46e5-a049-4f27b517247e)
![image](https://github.com/kcpgilbert/HeatIslandHero/assets/120534381/b2bab462-227e-4786-bea6-1381e0a24ed8)
![image](https://github.com/kcpgilbert/HeatIslandHero/assets/120534381/4ce3149d-6b1b-4d61-902a-01ca3eb5dfb4)
![image](https://github.com/kcpgilbert/HeatIslandHero/assets/120534381/5bf0afae-fc05-4ee6-b313-02d0eaa951eb)

## Setup

1. Create a file named `secrets.json` inside of the `server` directory. The contents of the file should be as follows:
```
{
    "gpt-token" : "<YOUR-OPEN-AI-TOKEN-HERE>"
}
```
2. In the root directory run `pip install -r requirements.txt`
3. To run the backend server `cd server`, then execute `flask run`
