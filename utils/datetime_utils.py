from datetime import datetime

def parse_iso_datetime(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
    except ValueError:
        raise ValueError("Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS ou YYYY-MM-DDTHH:MM)")