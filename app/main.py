from flask import Flask, request, url_for, render_template
from app.forms import UserInputForm
from app.states.madhyapradesh import MadhyaPradesh
from app.states.maharashtra import Maharashtra

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THISisNOTsoSECRET'
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    input_form = UserInputForm()
    if request.method == "GET":
        return render_template('home.html', form=input_form)
    elif request.method == "POST":
        input_form = UserInputForm(request.form)
        state = input_form.state.data
        if state == 'Maharashtra':
            consumption = int(input_form.consumption.data)
            if consumption == 0:
                return '<h1 class="container mt-4">Please start using electricity first</h1>'
            connection_type = input_form.connection.data
            if connection_type == 'Residential':
                ctype = 'R'
            elif connection_type == 'Commercial':
                ctype = input_form.commercial_type_mh.data
            elif connection_type == 'Industrial':
                ctype = input_form.industrial_type_mh.data

            load = input_form.connected_load.data
            if load != None:
                load = int(load)

            results = Maharashtra(consumption, connection_type, ctype, load).get_results()

            # DEBUG
            # print(f'System Size: {system_size}')
            # print(f'No of Panels: {no_of_panels} | Area: {area} | Area sq ft: {area_sq_ft}')
            # print(f'Cost: {cost}')
            # print(f'Tarif: {tarif} | Bill: {bill}')
            # print(f'ROI: {roi}')
            # print(f'Years: {years}')
            # print(f'Profit Years: {profit_years}')
            # print(f'Connection Type: {ctype}')

            return render_template('results.html', results=results)

        if state == 'MadhyaPradesh':
            consumption = int(input_form.consumption.data)
            if consumption == 0:
                return '<h1 class="container mt-4">Please start using electricity first</h1>'
            connection_type = input_form.connection.data
            if connection_type == 'Residential':
                ctype = 'R'
            elif connection_type == 'Commercial':
                ctype = input_form.commercial_type_mp.data
            elif connection_type == 'Industrial':
                ctype = input_form.industrial_type_mp.data

            load = input_form.connected_load.data
            if load != None:
                load = int(load)

            results = MadhyaPradesh(consumption, connection_type, ctype, load).get_results()

            # DEBUG
            # print(f'System Size: {system_size}')
            # print(f'No of Panels: {no_of_panels} | Area: {area} | Area sq ft: {area_sq_ft}')
            # print(f'Cost: {cost}')
            # print(f'Tarif: {results["tarif"]} | Bill: {results["bill"]}')
            # print(f'ROI: {roi}')
            # print(f'Years: {years}')
            # print(f'Profit Years: {profit_years}')
            # print(f'Connection Type: {ctype}')

            return render_template('results.html', results=results)


if __name__ == "__main__":
    app.run()
