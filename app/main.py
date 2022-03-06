from flask import Flask, request, url_for, render_template
from app.forms import UserInputForm
from math import ceil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THISisNOTsoSECRET'

# constants
PANEL_SIZE = 0.46
PANEL_AREA = 2.22
COST_1 = 53000
COST_2 = 1000
PEAK_HOURS = {
    'Maharashtra': 4.47,
}
CONNECTION_TYPES = {
    'Residential': 'R',
    'Commercial - LT2A': 'LT2A',
    'Commercial - LT2B': 'LT2B',
    'Commercial - LT2C': 'LT2C',
    'Industrial - LT3A': 'LT3A',
    'Industrial - LT3B': 'LT3B',
}


def get_system_size(consumption, peak_hrs):
    return consumption / (30 * peak_hrs)


def get_required_area(system_size):
    # 2.1
    no_of_panels = system_size / PANEL_SIZE
    # 2.2
    area = no_of_panels * PANEL_AREA
    area_sq_ft = area * 10.76

    return no_of_panels, area, area_sq_ft


def get_cost(system_size):
    return ((system_size * COST_1) + (system_size * COST_2)) * 1.1


def get_resident_tarif(consumption):
    wc = 1.47
    ed = 1.16
    st = 0.2604
    tariff = 0

    if consumption > 500:
        n = consumption // 500
        removed = n * 500
        consumption -= removed
        tariff += (145 + 7.8 * removed + wc *  removed) * ed + (removed * st)

    if 0 <= consumption <= 100:
        fc = 80
        ec = 3.05
    elif 100 < consumption <= 300:
        fc = 120
        ec = 5
    elif 300 < consumption <= 500:
        fc = 120
        ec = 6.7

    tariff += (fc + consumption * ec + consumption * wc) * ed + (st * consumption)

    return tariff


def get_commercial_tarif(consumption, type, load=None):
    if type == 'LT2A':
        fc = 425
        ec = 5.45 * consumption
        wc = 1.47 * consumption
        st = 0.3404 * consumption
        return (fc + ec + wc) * 1.21 + st

    if type in {'LT2B', 'default-c'}:
        if not load:
            load = 35
        ec = 6 * consumption
    elif type == 'LT2C':
        if not load:
            load = 60
        ec = 6.55 * consumption
    dc = 355 * load
    wc = 1.47 * consumption
    st = 0.3404 * consumption

    return (dc + ec + wc) * 1.21 + st


def get_industrial_tarif(consumption, type, load=None):
    wc = 1.47 * consumption
    st = 0.3404 * consumption

    if type == 'LT3A':
        fc = 425
        ec = 5.55 * consumption
        return (fc + ec + wc) * 1.075 + st
    if type == 'default-i':
        if not load:
            load = 35
        ec = 5.55 * consumption
    elif type == 'LT3B':
        if not load:
            load = 40
        ec = 5.95 * consumption
    dc = 355 * load
    return (dc + ec + wc) * 1.075 + st


def get_tarif_bill(consumption, type, load=None):
    if type == 'R':
        tarif = get_resident_tarif(consumption)
    elif type in {'LT2A', 'LT2B', 'LT2C', 'default-c'}:
        tarif = get_commercial_tarif(consumption, type, load)
    elif type in {'LT3A', 'LT3B', 'default-i'}:
        tarif = get_industrial_tarif(consumption, type, load)
    bill = tarif * 12
    return tarif, bill



@app.route('/', methods=['GET', 'POST'])
def home():
    input_form = UserInputForm()
    if request.method == "GET":
        return render_template('home.html', form=input_form)
    elif request.method == "POST":
        input_form = UserInputForm(request.form)
        state = input_form.state.data
        peak_hrs = PEAK_HOURS[state]
        consumption = int(input_form.consumption.data)
        if consumption == 0:
            return '<h1 class="container mt-4">Please start using electricity first</h1>'
        connection_type = input_form.connection.data
        if connection_type == 'Residential':
            ctype = 'R'
        elif connection_type == 'Commercial':
            ctype = input_form.commercial_type.data
        elif connection_type == 'Industrial':
            ctype = input_form.industrial_type.data

        load = input_form.connected_load.data
        if load != None:
            load = int(load)

        # 1. System Size
        system_size = get_system_size(consumption, peak_hrs)

        # 2. Area Req
        no_of_panels, area, area_sq_ft = get_required_area(system_size)

        # 3. Cost
        cost = get_cost(system_size)

        # 4. Tarif and Annual Bill
        tarif, bill = get_tarif_bill(consumption, ctype, load)

        # 5. ROI
        roi = max(0.2, bill / cost)

        # 6. Years
        years = ceil(1 / roi)

        # 7. Years of Profit
        profit_years = 25 - years

        results = {
            'state': state,
            'consumption': consumption,
            'connection': connection_type,
            'system_size': round(system_size, 2),
            'no_of_panels': ceil(no_of_panels),
            'area': round(area, 2),
            'area_sq_ft': round(area_sq_ft, 2),
            'cost': round(cost, 2),
            # 'tarif': tarif,
            # 'bill': bill,
            'roi': round(roi, 2),
            'years': years,
            'profit_years': profit_years
        }

        # DEBUG
        # print(f'System Size: {system_size}')
        # print(f'No of Panels: {no_of_panels} | Area: {area} | Area sq ft: {area_sq_ft}')
        # print(f'Cost: {cost}')
        # print(f'Tarif: {tarif} | Bill: {bill}')
        # print(f'ROI: {roi}')
        # print(f'Years: {years}')
        # print(f'Profit Years: {profit_years}')
        print(f'Connection Type: {ctype}')

        return render_template('results.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
