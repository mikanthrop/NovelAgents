from camel.models.model_manager import ModelProcessingError

class ModelNotFoundError(Exception): 
    """
    Custom exception raised when a specified model cannot be found or initialized.
    """
    pass