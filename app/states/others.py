from math import ceil

class Others:
    # constants
    PANEL_SIZE = 0.46
    PANEL_AREA = 2.22
    COST_1 = 53000
    COST_2 = 1000
    PEAK_HOURS = 4.47
    STATE = ''

    def __init__(self, consumption, tarif, state):
        self.consumption = consumption
        self.tarif = tarif
        self.STATE = state

    def get_system_size(self):
        return self.consumption / (30 * self.PEAK_HOURS)

    def get_required_area(self):
        # 2.1
        no_of_panels = self.system_size / self.PANEL_SIZE
        # 2.2
        area = no_of_panels * self.PANEL_AREA
        area_sq_ft = area * 10.76

        return no_of_panels, area, area_sq_ft

    def get_cost(self):
        return ((self.system_size * self.COST_1) + (self.system_size * self.COST_2)) * 1.1

    def get_bill(self):
        bill = self.tarif * 12
        return bill

    def get_results(self):
        # 1. System Size
        self.system_size = self.get_system_size()

        # 2. Area Req
        self.no_of_panels, self.area, self.area_sq_ft = self.get_required_area()

        # 3. Cost
        self.cost = self.get_cost()

        # 4. Tarif and Annual Bill
        self.bill = self.get_bill()

        # 5. ROI
        self.roi = max(0.2, self.bill / self.cost)

        # 6. Years and months
        years_months = ceil(12 / self.roi)
        self.years = years_months // 12
        self.months = years_months % 12

        # 7. Years of Profit
        profit_years_months = 300 - years_months
        self.profit_years = profit_years_months // 12
        self.profit_months = profit_years_months % 12

        return {
                'state': self.STATE,
                'consumption': self.consumption,
                'connection': 'Others',
                'system_size': round(self.system_size, 2),
                'no_of_panels': ceil(self.no_of_panels),
                'area': round(self.area, 2),
                'area_sq_ft': round(self.area_sq_ft, 2),
                'cost': round(self.cost, 2),
                'tarif': round(self.tarif, 2),
                'bill': self.bill,
                'roi': round(self.roi, 2) * 100,
                'years': self.years,
                'months': self.months,
                'profit_years': self.profit_years,
                'profit_months': self.profit_months
            }