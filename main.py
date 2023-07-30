# Invoice and Customer Data Program for One Stop Insurance
# Written by: Rob Vatcher
# Date: July 30th, 2023

import datetime
import time
from tqdm import tqdm

# Dat files

DEFAULTS_FILE = "OSICDef.dat"
POLICIES_FILE = "Policies.dat"

# Functions


def validate_province(province):
    provinces = ["NL", "PE", "NS", "NB", "QC", "ON", "MB", "SK", "AB", "BC", "YT", "NT", "NU"]
    return province.upper() in provinces


def calculate_total_premium(cars, extra_liability, glass_coverage, loaner_car, base_premium, discount,
                            liability_cost, glass_cost, loaner_cost):
    car_costs = []
    extra_liability_costs = []
    glass_coverage_costs = []
    loaner_car_costs = []
    for i in range(cars):
        car_costs.append(base_premium if i == 0 else base_premium * (1 - discount))
        extra_liability_costs.append(extra_liability[i] * liability_cost)
        glass_coverage_costs.append(glass_coverage[i] * glass_cost)
        loaner_car_costs.append(loaner_car[i] * loaner_cost)

    total_premium = sum(car_costs) + sum(extra_liability_costs) + sum(glass_coverage_costs) + sum(loaner_car_costs)

    return total_premium, car_costs, extra_liability_costs, glass_coverage_costs, loaner_car_costs


def calculate_total_cost(total_premium, hst_rate, processing_fee, payment_method):
    hst = total_premium * hst_rate
    total_cost = total_premium + hst
    if payment_method == "Monthly":
        total_cost += processing_fee
    return total_cost


def save_policy(policy_data):
    with open(POLICIES_FILE, "a") as f:
        f.write(policy_data + "\n")


def update_defaults(policy_number, base_premium, discount, liability_cost, glass_cost, loaner_cost, hst_rate, processing_fee):
    with open(DEFAULTS_FILE, "w") as f:
        f.write(f"{policy_number}\n{base_premium}\n{discount}\n{liability_cost}\n{glass_cost}\n{loaner_cost}\n{hst_rate}\n{processing_fee}")


def get_defaults():
    with open(DEFAULTS_FILE, "r") as f:
        lines = f.readlines()
        policy_number = int(lines[0].strip())
        base_premium = float(lines[1].strip())
        discount = float(lines[2].strip())
        liability_cost = float(lines[3].strip())
        glass_cost = float(lines[4].strip())
        loaner_cost = float(lines[5].strip())
        hst_rate = float(lines[6].strip())
        processing_fee = float(lines[7].strip())
    return policy_number, base_premium, discount, liability_cost, glass_cost, loaner_cost, hst_rate, processing_fee


def format_date(date):
    return date.strftime("%Y-%m-%d")


def format_receipt(policy_number, current_date, first_name, last_name, address, city, province, postal_code, phone_number,
                   cars, extra_liability, glass_coverage, loaner_car, payment_method, total_premium, base_premium,
                   car_costs, extra_liability_costs, glass_coverage_costs, loaner_car_costs, discount, hst_rate,
                   processing_fee, monthly_payment, next_payment_date):

    receipt = "--------------------------------------\n"
    receipt += "       ONE STOP INSURANCE RECEIPT      \n"
    receipt += "--------------------------------------\n\n"
    receipt += f"Policy Number: {policy_number}\n"
    receipt += f"Date: {format_date(current_date)}\n"
    receipt += f"Name: {first_name} {last_name}\n"
    receipt += f"Address: {address}\n"
    receipt += f"City: {city}\n"
    receipt += f"Province: {province}\n"
    receipt += f"Postal Code: {postal_code}\n"
    receipt += f"Phone Number: {phone_number}\n"
    receipt += "-----------------------------------------\n"
    receipt += "               COVERAGE              \n"
    receipt += "-----------------------------------------\n"
    receipt += f"Number of Cars Insured:    {cars:>14}\n"
    for i in range(cars):
        receipt += f"Base Premium (car {i+1}):     {'$' + format(car_costs[i], '.2f'):>15}\n"
        receipt += f"Extra Liability (car {i+1}):  {'Included' if extra_liability[i] else 'Not Included':>15}\n"
        if extra_liability[i]:
            receipt += f"Extra Liability Cost (car {i+1}):  {'$'+format(extra_liability_costs[i], '.2f'):>10}\n"
        receipt += f"Glass Coverage (car {i+1}):  {'Included' if glass_coverage[i] else 'Not Included':>16}\n"
        if glass_coverage[i]:
            receipt += f"Glass Coverage Cost (car {i+1}):  {'$'+format(glass_coverage_costs[i], '.2f'):>11}\n"
        receipt += f"Loaner Car (car {i+1}):  {'Included' if loaner_car[i] else 'Not Included':>20}\n"
        if loaner_car[i]:
            receipt += f"Loaner Car Cost (car {i+1}): {'$'+format(loaner_car_costs[i], '.2f'):>16}\n"
        receipt += "\n"

    if cars > 1:
        receipt += f"Extra Vehicle Discount:           {discount * 100:>6.0f}%\n"

    receipt += "-----------------------------------------\n"
    receipt += "             PAYMENT INFO            \n"
    receipt += "-----------------------------------------\n"
    receipt += f"Payment Method:               {payment_method:>11}\n"
    if payment_method == 'Full':
        receipt += "Processing Fee:                       N/A\n"
        receipt += "Monthly Payment:                      N/A\n"
        receipt += "Next Payment Date:                    N/A\n"
    else:
        receipt += f"Processing Fee:                {'$' + format(processing_fee, '.2f'):>10}\n"
        receipt += f"Monthly Payment:              {'$' + format(monthly_payment, '.2f'):>11}\n"
        receipt += f"Next Payment Date:             {format_date(next_payment_date)}\n"
    receipt += "-----------------------------------------\n"

    receipt += "             COST SUMMARY          \n"
    receipt += "-----------------------------------------\n"
    receipt += f"Total Premium:               {'$'+format(total_premium, '.2f'):>12}\n"
    receipt += f"HST:                          {'$' + format(total_premium * hst_rate, '.2f'):>11}\n"
    if payment_method == "Monthly":
        receipt += f"Processing Fee:                    ${processing_fee:.2f}\n"
    else:
        receipt += f"Processing Fee:                       N/A\n"
    receipt += "-----------------------------------------\n"
    receipt += f"Total:                     {'$' + format(calculate_total_cost(total_premium, hst_rate, processing_fee, payment_method), '.2f'):>14}\n"
    receipt += "-----------------------------------------\n"
    receipt += "        THANK YOU FOR CHOOSING       \n"
    receipt += "           ONE STOP INSURANCE       \n"
    receipt += "-----------------------------------------\n"
    return receipt


