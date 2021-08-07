import csv
import plotly.express as pe
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sb
planets= []

with open('planets.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        planets.append(row)
headers= planets[0]
planetdata = planets[1:]
print(planetdata[3])
headers[0]='Row_Num'

planetcount= {}
for i in planetdata:
    if planetcount.get(i[11]):
        planetcount[i[11]]+=1
    else:
        planetcount[i[11]]=1

maxsolarsystem = max(planetcount, key=planetcount.get)
print(maxsolarsystem, 'has the most planets. It has', planetcount[maxsolarsystem], 'planets.')

koi = []
for i in planetdata:
    #if name == 'KOI-3890', then we will appened the row to the list
    if i[11] == maxsolarsystem:
        koi.append(i)
print(len(koi))
print("Planets", koi)

tempplanetdata= list(planetdata)
print("Planet data unknowns",len(planetdata))
for i in tempplanetdata:
    planetmass = i[3]
    if planetmass.lower() == 'unknown':
        planetdata.remove(i)
        continue
    else:
        planetmassvalue = planetmass.split(" ")[0]
        planetmassref= planetmass.split(" ")[1]
        if planetmassref=='Jupiters':
            planetmassvalue = float(planetmassvalue)*317.8
        i[3]=float(planetmassvalue)
    planetradius = i[7]
    if planetradius.lower() == 'unknown':
        planetdata.remove(i)
        continue
    else:
        planetradiusvalue = planetradius.split(" ")[0]
        planetradiusref= planetradius.split(" ")[1]
        if planetradiusref=='Jupiters':
            planetradiusvalue = float(planetradiusvalue)*11.21
        i[7]=float(planetradiusvalue)
print("Planet data unknowns removed",len(planetdata))

koiplanets = []
for i in planetdata:
    if i[11] == maxsolarsystem:
        koiplanets.append(i)
print(len(koiplanets))


koiplanetmass = []
koiplanetname=[]

for i in koiplanets:
    koiplanetmass.append(i[3])
    koiplanetname.append(i[1])

koiplanetmass.append(1)
koiplanetname.append('Earth')

graph = pe.bar(x=koiplanetname, y=koiplanetmass, title='Planet Mass by Name')
graph.show()


#gravity formula = g= (G*M)/(R**2) G=6.67e-11 m/kgs**2

tempplanetdata= list(planetdata)

for i in tempplanetdata:
    if i[1].lower() == "hd 100546 b":
        planetdata.remove(i)
planetmass= []
planetradius=[]
planetname = []

for i in planetdata:
    planetmass.append(i[3])
    planetradius.append(i[7])
    planetname.append(i[1])
planetgravity = []

for index, name in enumerate(planetname):
    #6371000= Earth radius in meters
    #5.972e24= Earth mass in kg
    planetgravity.append(6.67e-11*(float(planetmass[index])*5.972e+24)/(float(planetradius[index])**2)*6371000*6371000)

scatter = pe.scatter(x=planetradius, y=planetmass, size=planetgravity, title='Planet Gravity by Name', hover_data=[planetname])
scatter.show()


lowgravityplanets = []
highgravityplanets = []

for index,gravity in enumerate(planetgravity):
    if gravity < 0.001*10**33:
        lowgravityplanets.append(planetdata[index])
    else:
        highgravityplanets.append(planetdata[index])
print("Number of low gravity planets", len(lowgravityplanets))
print("Number of high gravity planets", len(highgravityplanets))

planettype=[]
for i in planetdata:
    planettype.append(i[6])
print(list(set(planettype)))
print(len(planettype))

lgplanetmass = []
lgplanetradius = []
lgplanettype=[]
for i in lowgravityplanets:
    lgplanetmass.append(i[3])
    lgplanetradius.append(i[7])
    lgplanettype.append(i[6])
newscatter = pe.scatter(x=lgplanetradius, y=lgplanetmass, title='Low Gravity Planet Mass by Name')
newscatter.show()

X = []

for index, planetmass in enumerate(lgplanetmass):
    templist=[lgplanetradius[index], planetmass]
    X.append(templist)
#Within cluster sum of squares
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.figure(figsize=(12,6))
plt.title('The Elbow Method')
sb.lineplot(range(1,11), wcss, color= 'blue', marker= 'o', markersize=5, linewidth=2)
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

lgplanettypescatter = pe.scatter(x=lgplanetradius, y=lgplanetmass, title='Low Gravity Planet Mass by Type', color=lgplanettype)
lgplanettypescatter.show()

#terrestrial and super earth from lower gravity planets

habitableplanets=[]

for i in lowgravityplanets:
    if i[6].lower() == 'terrestrial' or i[6].lower() == 'super earth':
        habitableplanets.append(i)
print("Habitable", len(habitableplanets))
print("Total Low gravity planets",len(lowgravityplanets))
