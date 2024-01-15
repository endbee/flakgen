from evaluation.strategy.flakiness_evaluation_strategy import FlakinessEvaluationStrategy
from evaluation.strategy.category_evaluation_strategy import CategoryEvaluationStrategy
class Evaluator:

    def __init__(self, evaluation_strategy):
        self._evaluation_strategy = evaluation_strategy

    @property
    def evaluation_strategy(self):
        return self._evaluation_strategy

    def evaluation_strategy(self, evaluation_strategy):
        self._evaluation_strategy = evaluation_strategy

    def evaluate(self):
        self._evaluation_strategy.evaluate()

def get_evaluators():
    return [
        Evaluator(FlakinessEvaluationStrategy()),
        Evaluator(CategoryEvaluationStrategy())
    ]