"""Custom exceptions for Patient Health Analyzer application."""


class PatientHealthAnalyzerError(Exception):
    """Base exception for all patient health analyzer errors.

    This is the parent class for all custom exceptions raised by the
    patient health analyzer application.
    """

    pass


class BloodPressureFormatError(PatientHealthAnalyzerError):
    """Exception raised when blood pressure format is invalid.

    Raised when the blood pressure string cannot be parsed into
    systolic and diastolic values.
    """

    pass


class PatientDataError(PatientHealthAnalyzerError):
    """Exception raised when patient data is malformed or incomplete.

    Raised when patient data fails validation or required fields
    are missing or have invalid types.
    """

    pass


class DataLoadError(PatientHealthAnalyzerError):
    """Exception raised when CSV data cannot be loaded.

    Raised when the CSV file cannot be read, is missing, or has
    an invalid format.
    """

    pass


class VisualizationError(PatientHealthAnalyzerError):
    """Exception raised when chart generation fails.

    Raised when the health status distribution chart cannot be
    generated or saved.
    """

    pass
