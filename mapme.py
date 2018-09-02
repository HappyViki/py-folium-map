import pandas
import folium

volcano_data = pandas.read_csv("volcano.csv")

def active_color(n):
	if n != 0:
		return("red")
	else:
		return("green")

mymap = folium.Map(location=[volcano_data.iloc[0].loc["Latitude"],volcano_data.iloc[0].loc["Longitude"]], zoom_start=4, tiles="Mapbox Bright")

# Colors countries by 2005 population
world_data = open("world.json", "r", encoding="utf-8-sig")
pop_fg = folium.FeatureGroup(name="2005 Population")
pop_fg.add_child(folium.GeoJson(data=world_data.read(), 
style_function=lambda x : {'fillColor':'green' 
if x['properties']['POP2005'] < 50000000
else 'orange' 
if 50000000 <= x['properties']['POP2005'] < 100000000 
else 'red'}))
world_data.close()
mymap.add_child(pop_fg)

# Each volcanic region can be turned on/off
for region in volcano_data.groupby("Region"):
    region_fg = folium.FeatureGroup(name=region[0])
    for x, y, label, a in zip(region[1]["Latitude"], region[1]["Longitude"], region[1]["V_Name"], region[1]["H_active"]):
    	region_fg.add_child(folium.CircleMarker(location=[x,y], radius=6, 
		popup=folium.Popup(label,parse_html=True), fill_color=active_color(a), 
		color=active_color(a), fill=True, fill_opacity=0.7))
    mymap.add_child(region_fg)



mymap.add_child(folium.LayerControl())
mymap.save("mymap.html")

# http://folium.readthedocs.io/en/latest/quickstart.html
# for third app: block sites with file /etc/hosts on mac/linux and C:\Windows\System32\drivers\etc