def main():
    defaults_data = get_defaults()
    policy_number, base_premium, discount, liability_cost, glass_cost, loaner_cost, hst_rate, processing_fee = defaults_data

    # Convert policy_number to an integer
    policy_number = int(policy_number)

    while True:
        policy_number += 1  # Increment policy_number here

        print("Enter customer information:")
        first_name = input("First Name: ").title()
        last_name = input("Last Name: ").title()
        address = input("Address: ").title()
        city = input("City: ").title()
        province = input("Province (2-letter code): ").upper()
        while not validate_province(province):
            print("Invalid province. Please enter a valid 2-letter code.")
            province = input("Province (2-letter code): ").upper()
        postal_code = input("Postal Code: ").upper()
        phone_number = input("Phone Number(999-999-9999): ")
        cars = int(input("Number of Cars Insured: "))
        cars = min(cars, 10)  # Limit the number of cars to 10

        # Collect coverage options for each car
        extra_liabilities = [input(f"Extra Liability for car {i+1} (Y/N): ").upper() == "Y" for i in range(cars)]
        glass_coverages = [input(f"Glass Coverage for car {i+1} (Y/N): ").upper() == "Y" for i in range(cars)]
        loaner_cars = [input(f"Loaner Car for car {i+1} (Y/N): ").upper() == "Y" for i in range(cars)]

        payment_method = input("Payment Method (Full/Monthly): ").title()
        while payment_method not in ["Full", "Monthly"]:
            print("Invalid payment method. Please enter either 'Full' or 'Monthly'.")
            payment_method = input("Payment Method (Full/Monthly): ").title()

        # Calculations
        total_premium, car_costs, extra_liability_costs, glass_coverage_costs, loaner_car_costs = calculate_total_premium(
            cars, extra_liabilities, glass_coverages, loaner_cars, base_premium, discount, liability_cost, glass_cost,
            loaner_cost)

        total_cost = calculate_total_cost(total_premium, hst_rate, processing_fee, payment_method)
        monthly_payment = total_cost / 8 if payment_method == "Monthly" else 0

        next_payment_date = datetime.datetime.now().replace(day=1) + datetime.timedelta(days=32)
        next_payment_date = next_payment_date.replace(day=1)

        receipt = format_receipt(policy_number, datetime.datetime.now(), first_name, last_name, address, city, province,
                                 postal_code, phone_number, cars, extra_liabilities, glass_coverages, loaner_cars,
                                 payment_method, total_premium, base_premium, car_costs, extra_liability_costs,
                                 glass_coverage_costs, loaner_car_costs, discount, hst_rate, processing_fee, monthly_payment, next_payment_date)

        print("\nReceipt:\n")
        print(receipt)

        policy_data = f"{policy_number}, {format_date(datetime.datetime.now())}, {first_name}, {last_name}, {address}, {city}, {province}, {postal_code}, {phone_number}, {cars}, {''.join(['Y' if x else 'N' for x in extra_liabilities])}, {''.join(['Y' if x else 'N' for x in glass_coverages])}, {''.join(['Y' if x else 'N' for x in loaner_cars])}, {payment_method}, {total_premium:.2f}, {monthly_payment:.2f}, {format_date(next_payment_date) if next_payment_date else 'N/A'}"
        save_policy(policy_data)

        print()
        print()
        print("Saving data - please wait")
        # Processing bar
        for _ in tqdm(range(20), desc="Processing", unit="ticks", ncols=100, bar_format="{desc}  {bar}"):
            time.sleep(.1)
        print("Data successfully saved ...")
        time.sleep(1)

        print("Policy information processed and saved.")

        continue_input = input("\nEnter another policy? (Y/N): ").upper()
        if continue_input != "Y":
            update_defaults(policy_number, base_premium, discount, liability_cost, glass_cost, loaner_cost, hst_rate,
                            processing_fee)
            defaults_data = get_defaults()  # Update defaults_data after calling update_defaults
            print("Program ended.")
            break

# Run the main function


main()

