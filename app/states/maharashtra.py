from math import ceil

class Maharashtra:
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
        wc = 1.47
        ed = 1.16
        st = 0.2604
        tariff = 0
        consumption = self.consumption

        def get_tarrif_0_to_100(consumption):
            fc = 80
            ec = 3.05
            return (fc + consumption * ec + consumption * wc) * ed + (st * consumption)

        def get_tarrif_100_to_300(consumption):
            fc = 120
            ec = 5
            return (fc + consumption * ec + consumption * wc) * ed + (st * consumption)

        def get_tarrif_300_to_500(consumption):
            fc = 120
            ec = 6.7
            return (fc + consumption * ec + consumption * wc) * ed + (st * consumption)

        def get_tarrif_greater_500(consumption):
            fc = 145
            ec = 7.8
            return (fc + consumption * ec + consumption * wc) * ed + (st * consumption)

        if 0 <= consumption <= 100:
            tariff += get_tarrif_0_to_100(consumption)
        elif 100 < consumption <= 300:
            tariff += get_tarrif_0_to_100(100)
            tariff += get_tarrif_100_to_300(consumption - 100)
        elif 300 < consumption <= 500:
            tariff += get_tarrif_0_to_100(100)
            tariff += get_tarrif_100_to_300(200)
            tariff += get_tarrif_300_to_500(consumption - 300)
        elif consumption > 500:
            tariff += get_tarrif_0_to_100(100)
            tariff += get_tarrif_100_to_300(200)
            tariff += get_tarrif_300_to_500(200)
            tariff += get_tarrif_greater_500(consumption - 500)

        return tariff

    def get_commercial_tarif(self):
        if self.type == 'LT2A':
            fc = 425
            ec = 5.45 * self.consumption
            wc = 1.47 * self.consumption
            st = 0.3404 * self.consumption
            return (fc + ec + wc) * 1.21 + st

        if self.type in {'LT2B', 'default-c'}:
            if not self.load:
                self.load = 35
            ec = 6 * self.consumption
        elif self.type == 'LT2C':
            if not self.load:
                self.load = 60
            ec = 6.55 * self.consumption
        dc = 355 * self.load
        wc = 1.47 * self.consumption
        st = 0.3404 * self.consumption

        return (dc + ec + wc) * 1.21 + st


    def get_industrial_tarif(self):
        wc = 1.47 * self.consumption
        st = 0.3404 * self.consumption

        if self.type == 'LT3A':
            fc = 425
            ec = 5.55 * self.consumption
            return (fc + ec + wc) * 1.075 + st
        if self.type == 'default-i':
            if not load:
                load = 35
            ec = 5.55 * self.consumption
        elif self.type == 'LT3B':
            if not load:
                load = 40
            ec = 5.95 * self.consumption
        dc = 355 * load
        return (dc + ec + wc) * 1.075 + st


    def get_tarif_bill(self):
        if self.type == 'R':
            tarif = self.get_resident_tarif()
        elif self.type in {'LT2A', 'LT2B', 'LT2C', 'default-c'}:
            tarif = self.get_commercial_tarif()
        elif self.type in {'LT3A', 'LT3B', 'default-i'}:
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
        self.years = ceil(1 / self.roi)

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