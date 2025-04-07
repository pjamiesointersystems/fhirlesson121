import uuid
import requests
from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from patients import Patients
from observation import HeartRateObservation
import requests
from requests.auth import HTTPBasicAuth
from printresource import print_fhir_resource


class TransactionBundle:
    def __init__(self, patient: Patient, observations):
        """
        Initializes a TransactionBundle.
        
        :param patient: A FHIR Patient resource.
        :param observations: A single Observation or a list of Observation resources.
                             Each Observation's subject will be updated to reference the patient.
        """
        # Ensure observations is a list.
        if not isinstance(observations, list):
            observations = [observations]
            
        # Generate UUID-based fullUrl for the Patient entry.
        self.patient_fullUrl = f"urn:uuid:{uuid.uuid4()}"
        
        # Create the Patient BundleEntry.
        patient_entry = BundleEntry.construct(
            fullUrl=self.patient_fullUrl,
            resource=patient,
            request=BundleEntryRequest.construct(
                method="POST",
                url="Patient"
            )
        )
        
        # Process each Observation.
        self.observation_entries = []
        for obs in observations:
            # Generate a unique fullUrl for each Observation.
            obs_fullUrl = f"urn:uuid:{uuid.uuid4()}"
            # Update the Observation subject to reference the Patient fullUrl.
            obs.subject.reference = self.patient_fullUrl
            # Create the Observation BundleEntry.
            observation_entry = BundleEntry.construct(
                fullUrl=obs_fullUrl,
                resource=obs,
                request=BundleEntryRequest.construct(
                    method="POST",
                    url="Observation"
                )
            )
            self.observation_entries.append(observation_entry)
        
        # Construct the Bundle of type "transaction" with the Patient and Observation entries.
        self.bundle = Bundle.construct(
            type="transaction",
            entry=[patient_entry] + self.observation_entries
        )
        
        # Initialize IDs (to be set after posting)
        self.patient_id = ""
        self.observation_ids = []  # list for multiple observations


    # the return of this function is the id of the patient
    def post_bundle(self) -> str:
        """
        Posts a FHIR Transaction bundle to a local FHIR server.
        :return: The response object from the POST request.
        """
        bundle_json = self.bundle.json()
        endpoint = "http://127.0.0.1:8080/csp/healthshare/demo/fhir/r4/"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/fhir+json",
            "Accept-Encoding": "gzip, deflate, br",
            "Prefer": "return=representation"
        }
        response = requests.post(endpoint, data=bundle_json, headers=headers,
                                 auth=HTTPBasicAuth('_System', 'ISCDEMO'))
        
        if response.status_code in (200, 201):
            resource = response.json()
            # Extract the patient id from the first entry.
            self.patient_id = resource['entry'][0]['resource']['id']
            # For each observation entry (assuming they follow patient entry),
            # collect their ids.
            self.observation_ids = [entry['resource']['id'] for entry in resource['entry'][1:]]
            # (Optional) Call your print function here.
            # print_fhir_resource(resource)
            return self.patient_id
        else:
            print(f"Failed to post Transaction Bundle. Status code: {response.status_code}")
            print("Response:", response.text)
            return ""
        
        return response

    def get_patient_id(self):
        return self.patient_id

    def get_observation_ids(self):
        return self.observation_ids
    
    def print_ids(self):
        print("Patient ID:", self.get_patient_id())
        print("Observation IDs:", self.get_observation_ids())

# Example usage:
if __name__ == "__main__":
    # Assume that 'patient' is a valid FHIR Patient instance and
    # 'heart_rate_obs1' and 'heart_rate_obs2' are valid Observation instances.
    # They might have been created using your existing classes.
  

    # Retrieve a patient from your Patients class (or create a dummy one)
    allPatients = Patients()
    patient = allPatients.get_patient('356-444-9972')
    
    # Create one or more HeartRateObservation instances.
    heart_rate_obs1 = HeartRateObservation("2", 75, 5)
    heart_rate_obs2 = HeartRateObservation("2", 80, 10)
    
    # Pass a single Observation:
    # transaction_bundle = TransactionBundle(patient, heart_rate_obs1)
    
    # Or pass multiple Observations as a list:
    transaction_bundle = TransactionBundle(patient, [heart_rate_obs1, heart_rate_obs2])
    
    transaction_bundle.post_bundle()
    
    print("Patient ID:", transaction_bundle.get_patient_id())
    print("Observation IDs:", transaction_bundle.get_observation_ids())
