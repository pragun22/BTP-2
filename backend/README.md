# Backend Setup
* Install conda. Follow the instructions given [here](https://docs.anaconda.com/anaconda/install/linux/).
* Navigate to backend directory using command line.
* Run ```conda env create -f environment.yml```.
* Run ```conda activate btp-2```

# API endpoints
* /get_map

**Request Method** - GET

#### Request Parameters
* **City** - Name of city for which flood inundation has to be done
* **Date** - Date for which prediction needs to be done.

#### Response
* **matrix** * - Matrix containing amount of water at each pixel after hydrological simulation
* **bbox** - Coordinates of the bounding box corresponding to the returned matrix.
* **centre** - Coordinate of centre of the city in parameter. Google map is centred at this coordinate for display.
Sample response can be found [here](https://github.com/pragun22/BTP-2/blob/backend/backend/sample_response.json).
