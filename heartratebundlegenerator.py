import random
from fhir.resources.patient import Patient
from patients import Patients
from observation import HeartRateObservation
from batchbundle import BatchBundle   # Refactored to accept a list of Observations
from transactionbundle import TransactionBundle  # Existing TransactionBundle class

class HeartRateBundleGenerator:
    def __init__(self, patient_identifier: str, observation_count: int, low_hr: int, high_hr: int, patients: list[Patient]):
        """
        Initialize the generator.
        
        :param patient_identifier: The identifier of the patient.
        :param observation_count: The number of heart rate observations to generate (max 1000).
        :param low_hr: Lower bound for heart rate values.
        :param high_hr: Upper bound for heart rate values.
        :param patients: list of all patients for which bundles can be posted
        """

        if observation_count > 1000:
            raise ValueError("observation_count must be 1000 or less")
        self.patient_identifier = patient_identifier
        self.patients = patients
        self.observation_count = observation_count
        self.low_hr = low_hr
        self.high_hr = high_hr
        
         # Retrieve the Patient resource and FHIR id.
        patient_resource = self.patients.get_patient(patient_identifier)
        if patient_resource is None:
            raise ValueError(f"Patient with identifier '{patient_identifier}' not found. Terminating program.")
        
        # Generate the specified number of HeartRateObservation objects.
        self.observations = []
        for _ in range(observation_count):
            hr_value = random.randint(low_hr, high_hr)
            minutes_ago = random.randint(0, 1440)
            obs = HeartRateObservation(patient_identifier, hr_value, minutes_ago)
            self.observations.append(obs)

        patient_fhir_id = self.patients.get_patient_id(patient_identifier)
        
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
    
    def get_bundle(self):
        """
        Retrieve the generated bundle (either a BatchBundle or TransactionBundle).
        """
        return self.bundle
    
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

# Example usage:
if __name__ == "__main__":
    # Generate a bundle for a patient with identifier "12345" with 10 observations,
    # heart rate values between 60 and 120.
    patients = Patients()
    generator = HeartRateBundleGenerator("356-444-9972", 10, 60, 120, patients)
    bundle = generator.get_bundle()
    # Print the bundle JSON for inspection.
    print(bundle.bundle.json(indent=2))