# test_pickle.py
import pickle
from pathlib import Path

def test_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            print(f"Arquivo carregado com sucesso! Tipo: {type(data)}")
            return True
    except Exception as e:
        print(f"Erro ao carregar: {str(e)}")
        return False

# Teste todos os arquivos
current_dir = Path(__file__).parent
model_path = current_dir / ".." / ".." / "shared" / "machine_learning" / "modelo_risco_kde.pkl"
scaler_path = current_dir / ".." / ".." / "shared" / "machine_learning" / "scaler_risco.pkl"
features_path = current_dir / ".." / ".." / "shared" / "machine_learning" / "features_risco.pkl"

print("Testando modelo:")
test_pickle_file(model_path)

print("\nTestando scaler:")
test_pickle_file(scaler_path)

print("\nTestando features:")
test_pickle_file(features_path)