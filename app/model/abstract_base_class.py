from abc import ABC, abstractmethod

class AbstractBaseClass(ABC):
    """
    Abstract base class defining the structure for machine learning models.
    
    This class enforces the implementation of `fit` and `predict` methods in derived classes.
    """
    
    @abstractmethod
    def __init__():
        """
        Initializes the abstract base class.
        
        This method must be implemented in derived classes.
        """
        pass

    @abstractmethod
    def fit():
        """
        Abstract method for fitting a model to training data.
        
        This method must be implemented in derived classes.
        """
        pass

    @abstractmethod
    def predict():
        """
        Abstract method for making predictions using the trained model.
        
        This method must be implemented in derived classes.
        """
        pass
