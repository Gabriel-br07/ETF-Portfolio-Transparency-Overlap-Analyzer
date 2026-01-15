import io

import pandas as pd


class CSVWarning(Warning):
    def __init__(self, line, column, message):
        self.message = message
        self.line = line
        self.column = column


class CSVValidationError(Exception):
    def __init__(self, line, column, message):
        self.message = message
        self.line = line
        self.column = column


class CSVValidationErrors(Exception):
    def __init__(self, errors):
        self.errors = errors


def parse_csv(text):
    try:
        df = pd.read_csv(io.StringIO(text))
        return df
    except Exception as e:
        raise CSVValidationError(0, 0, f"Erro ao ler o CSV: {str(e)}")


def validate_header(df):
    expected = ["symbol", "name", "weight"]
    actual = list(df.columns)
    for col in expected:
        if col not in actual:
            raise CSVValidationError(1, "header", f"Coluna obrigatória '{col}' ausente")

    extra = [c for c in actual if c not in expected]
    warnings = []
    for c in extra:
        warnings.append(CSVWarning(1, c, f"Coluna extra '{c}' encontrada"))
    return warnings


def validate_weights(df):
    warnings = []
    errors = []

    for idx, val in df["weight"].items():
        line = idx + 2
        try:
            val = float(val)
            if val < 0:
                errors.append(
                    CSVValidationError(line, "weight", "Peso não pode ser negativo")
                )
        except Exception:
            errors.append(
                CSVValidationError(line, "weight", "Peso deve ser um valor numérico")
            )

    return warnings, errors


def validate_sum(df):
    total = df["weight"].sum()

    if 99 <= total <= 101:
        return [], []

    warnings = [
        CSVWarning(
            0,
            "weight",
            f"Soma total {total:.3f}, fora da faixa  99-101;será normalizada",
        )
    ]
    return warnings, []


def normalize_weights(df):
    total = df["weight"].sum()
    df["weight"] = df["weight"] * 100 / total
    return df


def validation_csv_portifolio(text):
    df = parse_csv(text)

    all_warnings = []
    all_errors = []

    # Cabeçalho
    h_warnings = validate_header(df)
    all_warnings.extend(h_warnings)

    # Peso
    w_warnings, w_errors = validate_weights(df)
    all_warnings.extend(w_warnings)
    all_errors.extend(w_errors)

    if all_errors:
        raise CSVValidationErrors(all_errors)

    # Soma
    s_warnings, s_errors = validate_sum(df)
    all_warnings.extend(s_warnings)
    all_errors.extend(s_errors)

    if all_errors:
        raise CSVValidationErrors(all_errors)

    # Normaliza quando necessário
    df = normalize_weights(df)

    return df, all_warnings
