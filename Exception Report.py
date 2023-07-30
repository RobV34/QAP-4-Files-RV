# Monthly Payment List Report for One Stop Insurance Company
# Rob Vatcher
# July 30th, 2023

# Import necessary modules
import datetime
import FormatValues as FV

# Constants
HST_RATE = 0.15

POLICIES_FILE = "Policies.dat"

# Before the loop: Print headings, Initialize summary data, Open the file.
print()
print("ONE STOP INSURANCE COMPANY")
print(f"MONTHLY PAYMENT LISTING AS OF {FV.FDateS(datetime.datetime.now()):<10s}")
print()
print("POLICY    CUSTOMER                    TOTAL       TOTAL      TOTAL      MONTHLY")
print("NUMBER    NAME                       PREMIUM       HST       COST       PAYMENT")
print("="*79)

# Initialize counters and accumulators
total_policies = 0
total_premium = 0
total_hst = 0
total_cost = 0
total_monthly_payment = 0

# Loop through the file: Read the next record, Print the detail line, Accumulate the summary data.
with open(POLICIES_FILE, "r") as PolicyFile:
    for line in PolicyFile:
        policy_details = line.strip().split(',')
        if len(policy_details) < 16:  # Check if there are at least 16 fields in the line.
            print(f"Unexpected line format: {line}")
            continue

        # Only process the line if the payment option is 'Monthly'
        if policy_details[13].strip() == 'Monthly':
            policy_number = policy_details[0]
            customer_name = policy_details[2] + ' ' + policy_details[3]
            total_premium_for_policy = float(policy_details[14])
            hst = total_premium_for_policy * HST_RATE
            total_cost_for_policy = total_premium_for_policy + hst
            monthly_payment = float(policy_details[15])  # Convert string to float

            print(f"{policy_number:<10s}{customer_name:<25s}{FV.FDollar2(total_premium_for_policy):>10s} {FV.FDollar2(hst):>10s}  {FV.FDollar2(total_cost_for_policy):>10s} {FV.FDollar2(monthly_payment):>10s}")

            total_policies += 1
            total_premium += total_premium_for_policy
            total_hst += hst
            total_cost += total_cost_for_policy
            total_monthly_payment += monthly_payment



