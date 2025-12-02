from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openpyxl
import os
from typing import List, Optional, Dict, Any
from collections import Counter
from datetime import datetime

app = FastAPI(title="API Avaliação de Oficina")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_NAME = "dados.xlsx"

# Modelo de resposta baseado nas colunas reais do Excel
class AvaliacaoResponse(BaseModel):
    id: int
    data_conclusao: Optional[str] = None
    nome: Optional[str] = None
    data_nascimento: Optional[str] = None
    idade: Optional[int] = None
    genero: Optional[str] = None
    ano_escolar: Optional[str] = None
    universidade_pretendida: Optional[str] = None
    avaliacao_explicacoes: Optional[str] = None
    avaliacao_aplicacoes: Optional[str] = None
    avaliacao_tecnologias: Optional[str] = None
    avaliacao_compreensao: Optional[str] = None
    avaliacao_geral: Optional[str] = None
    interesse_tecnologia: Optional[str] = None
    interesse_desafios: Optional[str] = None
    interesse_matematica: Optional[str] = None
    interesse_portugues: Optional[str] = None
    materia_preferida: Optional[str] = None
    turno_preferencia: Optional[str] = None
    contato_programacao: Optional[str] = None
    gosta_jogos: Optional[str] = None
    possui_videogame: Optional[str] = None
    possui_computador: Optional[str] = None
    possui_internet: Optional[str] = None
    possui_celular: Optional[str] = None
    possui_internet_celular: Optional[str] = None

def calcular_idade(data_nascimento):
    if not data_nascimento or not isinstance(data_nascimento, datetime):
        return None
    hoje = datetime.now()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

@app.get("/")
def root():
    return {
        "message": "API de Avaliação da Oficina",
        "endpoints": [
            "GET /avaliacoes - Lista todas as avaliações (com filtros)",
            "GET /estatisticas - Retorna estatísticas das respostas (com filtros)"
        ]
    }

@app.get("/avaliacoes", response_model=List[AvaliacaoResponse])
def listar_avaliacoes(
    genero: Optional[str] = Query(None, description="Filtrar por gênero"),
    ano_escolar: Optional[str] = Query(None, description="Filtrar por ano escolar"),
    universidade_pretendida: Optional[str] = Query(None, description="Filtrar por tipo de universidade (Pública/Privada)"),
    idade_min: Optional[int] = Query(None, description="Idade mínima"),
    idade_max: Optional[int] = Query(None, description="Idade máxima")
):
    """Lista todas as avaliações do Excel com filtros opcionais"""
    if not os.path.exists(FILE_NAME):
        print(f"ERRO: Arquivo não encontrado: {FILE_NAME}")
        return []
    
    try:
        wb = openpyxl.load_workbook(FILE_NAME)
        ws = wb.active
        
        avaliacoes = []
        
        # Mapeamento de colunas (baseado na inspeção do arquivo)
        # ID: 0, Hora conclusão: 2, Nome: 4, Data Nasc: 6, Gênero: 7, Ano: 8, Univ: 10
        # Perguntas de avaliação: 24, 25, 26, 27, 28
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] is not None:
                data_nasc = row[6]
                idade = calcular_idade(data_nasc)
                
                # Aplicar filtros
                if genero and row[7] != genero:
                    continue
                if ano_escolar and row[8] != ano_escolar:
                    continue
                if universidade_pretendida and row[10] != universidade_pretendida:
                    continue
                if idade_min and (idade is None or idade < idade_min):
                    continue
                if idade_max and (idade is None or idade > idade_max):
                    continue

                avaliacoes.append({
                    "id": row[0],
                    "data_conclusao": str(row[2]) if row[2] else None,
                    "nome": row[4] if row[4] else "Anônimo",
                    "data_nascimento": str(data_nasc) if data_nasc else None,
                    "idade": idade,
                    "genero": row[7],
                    "ano_escolar": row[8],
                    "universidade_pretendida": row[10],
                    "avaliacao_explicacoes": row[24],
                    "avaliacao_aplicacoes": row[25],
                    "avaliacao_tecnologias": row[26],
                    "avaliacao_compreensao": row[27],
                    "avaliacao_geral": row[28],
                    "interesse_tecnologia": row[12],
                    "interesse_desafios": row[13],
                    "interesse_matematica": row[14],
                    "interesse_portugues": row[15],
                    "materia_preferida": row[16],
                    "turno_preferencia": row[11],
                    "contato_programacao": row[17],
                    "gosta_jogos": row[18],
                    "possui_videogame": row[19],
                    "possui_computador": row[20],
                    "possui_internet": row[21],
                    "possui_celular": row[22],
                    "possui_internet_celular": row[23]
                })
        
        wb.close()
        return avaliacoes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler arquivo: {str(e)}")

