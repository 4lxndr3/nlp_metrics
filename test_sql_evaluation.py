# test_sql_evaluation.py

import pytest
import pickle
from deepeval import assert_test
from deepeval.models import LLMTestCase # Importe para o pickle funcionar corretamente
from custom_metrics import ExecutionAccuracyMetric

# --- CARREGUE OS CASOS DE TESTE DO ARQUIVO ---
def load_test_cases(filename="test_cases_config_1.pkl"):
    """Carrega os casos de teste salvos."""
    with open(filename, "rb") as f:
        return pickle.load(f)

# Carrega os casos de teste que você gerou no outro script
test_cases = load_test_cases()

# --- DEFINIÇÃO DO TESTE ---
# O decorador @pytest.mark.parametrize diz ao pytest para rodar a função
# `test_sql_execution` uma vez para cada item na lista 'test_cases'.
@pytest.mark.parametrize("test_case", test_cases)
def test_sql_execution(test_case: LLMTestCase):
    # Garante que estamos testando um objeto do tipo correto
    assert isinstance(test_case, LLMTestCase), "O item não é um LLMTestCase válido"
    
    # Instancia a métrica, passando o caminho para as bases de dados do Spider
    # Certifique-se que este caminho está correto
    accuracy_metric = ExecutionAccuracyMetric(
        db_path_template="./spider/database/{db_id}/{db_id}.sqlite"
    )
    
    # Roda a avaliação para o caso de teste atual
    assert_test(test_case, [accuracy_metric])