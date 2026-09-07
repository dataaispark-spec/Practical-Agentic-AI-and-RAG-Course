class AIServiceError(Exception):
    """Expected application-level AI service failure."""


class AIValidationError(AIServiceError):
    pass


class AIRateLimitError(AIServiceError):
    pass


class AITimeoutError(AIServiceError):
    pass


class AIProviderError(AIServiceError):
    pass
