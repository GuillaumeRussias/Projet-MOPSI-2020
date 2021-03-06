import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


from flask import Flask,render_template,url_for,request,redirect,json

import load_data.load_compiled_graph2 as load_graph
import display_on_map.Display_geojson as display_geo
import isochrones.compute_iso as compute_iso
import numpy as np





# Pour que ça fonctionne ne pas oublier de faire clic droit,
# "définir le répertoire courant en accord avec le fichier ouvert dans l'éditeur"

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

graph = load_graph.load_graph()


default_time = 8*3600
default_origine = 0
default_destination = 1

def extract_index(gare_name):
    #extract station_index from gare_name : gare_name = "station_name / station_index"
    gare_name = gare_name.split("/")
    index = int(gare_name[-1][1:])
    return index

def time_to_sec(time):
    try :
        time=time.split(":")
        time = int(time[0])*3600 + int(time[1])*60
    except:
        time = default_time
    if time>=24*3600 or time<0 :
        time = default_time

    return time

def city_mapper_single_user(request):
    h_debut = time_to_sec(request.form['time'])
    origine = request.form['origine']
    destination = request.form['destination']

    try :
        i = extract_index(origine)
        j = extract_index(destination)
        path = graph.time_changement_path_finder(i,j,h_debut)
    except Exception as e:
        i = default_origine
        j = default_destination
        path = graph.time_changement_path_finder(default_origine,default_destination,default_time)
        print(e)

    print("==============================")
    print(i,j)
    print("From",load_graph.PandaV["station_name"][i],"to",load_graph.PandaV["station_name"][j])
    dep = display_geo.seconds_to_hours(graph[path[0]].time())
    arr = display_geo.seconds_to_hours(graph[path[-1]].time())
    print("Departure time =",dep,"| Arrival time =",arr)
    print("==============================")
    return path

def create_geojson_file_custom(path,name):
    display_geo.create_geojson_file(VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , Display = load_graph.PandaDisp ,LineData = load_graph.PandaC, Path = path , CompiledGraph = graph , file_path = currentdir + "/templates/geojson/"+name+".js")

def create_geojson_file(path):
    try :
        display_geo.create_geojson_file(VertexData = load_graph.PandaV , EdgeData = load_graph.PandaE , Display = load_graph.PandaDisp ,LineData = load_graph.PandaC, Path = path , CompiledGraph = graph , file_path = currentdir + "/templates/geojson/geojson_singleuser.js")
    except Exception as e:
        print(e)
        print("path not displayable")


def city_mapper_arrival_time(start,end,arrival_time):
    max = 3600*24
    min = 0
    Tmid = np.inf
    iter = 0
    while (abs(Tmid - arrival_time)>15*60 and iter<=10):
        mid = (max+min)//2
        path = graph.time_changement_path_finder(start,end,mid)
        Tmid = graph[path[-1]].time()%(3600*24)
        #print(iter,display_geo.seconds_to_hours(Tmid),display_geo.seconds_to_hours(min),display_geo.seconds_to_hours(max))
        if Tmid>arrival_time :
            max = mid
        else:
            min = mid
        iter+=1
    print("==============================")
    print("asked arrival time",display_geo.seconds_to_hours(arrival_time))
    print(start,end)
    print("From",load_graph.PandaV["station_name"][start],"to",load_graph.PandaV["station_name"][end])
    dep = display_geo.seconds_to_hours(graph[path[0]].time())
    arr = display_geo.seconds_to_hours(graph[path[-1]].time())
    print("Departure time =",dep,"| Arrival time =",arr)
    print("==============================")
    return path


def city_mapper_multi_user(request,n_users,start_time):
    start_points = np.array([extract_index(request.form[f"{i}"]) for i in range(int(n_users))])
    h_debut = time_to_sec(start_time)
    destination = graph.multi_users_dijkstra(start_points,h_debut)
    print("==================================================================")
    print(start_points)
    print("Meeting point" , load_graph.PandaV["station_name"][destination])
    dict = {}
    for i in range(int(n_users)):
        """dict["origine"] = " / "+str(start_points[i])
        dict["destination"] = " / "+str(destination)
        dict["time"] = start_time
        r = requete(dict)"""
        path = city_mapper_arrival_time(start_points[i],destination,h_debut)
        create_geojson_file_custom(path,"meeting_point_"+str(i))
    print("==================================================================")


