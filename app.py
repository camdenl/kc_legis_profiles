from flask import Flask, render_template, request, Markup, make_response, url_for
from indicator_api_dl import *
import pdfkit

json_data = None

#pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
     return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    global json_data
    if request.method == 'POST':
        dist_type = request.form['district-select']
        dist_num  = int(request.form['district-number'])
        indicators =  request.form.getlist('indic-check-legis')
        json_data = {
            'dist_type' : dist_type,
            'dist_num'  : dist_num
        }
        for idx, indic_string in enumerate(indicators):
            file_string = 'static/pkl/{}_{}.pkl'.format(pkls[indic_string], dist_type.lower())
            data_val = pd.read_pickle(file_string).ix[str_fill(dist_num)]
            # data_val = funcs[indic_string](dist_type.lower(), str_fill(dist_num))
            data_val *= 100
            data_val = round(data_val, 1)
            data_val = str(data_val) + '%'
            data_key = 'indic_value{}'.format(idx+1)
            json_data[data_key] = data_val
            json_data['indic_descr{}'.format(idx+1)] = indicator_descriptions[indic_string]
            json_data['ga_avg{}'.format(idx+1)] = state_averages[indic_string]
            #json_data['indic_ways{}'.format(idx+1)] = indicator_ways[indic_string]
        coordinators = coordinator_list(dist_type.lower(), int(dist_num))
        json_data['table_rows'] = coordinators
    return render_template('profile.html', data = json_data)

@app.route('/profile_pdf', methods=['GET', 'POST'])
def profile_pdf():
    response = make_pdf(render_template('profile_pdfkit.html', data = json_data))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=profile.pdf'
    return response

@app.route('/countyProfile', methods=['GET', 'POST'])
def county_profile():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    indicators =  request.form.getlist('indic-check-county')
    county = request.form['county-selector']
    districts = get_districts(county)
    list_of_json_data = []
    for district in districts:
        dist_type = district[0]
        dist_num = district[1]
        json_data = {
            'dist_type' : dist_type.title(),
            'dist_num'  : dist_num
        }
        for idx, indic_string in enumerate(indicators):
            file_string = 'static/pkl/{}_{}.pkl'.format(pkls[indic_string], dist_type.lower())
            data_val = pd.read_pickle(file_string).ix[str_fill(dist_num)]
            #data_val = funcs[indic_string](dist_type.lower(), str_fill(dist_num))
            data_val *= 100
            data_val = round(data_val, 1)
            data_val = str(data_val) + '%'
            data_key = 'indic_value{}'.format(idx+1)
            json_data[data_key] = data_val
            json_data['indic_descr{}'.format(idx+1)] = indicator_descriptions[indic_string]
            json_data['ga_avg{}'.format(idx+1)] = state_averages[indic_string]
            #json_data['indic_ways{}'.format(idx+1)] = indicator_ways[indic_string]
        coordinators = coordinator_list(dist_type.lower(), int(dist_num))
        json_data['table_rows'] = coordinators
        list_of_json_data.append(json_data)
    return render_template('countyProfile.html', datalist = list_of_json_data)

@app.route('/find_district')
def find_district():
    return render_template('find_district.html')


@app.route('/map_submit', methods=['GET', 'POST'])
def map_submit():
    number = request.form.get('dist-number')
    type = request.form.get('dist-type')
    if type == 'senate':
        house = False
    elif type == 'house':
        house = True
    return render_template('index.html', dist_number=number, house=house)

@app.errorhandler(500)
def internal_service_error(e):
    return render_template('internal_error.html')

def make_pdf(rendered_template):
    encoded = rendered_template.encode('utf-8')
    options = {
    'page-size': 'Letter',
    'encoding': "UTF-8",
    'no-outline': False
}
    css = ['./static/css/profile_style_pdfkit.css'
        #, './static/css/sheets-of-paper.css', './static/css/sheets-of-paper-pdfkit.css'
           ]
    pdf = pdfkit.from_string(encoded, False, configuration=pdfkit_config, css = css, options= options)
    return make_response(pdf)

if __name__ == '__main__':
    app.run(debug=True, threaded = True)