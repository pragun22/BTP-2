import json 
  
# Opening JSON file 
with open('Hyd.js') as json_file: 
    data = json.load(json_file) 
    co = 0
    data = data['geometries'][0]['coordinates']
    print("const Pune = [")
    mnl, mxl, mnln, mxln = 1e6, -1, 1e6, -1
    for v in data:
    	for x in v[0]:
    		mnl = min(mnl, x[0])
    		mxl = max(mxl, x[0])
    		mnln = min(mnln, x[1])
    		mxln = max(mxln, x[1])
	    	print("{lng:" + str(x[0]) + "," + "lat:" + str(x[1]) + "},")
    print("]")
    print("export default Pune;")
    print(mnl, mxl, mnln, mxln)
# with open('Hyd.js', 'r') as file:
# 	data = file.read().split(" ")
# 	print("const Guwahati = [")
# 	mnl, mxl, mnln, mxln = 1e6, -1, 1e6, -1
# 	for x in data:
# 		x = x.split(",")
# 		x[0] = float(x[0])
# 		x[1] = float(x[1])
# 		mnl = min(mnl, x[0])
# 		mxl = max(mxl, x[0])
# 		mnln = min(mnln, x[1])
# 		mxln = max(mxln, x[1])
# 		print("{lng:" + str(x[0]) + "," + "lat:" + str(x[1]) + "},")
# 	print("]")
# 	print("export default Guwahati;")
