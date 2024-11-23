from datetime import datetime

class Caregiver:
    def __init__(self, name, phone, email, pay_rate):
        self.name = name
        self.phone = phone
        self.email = email
        self.pay_rate = pay_rate
        self.hours = 0  # Tracks total scheduled hours for the caregiver
        self.availability = self.initialize_availability()

    def initialize_availability(self):
        """Creates an availability dictionary for a month."""
        availability = {}
        for day in range(1, 32):  # Range for 1-31 inclusive
            availability[day] = {
                '7:00 AM - 1:00 PM': 'available',
                '1:00 PM - 7:00 PM': 'available'
            }
        return availability

    def set_availability(self, day, shift, status):
        """Updates the caregiver's availability for a specific day and shift."""
        if day in self.availability and shift in self.availability[day]:
            self.availability[day][shift] = status
        else:
            raise ValueError("Invalid day or shift!")

    def __str__(self):
        return f"Caregiver: {self.name}, Pay Rate: ${self.pay_rate}/hr"


class Schedule:
    def __init__(self):
        self.caregivers = []
        self.schedule = self.initialize_schedule()

    def initialize_schedule(self):
        """Creates an empty schedule for a month."""
        schedule = {}
        for day in range(1, 32):
            schedule[day] = {
                '7:00 AM - 1:00 PM': None,
                '1:00 PM - 7:00 PM': None
            }
        return schedule

    def add_caregiver(self, caregiver):
        """Adds a caregiver to the schedule."""
        self.caregivers.append(caregiver)

    def assign_shift(self, day, shift, caregiver_name):
        """Assigns a caregiver to a specific shift."""
        caregiver = next((c for c in self.caregivers if c.name == caregiver_name), None)
        if not caregiver:
            raise ValueError("Caregiver not found!")
        if caregiver.availability[day][shift] == 'unavailable':
            raise ValueError(f"{caregiver.name} is unavailable for this shift!")
        if self.schedule[day][shift]:
            raise ValueError("This shift is already assigned!")

        self.schedule[day][shift] = caregiver.name
        caregiver.hours += 6  # Each shift is 6 hours long

    def view_schedule(self):
        """Displays the full schedule."""
        for day, shifts in self.schedule.items():
            print(f"Day {day}:")
            for shift, caregiver in shifts.items():
                print(f"{shift}: {caregiver if caregiver else 'Unassigned'}")

    def view_caregiver_hours(self):
        """Displays the total hours worked by each caregiver."""
        for caregiver in self.caregivers:
            print(f"{caregiver.name}: {caregiver.hours} hours")


import calendar

# Caregiver data with availability
caregivers = [
    {"name": "Alice", "availability": {"AM": "preferred", "PM": "available"}},
    {"name": "Bob", "availability": {"AM": "available", "PM": "preferred"}},
    {"name": "Charlie", "availability": {"AM": "unavailable", "PM": "available"}},
    {"name": "Diana", "availability": {"AM": "preferred", "PM": "preferred"}},
]

# Function to generate a schedule based on availability
def generate_schedule(caregivers, year, month):
    shifts = ["7:00AM - 1:00PM", "1:00PM - 7:00PM"]
    num_days = calendar.monthrange(year, month)[1]
    schedule = {}

    for day in range(1, num_days + 1):
        schedule[day] = {}
        for i, shift in enumerate(shifts):
            assigned = None

            # Prioritize caregivers with "preferred" availability
            for caregiver in caregivers:
                if caregiver["availability"]["AM" if i == 0 else "PM"] == "preferred":
                    assigned = caregiver["name"]
                    break
            
            # If no "preferred", assign from "available"
            if not assigned:
                for caregiver in caregivers:
                    if caregiver["availability"]["AM" if i == 0 else "PM"] == "available":
                        assigned = caregiver["name"]
                        break

            # Assign the caregiver to the shift
            schedule[day][shift] = assigned if assigned else "Unassigned"
    
    return schedule

