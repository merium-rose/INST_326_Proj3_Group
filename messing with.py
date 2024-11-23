from datetime import datetime, timedelta
class Caregiver:
    def __init__(self, name, phone, email, pay_rate):
        self.name = name 
        self.phone = phone 
        self.email = email
        self.pay_rate = pay_rate
        self.hours = 0 #tracks total schedulding hours for each caregiver
        self.availability = self.initialize_availability()

    def initialize_availability(self):
    #creates an availability dictionary for a month
        availability = {}
        for day in range(1,32): #range of 1-31 inclusive days 
            availability[day] = {
                '7:00 AM - 1:00 PM': 'available',
                '1:00 PM - 7:00 PM' : 'avaiable'
            }
        return availability

    def set_availability(self, day, shift, status):
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
        schedule = {}
        for day in range(1,32):
            schedule[day] = {
                '7:00 AM - 1:00 PM' : None,
                '1:00 PM - 7:00 PM' : None
            }
        return schedule

    def add_caregiver(self, caregiver):
        self.caregivers.append(caregiver)

    def assign_shift(self, day, shift, caregiver_name):
        caregiver = next((c for c in self.caregivers if c.name == caregiver_name), None)
        if not caregiver:
            raise ValueError("Caregiver not found!")
        if caregiver.availability[day][shift] == 'unavailable':
            raise ValueError(f"{caregiver.name} is unavailable for this shift!")
        if self.schedule[day][shift]:
            raise ValueError("This shift is already assigned!")

        self.schedule[day][shift] = caregiver.name
        caregiver.hours += 6 #each shift is 6 hours long 

    def view_schedule(self):
        for day, shifts in self.schedule.items():
            print(f"Day{day}:")
            for shift, caregiver in shifts.items():
                print(f"{shift}: {caregiver if caregiver else 'Unassigned'}")

    def view_caregiver_hours(self):
        for caregiver in self.caregivers:
            print(f"{caregiver.name}: {caregiver.hours} hours") 

if __name__ == "__main__":
    caregiver1 = Caregiver("Alice","123","a@gmail.com", 15.0)
    caregiver2 = Caregiver("Bob","456","bob@gmail.com", 18.0)

    caregiver1.set_availability(1, '7:00 AM - 1:00 PM', 'preferred')
    caregiver1.set_availability(1, '1:00 PM - 7:00 PM', 'unavailable')

    caregiver2.set_availability(1, '7:00 AM - 1:00 PM', 'avaiable')
    caregiver2.set_availability(1, '1:00 PM - 7:00 PM', 'preferred')

    schedule = Schedule()
    schedule.add_caregiver(caregiver1)
    schedule.add_caregiver(caregiver2)

    try:
        schedule.assign_shift(1, '7:00 AM - 1:00 PM', "Alice")
        schedule.assign_shift(1, '1:00 PM - 7:00 PM', "Bob")
    except ValueError as e:
        print(e)

    schedule.view_schedule()
    schedule.view_caregiver_hours()




class PayReport:
    def __init__(self, caregivers):
        self.caregivers = caregivers
        self.paid_caregivers = []
        self.family_caregivers = []

        for caregiver in self.caregivers:
            if caregiver.pay_rate > 0:
                self.paid_caregivers.append(caregiver)
            else:
                self.family_caregivers.append(caregiver)
    
    def calculate_weekly_pay(self):
        #Calculate weekly pay for all caregivers
        report_data = []
        total_weekly_pay = 0

        for caregivers in self.caregivers:
            weekly_pay = caregivers.hours * caregivers.pay_rate
            report_data.append ({
                "name": caregivers.name,
                "hours": caregivers.hours,
                "pay_rate" : caregivers.pay_rate,
                "weekly_pay": weekly_pay,
            })
            total_weekly_pay += weekly_pay
        
        return report_data, total_weekly_pay
    
    def calculate_monthly_pay(self):
            #Calculate monthly pay for all caregivers
            report_data = []
            total_monthly_pay = 0

            for caregiver in self.paid_caregivers:
                # Assuming monthly pay is based on total hours (same as for weekly pay)
                monthly_pay = caregiver.hours * caregiver.pay_rate
                report_data.append({
                    "name": caregiver.name,
                    "hours": caregiver.hours,
                    "pay_rate": caregiver.pay_rate,
                    "monthly_pay": monthly_pay
                })
                total_monthly_pay += monthly_pay
            
            return report_data, total_monthly_pay
    
    def generate_report(self):

        report_data, total_weekly_pay = self.calculate_weekly_pay()
        report_data, total_monthly_pay = self.calculate_monthly_pay()
        print("\nPay Report:")
        print("-" * 40)
        for data in report_data:
            print(f"Caregiver: {data['name']}, Hours: {data['hours']}, Pay Rate: ${data['pay_rate']:.2f}, Weekly Pay: ${data['weekly_pay']:.2f}")
        print("-" * 40)

        print(f"Total Monthly Pay: ${total_monthly_pay:.2f}")

        print("\nPay Report:")
        print("-" * 40)
        for data in report_data:
            print(f"Caregiver: {data['name']}, Hours: {data['hours']}, Pay Rate: ${data['pay_rate']:.2f}, Weekly Pay: ${data['weekly_pay']:.2f}, "f"Monthly Pay: ${data['monthly_pay']:.2f}")
        print("-" * 40)
        print(f"Total Weekly Pay: ${total_weekly_pay:.2f}")
        print(f"Total Monthly Pay: ${total_monthly_pay:.2f}")

def generate_html_report(self):
    """Generate the HTML report and save it to a predefined file."""
    weekly_data, total_weekly_pay = self.calculate_weekly_pay()
    monthly_data, total_monthly_pay = self.calculate_monthly_pay()

    # Define the fixed filename
    filename = "pay_report.html"

    html_report = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Caregiver Pay Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            h1, h2 { text-align: center; }
        </style>
    </head>
    <body>
        <h1>Caregiver Pay Report</h1>
        <h2>Weekly Pay Report</h2>
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
                    <td>${data['weekly_pay']:.2f}</td>
                </tr>
        """

    html_report += f"""
            </tbody>
        </table>
        <h3>Total Weekly Pay: ${total_weekly_pay:.2f}</h3>

        <h2>Monthly Pay Report</h2>
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
                    <td>${data['monthly_pay']:.2f}</td>
                </tr>
        """

    html_report += f"""
            </tbody>
        </table>
        <h3>Total Monthly Pay: ${total_monthly_pay:.2f}</h3>
    </body>
    </html>
    """

    # Save the report to the predefined filename
    with open(filename, "w") as file:
        file.write(html_report)

    print(f"Pay report saved as '{filename}'.")

def reset_hours(self):
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

    #creating pay report
    report = PayReport([caregiver1, caregiver2, caregiver3])
    report.generate_report()

    #resetting all caregivers hours back to 0
    report.reset_hours()
