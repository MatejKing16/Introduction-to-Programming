from abc import ABC, abstractmethod


# Úkol b, c: Třída pro pacienta a doktora
class Patient:

  def __init__(self, first_name, last_name, age, condition):
    self.first_name = first_name
    self.last_name = last_name
    self.age = age
    self.condition = condition

  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"

  def __str__(self):
    return f"{self.full_name} ({self.age}) – {self.condition}"


class Doctor:

  def __init__(self, name, specialization):
    self.name = name
    self.specialization = specialization

  def __str__(self):
    return f"Dr. {self.name} ({self.specialization})"


# Hlavní nemocniční systém
class HospitalSystem:

  def __init__(self):
    self.patients = []
    self.doctors = []
    self.appointments = {}  # Slovník pro rezervační systém

  def register_patient(self, patient):
    self.patients.append(patient)

  def register_doctor(self, doctor):
    self.doctors.append(doctor)

  # Úkol f: Systém pro ověření, zda je pacient zaregistrovaný (uvnitř třídy s cyklem a podmínkou)
  def is_patient_registered(self, search_name):
    for patient in self.patients:
      if (
          patient.first_name.lower() in search_name.lower()
          and patient.last_name.lower() in search_name.lower()
      ):
        return True
    return False

  # Úkol e: Rezervační systém
  def create_appointment(self, patient_name, doctor_name, time_str):
    self.appointments[patient_name] = {"doctor": doctor_name, "time": time_str}
    print(
        f"{patient_name} has appointment with Dr. {doctor_name} at {time_str}."
    )


# --- Ukázka použití a spuštění úkolů ---

if __name__ == "__main__":
  hospital = HospitalSystem()

  # Úkol a, b: Registrace 5 pacientů s medicínskými daty
  patients_data = [
      ("Anna", "Nováková", 23, "tinnitus"),
      ("Martin", "Pokorný", 41, "nosní polypy"),
      ("Petra", "Svobodová", 35, "migréna"),
      ("Jan", "Novotný", 52, "vysoký tlak"),
      ("Eva", "Černá", 29, "alergická rýma"),
  ]

  print("--- Úkol a & b: Registrovaní pacienti ---")
  for f_name, l_name, age, cond in patients_data:
    p = Patient(f_name, l_name, age, cond)
    hospital.register_patient(p)
    print(p)

  # Úkol c: Definice dalších 4 doktorů (plus primární doktor Sekyra)
  sekyra = Doctor("Sekyra", "Všeobecné lékařství")
  other_doctors = [
      Doctor("Okula", "Oční"),
      Doctor("Smetana", "ORL"),
      Doctor("Veselý", "Kardiologie"),
      Doctor("Krátká", "Alergologie"),
  ]

  for doc in other_doctors:
    hospital.register_doctor(doc)

  print("\n--- Úkol d: Přerozdělení pacientů od zaneprázdněného Dr. Sekyry ---")
  # Příklad přiřazení pacientů ke zbývajícím doktorům
  assignments = [
      ("Anna Nováková", "Okula"),
      ("Martin Pokorný", "Smetana"),
      ("Petra Svobodová", "Veselý"),
      ("Jan Novotný", "Veselý"),
      ("Eva Černá", "Krátká"),
  ]

  for patient_name, doc_name in assignments:
    print(f"Pacient {patient_name} is treated by Dr. {doc_name}")

  print("\n--- Úkol e: Rezervační systém ---")
  hospital.create_appointment("Anna Nováková", "Smetana", "10:00")
  hospital.create_appointment("Martin Pokorný", "Okula", "11:30")

  print("\n--- Úkol f: Ověření registrace pacienta ---")
  search_query = "Anna Nováková"
  if hospital.is_patient_registered(search_query):
    print(f"Ověření: Pacient '{search_query}' je v nemocnici zaregistrovaný.")
  else:
    print(f"Ověření: Pacient '{search_query}' nebyl nalezen.")

  print("\n--- Úkol g: Platební systém (Polymorfismus) ---")


  # Úkol g: Polymorfní platební systém
  class Payment(ABC):

    @abstractmethod
    def process_payment(self):
      print("Processing payment")


  class CashPayment(Payment):

    def process_payment(self):
      super().process_payment()
      print("Paid with cash")


  class CardPayment(Payment):

    def process_payment(self):
      super().process_payment()
      print("Paid with card")


  # Simulace platby za jednorázový materiál
  payments = [CashPayment(), CardPayment()]
  for payment in payments:
    payment.process_payment()
    print("-" * 20)