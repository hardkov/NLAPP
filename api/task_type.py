from enum import Enum


class TaskType(Enum):
    FILL_MASK = 1
    QUESTION_ANSWERING = 2
    SUMMARIZATION = 3
    TABLE_QUESTION_ANSWERING = 4
    TEXT_CLASSIFICATION = 5
    TEXT_GENERATION = 6
    TEXT_2_TEXT_GENERATION = 7
    TOKEN_CLASSIFICATION = 8
    TRANSLATION = 9
    ZERO_SHOT_CLASSIFICATION = 10
    SENTENCE_SIMILARITY = 11
    CONVERSATIONAL = 12
    FEATURE_EXTRACTION = 13
    TEXT_TO_SPEECH = 14
    AUTOMATIC_SPEECH_RECOGNITION = 15
    AUDIO_SOURCE_SEPARATION = 16
    VOICE_ACTIVITY_DETECTION = 17
    IMAGE_CLASSIFICATION = 18
    OBJECT_DETECTION = 19
    IMAGE_SEGMENTATION = 20


    @staticmethod
    def from_str(label):
        switcher = {
            'text2text-generation': TaskType.TEXT_2_TEXT_GENERATION,
            'summarization': TaskType.SUMMARIZATION,
            'feature-extraction': TaskType.FEATURE_EXTRACTION,
            'image-segmentation': TaskType.IMAGE_SEGMENTATION,
            'fill-mask': TaskType.FILL_MASK,
            'translation': TaskType.TRANSLATION,
            'text-to-speech': TaskType.TEXT_TO_SPEECH,
            'conversational': TaskType.CONVERSATIONAL,
            'text-generation': TaskType.TEXT_GENERATION,
            'table-question-answering': TaskType.TABLE_QUESTION_ANSWERING,
            'audio-source-separation': TaskType.AUDIO_SOURCE_SEPARATION,
            'text-classification': TaskType.TEXT_CLASSIFICATION,
            'zero-shot-classification': TaskType.ZERO_SHOT_CLASSIFICATION,
            'question-answering': TaskType.QUESTION_ANSWERING,
            'token-classification': TaskType.TOKEN_CLASSIFICATION,
            'voice-activity-detection': TaskType.VOICE_ACTIVITY_DETECTION,
            'image-classification': TaskType.IMAGE_CLASSIFICATION,
            'object-detection': TaskType.OBJECT_DETECTION,
            'automatic-speech-recognition': TaskType.AUTOMATIC_SPEECH_RECOGNITION,
            'sentence-similarity': TaskType.SENTENCE_SIMILARITY
        }
        if label in switcher:
            return switcher[label]
        else:
            raise NotImplementedError