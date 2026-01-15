import io
import sys
from pathlib import Path

# Garantir que o diretório pai (backend) esteja no sys.path para importar `main`
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Caminho base para os arquivos de teste (agora estão no mesmo diretório)
TEST_FILES_DIR = Path(__file__).parent


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_csv_valid():
    file_path = TEST_FILES_DIR / "portifolio_valid.csv"
    with open(file_path, "rb") as f:
        response = client.post(
            "/upload-csv", files={"file": ("portifolio_valid.csv", f, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()
    assert "holdings" in data
    assert "warnings" in data
    assert "errors" in data
    assert len(data["holdings"]) == 3
    assert len(data["errors"]) == 0
    total_weight = sum(holding["weight"] for holding in data["holdings"])
    assert 99.9 <= total_weight <= 100.1


def test_upload_csv_with_error():
    file_path = TEST_FILES_DIR / "portifolio_error.csv"
    with open(file_path, "rb") as f:
        response = client.post(
            "/upload-csv", files={"file": ("portifolio_error.csv", f, "text/csv")}
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert len(detail) > 0
    error_message = " ".join(detail)
    assert "peso" in error_message.lower() or "weight" in error_message.lower()
    assert "numérico" in error_message.lower() or "número" in error_message.lower()


def test_upload_csv_with_warning():
    file_path = TEST_FILES_DIR / "portifolio_warning.csv"
    with open(file_path, "rb") as f:
        response = client.post(
            "/upload-csv", files={"file": ("portifolio_warning.csv", f, "text/csv")}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data["holdings"]) == 3
    assert len(data["warnings"]) > 0
    assert len(data["errors"]) == 0
    warning_messages = [w["message"] for w in data["warnings"]]
    assert any(
        "normalizada" in msg.lower() or "soma" in msg.lower()
        for msg in warning_messages
    )
    total_weight = sum(holding["weight"] for holding in data["holdings"])
    assert 99.9 <= total_weight <= 100.1


def test_upload_non_csv_file():
    fake_file = io.BytesIO(b"not a csv")
    response = client.post(
        "/upload-csv", files={"file": ("test.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400
    assert "apenas arquivos .csv" in response.json()["detail"].lower()


def test_upload_csv_missing_required_column():
    csv_content = b"symbol,name\nVTI,Vanguard\nVOO,Vanguard"
    fake_file = io.BytesIO(csv_content)
    response = client.post(
        "/upload-csv", files={"file": ("test.csv", fake_file, "text/csv")}
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    error_message = " ".join(detail) if isinstance(detail, list) else detail
    assert "ausente" in error_message.lower() or "weight" in error_message.lower()


def test_upload_csv_with_negative_weight():
    csv_content = (
        b"symbol,name,weight\nVTI,Vanguard,50\nVOO,Vanguard,-10\nQQQ,Invesco,60"
    )
    fake_file = io.BytesIO(csv_content)
    response = client.post(
        "/upload-csv", files={"file": ("test.csv", fake_file, "text/csv")}
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    error_message = " ".join(detail) if isinstance(detail, list) else detail
    assert "negativo" in error_message.lower()
