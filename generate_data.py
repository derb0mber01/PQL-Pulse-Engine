---
import pandas as pd
import numpy as np
from faker import Faker
import uuid
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)

# Configuration
NUM_USERS = 1000
START_DATE = datetime(2025, 1, 1)

def generate_saas_data():
    # Create Users
    users = []
    for _ in range(NUM_USERS):
        u_id = str(uuid.uuid4())[:8]
        signup = START_DATE + timedelta(days=np.random.randint(0, 30))
        # Logic: 20% of users are from 'Enterprise' domains (higher conversion intent)
        is_enterprise = np.random.random() < 0.2
        domain = fake.company_email().split('@')[1] if is_enterprise else fake.free_email_domain()
        
        users.append({
            'user_id': u_id,
            'signup_date': signup,
            'domain': domain,
            'org_size': 'Enterprise' if is_enterprise else np.random.choice(['SMB', 'Mid-Market'])
        })
    df_users = pd.DataFrame(users)

    # Create Events
    events = []
    for _, user in df_users.iterrows():
        # Assign a 'User Profile' to create patterns
        # Profile 0: Casual (low events), Profile 1: Power User (PQL pattern)
        profile = np.random.choice([0, 1], p=[0.7, 0.3])
        
        num_events = np.random.randint(5, 15) if profile == 0 else np.random.randint(30, 60)
        
        for _ in range(num_events):
            days_since_signup = np.random.exponential(scale=5) # Most action happens early
            ev_date = user['signup_date'] + timedelta(days=days_since_signup)
            
            # Power Users trigger more 'team_invited' and 'integration_connected'
            if profile == 1:
                ev_name = np.random.choice(['video_recorded', 'video_shared', 'team_invited', 'integration_connected'], p=[0.3, 0.3, 0.3, 0.1])
            else:
                ev_name = np.random.choice(['video_recorded', 'video_shared', 'app_error'], p=[0.6, 0.3, 0.1])
                
            events.append({
                'event_id': str(uuid.uuid4())[:8],
                'user_id': user['user_id'],
                'timestamp': ev_date,
                'event_name': ev_name
            })
    df_events = pd.DataFrame(events)
# Create Subscriptions
    subscriptions = []
    
    # Get the latest timestamp for each user to see if they are still active
    last_events = df_events.groupby('user_id')['timestamp'].max()

    for _, user in df_users.iterrows():
        u_id = user['user_id']
        # Logic: If user is in the 'Power User' profile (from our event logic), 
        # give them an 80% chance of being on a 'Paid' plan.
        # Otherwise, only a 5% chance.
        
        # We find if they were a power user by looking at their event count
        user_event_count = len(df_events[df_events['user_id'] == u_id])
        is_power_user = user_event_count > 25 
        
        if is_power_user:
            plan = np.random.choice(['Pro', 'Enterprise'], p=[0.7, 0.3])
            status = 'Active'
            mrr = 50 if plan == 'Pro' else 500
            # Set upgrade date to a few days after signup
            upgrade_date = user['signup_date'] + timedelta(days=np.random.randint(2, 10))
        else:
            plan = 'Free'
            status = 'Active'
            mrr = 0
            upgrade_date = None

        subscriptions.append({
            'subscription_id': str(uuid.uuid4())[:8],
            'user_id': u_id,
            'plan_level': plan,
            'status': status,
            'mrr': mrr,
            'upgrade_date': upgrade_date
        })
    
    df_subs = pd.DataFrame(subscriptions)
    return df_users, df_events, df_subs

# Execute and Save
df_users, df_events, df_subs = generate_saas_data()
df_users.to_csv('C:/Users/uduok/git_folder/Saas_Lead_Conversion/data/dim_users.csv', index=False)
df_events.to_csv('C:/Users/uduok/git_folder/Saas_Lead_Conversion/data/fact_events.csv', index=False)
df_subs.to_csv('C:/Users/uduok/git_folder/Saas_Lead_Conversion/data/fact_subs.csv', index=False)

print('Done!')
---