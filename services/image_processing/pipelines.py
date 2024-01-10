from .preprocessors import FakePreprocessor, FakeCriminalProfilerByImageRetriever


class FakePeopleDetectionPipeline:
    # Chance of retrieval set to <1 to prevent profiler retrieving all the criminal records
    def __init__(self, chance_of_retrieval: float = 0.95):
        self.pipeline = FakePreprocessor()
        self.pipeline.set_next(FakeCriminalProfilerByImageRetriever(chance_of_retrieval))

    # hashable will be used to seed a random value
    def run(self, hashable):
        return self.pipeline.handle(hashable)
