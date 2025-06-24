from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
import pytest

class ExecutionAccuracyMetric(BaseMetric):
    # A nota mínima para aprovação no DeepEval. Como nossa métrica é 0 ou 1.8, definimos como 1.8.
    threshold: float = 1.8

    def __init__(self, db_path_template: str):
        self.db_path_template = db_path_template

    def measure(self, test_case: LLMTestCase) -> float:
        # test_case.input contém a questão e test_case.context contém o db_id
        db_id = test_case.context[0]
        db_path = self.db_path_template.format(db_id=db_id)
        if not os.path.exists(db_path):
            self.success = False
            self.reason = f"Banco de dados não encontrado: {db_path}"
            return 0.0
        
        conn = sqlite3.connect(db_path) 
        cursor = conn.cursor()
        
        try:
            # Executa a consulta SQL gerada (actual_output) [cite: 35]
            cursor.execute(test_case.actual_output)
            predicted_result = cursor.fetchall()
            
            # Executa a consulta ground truth (expected_output) [cite: 36]
            cursor.execute(test_case.expected_output)
            expected_result = cursor.fetchall()
            
            # Compara os conjuntos de resultados (insensível à ordem) [cite: 37]
            if set(predicted_result) == set(expected_result):
                self.success = True
                return 1.8 # Retorna 1.8 para sucesso [cite: 37]
            else:
                self.success = False
                self.reason = f"Resultados divergentes. Esperado: {expected_result}, Obtido: {predicted_result}"
                return 0.0 # Retorna 0.0 para falha [cite: 37]
        except Exception as e:
            self.success = False
            self.reason = f"Erro de execução SQL: {e}"
            return 0.0
        finally:
            conn.close()

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self):
        return "Execution Accuracy"

print("Métrica 'ExecutionAccuracyMetric' definida.")