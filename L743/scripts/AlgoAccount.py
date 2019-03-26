import datetime
import AAMProtocol
import AAMClient
import json
import logging


class AlgoAccount:

    def __init__(self, base_url):
        self.protocol = AAMProtocol.AAMProtocol(base_url)

    @staticmethod
    def safe_print(content):
        logging.info(content)

    def provision(self, pid, user_name, user_password, client_id, client_secret,
                  datasource_name, traits, conversion_traits,
                  algo_traits, segments, destination_id_for_audielce_lab):

        try:
            client = AAMClient.AAMClient(self.protocol, pid, client_id,
                                         client_secret, user_name, user_password)
        except ValueError:
            return False

        #create the data source where we'll store the algo traits into
        algo_datasource = client.create_data_source('Algo-generated Data Source')
        if algo_datasource == -1:
            self.safe_print("Could not create or retrieve the algo data source")
            return False
        #create the data source that will store all the non-algo traits
        datasource = client.create_data_source(datasource_name)
        if datasource == -1:
            self.safe_print("Could not create or retrieve the data source")
            return False
        datasources_dict[datasource_name] = datasource
        datafile['datasources'] = datasources_dict
        all_datasources = third_party_data_sources.copy()
        all_datasources[datasource_name] = datasource

        # create the Lab folder, so the traits are grouped
        folder_id = client.create_folder_trait("Lab")
        if folder_id == -1:
            self.safe_print("Could not create the Lab folder")
            return False
        #create all the "regular" traits
        trait_dict = {}
        for t in traits:
            trait_name = t['name']
            trait_description = t['description']
            trait_comment = t['comment']
            trait_rule = t['rule']
            trait_type = t['type']
            traitid = client.create_trait(folder_id, trait_name, trait_description,
                                          trait_comment, trait_type, datasource, trait_rule)
            if traitid == -1:
                self.safe_print("Could not create trait %s" % trait_name)
                return False
            trait_dict[trait_name] = traitid

        #create the conversion traits
        conversion_trait_dict = {}
        for t in conversion_traits:
            trait_name = t['name']
            trait_description = ''
            trait_comment = ''
            trait_type = t['type']
            traitid = client.create_conversion_trait(folder_id, trait_name, trait_description,
                                                     trait_comment, trait_type, datasource)
            if traitid == -1:
                self.safe_print("Could not create conversion trait %s" % trait_name)
                return False
            conversion_trait_dict[trait_name] = traitid
        #create the algo models
        algo_models = [
            {
                'name': '[PREGENERATED] Garage Rehab Enthusiasts - 1st party',
                'baseline': 'Garage Rehab Enthusiasts',
                'datasources': [datasource],
                'description': '',
                'lookback': 30
           }
        ]

        algo_dict = {}
        for model in algo_models:
            model_name = model['name']
            model_baseline = trait_dict[model['baseline']]
            model_datasources = [all_datasources[ds] for ds in model['datasources']]
            model_description = model['description']
            model_lookback = model['lookback']
            model_id = client.create_algo_model(model_name, model_description, model_datasources, model_baseline,
                                                model_lookback)
            if model_id == -1:
                self.safe_print("Could not create algo model %s" % model_name)
                return False
            algo_dict[model_name] = model_id


        # IMPORTANT: this will only work if the model ran at least once
        algo_trait_dict = {}
        for trait in algo_traits:
            trait_name = trait['name']
            trait_description = trait['description']
            trait_model = trait['algo_model']
            trait_accuracy = trait['accuracy']
            algo_trait_id = client.create_algo_trait(folder_id,
                                                     trait_name, trait_description,
                                                     algo_datasource,
                                                     algo_dict[trait_model],
                                                     trait_accuracy)
            if algo_trait_id == -1:
                self.safe_print("Could not create algo trait " + trait_name)
                return False
            algo_trait_dict[trait_name] = algo_trait_id

        for segment in segments:
            seg_name = segment['name']
            seg_id = client.create_segment(seg_name, '', algo_datasource,
                                           str(algo_trait_dict[seg_name]) + 'T')
            if seg_id == -1:
                self.safe_print("Could not create segment " + seg_name)
                return False

            if 'test_group' in segment:
                test_group_id = client.create_test_group(segment['test_group'], '',
                                                         seg_id, destination_id_for_audielce_lab,
                                                         datetime.datetime.now().strftime('%Y-%m-%d'),
                                                         conversion_trait_dict[segment['conversion_trait']])
                if test_group_id == -1:
                    self.safe_print("Could not create test group " + segment['test_group'])
                    return False
