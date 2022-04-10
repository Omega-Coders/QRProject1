import what3words
geocoder=what3words.Geocoder("FLKKRIUH")

three_words = "lawfully.burglars.afflict"
res = geocoder.convert_to_coordinates(three_words)

my_lat = res["square"]["southwest"]["lat"]
my_lon = res["square"]["southwest"]["lng"]

my_link = "https://www.google.co.in/maps/place/"+str(my_lat)+","+str(my_lon)

print(my_link)
print(res)