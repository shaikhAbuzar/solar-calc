from math import ceil

class MadhyaPradesh:
    # constants
    PANEL_SIZE = 0.46
    PANEL_AREA = 2.22
    COST_1 = 53000
    COST_2 = 1000
    PEAK_HOURS = 4.47
    CONNECTION_TYPES = {
        'Residential': 'R',
        'Commercial - LT2A': 'LT2A',
        'Commercial - LT2B': 'LT2B',
        'Commercial - LT2C': 'LT2C',
        'Industrial - LT3A': 'LT3A',
        'Industrial - LT3B': 'LT3B',
    }
    STATE = 'Maharashtra'

    def __init__(self, consumption, connection_type, type, load=None):
        self.consumption = consumption
        self.connection_type = connection_type
        self.type = type
        self.load = load

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

    def get_resident_tarif(self):
        consumption = self.consumption
        fac = 0.07 * consumption
        fc = 1.67 * consumption
        ed = 1.12
        tariff = 0

        def get_tarrif_0_to_50(consumption):
            ec = 4.21
            return fc + (consumption * ec + consumption * fac) * ed

        def get_tarrif_50_to_150(consumption):
            ec = 5.17
            return fc + (consumption * ec + consumption * fac) * ed

        def get_tarrif_150_to_300(consumption):
            ec = 6.55
            return fc + (consumption * ec + consumption * fac) * ed

        def get_tarrif_greater_300(consumption):
            ec = 6.74
            return fc + (consumption * ec + consumption * fac) * ed

        if 0 <= consumption <= 50:
            tariff += get_tarrif_0_to_50(consumption)
        elif 50 < consumption <= 150:
            tariff += get_tarrif_0_to_50(50)
            tariff += get_tarrif_50_to_150(consumption - 50)
        elif 150 < consumption <= 300:
            tariff += get_tarrif_0_to_50(50)
            tariff += get_tarrif_50_to_150(100)
            tariff += get_tarrif_150_to_300(consumption - 150)
        elif consumption > 300:
            tariff += get_tarrif_0_to_50(50)
            tariff += get_tarrif_50_to_150(100)
            tariff += get_tarrif_150_to_300(150)
            tariff += get_tarrif_greater_300(consumption - 300)

        return tariff


    def get_commercial_tarif(self):
        if self.consumption <= 700:
            fc = 138
            ec = 7.8
            if not self.load:
                self.load = 6
        else:
            fc = 296
            ec = 6.9
            if not self.load:
                if self.type == 'small':
                    self.load = 30
                elif self.type in {'medium', 'default-c'}:
                    self.load = 50
                elif self.type == 'large':
                    self.load = 80
        return fc * self.load + (ec * self.consumption + 0.07 * self.consumption) * 1.15


    def get_industrial_tarif(self):
        if self.consumption <= 1000:
            fc = 224
            ec = 4.62
            if not self.load:
                self.load = 10
        else:
            fc = 320
            ec = 6.6
            if not self.load:
                if self.type == 'small':
                    self.load = 40
                elif self.type in {'medium', 'default-i'}:
                    self.load = 60
                elif self.type == 'heavy':
                    self.load = 90
        self.load = min(self.load, 112)
        return fc * self.load + (ec * self.consumption + 0.07 * self.consumption) * 1.09


    def get_tarif_bill(self):
        if self.type == 'R':
            tarif = self.get_resident_tarif()
        elif self.type in {'small', 'medium', 'large', 'default-c'}:
            tarif = self.get_commercial_tarif()
        elif self.type in {'small', 'medium', 'heavy', 'default-i'}:
            tarif = self.get_industrial_tarif()
        bill = tarif * 12
        return tarif, bill

    def get_results(self):
        # 1. System Size
        self.system_size = self.get_system_size()

        # 2. Area Req
        self.no_of_panels, self.area, self.area_sq_ft = self.get_required_area()

        # 3. Cost
        self.cost = self.get_cost()

        # 4. Tarif and Annual Bill
        self.tarif, self.bill = self.get_tarif_bill()

        # 5. ROI
        self.roi = max(0.2, self.bill / self.cost)

        # 6. Years
        years_months = ceil(1 / self.roi * 12)
        self.years = years_months // 12
        self.months = years_months % 12

        # 7. Years of Profit
        self.profit_years = 25 - self.years

        return {
                'state': self.STATE,
                'consumption': self.consumption,
                'connection': self.connection_type,
                'system_size': round(self.system_size, 2),
                'no_of_panels': ceil(self.no_of_panels),
                'area': round(self.area, 2),
                'area_sq_ft': round(self.area_sq_ft, 2),
                'cost': round(self.cost, 2),
                # 'tarif': self.tarif,
                # 'bill': self.bill,
                'roi': round(self.roi, 2),
                'years': self.years,
                'profit_years': self.profit_years
            }