# Cloud function: Execute campaign
# 
# When a new campaign is created, this function is run the first time.`
# This function keeps rescheduling itself until all the calls have been made. 
#
#  This function runs in batches
# 
# A batch is the number of active calls in a campaign
# 
BATCH_SIZE = 5 # default batch size

from cloudevents.http import CloudEvent
import functions_framework
from google.cloud import firestore
from google.events.cloud import firestore as firestoredata
from google.cloud.firestore_v1.base_query import FieldFilter


client = firestore.Client()


# firestore filter: tenants/{tenant}/campaigns/{campaignId}
# this function is always triggered only when a new campaign is created.
# then the job of this function is to check the groups field(an array of strings) of the campaign document i.e. the document that has been created
# which can be accessed using DocumentEventData, and then get employees from the tenant document's sub-collection 'employees', while filtering only the employees
# which have a group field with array that belong to at least one group from the campaign's group. Copy  those employees that do belong to the group in a sub-collection
# under campaign named 'pending_calls'
@functions_framework.cloud_event
def start(cloud_event: CloudEvent) -> None:
    """Triggers by a change to a Firestore document.
    Args:
        cloud_event: cloud event with information on the firestore event trigger
    """
    firestore_payload = firestoredata.DocumentEventData()
    firestore_payload._pb.ParseFromString(cloud_event.data)
    # print("cloudevent: ", cloud_event.data)

    path_parts = firestore_payload.value.name.split("/")
    separator_idx = path_parts.index("documents")
    tenant_document_path = "/".join(path_parts[(separator_idx + 1) : (separator_idx + 3)])
    campaign_document_path = "/".join(path_parts[(separator_idx + 1) :])

    tenant_document_ref = client.document(tenant_document_path)
    employees_collection_ref = tenant_document_ref.collection("employees")

    campaign_document_ref = client.document(campaign_document_path)
    pending_calls_collection_ref = campaign_document_ref.collection("pending_calls")

    groups_to_copy = firestore_payload.value.fields["groups"].array_value.values
    groups_array = [group.string_value for group in groups_to_copy]

    print("Campaign: ", campaign_document_path)
    print("Queing for calls, employees with groups: ", groups_array)
    count  = 0
    # copy employees that belong to the group in a sub-collection under campaign named 'pending_calls'
    for employee_document in employees_collection_ref.where(filter=FieldFilter("groups", "array_contains_any", groups_array)).stream():
        employee_data = employee_document.to_dict()
        employee_id = employee_document.id
        pending_calls_collection_ref.document(employee_id).set(employee_data)
        count += 1
    print("Queued ", count, " calls")
    campaign_document_ref.update({"status": "running", "users_targeted": count, "created_at": firestore.SERVER_TIMESTAMP})






### TESTING
binary_data = b'\n\x95\x03\nrprojects/callstrike-prod/databases/(default)/documents/tenants/FeCc0F9p4IForSRlze0g/campaigns/4Suc6KpObgliHCXUGRv2\x12\x1a\n\x08end_date\x12\x0eR\x0c\x08\xb3\xb8\xb4\xaf\x06\x10\xc0\xb4\xbb\x9c\x03\x12%\n\rtemplate_name\x12\x14\x8a\x01\x11IT password reset\x12\x14\n\x0eusers_targeted\x12\x02\x107\x12\x1d\n\x04name\x12\x15\x8a\x01\x12marketing team feb\x12!\n\x06groups\x12\x17J\x15\n\x0c\x8a\x01\tmarketing\n\x05\x8a\x01\x02hr\x12\x19\n\x04days\x12\x11J\x0f\n\x05\x8a\x01\x02Mo\n\x06\x8a\x01\x03Tue\x12\x1c\n\x0btemplate_id\x12\r\x8a\x01\n435jkljifd\x12\x1b\n\nstart_date\x12\rR\x0b\x08\x9a\xe6\x94\xaf\x06\x10\x80\x89\x83{\x12\x14\n\x06status\x12\n\x8a\x01\x07running\x1a\x0b\x08\x8b\xb5\xca\xaf\x06\x10\x98\xd8\x81r"\x0b\x08\x8b\xb5\xca\xaf\x06\x10\x98\xd8\x81r'
attributes = {
    "specversion": "1.0",
    "type": "com.google.cloud.firestore.document.v1.created",
    "source": "your-source",
    "id": "your-id",
    "time": "2024-03-14T12:34:56.789Z",
    "datacontenttype": "application/json"
}

event = CloudEvent(attributes, binary_data)

execute_campaign(event)
