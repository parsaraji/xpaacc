from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
import json

class AuditService:
    def __init__(self, session: Session):
        self.session = session

    def log_action(self, action_type: str, entity_type: str, entity_id: int = None,
                   prev_vals: dict = None, new_vals: dict = None, user: str = "Admin"):
        prev_str = json.dumps(prev_vals, ensure_ascii=False) if prev_vals else None
        new_str = json.dumps(new_vals, ensure_ascii=False) if new_vals else None

        log = AuditLog(
            action_type=action_type,
            entity_type=entity_type,
            entity_id=entity_id,
            previous_values=prev_str,
            new_values=new_str,
            user=user
        )
        self.session.add(log)
        self.session.flush()
