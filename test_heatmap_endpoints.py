"""
Script de teste para verificar os endpoints de heatmap
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_accidents_heatmap():
    """Testa endpoint de heatmap de acidentes"""
    try:
        response = requests.get(f"{BASE_URL}/cargo_accidents/heatmap?limit=10")
        print(f"✓ Accidents Heatmap: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  - Pontos retornados: {data.get('count', 0)}")
            if data.get('data'):
                print(f"  - Exemplo de ponto: {data['data'][0]}")
        else:
            print(f"  - Erro: {response.text}")
    except Exception as e:
        print(f"✗ Accidents Heatmap: Erro - {e}")

def test_thefts_heatmap():
    """Testa endpoint de heatmap de roubos"""
    try:
        response = requests.get(f"{BASE_URL}/cargo_thefts/heatmap?limit=10")
        print(f"✓ Thefts Heatmap: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  - Pontos retornados: {data.get('count', 0)}")
            if data.get('data'):
                print(f"  - Exemplo de ponto: {data['data'][0]}")
        else:
            print(f"  - Erro: {response.text}")
    except Exception as e:
        print(f"✗ Thefts Heatmap: Erro - {e}")

def test_health():
    """Testa se a API está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ API Health: Status {response.status_code}")
        if response.status_code == 200:
            print(f"  - {response.json()}")
    except Exception as e:
        print(f"✗ API Health: Erro - {e}")
        print("  - Certifique-se de que a API está rodando: uvicorn main:app --reload")

if __name__ == "__main__":
    print("=" * 50)
    print("Testando Endpoints de Heatmap")
    print("=" * 50)
    print()

    test_health()
    print()
    test_accidents_heatmap()
    print()
    test_thefts_heatmap()
    print()
    print("=" * 50)
