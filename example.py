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
        schedule.assign_shift(a, '1:00 PM - 7:00 PM', "Bob")
    except ValueError as e:
        print(e)

    schedule.view_schedule()
    schedule.view_caregiver_hours()
