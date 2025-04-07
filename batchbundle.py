import requests
from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest
from requests.auth import HTTPBasicAuth
from printresource import print_fhir_resource  # Assuming this utility exists
from observation import HeartRateObservation

class BatchBundle:
    def __init__(self, patientId: str, heart_rate_observations):
        """
        Initialize a BatchBundle.

        :param patientId: The FHIR id of the Patient.
        :param heart_rate_observations: A single Observation or a list of Observations.
        """
        # Ensure observations is a list.
        if not isinstance(heart_rate_observations, list):
            heart_rate_observations = [heart_rate_observations]

        entries = []
        self.observation_ids = []  # list for multiple observations, we can access after posting
        self.patientId = patientId
        for observation in heart_rate_observations:
            # Update the observation's subject to reference the Patient id.
            observation.subject.reference = f"Patient/{patientId}"
            # Create a BundleEntry for each Observation.
            entry = BundleEntry.construct(
                resource=observation,
                request=BundleEntryRequest.construct(
                    method="POST",
                    url="Observation"
                )
            )
            entries.append(entry)

        # Construct the Bundle of type "batch" with all the entries.
        self.bundle = Bundle.construct(
            type="batch",
            entry=entries
        )

    # the return is the id of the patient we passed in
    def post_bundle(self) -> str:
        """
        Posts a FHIR Batch bundle to a local FHIR server.
        :return: The response object from the POST request.
        """
        bundle_json = self.bundle.json()
        endpoint = "http://127.0.0.1:8080/csp/healthshare/demo/fhir/r4/"
        headers = {
            "Accept": "*/*",
            "content-type": "application/fhir+json",
            "Accept-Encoding": "gzip, deflate, br",
            "Prefer": "return=representation"
        }
        response = requests.post(endpoint, data=bundle_json, headers=headers, auth=HTTPBasicAuth('_System', 'ISCDEMO'))
        
        if response.status_code in (200, 201):
            resource = response.json()
            # For each observation entry (assuming they follow patient entry),
            # collect their ids.
            self.observation_ids = [entry['resource']['id'] for entry in resource['entry'][1:]]
            return  self.patientId 
            #print_fhir_resource(resource)
        else:
            print(f"Failed to post Batch Bundle. Status code: {response.status_code}")
            print("Response:", response.text)
            return ""

        return response
    
    def print_ids(self):
        print("Patient ID - Known before Posting", self.patientId)
        print("Observation IDs:", self.observation_ids)

# Example usage:
if __name__ == "__main__":
    # Assume 'patient' and 'heart_rate_obs' are valid FHIR Patient and Observation instances.

    heart_rate_obs = HeartRateObservation('70542', 75, 60) #the subject id will be updated
    
    batch_bundle = BatchBundle('70542', heart_rate_obs)
    # Print out the bundle JSON for inspection.
    print(batch_bundle.bundle.json(indent=2))
    #batch_bundle.post_bundle()