import logging
from datetime import datetime
from .models import db, SystemLog


class DatabaseLogHandler(logging.Handler):
    """
    A custom logging handler that stores logs in the SystemLog database table.
    """
    def emit(self, record):
        try:
            # Create a log entry
            log_entry = SystemLog(
                timestamp=datetime.utcnow(),  # Current timestamp
                severity=record.levelname,    # Log level (e.g., INFO, WARNING)
                message=self.format(record)  # Formatted log message
            )
            # Add the log entry to the session and commit
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            # Fallback to standard error to avoid silent failures
            print(f"Failed to log to database: {e}", flush=True)
