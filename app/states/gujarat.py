from math import ceil

class Gujarat:
    # constants
    PANEL_SIZE = 0.46
    PANEL_AREA = 2.22
    COST_1 = 53000
    COST_2 = 1000
    PEAK_HOURS = 4.47
    CONNECTION_TYPES = {
        'Residential General Purpose': 'RGP',
        'Non Residential General Purpose': 'NRGP',
    }
    STATE = 'Gujarat'

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

    def get_rgp_tarif(self):
        consumption = self.consumption
        FPPPA = 2.17 * consumption

        if 0 < consumption <= 1000:
            ED = 1.15
            MF = 1
            if not self.load:
                self.load = 10
            self.load = min(15, self.load)
            FC = 70 * self.load
            EC = 3.2 * consumption
            if 50 < consumption <= 200:
                # consumption b/w 50 to 200
                EC += 3.95 * consumption
                MF = 2
            elif consumption > 200:
                # consumption b/w 50 to 200
                EC += 3.95 * consumption
                # consumption b/w 200 to 1000
                EC += 5 * consumption
                MF = 3

            return (FC * MF + EC + FPPPA * MF) * ED
        elif 1000 < consumption <= 3000:
            ED = 1.1
            FC = 150 * self.load

            if not self.load:
                self.load = 30
            self.load = max(15, self.load)
            self.load = min(50, self.load)
            EC = 4.65 * consumption

            return (FC + EC + FPPPA) * ED
        elif consumption > 3000:
            ED = 1.1
            MF = 1
            EC = 4.8 * consumption
            if not self.load:
                self.load = 75
            self.load = max(50, self.load)
            self.load = min(100, self.load)

            FC = 150 * self.load
            if 50 < self.load <= 80:
                # load b/w 50 to 80
                FC += 185 * self.load
                MF = 2
            elif 80 < self.load <= 100:
                # consumption b/w 50 to 80
                FC += 185 * self.load
                # consumption b/w 80 to 100
                FC += 245 * self.load
                MF = 3
            return (FC + EC * MF + FPPPA * MF) * ED


    def get_nrgp_tarif(self):
        consumption = self.consumption
        FPPPA = 2.17 * consumption

        if 0 < consumption <= 400:
            if not self.load:
                self.load = 5
            self.load = max(0, self.load)
            self.load = min(5, self.load)

            FC = 70 * self.load
            EC = 4.6 * consumption
            ED = 1.2
            return (FC + EC + FPPPA) * ED
        elif 400 < consumption <= 1000:
            if not self.load:
                self.load = 10
            self.load = max(5, self.load)
            self.load = min(15, self.load)

            FC = 90 * self.load
            EC = 4.6 * consumption
            ED = 1.2
            return (FC + EC + FPPPA) * ED
        elif 1000 < consumption <= 3000:
            if not self.load:
                self.load = 30
            self.load = max(15, self.load)
            self.load = min(30, self.load)

            FC = 175 * self.load
            EC = 4.8 * consumption
            ED = 1.1
            return (FC + EC + FPPPA) * ED
        elif consumption > 3000:
            ED = 1.1
            MF = 1
            EC = 5 * consumption
            if not self.load:
                self.load = 75
            self.load = max(50, self.load)
            self.load = min(100, self.load)

            FC = 175 * self.load
            if 50 < self.load <= 80:
                # load b/w 50 to 80
                FC += 230 * self.load
                MF = 2
            elif 80 < self.load <= 100:
                # consumption b/w 50 to 80
                FC += 230 * self.load
                # consumption b/w 80 to 100
                FC += 300 * self.load
                MF = 3
            return (FC + EC * MF + FPPPA * MF) * ED


    def get_tarif_bill(self):
        tarif = self.get_rgp_tarif() if self.type == 'RGP' else self.get_nrgp_tarif()

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

        # 6. Years and months
        years_months = ceil(1 / self.roi * 12)
        self.years = years_months // 12
        self.months = years_months % 12

        # 7. Years of Profit
        profit_years_months = 300 - years_months
        self.profit_years = profit_years_months // 12
        self.profit_months = profit_years_months % 12

        return {
                'state': self.STATE,
                'consumption': self.consumption,
                'connection': self.connection_type,
                'system_size': round(self.system_size, 2),
                'no_of_panels': ceil(self.no_of_panels),
                'area': round(self.area, 2),
                'area_sq_ft': round(self.area_sq_ft, 2),
                'cost': round(self.cost, 2),
                'tarif': round(self.tarif, 2),
                'bill': self.bill,
                'roi': round(self.roi, 2),
                'years': self.years,
                'months': self.months,
                'profit_years': self.profit_years,
                'profit_months': self.profit_months
            }