# Function to display the schedule as an HTML calendar
def display_schedule_as_html(schedule, caregivers, year, month):
    html_schedule = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Care Schedule - {calendar.month_name[month]} {year}</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
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
            td {{
                vertical-align: top;
                height: 80px;
            }}
        </style>
    </head>
    <body>
        <h1 style="text-align: center;">Care Schedule for {calendar.month_name[month]} {year}</h1>
        <table>
            <tr>
                <th>Mon</th>
                <th>Tue</th>
                <th>Wed</th>
                <th>Thu</th>
                <th>Fri</th>
                <th>Sat</th>
                <th>Sun</th>
            </tr>
    """

    # Get the first weekday and the number of days in the month
    first_weekday, num_days = calendar.monthrange(year, month)
    current_day = 1

    # Generate rows for each week
    for week in range((num_days + first_weekday) // 7 + 1):
        html_schedule += "<tr>"
        for day in range(7):
            if (week == 0 and day < first_weekday) or current_day > num_days:
                html_schedule += "<td></td>"
            else:
                shifts = schedule.get(current_day, {})
                html_schedule += f"<td>{current_day}<br>"
                for shift, caregiver in shifts.items():
                    html_schedule += f"<b>{shift}:</b> {caregiver}<br>"
                html_schedule += "</td>"
                current_day += 1
        html_schedule += "</tr>"

    html_schedule += """
        </table>
    </body>
    </html>
    """

    with open(f"care_schedule_{year}_{month}.html", "w") as file:
        file.write(html_schedule)
    print(f"Care schedule for {calendar.month_name[month]} {year} saved as HTML!")

# Specify the year and month for the schedule
year = int(input("Enter the year: "))
month = int(input("Enter the month (1-12): "))

# Generate and display the schedule
schedule = generate_schedule(caregivers, year, month)
display_schedule_as_html(schedule, caregivers, year, month)

class PayReport:
    def __init__(self, caregivers):
        self.caregivers = caregivers
        self.paid_caregivers = [c for c in caregivers if c.pay_rate > 0]
        self.family_caregivers = [c for c in caregivers if c.pay_rate == 0]

    def calculate_pay(self, time_period_multiplier=1):
        """Calculates pay for weekly or monthly periods."""
        report_data = []
        total_pay = 0

        for caregiver in self.caregivers:
            pay = caregiver.hours * caregiver.pay_rate * time_period_multiplier
            report_data.append({
                "name": caregiver.name,
                "hours": caregiver.hours * time_period_multiplier,
                "pay_rate": caregiver.pay_rate,
                f"pay_{time_period_multiplier}x": pay
            })
            total_pay += pay

        return report_data, total_pay

    def generate_report(self):
        """Prints the weekly and monthly pay report."""
        weekly_data, total_weekly_pay = self.calculate_pay(time_period_multiplier=1)
        monthly_data, total_monthly_pay = self.calculate_pay(time_period_multiplier=4)

        print("\nWeekly Pay Report:")
        print("-" * 40)
        for data in weekly_data:
            print(f"Caregiver: {data['name']}, Hours: {data['hours']}, Pay Rate: ${data['pay_rate']:.2f}, Weekly Pay: ${data['pay_1x']:.2f}")
        print("-" * 40)
        print(f"Total Weekly Pay: ${total_weekly_pay:.2f}")

        print("\nMonthly Pay Report:")
        print("-" * 40)
        for data in monthly_data:
            print(f"Caregiver: {data['name']}, Hours: {data['hours']}, Pay Rate: ${data['pay_rate']:.2f}, Monthly Pay: ${data['pay_4x']:.2f}")
        print("-" * 40)
        print(f"Total Monthly Pay: ${total_monthly_pay:.2f}")

    def generate_html_report(self):
        """Generates an HTML report for weekly and monthly pay."""
        weekly_data, total_weekly_pay = self.calculate_pay(time_period_multiplier=1)
        monthly_data, total_monthly_pay = self.calculate_pay(time_period_multiplier=4)

        html_report = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Caregiver Pay Report - {calendar.month_name[month]} {year}</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                h1, h2 { text-align: center; }
            </style>
        </head>
        <body>
            <h1>Caregiver Pay Report - {calendar.month_name[month]} {year}</h1>
            <h2>Weekly Pay Report - {calendar.month_name[month]} {year}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Caregiver</th>
                        <th>Hours Worked</th>
                        <th>Pay Rate ($)</th>
                        <th>Weekly Pay ($)</th>
                    </tr>
                </thead>
                <tbody>
        """

        for data in weekly_data:
            html_report += f"""
                <tr>
                    <td>{data['name']}</td>
                    <td>{data['hours']}</td>
                    <td>${data['pay_rate']:.2f}</td>
                    <td>${data['pay_1x']:.2f}</td>
                </tr>
            """

        html_report += f"""
                </tbody>
            </table>
            <h3>Total Weekly Pay: ${total_weekly_pay:.2f}</h3>
            <h2>Monthly Pay Report - {calendar.month_name[month]} {year}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Caregiver</th>
                        <th>Hours Worked</th>
                        <th>Pay Rate ($)</th>
                        <th>Monthly Pay ($)</th>
                    </tr>
                </thead>
                <tbody>
        """

        for data in monthly_data:
            html_report += f"""
                <tr>
                    <td>{data['name']}</td>
                    <td>{data['hours']}</td>
                    <td>${data['pay_rate']:.2f}</td>
                    <td>${data['pay_4x']:.2f}</td>
                </tr>
            """

        html_report += f"""
                </tbody>
            </table>
            <h3>Total Monthly Pay: ${total_monthly_pay:.2f}</h3>
        </body>
        </html>
        """

        filename = f"pay_report_{year}_{month:02}.html"
        with open(filename, "w") as file:
            file.write(html_report)

        print(f"Pay report saved as '{filename}'.")

    def reset_hours(self):
        #Resets all caregiver hours to zero
        for caregiver in self.caregivers:
            caregiver.hours = 0


#example of how pay report class would work
if __name__ == "__main__":
    caregiver1 = Caregiver("Alice", "123", "a@gmail.com", 20.0)
    caregiver2 = Caregiver("Bob", "456", "bob@gmail.com", 20.0)
    caregiver3 = Caregiver("Charlie", "789", "char@gmail.com", 0.0)

    caregiver1.hours = 24
    caregiver2.hours = 30
    caregiver3.hours = 18

    report = PayReport([caregiver1, caregiver2, caregiver3])
    report.generate_report()
    report.generate_html_report()
    report.reset_hours()
