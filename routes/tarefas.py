import sqlite3
from fastapi import APIRouter, HTTPException, Path
from banco import conectar_banco
from schemas.tarefas import EntradaCriarTarefa, SaidaCriarTarefa, SaidaListarTarefas, SaidaListarTarefaEspecifica, EntradaAtualizarTarefa, SaidaAtualizarTarefa, SaidaDeletarTarefa

router = APIRouter(prefix="/tarefas")


@router.post("", response_model=SaidaCriarTarefa)
def criar_tarefa(entrada: EntradaCriarTarefa):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM tarefas WHERE titulo = ?",
            (entrada.titulo,)
        )

        titulo_encontrado = cursor.fetchone()
        if titulo_encontrado is not None:
            raise HTTPException(
                status_code=409,
                detail="Ja existe outro titulo com o mesmo nome"
            )

        cursor.execute("""
        INSERT INTO tarefas ( titulo, concluido) VALUES (?, ?)""",
        (entrada.titulo, 0)
        )

        tarefa_id = cursor.lastrowid

        conexao.commit()

        return {
            "mensagem": "Tarefa criada com sucesso",
            "id": tarefa_id,
            "titulo": entrada.titulo,
            "concluido": 0
        }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no criar tarefa: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()


@router.get("", response_model=list[SaidaListarTarefas])
def listar_tarefas(concluido_status: int | None = None):
    conexao = conectar_banco()

    try:
        if concluido_status is not None and concluido_status not in [0,1]:
            raise HTTPException(
                status_code=400,
                detail="O Status de concluido precisa ser 0 ou 1"
            )
        
        cursor = conexao.cursor()

        if concluido_status is not None:
            cursor.execute(
                "SELECT * FROM tarefas WHERE concluido = ?",
                (concluido_status,)
            )

        else:
            cursor.execute("SELECT * FROM tarefas")

        tarefas_encontradas = cursor.fetchall()
        if tarefas_encontradas == []:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma tarefa encontrada"
            )

        resultado = []

        for tarefa in tarefas_encontradas:
            resultado.append({
                "id": tarefa[0],
                "titulo": tarefa[1],
                "concluido": tarefa[2]
            })

        return resultado

    except sqlite3.Error as erro:
        print(f"Erro no listar tarefas: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()



@router.get("/{id}", response_model=SaidaListarTarefaEspecifica)
def listar_tarefa_especifica(id: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (id,)
        )

        tarefa_encontrada = cursor.fetchone()
        if tarefa_encontrada is None:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma tarefa encontrada"
            )

        return {
            "id": tarefa_encontrada[0],
            "titulo": tarefa_encontrada[1],
            "concluido": tarefa_encontrada[2]
        }

    except sqlite3.Error as erro:
        print(f"Erro no listar tarefa especifica: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()


@router.patch("/{id}/status", response_model=SaidaAtualizarTarefa)
def atualizar_status_tarefa(entrada: EntradaAtualizarTarefa, id: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (id,)
        )

        tarefa_encontrada = cursor.fetchone()
        if tarefa_encontrada is None:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma tarefa encontrada"
            )

        if entrada.status_concluido not in [0, 1]:
            raise HTTPException(
                status_code=400,
                detail="O Status de concluido precisa ser 0 ou 1"
            )

        cursor.execute("""
        UPDATE tarefas
        SET concluido = ? WHERE id = ?
        """, (entrada.status_concluido, id)
        )

        conexao.commit()

        if entrada.status_concluido == 1:

            return {
                "mensagem": "Status atualizado com sucesso",
                "id": tarefa_encontrada[0],
                "titulo": tarefa_encontrada[1],
                "concluido": "Tarefa concluida"
            }

        if entrada.status_concluido == 0:

            return {
                "mensagem": "Status atualizado com sucesso",
                "id": tarefa_encontrada[0],
                "titulo": tarefa_encontrada[1],
                "concluido": "A tarefa ainda não foi concluida"
            }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no atualizar status tarefa: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()


@router.delete("/{id}", response_model=SaidaDeletarTarefa)
def deletar_tarefa(id: int = Path(gt=0)):
    conexao = conectar_banco()

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM tarefas WHERE id = ?",
            (id,)
        )

        tarefa_encontrada = cursor.fetchone()
        if tarefa_encontrada is None:
            raise HTTPException(
                status_code=404,
                detail="Nenhuma tarefa encontrada"
            )

        cursor.execute("""
        DELETE FROM tarefas 
        WHERE id = ? """,
        (id,)
        )

        conexao.commit()

        return {
            "mensagem": "Tarefa deletada com sucesso",
            "id": id
        }

    except sqlite3.Error as erro:
        conexao.rollback()

        print(f"Erro no deletar tarefa: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno no SQLITE"
        )

    finally:
        conexao.close()