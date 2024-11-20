import logging
from datetime import datetime
from .models import db, SystemLog


class DatabaseLogHandler(logging.Handler):
    """
    A custom logging handler that stores logs in the SystemLog database table.
    """
    def __init__(self, app):
        """
        Initialize the handler with the Flask application instance.
        """
        super().__init__()
        self.app = app

    def emit(self, record):
        with self.app.app_context():  # Use the app context for database operations
            try:
                # Create a log entry
                log_entry = SystemLog(
                    timestamp=datetime.utcnow(),
                    severity=record.levelname,
                    message=self.format(record)
                )
                # Add the log entry to the session and commit
                db.session.add(log_entry)
                db.session.commit()
            except Exception as e:
                # Fallback to standard error to avoid silent failures
                print(f"Failed to log to database: {e}", flush=True)
