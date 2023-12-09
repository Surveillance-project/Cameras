from abc import ABC, abstractmethod
import random
from connectivity.models import CriminalRecord, Profile, CriminalCode


class Preprocessor(ABC):
    def __init__(self):
        self.next_preprocessor = None

    def handle(self, image):
        processed_image = self._process(image)
        if self.next_preprocessor:
            return self.next_preprocessor.handle(processed_image)
        return processed_image

    @abstractmethod
    def _process(self, image) -> object:
        pass

    def set_next(self, preprocessor):
        self.next_preprocessor = preprocessor
        return self.next_preprocessor


class FakePreprocessor(Preprocessor):
    def _process(self, image):
        return image


class FakeCriminalProfilerByImageRetriever(Preprocessor):
    def __init__(self, chance_of_retrieval: int = 0.5):
        super().__init__()
        self.chance_of_retrieving = chance_of_retrieval

    def _process(self, image):
        hash_value = hash(image)
        random.seed(hash_value)
        chance = self.chance_of_retrieving

        profiles = Profile.objects.filter(criminalrecord__isnull=False).distinct()
        sampled_profiles = random.sample(list(profiles), int(chance * len(profiles)))

        return sampled_profiles

