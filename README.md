# kml2g1000
Convert FlightAware KML tracklogs to G1000 CSV for importing to ForeFlight

## Usage
1. Download KML tracklogs from FlightAware ([Read more about this from FlightAware](https://discussions.flightaware.com/t/klm-file-for-google-earth/41505/2)) and store in the same directory with the `kml2g1000.py` script (probably this directory)
1. Ensure you have your Python environment ready with the required packages installed. If you're using pip, you can install such as `pip install -r requirements.txt`
1. Run `kml2g1000.py` python script such as `python kml2g1000.py`
1. Upload resulting csv files to where you can easily access them on your iPad (e.g. Google Drive). Access the files on your iPad or iPhone and save them to the local storage. This is usually done by choosing the file, then us "Open in ..." and finally "Save to Files"
1. Import into ForeFight from More > Track Logs > Import (icon) ([Read more about this on ForeFlight](https://support.foreflight.com/hc/en-us/articles/360042091114-How-can-I-import-a-Garmin-G1000-Track-Log-into-ForeFlight-Mobile-))
