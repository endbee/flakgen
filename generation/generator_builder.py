import json
import generation.random_api as random_api


class GeneratorBuilder:
    def __init__(self, config_file_name):
        with open(config_file_name) as config_file:
            self.data = json.load(config_file)

    def build_generator_dict(self):
        return {
            'random_api': {
                'summation': random_api.SummationGenerator(
                    self.data['random_api']["summation"]["summation_depth"],
                    self.data['random_api']["summation"]["flakiness_prob"]
                ),
                'multiplication': random_api.MultiplicationGenerator(
                    self.data['random_api']["multiplication"]["multiplication_depth"],
                    self.data['random_api']["multiplication"]["flakiness_prob"]
                ),
            }
        }
