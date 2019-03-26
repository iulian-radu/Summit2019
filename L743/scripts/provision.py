import AlgoAccount
import argparse

first_party_traits = [
    {'name': 'Product Segment-consumer ultra-low voltage', 'description': 'Product Segment-consumer ultra-low voltage',
     'comment': 'Product Segment-consumer ultra-low voltage',
     'rule': 'property=="Product Segment-consumer ultra-low voltage"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Air Compressors & Accessories - Tools', 'description': 'Air Compressors & Accessories - Tools',
     'comment': 'Air Compressors & Accessories - Tools', 'rule': 'property=="Air Compressors & Accessories - Tools"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Search: Garage Organization & Shelving', 'description': 'Search: Garage Organization & Shelving',
     'comment': 'Search: Garage Organization & Shelving', 'rule': 'property=="Search: Garage Organization & Shelving"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Search: Garage Door', 'description': 'Search: Garage Door', 'comment': 'Search: Garage Door',
     'rule': 'property=="Search: Garage Door"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Garage Workbenches', 'description': 'Garage Workbenches', 'comment': 'Garage Workbenches',
     'rule': 'property=="Garage Workbenches"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Garage Rehab Enthusiasts', 'description': 'Garage Rehab Enthusiasts',
     'comment': 'Garage Rehab Enthusiasts',
     'rule': 'property=="Garage Rehab Enthusiasts"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Garage Doors & Openers', 'description': 'Garage Doors & Openers', 'comment': 'Garage Doors & Openers',
     'rule': 'property=="Garage Doors & Openers"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Home Security & Garage Door Openers', 'description': 'Home Security & Garage Door Openers',
     'comment': 'Home Security & Garage Door Openers', 'rule': 'property=="Home Security & Garage Door Openers"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Garage Furniture & Decor', 'description': 'Garage Furniture & Decor',
     'comment': 'Garage Furniture & Decor', 'rule': 'property=="Garage Furniture & Decor"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Work Lighting', 'description': 'Work Lighting', 'comment': 'Work Lighting',
     'rule': 'property=="Work Lighting"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Garage Organization & Shelving > Garage Flooring',
     'description': 'Garage Organization & Shelving > Garage Flooring',
     'comment': 'Garage Organization & Shelving > Garage Flooring',
     'rule': 'property=="Garage Organization & Shelving > Garage Flooring"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Ladders', 'description': 'Ladders', 'comment': 'Ladders', 'rule': 'property=="Ladders"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Wall Storage', 'description': 'Wall Storage', 'comment': 'Wall Storage',
     'rule': 'property=="Wall Storage"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Storage Hooks & Accessories', 'description': 'Storage Hooks & Accessories',
     'comment': 'Storage Hooks & Accessories', 'rule': 'property=="Storage Hooks & Accessories"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Forums: tag - Garage', 'description': 'Forums: tag - Garage', 'comment': 'Forums: tag - Garage',
     'rule': 'property=="Forums: tag - Garage"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Mobile: Viewed Garage Doors Q1 2019', 'description': 'Mobile: Viewed Garage Doors Q1 2019',
     'comment': 'Mobile: Viewed Garage Doors Q1 2019', 'rule': 'property=="Mobile: Viewed Garage Doors Q1 2019"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Mobile: Viewed Heavy-duty Shelving Q1 2019', 'description': 'Mobile: Viewed Heavy-duty Shelving Q1 2019',
     'comment': 'Mobile: Viewed Heavy-duty Shelving Q1 2019',
     'rule': 'property=="Mobile: Viewed Heavy-duty Shelving Q1 2019"', 'type': 'RULE_BASED_TRAIT'},
    {'name': 'Forums: tag - Garage Junkie', 'description': 'Forums: tag - Garage Junkie',
     'comment': 'Forums: tag - Garage Junkie', 'rule': 'property=="Forums: tag - Garage Junkie"',
     'type': 'RULE_BASED_TRAIT'},
    {'name': 'Blog > tag: Garage Storage', 'description': 'Blog > tag: Garage Storage',
     'comment': 'Blog > tag: Garage Storage', 'rule': 'property=="Blog > tag: Garage Storage"',
     'type': 'RULE_BASED_TRAIT'},
]

conversion_traits = [
    {'name': '[PREGENERATED] My Conversion Trait', 'type': 'RULE_BASED_TRAIT'}
]

algo_traits = [
    {'name': '[PREGENERATED] Garage Rehab Algo Accu > 85%', 'description': '',
     'algo_model': '[PREGENERATED] Garage Rehab Enthusiasts - 1st party', 'accuracy': '0.85'}
]

segments = [
    {'name': '[PREGENERATED] 1st party - Accu > 85%', 'description': '', 'test_group': '[PREGENERATED] firstparty Test',
     'conversion_trait': '[PREGENERATED] My Conversion Trait'}
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Provision accounts for the summit algo lab')
    parser.add_argument('pid', help='Partner id. Your company id')
    parser.add_argument('user', help='Name for a user that can connect to your administration portal')
    parser.add_argument('password', help='Password to connect to the administration portal')
    parser.add_argument('client_id', help='OAuth client id')
    parser.add_argument('client_secret', help='OAuth client secret')
    parser.add_argument('destination_id', help='Destinatino used for Audience Lab')

    args = parser.parse_args()

    base_url = 'https://api-sandbox.demdex.com'

    algo_account = AlgoAccount.AlgoAccount(base_url)
    algo_account.provision(int(args.pid),
                           args.user,  # Admin user name for the account you're provisioning
                           args.password,  # user password
                           args.client_id,  # Oauth2 client id
                           args.client_secret,
                           'BuildIT Main',  # name of the created data source
                           first_party_traits,  # all the first party traits
                           conversion_traits,  # all the conversion traits
                           algo_traits,  # the algorithmic traits to be created
                           segments,
                           args.destination_id
                           )
