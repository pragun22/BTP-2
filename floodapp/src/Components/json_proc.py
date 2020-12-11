import json 
  
# Opening JSON file 
with open('Hyd.js') as json_file: 
    data = json.load(json_file) 
    co = 0
    data = data['geometries'][0]['coordinates']
    print("const Chennai = [")
    for v in data:
    	for x in v[0]:
	    	print("{lng:" + str(x[0]) + "," + "lat:" + str(x[1]) + "},")
    print("]")
    print("export default Chennai;")
