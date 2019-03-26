import AAMProtocol
import logging

success = AAMProtocol.AAMProtocol.success


class AAMClient:

    def __init__(self, protocol, pid, client_id, client_secret, user_name, user_password):
        self.pid = pid
        self.protocol = protocol  # type: AAMProtocol
        self.api_base_url = '/v1'
        self.trait_cache = {}  # cache for making less calls to the trait get api if the trait was already created
        self.user_token = self.protocol.get_token(client_id, client_secret, user_name, user_password)
        if self.user_token is None:
            raise ValueError('Incorrect credentials or secrets!')

    @staticmethod
    def safe_print(content):
        logging.info(content)

    def get_destination(self, pid, name):
        response = self.protocol.get(self.user_token, "/v1/destinations")
        if success(response):
            data = response.json()
            destinations_with_name = [x for x in data if x['name'] == name]
            if len(destinations_with_name) > 0:
                return destinations_with_name[0]['destinationId']
        return -1

    def create_data_source(self, name):
        data_source = self.get_data_source(name)
        if data_source != -1:
            return data_source
        data_source = {
            'pid': self.pid,
            'name': name,
            'description': 'Store all the things',
            'type': 'GENERAL',
            'idType': 'COOKIE',
            'dataExportRestrictions': [],
            'inboundS2S': 'true',
            'outboundS2S': 'false',
            'useAudienceManagerVisitorID': 'true'  # must be used so we don't generate the dpid activity trait
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/datasources/', data_source)
        if success(response):
            data_source = response.json()
            return data_source['dataSourceId']
        return -1

    def get_data_source(self, name):
        response = self.protocol.get(self.user_token, self.api_base_url + '/datasources?pid=' + str(self.pid))
        if success(response):
            data_source = response.json()
            ds = [x for x in data_source if x['name'] == name]
            if len(ds) > 0:
                return ds[0]['dataSourceId']
        return -1

    def create_folder_trait(self, name):
        folder_trait = self.get_folder_trait(name)
        if folder_trait != -1:
            return folder_trait
        folder_trait = {
            'pid': self.pid,
            'parentFolderId': 0,
            'name': name
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/folders/traits/', folder_trait)
        if success(response):
            folder_trait = response.json()
            return folder_trait['folderId']
        else:
            return -1

    def get_folder_trait(self, name):
        response = self.protocol.get(self.user_token, self.api_base_url + '/folders/traits')
        d = response.json()
        if success(response):
            sub_folders = d[0]['subFolders']
            filtered = [x for x in sub_folders if x['name'] == name]
            if len(filtered) > 0:
                return filtered[0]['folderId']
            else:
                return -1
        else:
            return -1

    def create_trait(self, folder_id, name, description, comment, trait_type, data_source, trait_rule):
        trait = self.get_trait(name)
        if trait != -1:
            return trait
        trait = {
            'pid': self.pid,
            'name': name,
            'description': description,
            'integrationCode': name,
            'comments': comment,
            'traitType': trait_type,
            'status': 'ACTIVE',
            'dataSourceId': data_source,
            'folderId': folder_id,
            'traitRule': trait_rule,
            'type': 0,
            'categoryId': 0,
            'crUID': 0,
            'upUID': 0,
            'createTime': 0,
            'updateTime': 0,
            'ttl': 0
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/traits/', trait)
        if success(response):
            trait = response.json()
            return trait['sid']
        else:
            return -1

    def create_conversion_trait(self, folder_id, name, description, comment, trait_type, data_source):
        trait = self.get_trait(name)
        if trait != -1:
            return trait
        trait = {
            'pid': self.pid,
            'name': name,
            'description': description,
            'integrationCode': name,
            'comments': comment,
            'traitType': trait_type,
            'status': 'ACTIVE',
            'dataSourceId': data_source,
            'folderId': folder_id,
            'traitRule': '',
            'type': 38,
            'categoryId': 0,
            'crUID': 0,
            'upUID': 0,
            'createTime': 0,
            'updateTime': 0,
            'ttl': 0
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/traits/', trait)
        if success(response):
            trait = response.json()
            return trait['sid']
        else:
            return -1

    def create_algo_trait(self, folder_id, name, description, data_source, algo_model_id, accuracy):
        trait = self.get_trait(name)
        if trait != -1:
            return trait
        trait = {
            'pid': self.pid,
            'name': name,
            'description': description,
            'integrationCode': name,
            'traitType': 'ALGO_TRAIT',
            'status': 'ACTIVE',
            'dataSourceId': data_source,
            'folderId': folder_id,
            'categoryId': 0,
            'crUID': 0,
            'upUID': 0,
            'createTime': 0,
            'updateTime': 0,
            'ttl': 0,
            'algoModelId': algo_model_id,
            'accuracy': accuracy,
            'thresholdType': 'ACCURACY'
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/traits/', trait)
        if success(response):
            trait = response.json()
            return trait['sid']
        else:
            self.safe_print(response.json())
            return -1

    def get_trait(self, name):
        if name in self.trait_cache:
            return self.trait_cache[name]

        response = self.protocol.get(self.user_token, self.api_base_url + '/traits?pid=' + str(self.pid))
        if not success(response):
            return -1
        d = response.json()

        # populate the cache
        for trait in d:
            self.trait_cache[trait['name']] = trait['sid']
        filtered = [x for x in d if x['name'] == name]
        if len(filtered) > 0:
            return filtered[0]['sid']
        else:
            return -1

    def get_segment(self, name):
        response = self.protocol.get(self.user_token, self.api_base_url + '/segments?pid=' + str(self.pid))
        d = response.json()
        filtered = [x for x in d if x['name'] == name]
        if len(filtered) > 0:
            return filtered[0]['sid']
        else:
            return -1

    def create_segment(self, name, description, data_source, rule):
        segment = self.get_segment(name)
        if segment != -1:
            return segment
        segment = {
            'name': name,
            'description': description,
            'integrationCode': name,
            'segmentRule': rule,
            'dataSourceId': data_source,
            'folderId': 0,
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/segments/', segment)
        if success(response):
            segment = response.json()
            return segment['sid']
        else:
            return -1

    def create_test_group(self, name, description, base_sid, destination_id, start_date, conversion_trait):
        segment_test_group = self.get_test_group(name)
        if segment_test_group != -1:
            return segment_test_group
        segment_test_group = {
            'name': name,
            'description': description,
            'baseSegmentSid': base_sid,
            'testSegments': [
                {
                    'name': 'Test Segment 1', 'percentage': 10, 'controlSegment': True
                },
                {
                    'name': 'Test Segment 2', 'percentage': 90
                }],
            'conversionSids': [conversion_trait],
            'destinationMappings': [
                {'destinationId': destination_id, 'testSegmentName': 'Test Segment 2', 'traitAlias': '4'}],
            'startDate': start_date,
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/segment-test-groups/', segment_test_group)
        if success(response):
            return response.json()['segmentTestGroupId']
        else:
            self.safe_print(response.json())
        return -1

    def get_test_group(self, name):
        response = self.protocol.get(self.user_token, self.api_base_url + '/segment-test-groups/')
        d = response.json()
        filtered = [x for x in d if x['name'] == name]
        if len(filtered) > 0:
            return filtered[0]['segmentTestGroupId']
        else:
            return -1

    def get_raw_test_group(self, test_group_id):
        response = self.protocol.get(self.user_token, self.api_base_url + '/segment-test-groups/' + str(test_group_id))
        d = response.json()
        if d['segmentTestGroupId'] == test_group_id:
            return d
        else:
            return None

    def get_all_test_groups(self):
        response = self.protocol.get(self.user_token, self.api_base_url + '/segment-test-groups/')
        return response.json()

    def get_data_feed_free_plans(self, data_source_id):
        response = self.protocol.get(self.user_token, self.api_base_url + '/available-data-feeds/' + str(
            data_source_id) + '/plans?includeSubscriptionDetails=true&no-cache=true')
        if success(response):
            return [plan['planId'] for plan in response.json() if plan['price'] == 0]
        else:
            self.safe_print(response.json())
        return []

    def subscribe_to_data_feed(self, data_source_id):
        response = self.protocol.get.post(self.user_token,
                                          self.api_base_url + '/available-data-feeds/' + str(
                                              data_source_id) + '/subscribe?no-cache=true',
                                          self.get_data_feed_free_plans(data_source_id))
        if success(response):
            return True
        else:
            return False

    def create_data_feed(self, data_source_id, name, description):
        data_feed = self.get_data_feed(data_source_id, name)
        if data_feed != -1:
            return data_feed
        data_feed = {
            'name': name,
            'description': description,
            'billing': 'ADOBE',
            'dataSourceId': data_source_id,
            'status': 'ACTIVE',
            'distribution': 'PUBLIC',
            'dataBrandingType': 'BRANDED'
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/data-feeds/', data_feed)
        if success(response):
            return data_source_id
        return -1

    def get_data_feed(self, data_source_id, name):
        response = self.protocol.get(self.user_token, self.api_base_url + '/data-feeds/' + str(data_source_id))
        if success(response):
            data_feed = response.json()
            if data_feed['name'] == name:
                return data_source_id
        return -1

    def create_data_feed_free_plans(self, data_source_id):
        if self.have_data_feed_plan(data_source_id):
            return True
        plan = {
            'description': 'string',
            'useCase': [
                'SEGMENTS_AND_OVERLAP',
                'MODELING',
                'FEED_EXPORT'
            ],
            'billingCycle': 'MONTHLY_IN_ARREARS',
            'billingUnit': 'FIXED',
            'price': 0,
            'status': 'ACTIVE'
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/data-feeds/' + str(data_source_id) +
                                      '/plans/', plan)
        if success(response):
            return True
        return False

    def have_data_feed_plan(self, data_source_id):
        response = self.protocol.get(self.user_token, self.api_base_url + '/data-feeds/' + str(data_source_id) +
                                     '/plans/')
        if success(response) and len(response.json()) > 0:
            return True
        return False

    def create_algo_model(self, name, description, data_sources, baseline, look_back_period):
        algo_model = self.get_algo_model(name)
        if algo_model != -1:
            return algo_model
        algo = {
            'pid': self.pid,
            'name': name,
            'description': description,
            'dataSources': data_sources,
            'sid': baseline,
            'algoTypeId': 1,
            'lookBackPeriod': look_back_period
        }
        response = self.protocol.post(self.user_token, self.api_base_url + '/models/', algo)
        if success(response):
            algo = response.json()
            return algo['algoModelId']
        else:
            self.safe_print(response.json())
        return -1

    def get_algo_model(self, name):
        response = self.protocol.get(self.user_token, self.api_base_url + '/models')
        if success(response):
            m = [x for x in response.json() if x['name'] == name]
            if len(m) > 0:
                return m[0]['algoModelId']
        return -1
