import pandas as pd
from flask import Flask, request, url_for, render_template
from forms import UserInputForm
from states.others import Others

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THISisNOTsoSECRET'
app.config['DEBUG'] = True


def create_table(principal, consumption, tarif):
    rate = tarif / consumption
    annual_consumption = consumption * 12
    maintenance_cost = 0
    period = 25
    net_savings = 0
    break_even = False
    data_dict = {
        'Year': [],
        'KWH': [],
        'Rate': [],
        'Savings': [],
        'Maintenance': [],
        'Net Savings': [],
    }

    for year in range(1, period + 1):
        annual_output = annual_consumption * (0.90 if year <= 10 else 0.85)
        savings = annual_output * rate
        net_savings += savings - maintenance_cost

        data_dict['Year'].append(year)
        data_dict['KWH'].append(annual_output)
        data_dict['Rate'].append(rate)
        data_dict['Savings'].append(round(savings, 2))
        data_dict['Maintenance'].append(maintenance_cost)
        if not break_even and net_savings >= principal:
            data_dict['Net Savings'].append(f'{str(round(net_savings, 2))} (Break Even)')
            break_even = True
        else:
            data_dict['Net Savings'].append(str(round(net_savings, 2)))

        rate += (rate * 0.03 if year <= 10 else 0)
        if year == 3:
            maintenance_cost = principal * 0.025
        elif year > 3:
            maintenance_cost += maintenance_cost * 0.05

    rounded_df = pd.DataFrame(data_dict).round(2)
    # print(rounded_df.to_html())
    return rounded_df.to_html(
        index=False,
        classes='table table-bordered table-hover table-responsive',
        justify='justify-all'
    )


@app.route('/', methods=['GET', 'POST'])
def home():
    input_form = UserInputForm()
    if request.method == "GET":
        return render_template('home.html', form=input_form)
    elif request.method == "POST":
        consumption = int(input_form.consumption.data)
        tariff = float(input_form.tariff.data)
        if consumption == 0:
            return '<h1 class="container mt-4">Please start using electricity first</h1>'

        results = Others(consumption, tariff).get_results()

        # DEBUG
        # print(f'System Size: {system_size}')
        # print(f'No of Panels: {no_of_panels} | Area: {area} | Area sq ft: {area_sq_ft}')
        # print(f'Cost: {cost}')
        # print(f'Tarif: {tarif} | Bill: {results["bill"]}')
        # print(f'ROI: {roi}')
        # print(f'Years: {years}')
        # print(f'Profit Years: {profit_years}')
        # print(f'Connection Type: {ctype}')

        data_table = create_table(results['cost'], consumption, results['tarif'])
        return render_template(
            'results.html',
            results=results,
            data_table=data_table
        )


if __name__ == "__main__":
    app.run()