@app.get("/estatisticas")
def obter_estatisticas(
    genero: Optional[str] = Query(None),
    ano_escolar: Optional[str] = Query(None),
    universidade_pretendida: Optional[str] = Query(None),
    idade_min: Optional[int] = Query(None),
    idade_max: Optional[int] = Query(None)
):
    """Retorna estatísticas das respostas de avaliação com suporte a filtros"""
    if not os.path.exists(FILE_NAME):
        return {"message": f"Erro: Arquivo de dados '{FILE_NAME}' não encontrado no servidor."}

    avaliacoes = listar_avaliacoes(
        genero=genero, 
        ano_escolar=ano_escolar, 
        universidade_pretendida=universidade_pretendida,
        idade_min=idade_min,
        idade_max=idade_max
    )
    
    if not avaliacoes:
        return {"message": "Nenhuma avaliação encontrada com os filtros selecionados"}
    
    # Já são dicionários, não precisa converter
    avaliacoes_dicts = avaliacoes
    
    def contar_respostas(campo):
        respostas = [a[campo] for a in avaliacoes_dicts if a[campo]]
        return dict(Counter(respostas))

    return {
        "total_participantes": len(avaliacoes),
        "filtros_aplicados": {
            "genero": genero,
            "ano_escolar": ano_escolar,
            "universidade_pretendida": universidade_pretendida,
            "idade_min": idade_min,
            "idade_max": idade_max
        },
        "demografia": {
            "genero": contar_respostas("genero"),
            "ano_escolar": contar_respostas("ano_escolar"),
            "universidade_pretendida": contar_respostas("universidade_pretendida"),
            "idades": [a["idade"] for a in avaliacoes_dicts if a["idade"] is not None]
        },
        "avaliacoes": {
            "explicacoes_claras": contar_respostas("avaliacao_explicacoes"),
            "interesse_aplicacoes": contar_respostas("avaliacao_aplicacoes"),
            "uso_tecnologias": contar_respostas("avaliacao_tecnologias"),
            "compreensao_curso": contar_respostas("avaliacao_compreensao"),
            "experiencia_geral": contar_respostas("avaliacao_geral")
        },
        "interesses_areas": {
            "tecnologia": contar_respostas("interesse_tecnologia"),
            "desafios": contar_respostas("interesse_desafios"),
            "matematica": contar_respostas("interesse_matematica"),
            "portugues": contar_respostas("interesse_portugues"),
            "materia_preferida": contar_respostas("materia_preferida")
        },
        "perfil_tecnologico": {
            "turno_preferencia": contar_respostas("turno_preferencia"),
            "contato_programacao": contar_respostas("contato_programacao"),
            "gosta_jogos": contar_respostas("gosta_jogos"),
            "dispositivos": {
                "videogame": contar_respostas("possui_videogame"),
                "computador": contar_respostas("possui_computador"),
                "internet": contar_respostas("possui_internet"),
                "celular": contar_respostas("possui_celular"),
                "internet_celular": contar_respostas("possui_internet_celular")
            }
        }
    }

