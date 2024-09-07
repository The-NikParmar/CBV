from datetime import time
from datetime import timedelta, datetime
from patient.models import Appointment

def get_doctor_working_hours():
    return {
        'morning': (time(9, 0), time(13, 0)),  # 9 AM to 1 PM
        'evening': (time(17, 0), time(21, 0))  # 5 PM to 9 PM
    }

def calculate_available_slots(doctor, appointment_date, disease_duration):
    working_hours = get_doctor_working_hours()
    print("working houre=============",working_hours)
    available_slots = []
    buffer_time = timedelta(minutes=2) 

    for period, (start_time, end_time) in working_hours.items():
        current_time = datetime.combine(appointment_date, start_time)
        end_datetime = datetime.combine(appointment_date, end_time)

        while current_time + disease_duration + buffer_time <= end_datetime:
            slot_end_time = current_time + disease_duration

            overlap = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time__lt=slot_end_time.time(),
                end_time__gt=current_time.time()
            ).exists()

            if not overlap:
                available_slots.append(current_time.time().strftime("%H:%M"))

            current_time += timedelta(minutes=30) + buffer_time  

    return available_slots
