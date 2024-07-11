from flask import Flask,render_template,request
import data

app = Flask(__name__)
@app.route("/")
def index():
    #print(list(map(lambda value:value[0],data.get_areas())))
<<<<<<< HEAD
    selected_area = request.args.get('area')
=======
    
>>>>>>> 247a818420b41c7d803a1ebcfcef4b6c99cb9cb5
    areas = [tup[0] for tup in data.get_areas()]
    selected_area = '士林區' if selected_area is None else selected_area  
        
    return render_template('index.html.jinja',areas=areas,show_area=selected_area)    
    
    
    