# Monthly Payment List Report for One Stop Insurance Company
# Rob Vatcher
# July 30th, 2023

# Import necessary modules
import datetime
import FormatValues as FV

POLICIES_FILE = "Policies.dat"

# Read the defaults file
with open("OSICDef.dat", 'r') as file:
    lines = file.readlines()
    base_premium = float(lines[1].strip())
    discount = float(lines[2].strip())
    liability_cost = float(lines[3].strip())
    glass_cost = float(lines[4].strip())
    loaner_cost = float(lines[5].strip())

# Before the loop: Print headings, Initialize summary data, Open the file.
print()
print("ONE STOP INSURANCE COMPANY")
print(f"POLICY LISTING AS OF {FV.FDateS(datetime.datetime.now()):<10s}")
print()
print("POLICY      CUSTOMER                  POLICY     INSURANCE     EXTRA       TOTAL")
print("NUMBER       NAME                      DATE       PREMIUM      COSTS      PREMIUM")
print("=" * 82)

# Initialize counters and accumulators
total_policies = 0
total_insurance_premium = 0
total_extra_costs = 0
total_premium = 0

# Loop through the file: Read the next record, Print the detail line, Accumulate the summary data.
with open(POLICIES_FILE, "r") as PolicyFile:
    for line in PolicyFile:
        policy_details = line.strip().split(',')

        # Check if the record has the required number of fields
        if len(policy_details) < 14:
            print(f"Skipping incomplete record: {line.strip()}")
            continue

        policy_number = policy_details[0]
        customer_name = policy_details[2] + ' ' + policy_details[3]
        policy_date = policy_details[1]
        num_cars = int(policy_details[9])

        # Compute insurance premium for each car
        insurance_premium = base_premium + (num_cars - 1) * base_premium * (1 - discount)

        # Compute the extra costs for each car
        extra_costs = 0
        liability_coverage = policy_details[10]
        glass_coverage = policy_details[11]
        loaner_coverage = policy_details[12]

        # Count the "Y"s and calculate extra costs
        extra_costs += liability_coverage.count("Y") * liability_cost
        extra_costs += glass_coverage.count("Y") * glass_cost
        extra_costs += loaner_coverage.count("Y") * loaner_cost

        total_premium_for_policy = insurance_premium + extra_costs

        print(
            f"{policy_number:<10s}{customer_name:<25s}{policy_date:<10s}  {FV.FDollar2(insurance_premium):>10s}  "
            f"{FV.FDollar2(extra_costs):>10s}  {FV.FDollar2(total_premium_for_policy):>10s}")

        total_policies += 1
        total_insurance_premium += insurance_premium
        total_extra_costs += extra_costs
        total_premium += total_premium_for_policy


print("=" * 82)
print(
    f"{'TOTALS':<10s}                       {FV.FDollar2(total_insurance_premium):>25s}  {FV.FDollar2(total_extra_costs):>10s}  {FV.FDollar2(total_premium):>10s}")
print(f"Total policies: {total_policies}")
print()
print("END OF REPORT")
print()























