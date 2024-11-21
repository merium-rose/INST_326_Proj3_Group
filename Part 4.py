# Data for caregivers: Name and weekly hours worked
caregivers = [
    {"name": "Alice", "hours": 35},
    {"name": "Bob", "hours": 40},
    {"name": "Charlie", "hours": 30},
    {"name": "Diana", "hours": 25}
]

# Constants
HOURLY_RATE = 20  # $20/hour

# Calculate weekly gross pay for each caregiver
for caregiver in caregivers:
    caregiver["weekly_pay"] = caregiver["hours"] * HOURLY_RATE

# Calculate totals
total_weekly_pay = sum(c["weekly_pay"] for c in caregivers)
total_monthly_pay = total_weekly_pay * 4  # Assume 4 weeks in a month

# Generate HTML report
html_report = """
<!DOCTYPE html>
<html>
<head>
    <title>Caregiver Pay Report</title>
    <style>
        table {{
            width: 50%;
            border-collapse: collapse;
            margin: 20px auto;
        }}
        table, th, td {{
            border: 1px solid black;
        }}
        th, td {{
            padding: 10px;
            text-align: center;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h1 style="text-align: center;">Caregiver Pay Report</h1>
    <table>
        <tr>
            <th>Caregiver</th>
            <th>Weekly Hours</th>
            <th>Weekly Pay ($)</th>
        </tr>
"""

for caregiver in caregivers:
    html_report += f"""
        <tr>
            <td>{caregiver['name']}</td>
            <td>{caregiver['hours']}</td>
            <td>{caregiver['weekly_pay']}</td>
        </tr>
    """

html_report += f"""
        <tr>
            <td colspan="2"><strong>Total Weekly Pay</strong></td>
            <td><strong>{total_weekly_pay}</strong></td>
        </tr>
        <tr>
            <td colspan="2"><strong>Total Monthly Pay</strong></td>
            <td><strong>{total_monthly_pay}</strong></td>
        </tr>
    </table>
</body>
</html>
"""

# Save HTML report to file
with open("caregiver_pay_report.html", "w") as file:
    file.write(html_report)

print("Pay report generated: caregiver_pay_report.html")