import json
import sys

import generation.random_api.arithmetical
import generation.random_api.multiplication
import generation.random_api.summation
import generation.random_api.combination
import generation.test_order_dependent.basic_brittle_state_setter
import generation.test_order_dependent.basic_victim_polluter
import generation.test_order_dependent.classes_brittle_state_setter
import generation.test_order_dependent.classes_victim_polluter
import generation.test_order_dependent.multiple_classes_victim_polluter



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
                'summation': generation.random_api.summation.SummationGenerator(
                    self.data['random_api']["summation"]["flakiness_prob"]
                ),
                'multiplication': generation.random_api.multiplication.MultiplicationGenerator(
                    self.data['random_api']["multiplication"]["flakiness_prob"]
                ),
                'arithmetical': generation.random_api.arithmetical.ArithmeticalGenerator(
                    self.data['random_api']["arithmetical"]["flakiness_prob"]
                ),
                'combination': generation.random_api.combination.RandomApiCombinationGenerator(
                    generation.random_api.summation.SummationGenerator(
                        self.data['random_api']["combination"]["summation"]["flakiness_prob"]
                    ),
                    generation.random_api.multiplication.MultiplicationGenerator(
                        self.data['random_api']["combination"]["multiplication"]["flakiness_prob"]
                    ),
                    generation.random_api.arithmetical.ArithmeticalGenerator(
                        self.data['random_api']["combination"]["arithmetical"]["flakiness_prob"]
                    )
                )
            },
            'test_order_dependent': {
                'basic_victim_polluter':
                    generation.test_order_dependent.basic_victim_polluter.BasicVictimPolluterTestOrderDependentGenerator(),
                'basic_brittle_state_setter':
                    generation.test_order_dependent.basic_brittle_state_setter.BasicBrittleStateSetterTestOrderDependentGenerator(),
                'classes_brittle_state_setter':
                    generation.test_order_dependent.classes_brittle_state_setter.ClassesBrittleStateSetterTestOrderDependentGenerator(),
                'classes_victim_polluter':
                    generation.test_order_dependent.classes_victim_polluter.ClassesVictimPolluterTestOrderDependentGenerator(),
                'multiple_classes_victim_polluter':
                    generation.test_order_dependent.multiple_classes_victim_polluter.MultipleClassesVictimPolluterTestOrderDependentGenerator(),
            }
        }
