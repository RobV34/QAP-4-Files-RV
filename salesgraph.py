# Sales Graph
# Rob Vatcher
# July 26, 2023

import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = []

# Get user input for total sales for each month
for month in months:
    try:
        sales.append(float(input(f"Enter total sales for {month}: ")))
    except ValueError:
        print("Invalid input. Please enter a valid sales value.")

# Create the graph
plt.plot(months, sales, marker='o', linestyle='-', color='b')
plt.xlabel("Months")
plt.ylabel("Total Sales ($)")
plt.title("Total Sales per Month")

# Display the graph
plt.show()

