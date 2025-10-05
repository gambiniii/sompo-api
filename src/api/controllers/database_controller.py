from pathlib import Path
from src.api.logic.database_logic import DatabaseLogic

class DatabaseController:
    def __init__(self):
        self.logic = DatabaseLogic()

    def seed(self):
        caminho_arquivo = Path(__file__).parent.parent.parent.parent / "DATASHEETS"
        return self.logic.import_all_files_in_folder(str(caminho_arquivo))