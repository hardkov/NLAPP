import sys
from enum import Enum

from api.models.model import Model
from api.task_type import TaskType

MODEL_DIR = sys.path[1] + '/data/models'


class ModelDir(Enum):
    FILL_MASK = MODEL_DIR + '/fillMask',
    QUESTION_ANSWERING = MODEL_DIR + '/questionAnswering',
    SUMMARIZATION = MODEL_DIR + '/summarization',
    TABLE_QUESTION_ANSWERING = MODEL_DIR + '/tableQuestionAnswering',
    TEXT_CLASSIFICATION = MODEL_DIR + '/textClassification',
    TEXT_GENERATION = MODEL_DIR + '/textGeneration'
    TEXT_2_TEXT_GENERATION = MODEL_DIR + '/text2TextGeneration',
    TOKEN_CLASSIFICATION = MODEL_DIR + '/tokenClassification',
    TRANSLATION = MODEL_DIR + '/translation',
    ZERO_SHOT_CLASSIFICATION = MODEL_DIR + '/zeroShotClassification',
    SENTENCE_SIMILARITY = MODEL_DIR + '/sentenceSimilarity',
    CONVERSATIONAL = MODEL_DIR + '/conversational',
    FEATURE_EXTRACTION = MODEL_DIR + '/featureExtraction',
    TEXT_TO_SPEECH = MODEL_DIR + '/textToSpeech',
    AUTOMATIC_SPEECH_RECOGNITION = MODEL_DIR + '/automaticSpeechRecognition',
    AUDIO_SOURCE_SEPARATION = MODEL_DIR + '/audioSourceSeparation',
    VOICE_ACTIVITY_DETECTION = MODEL_DIR + '/voiceActivityDetection',
    IMAGE_CLASSIFICATION = MODEL_DIR + '/imageClassification',
    OBJECT_DETECTION = MODEL_DIR + '/objectDetection',
    IMAGE_SEGMENTATION = MODEL_DIR + '/imageSegmentation'

    @staticmethod
    def from_task_type(task_type: TaskType):
        switcher = {
            TaskType.TEXT_2_TEXT_GENERATION:        ModelDir.TEXT_2_TEXT_GENERATION,
            TaskType.SUMMARIZATION:                 ModelDir.SUMMARIZATION,
            TaskType.FEATURE_EXTRACTION:            ModelDir.FEATURE_EXTRACTION,
            TaskType.IMAGE_SEGMENTATION:            ModelDir.IMAGE_SEGMENTATION,
            TaskType.FILL_MASK:                     ModelDir.FILL_MASK,
            TaskType.TRANSLATION:                   ModelDir.TRANSLATION,
            TaskType.TEXT_TO_SPEECH:                ModelDir.TEXT_TO_SPEECH,
            TaskType.CONVERSATIONAL:                ModelDir.CONVERSATIONAL,
            TaskType.TEXT_GENERATION:               ModelDir.TEXT_GENERATION,
            TaskType.TABLE_QUESTION_ANSWERING:      ModelDir.TABLE_QUESTION_ANSWERING,
            TaskType.AUDIO_SOURCE_SEPARATION:       ModelDir.AUDIO_SOURCE_SEPARATION,
            TaskType.TEXT_CLASSIFICATION:           ModelDir.TEXT_CLASSIFICATION,
            TaskType.ZERO_SHOT_CLASSIFICATION:      ModelDir.ZERO_SHOT_CLASSIFICATION,
            TaskType.QUESTION_ANSWERING:            ModelDir.QUESTION_ANSWERING,
            TaskType.TOKEN_CLASSIFICATION:          ModelDir.TOKEN_CLASSIFICATION,
            TaskType.VOICE_ACTIVITY_DETECTION:      ModelDir.VOICE_ACTIVITY_DETECTION,
            TaskType.IMAGE_CLASSIFICATION:          ModelDir.IMAGE_CLASSIFICATION,
            TaskType.OBJECT_DETECTION:              ModelDir.OBJECT_DETECTION,
            TaskType.AUTOMATIC_SPEECH_RECOGNITION:  ModelDir.AUTOMATIC_SPEECH_RECOGNITION,
            TaskType.SENTENCE_SIMILARITY:           ModelDir.SENTENCE_SIMILARITY
        }
        if task_type in switcher:
            return switcher[task_type].value[0]
        else:
            raise NotImplementedError

    @staticmethod
    def cache_dir(model: Model):
        model.cached = True
        return f'{ModelDir.from_task_type(model.task_type)}/{model.name}'