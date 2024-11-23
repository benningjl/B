class ErrorManager:
    @staticmethod
    def handle_error(error, log_function=None):
        message = f"An error occurred: {str(error)}"
        if log_function:
            log_function(message)
        return {"error": message}
