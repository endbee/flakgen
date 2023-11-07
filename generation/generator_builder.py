import json
import sys
import generation.random_api as random_api
import generation.test_order_dependent as test_order_dependent


class GeneratorBuilder:
    # Reads the config file provided in path
    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                self.data = json.load(config_file)
        except OSError as e:
            print(f"Unable open file \"{config_file_path}\": {e}", file=sys.stderr)
            sys.exit()

    # Builds all implemented generator classes with respective parameters from config file
    def build_generator_dict(self):
        return {
            'random_api': {
                'summation': random_api.SummationGenerator(
                    self.data['random_api']["summation"]["flakiness_prob"]
                ),
                'multiplication': random_api.MultiplicationGenerator(
                    self.data['random_api']["multiplication"]["flakiness_prob"]
                ),
                'arithmetical': random_api.ArithmeticalGenerator(
                    self.data['random_api']["arithmetical"]["expression_count"],
                    self.data['random_api']["arithmetical"]["flakiness_prob"]
                )
            },
            'test_order_dependent': {
                'basic_victim_polluter': test_order_dependent.BasicVictimPolluterTestOrderDependentGenerator(),
                'basic_brittle_state_setter': test_order_dependent.BasicBrittleStateSetterTestOrderDependentGenerator(),
                'classes': test_order_dependent.ClassesTestOrderDependentGenerator(),
            }
        }
