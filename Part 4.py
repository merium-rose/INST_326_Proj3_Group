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
