class PatientNotFoundException(Exception):
    def __init__(self, message: str = "Patient not found"):
        self.message = message
        super().__init__(self.message)
