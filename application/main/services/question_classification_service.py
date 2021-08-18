import re
import nltk
nltk.download('punkt')
import pickle
from application.main.config import settings
from application.initializer import logger_instance

class QuestionIdentification(object):

    def __init__(self):
        self.logger = logger_instance.get_logger(__name__)
        self.classifier = pickle.load(open(settings.APP_CONFIG.CLASSIFICATION_MODEL, 'rb'))

    def dialogue_act_features(self, question: str):
        features = {}
        for word in nltk.word_tokenize(question):
            features['contains({})'.format(word.lower())] = True
        return features

    def identify_questions_type(self, question: str) -> str:
        self.logger.debug(f"Query Question : {question}")
        return self.classifier.classify(self.dialogue_act_features(question))


class QuestionClassificationService(object):

    def __init__(self) -> None:
        self.logger = logger_instance.get_logger(__name__)
        self.question_identification = QuestionIdentification()

    
    def data_cleaning(self, input_text: str) -> str:
        # function to remove non-ascii characters
        def _removeNonAscii(s): return "".join(i for i in s if ord(i) < 128)
        clean_text = _removeNonAscii(input_text)
        # remove url
        clean_text = re.sub(r'http\S+', '', clean_text)
        # replace special chars
        clean_text = clean_text.replace("[^a-zA-Z0-9]", " ")
        self.logger.debug(f" Cleaning Completed: {clean_text}")
        return clean_text

    def classify(self, input_text: str) -> str:
        cleaned_text = self.data_cleaning(input_text)
        return self.question_identification.identify_questions_type(cleaned_text)