def build_isochrones(request):
    start = extract_index(request.form["start"])
    time = time_to_sec(request.form["time"])
    geojson_isochrones = compute_iso.create_isochrones_hulls(graph,start,time,load_graph.PandaV)
    compute_iso.create_geojson_file(file_path = currentdir + "/templates/geojson/geojson_isochrones.js", geojson_feature = geojson_isochrones)




## Affichage des résultats d'une recherche
@app.route('/affichagecarte/')
def affiche():
    return render_template("carte_accueil.html")

@app.route('/route_display_single_user/')
def route_display_single_user():
    return render_template("route_display.html", geojson_url = "/geojson_single_user")

@app.route('/route_description_single_user/')
def route_description_single_user():
    return render_template("route_info_display.html", geojson_url = "/geojson_single_user")

@app.route('/geojson_single_user/')
def render_geojson_single_user():
    return render_template("geojson/geojson_singleuser.js")

##Affichage isochrones

@app.route('/isochrone_display/')
def isochrone_display():
    return render_template("isochrones_display.html", geojson_url = "/geojson_isochrone")

@app.route('/geojson_isochrone/')
def render_geojson_isochrone():
    return render_template("geojson/geojson_isochrones.js")

##Affichage multi-users
@app.route('/route_display/<user>')
def route_display_user(user):
    return render_template("route_display.html", geojson_url = "/meeting_point_"+str(user))

@app.route('/route_description/<user>')
def route_description_user(user):
    return render_template("route_info_display.html", geojson_url = "/meeting_point_"+str(user))

@app.route('/meeting_point_<user>')
def render_geojson_multi_user(user):
    return render_template("geojson/meeting_point_"+str(user)+".js")

# Affichage des différents plans de réseaux (RER & métro ou Bus)
@app.route('/affichagereseauRER')
def affichagereseaRER():
    return render_template("reseauRER.html")


# Onglets de la barre de navigation
@app.route('/')
@app.route('/accueil/')
def accueil():
    return render_template("accueil.html")

@app.route('/itineraire/')
def itineraire():
    return render_template("itineraire.html")


@app.route('/isochrones_map/')
def isochrones_map():
    return render_template("isochrones_map.html")


@app.route('/meeting_point_traject/<n_users>')
def meeting_point_itineraire(n_users):
    return render_template("meeting_point_itineraire.html",n=int(n_users))

@app.route('/reseau/')
def reseau():
    return render_template("reseau.html")

@app.route('/meeting_point/',methods=['GET','POST'])
def meeting_point_1():
    if request.method == "GET":
        return render_template("meeting_point1.html")
    if request.method == 'POST':
        n_users = request.form["n_users"]
        time = request.form["time"]
        return redirect(f"/meeting_point_2/{n_users}/{time}")

@app.route('/meeting_point_2/<n_users>/<time>',methods=['GET','POST'])
def meeting_point_2(n_users,time):
    if request.method == "GET":
        return render_template("meeting_point2.html",n=int(n_users),liste_stations = json.dumps(load_graph.station_names))
    if request.method == 'POST':
        city_mapper_multi_user(request,n_users,time)
        return redirect(f"/meeting_point_traject/{n_users}")

@app.route('/carte/', methods=['GET', 'POST'])
def carte():
    if request.method == "GET":
        return render_template("carte.html",liste_stations = json.dumps(load_graph.station_names))
    if request.method == 'POST':
        path = city_mapper_single_user(request)
        create_geojson_file(path)
        return redirect(url_for ('itineraire'))

@app.route('/isochrones/', methods=['GET','POST'])
def isochrones():
    if request.method == "GET":
        return render_template("isochrones.html",liste_stations = json.dumps(load_graph.station_names))
    if request.method == 'POST':
        build_isochrones(request)
        return redirect(url_for ('isochrones_map'))


if __name__ == "__main__":
    app.run()
