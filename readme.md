# Bloomberg Connects Exporter

This exports data from the HAM APIs to the Bloomberg Connects (BC) bulk upload format.

The script currently fetches and processes: 
* All current exhibitions
    * Poster image, title, description, dates
* All upcoming exhibitions
    * Poster image, title, description, dates
* The past three exhibitions
    * Poster image, title, description, dates
* [Forbes Pigment Collection Digital Tour](https://harvardartmuseums.org/tour/660) (id = 660)
    * Audio file, transcription, title
* All upcoming events
    * Poster image, title, description, dates, relationship to exhibitoins

## Output

Everytime the script runs, it deletes the existing `temp` folder of CSV files and receates the folder by copying the template files in `templates/CSV_TEMPLATE`. (Templates are provided BC.)

The temp folder is zipped and saved in the `archives` folder. Zip files are unique and use the naming scheme `data-YYYY-MM-DD-TIMESTAMP.zip`. 




## Data Sources
* HAM API - Exhibitions, Exhibition Images
* Website API - Events, Event Images, Event-Exhibition Relationships, Tours

## ID Sequences

Some IDs are amended in order to enforce uniqueness across data sources.

* Events - Event ID + 100000000
* Event Images - Event ID + 110000000
* Event Creators - Event ID + 120000000

* Audio - Module ID + Audio File ID + Slide ID
