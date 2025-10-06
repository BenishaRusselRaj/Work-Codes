from flask import Flask, render_template, request
import math

def number_format(number):
    s = str(abs(int(number)))
    if len(s) <= 3:
        return s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.append(rest)
        return ','.join(parts[::-1]) + ',' + last3

Flask_App = Flask(__name__)

@Flask_App.route('/', methods = ['GET'])

def index():
    return render_template('index.html')

@Flask_App.route('/section1_result/', methods = ['POST'])
def section1_result():
    error = None
    result = None

    # request.form looks for:
    # html tags with matching "name= "
    number_of_zets_per_day = request.form['ZetNum']  
    length_of_highway = request.form['highwayLength']
    state_name = request.form['state']
    solar_percentage = request.form['solar']
    investment_type = request.form['investmentType']

# Setting default values
    tax_percentage = 5 * 0.01  # 5% tax
    per_unit_DG_cost = 31.33
    meter_rent = 3965
    converter_cost_per_kw = 3700
    re_maintenance_cost_percent = 1.4 * 0.01
    grid_per_unit_emissions = 0.727
    wind_per_unit_emissions = 0.126
    solar_per_unit_emissions = 0.045
    wind_per_unit_group_captive = 4.52
    solar_per_unit_group_captive = 4.57


    truck_capacity = 230
    truck_range = 208
    charge_available_in_vehicle = 50 * 0.01
    solar_output_per_kw = 4.5
    wind_output_per_kw = 7.2
    captive_solar_per_mw = 34400000 # 3,44,00,000
    captive_wind_per_mw = 80500000 # 8,05,00,000
    group_captive_solar_per_mw = 3200000 # 32,00,000
    group_captive_wind_per_mw = 7000000 # 70,00,000
    land_required_solar_per_mw = 3.5
    land_required_wind_per_mw = 1.5


    try:
        number_of_zets_per_day = float(number_of_zets_per_day)
        length_of_highway = float(length_of_highway)
        solar_percentage = float(solar_percentage) * 0.01

        
        frequency_of_charging = (length_of_highway) / (truck_range)

        if frequency_of_charging > 1:
            no_of_vehicles_to_charge_per_day = (1 * number_of_zets_per_day * charge_available_in_vehicle) + (number_of_zets_per_day * (frequency_of_charging - 1))
        else:
            no_of_vehicles_to_charge_per_day = number_of_zets_per_day * frequency_of_charging * charge_available_in_vehicle
        
        # Calculate outputs for Section 1

        # Output #1
        energy_required_per_day = truck_capacity * no_of_vehicles_to_charge_per_day

        # Output #2
        required_re_capacity = (((energy_required_per_day * solar_percentage) / solar_output_per_kw) + ((energy_required_per_day * (1 - solar_percentage)) / wind_output_per_kw)) / 1000
        required_re_capacity_solar = ((energy_required_per_day * solar_percentage) / solar_output_per_kw) / 1000
        required_re_capacity_wind = ((energy_required_per_day * (1 - solar_percentage)) / wind_output_per_kw) / 1000

        # Calculate output for section 2
        energy_required_per_hour = energy_required_per_day / 24
        demand_kw = 500 * round(energy_required_per_hour / 500)
        total_converter_cost = converter_cost_per_kw * 2 * demand_kw
        
        if state_name == "TN":
            per_unit_grid_rate = 8.2
            demand_charges = 145
            grid_avg_rate_DG = 9.06
            solar_tnd = 1.25
            wind_tnd = 1.19
            

        elif state_name == "KA":
            per_unit_grid_rate = 7.4
            demand_charges = 80
            grid_avg_rate_DG = 9.98
            solar_tnd = 1.31
            wind_tnd = 1.43

        else:
            return render_template(
                'index.html',
                ZetNum = math.floor(number_of_zets_per_day),
                highwayLength = math.floor(length_of_highway),
                state = state_name,
                investmentType=investment_type,
                solar = math.floor(solar_percentage * 100),
                wind = math.floor((1 - solar_percentage) * 100),
                energy_required_per_day = "Bad Input",
                calculation_success=False,
                error="Invalid State Selected"
            )
        
        coal_powered_cost_per_month = ((energy_required_per_day * 0.95 * per_unit_grid_rate) + 
                                       (energy_required_per_day * 0.05 * per_unit_DG_cost) + 
                                       (demand_kw * demand_charges) + 
                                       meter_rent) * 30
        


        if investment_type == "C":
            re_total_cost = (captive_solar_per_mw * required_re_capacity_solar) + (captive_wind_per_mw * required_re_capacity_wind)
            
            re_cost_per_month = ((energy_required_per_day * 0.075 * 8.2) +
                                (energy_required_per_day * 0.025 * per_unit_DG_cost) +
                                (demand_kw * demand_charges) + 
                                meter_rent +
                                (energy_required_per_day * 0.9 * solar_percentage * solar_tnd) +
                                (energy_required_per_day * 0.9 * (1 - solar_percentage) * wind_tnd)) * 30
            
            total_investment_converter_maintenance = total_converter_cost + re_total_cost + (re_total_cost * re_maintenance_cost_percent)
            total_cost_incurred = (((((energy_required_per_day * solar_percentage) / (solar_output_per_kw)) / 1000) * captive_solar_per_mw) + 
                               ((((energy_required_per_day * (1 - solar_percentage)) / (wind_output_per_kw)) / 1000) * captive_wind_per_mw))



        elif investment_type == "GC":
            re_total_cost = ((group_captive_solar_per_mw * required_re_capacity_solar) + 
                             (group_captive_wind_per_mw * required_re_capacity_wind))
            
            re_cost_per_month = ((energy_required_per_day * 0.075 * 8.2) +
                                (energy_required_per_day * 0.025 * per_unit_DG_cost) +
                                (demand_kw * demand_charges) + 
                                meter_rent +
                                (energy_required_per_day * 0.9 * solar_percentage * solar_per_unit_group_captive) +
                                (energy_required_per_day * 0.9 * (1 - solar_percentage) * wind_per_unit_group_captive)) * 30
            
            total_investment_converter_maintenance = total_converter_cost + re_total_cost
            total_cost_incurred = (((((energy_required_per_day * solar_percentage) / (solar_output_per_kw)) / 1000) * group_captive_solar_per_mw) + 
                               ((((energy_required_per_day * (1 - solar_percentage)) / (wind_output_per_kw)) / 1000) * group_captive_wind_per_mw))

        else:
            return render_template(
                'index.html',
                ZetNum = math.floor(number_of_zets_per_day),
                highwayLength = math.floor(length_of_highway),
                state = state_name,
                investmentType=investment_type,
                solar = math.floor(solar_percentage * 100),
                wind = math.floor((1 - solar_percentage) * 100),
                energy_required_per_day = "Bad Input",
                calculation_success=False,
                error="Invalid Investment Type Selected"
            )


    
        total_land_required_for_re_infrastructure = ((land_required_solar_per_mw * required_re_capacity_solar) + 
                                                     (land_required_wind_per_mw * required_re_capacity_wind))

        
        annual_cost_savings = (coal_powered_cost_per_month - re_cost_per_month) * 12

        # Output #5
        emissions_for_coal_powered = (energy_required_per_day * 0.03 * grid_per_unit_emissions)
        emissions_for_re_powered = ((energy_required_per_day * 0.03 * wind_per_unit_emissions * (1 - solar_percentage)) +
                                    (energy_required_per_day * 0.03 * solar_per_unit_emissions * solar_percentage))
        
        # Output #6
        percentage_decrease_in_emissions = ((emissions_for_coal_powered - emissions_for_re_powered) / emissions_for_coal_powered) * 100

        # Output #1
        energy_required_per_day = round(energy_required_per_day, 2)
        required_re_capacity = round(required_re_capacity, 2)
        
        # Output #2
        total_cost_incurred = round(total_cost_incurred)                    

        # Output #3
        total_land_required_for_re_infrastructure = round(total_land_required_for_re_infrastructure, 2)


        # Output #4
        annual_cost_savings = round(annual_cost_savings)

        # Output #5
        emissions_for_coal_powered = round(emissions_for_coal_powered)
        emissions_for_re_powered = round(emissions_for_re_powered)

        # Output #6
        percentage_decrease_in_emissions = round(percentage_decrease_in_emissions)

        # Output #7
        required_re_capacity_solar = round(required_re_capacity_solar, 2)
        required_re_capacity_wind = round(required_re_capacity_wind, 2)


        return render_template(
            'index.html',
            ZetNum = math.floor(number_of_zets_per_day),
            highwayLength = math.floor(length_of_highway),
            state = state_name,
            solar = math.floor(solar_percentage * 100),
            wind = math.floor((1 - solar_percentage) * 100),
            investmentType=investment_type,

            energy_required_per_day = energy_required_per_day,
            required_re_capacity = required_re_capacity,
            required_re_capacity_solar = required_re_capacity_solar,
            required_re_capacity_wind = required_re_capacity_wind,

            total_cost_incurred = number_format(total_cost_incurred),
            total_land_required_for_re_infrastructure = total_land_required_for_re_infrastructure,

            annual_cost_savings = number_format(annual_cost_savings),

            emissions_for_coal_powered = emissions_for_coal_powered,
            emissions_for_re_powered = emissions_for_re_powered,
            percentage_decrease_in_emissions = percentage_decrease_in_emissions,
            
            calculation_success = True
        )
        
    except ZeroDivisionError:
        return render_template(
            'index.html',
            ZetNum = math.floor(number_of_zets_per_day),
            highwayLength = math.floor(length_of_highway),
            state = state_name,
            investmentType=investment_type,
            solar = math.floor(solar_percentage * 100),
            wind = math.floor((1 - solar_percentage) * 100),
            energy_required_per_day = "Bad Input",
            calculation_success=False,
            error="You cannot divide by zero"
        )
        
    except ValueError:
        return render_template(
            'index.html',
            ZetNum = math.floor(number_of_zets_per_day),
            highwayLength = math.floor(length_of_highway),
            state = state_name,
            investmentType=investment_type,
            solar = math.floor(solar_percentage * 100),
            wind = math.floor((1 - solar_percentage) * 100),
            energy_required_per_day = "Bad Input",
            calculation_success=False,
            error="Cannot perform numeric operations with provided input"
        )

if __name__ == '__main__':
    Flask_App.debug = True
    Flask_App.run()
    
