import ast
from datetime import datetime
from fhir.resources.patient import Patient
from patients import Patients
from observation import HeartRateObservation
from batchbundle import BatchBundle
from transactionbundle import TransactionBundle

class HeartRateFileBundleGenerator:
    def __init__(self, patient_identifier: str, patients: list[Patient]):
        """
        Initialize the generator.
        
        :param patient_identifier: The identifier of the patient in the form '356-444-9972'.
        """
        self.patient_identifier = patient_identifier
        self.patients = patients
        
        patient_resource = patients.get_patient(patient_identifier)
        if patient_resource is None:
            raise ValueError(f"Patient with identifier '{patient_identifier}' not found. Terminating program.")
        
        # Read observations from file. File name is the patient_identifier with dashes removed and '.txt' appended.
        self.observations = []
        file_name = f"{patient_identifier.replace('-', '')}.txt"
        observation_count = 0
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        # Safely evaluate the tuple. Expected format: (heart_rate, effective_date_str)
                        tup = ast.literal_eval(line)
                        heart_rate_value, effective_date_str = tup
                        # Convert the effective_date_str to a datetime object.
                        effective_dt = datetime.fromisoformat(effective_date_str)
                        # Create a HeartRateObservation using the provided effective_dt.
                        obs = HeartRateObservation(patient_identifier, heart_rate_value, effective_dt=effective_dt)
                        self.observations.append(obs)
                        observation_count += 1
                    except Exception as e:
                        print(f"Error parsing line: {line}. Error: {e}")
            print(f"Processed {observation_count} observation entries from file '{file_name}'.")
        except FileNotFoundError:
            raise ValueError(f"File '{file_name}' not found.")
        
        # Retrieve the FHIR patient id from the Patients class.
        patient_fhir_id = patients.get_patient_id(patient_identifier)
        
        if patient_fhir_id:
            # If a FHIR id exists, create a BatchBundle with only the observations.
            self.bundle = BatchBundle(patient_fhir_id, self.observations)
        else:
            # If no FHIR id exists, create a TransactionBundle including the Patient resource.
            self.bundle = TransactionBundle(patient_resource, self.observations)
            
    def post_bundle(self):
        patientId = self.bundle.post_bundle()
        if patientId != '':
            self.patients.store_patient_id(self.patient_identifier, patientId)
        
    def print_ids(self):
        self.bundle.print_ids()
            
    def print_two(self):
        bundle = self.get_bundle()
        total_entries = len(bundle.bundle.entry)  # Define total_entries here
        print(f"Total entries in bundle: {total_entries}")
        # To inspect the first two entries, for example:
        # Print the first two entries:
        print("First entry (Patient):")
        print(bundle.bundle.entry[0].json(indent=2))
    
        if total_entries > 1:
          print("Second entry (First Observation):")
          print(bundle.bundle.entry[1].json(indent=2))
    
    def get_bundle(self):
        """
        Retrieve the generated bundle (either a BatchBundle or TransactionBundle).
        """
        return self.bundle

# Example usage:
if __name__ == "__main__":
    patients = Patients()
    generator = HeartRateFileBundleGenerator("356-444-9972", patients)
    generator.print_two()