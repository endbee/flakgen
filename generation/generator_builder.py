import json
import sys
import generation.random_api as random_api


class GeneratorBuilder:
    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                self.data = json.load(config_file)
        except OSError as e:
            print(f"Unable open file \"{config_file_path}\": {e}", file=sys.stderr)
            sys.exit()

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
                'arithmetic': random_api.ArithmeticalGenerator(
                    self.data['random_api']["arithmetical"]["expression_count"],
                    self.data['random_api']["arithmetical"]["flakiness_prob"]
                )
            }
        }
