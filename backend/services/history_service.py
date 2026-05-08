import csv
import io
from sqlalchemy.orm import Session
from backend.database import crud

class HistoryService:
    @staticmethod
    def export_as_csv(db: Session, conversation_id: int):
        messages = crud.get_messages(db, conversation_id)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Sender", "ASL Gloss", "Translated Sentence", "Confidence", "Timestamp"])
        for msg in messages:
            writer.writerow([msg.sender, msg.raw_words, msg.translated_sentence, msg.confidence, msg.created_at])
        return output.getvalue()

    @staticmethod
    def export_as_txt(db: Session, conversation_id: int):
        messages = crud.get_messages(db, conversation_id)
        output = []
        for msg in messages:
            output.append(f"[{msg.created_at}] {msg.sender.upper()}: {msg.translated_sentence}")
        return "\n".join(output)
