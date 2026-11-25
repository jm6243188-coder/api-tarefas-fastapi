from pydantic import BaseModel

class EntradaCriarTarefa(BaseModel):
    titulo: str

class SaidaCriarTarefa(BaseModel):
    mensagem: str
    id: int
    titulo: str
    concluido: int

class SaidaListarTarefas(BaseModel):
    id: int
    titulo: str
    concluido: int

class SaidaListarTarefaEspecifica(BaseModel):
    id: int
    titulo: str
    concluido: int

class EntradaAtualizarTarefa(BaseModel):
    status_concluido: int
    
class SaidaAtualizarTarefa(BaseModel):
    mensagem: str
    id: int
    titulo: str
    concluido: 

class SaidaDeletarTarefa(BaseModel):
    mensagem: str
    id: int