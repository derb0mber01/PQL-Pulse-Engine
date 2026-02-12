import pandas as pd
import os
import requests
from datetime import datetime

# CONFIGURATION
INPUT_FILE = r"C:\Users\uduok\git_folder\Saas_Lead_Conversion\data\processed\hubspot_pql_sync.csv"
LOG_FILE = r"C:\Users\uduok\git_folder\Saas_Lead_Conversion\data\processed\alert_log.txt"
N8N_WEBHOOK_URL = #Insert Webhook Link

def simulate_clay_enrichment(org_size):
    enrichment_map = {
        'Enterprise': {'industry': 'FinTech', 'funding': '$50M+ Series C', 'tech_stack': 'Salesforce, AWS'},
        'Mid-Market': {'industry': 'SaaS', 'funding': '$12M Series A', 'tech_stack': 'HubSpot, GCP'},
        'SMB': {'industry': 'Agency', 'funding': 'Bootstrapped', 'tech_stack': 'Pipedrive, Vercel'}
    }
    return enrichment_map.get(org_size, {'industry': 'Unknown', 'funding': 'N/A', 'tech_stack': 'N/A'})

def get_gtm_strategy(row):
    mapping = {
        'Enterprise': {
            'persona': 'VP of Operations',
            'value_prop': 'enterprise-grade security and admin controls',
            'cta': 'schedule a security review'
        },
        'Mid-Market': {
            'persona': 'Product Lead',
            'value_prop': 'team collaboration and library management',
            'cta': 'start a team trial'
        },
        'SMB': {
            'persona': 'Founder',
            'value_prop': 'individual productivity and instant sharing',
            'cta': 'view pro features'
        }
    }
    # Fallback to Small Business if org_size is unexpected
    return mapping.get(row['org_size'], mapping['S'])
    
def generate_gtm_alerts():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Sync file not found at {INPUT_FILE}")
        return

    # Load the leads
    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        print("No hot leads found.")
        return

    print(f"GTM Engine Active: Firing webhooks for {len(df)} leads...")
    print("="*60)

    for _, row in df.iterrows():
        # Enrich the data
        metadata = simulate_clay_enrichment(row['org_size'])
        strategy = get_gtm_strategy(row)
        
        # Construct the data being sent to n8n
        payload = {
            "user_id": row['user_id'],
            "intent_tier": row['intent_tier'],
            "intent_score": row['intent_score'],
            "org_size": row['org_size'],
            "industry": metadata['industry'],
            "funding": metadata['funding'],
            "target_persona": strategy['persona'],
            "value_prop": strategy['value_prop'],
            "cta": strategy['cta'],
            "outreach_template": f"Hi {row['user_id']}, as the {strategy['persona']} at a {metadata['industry']} firm..."
        }

        # Fire the Webhook
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"✅ Alert Sent: {row['user_id']}")
            else:
                print(f"⚠️ Webhook received status {response.status_code} for {row['user_id']}")
        except Exception as e:
            print(f"❌ Failed to reach n8n: {e}")

        # Log the attempt
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()}: Webhook fired for {row['user_id']}\n")

if __name__ == "__main__":
    generate_gtm_alerts()