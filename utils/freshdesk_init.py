import requests
import json
import time
from base64 import b64encode
from freshdesk_init_data import contacts, tickets, agents

# Configuration - Replace with your actual values
FRESHDESK_DOMAIN = "sumandproduct"  # e.g., "mycompany" (without .freshdesk.com)
API_KEY = "QXnEL3dtzdjvylrO4gmj"  # Get this from Admin > API Keys in Freshdesk
API_BASE_URL = f"https://{FRESHDESK_DOMAIN}.freshdesk.com/api/v2"

# Create headers for authentication
def get_headers():
    credentials = b64encode(f"{API_KEY}:X".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

# Function to create contacts
def create_contacts(contacts_data):
    print("Creating contacts...")
    created_contacts = {}
    
    for contact in contacts_data:
        try:
            response = requests.post(
                f"{API_BASE_URL}/contacts",
                headers=get_headers(),
                json=contact
            )
            
            if response.status_code == 201:
                contact_data = response.json()
                created_contacts[contact['email']] = contact_data['id']
                print(f"✓ Created contact: {contact['name']} (ID: {contact_data['id']})")
            else:
                print(f"✗ Failed to create contact {contact['name']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"✗ Error creating contact {contact['name']}: {str(e)}")
        
        time.sleep(0.5)  # Rate limiting
    
    return created_contacts

# Function to create tickets
def create_tickets(tickets_data, contact_mapping):
    print("\nCreating tickets...")
    
    for ticket in tickets_data:
        try:
            # Get requester_id from contact mapping if available
            if ticket['email'] in contact_mapping:
                ticket['requester_id'] = contact_mapping[ticket['email']]
            
            response = requests.post(
                f"{API_BASE_URL}/tickets",
                headers=get_headers(),
                json=ticket
            )
            
            if response.status_code == 201:
                ticket_data = response.json()
                print(f"✓ Created ticket: {ticket['subject']} (ID: {ticket_data['id']})")
            else:
                print(f"✗ Failed to create ticket {ticket['subject']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"✗ Error creating ticket {ticket['subject']}: {str(e)}")
        
        time.sleep(0.5)  # Rate limiting

# Function to create agents
def create_agents(agents_data):
    print("Creating agents...")
    created_agents = {}
    
    for agent in agents_data:
        try:
            response = requests.post(
                f"{API_BASE_URL}/agents",
                headers=get_headers(),
                json=agent
            )
            
            if response.status_code == 201 or response.status_code == 200:
                agent_data = response.json()
                created_agents[agent['email']] = agent_data['id']
                print(f"✓ Created agent: {agent['name']} )")
            else:
                print(f"✗ Failed to create agent {agent['name']} : {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"✗ Error creating agent {agent['name']} : {str(e)}")
        
        time.sleep(0.5)  # Rate limiting
    
    return created_agents
# Load test data
def load_test_data():
    contacts_data = contacts
    tickets_data = tickets
    agents_data = agents
    return contacts_data, tickets_data, agents_data

# Main function
def main():
    print("Freshdesk Test Data Upload Script")
    print("=" * 40)
    
    # Validate configuration
    if FRESHDESK_DOMAIN == "your-domain" or API_KEY == "your-api-key":
        print("❌ Please update the FRESHDESK_DOMAIN and API_KEY in the script!")
        return
    
    # Load test data
    contacts_data, tickets_data, agents_data = load_test_data()
    
    if not contacts_data or not tickets_data:
        print("❌ Please add your test data to the script!")
        return
    
    # Create contacts first
    #contact_mapping = create_contacts(contacts_data)
    
    # Create tickets
    #create_tickets(tickets_data, contact_mapping)
    agents_mapping = create_agents(agents_data)

    print(f"\n✅ Upload completed!")
#    print(f"Contacts created: {len(contact_mapping)}")
 #   print(f"Tickets processed: {len(tickets_data)}")
    print(f"Agents created: {len(agents_mapping)}")

if __name__ == "__main__":
    main()