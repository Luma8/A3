# API de Avaliação de Oficina

API REST para leitura e análise de dados do formulário de avaliação de oficinas (Excel). A API processa os dados, calcula idades e fornece endpoints com filtros avançados para alimentar dashboards.

## Instalação

```bash
pip install -r requirements.txt
```

## Executar a API

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## Endpoints Disponíveis

### 1. GET `/`
Retorna informações sobre a API e lista de endpoints disponíveis.

### 2. GET `/avaliacoes`
Lista todas as avaliações registradas no Excel, com suporte a filtros.

**Parâmetros de Consulta (Opcionais):**
- `genero`: Filtrar por gênero (ex: "Homem", "Mulher")
- `ano_escolar`: Filtrar por ano escolar (ex: "3º ano")
- `universidade_pretendida`: Filtrar por tipo de universidade (ex: "Pública", "Privada")
- `idade_min`: Idade mínima
- `idade_max`: Idade máxima

**Exemplo de Requisição:**
`GET /avaliacoes?genero=Mulher&idade_min=16`

**Resposta:**
```json
[
  {
    "id": 1,
    "data_conclusao": "2025-10-08 09:06:29",
    "nome": "Anônimo",
    "data_nascimento": "2008-05-15 00:00:00",
    "idade": 17,
    "genero": "Mulher",
    "ano_escolar": "3º ano",
    "universidade_pretendida": "Pública",
    "avaliacao_explicacoes": "Concordo totalmente",
    "avaliacao_aplicacoes": "Concordo totalmente",
    "avaliacao_tecnologias": "Concordo totalmente",
    "avaliacao_compreensao": "Concordo totalmente",
    "avaliacao_geral": "Concordo totalmente"
  }
]
```

### 3. GET `/estatisticas`
Retorna estatísticas completas e demografia das avaliações, respeitando os filtros aplicados.

**Parâmetros de Consulta (Opcionais):**
Mesmos parâmetros do endpoint `/avaliacoes`.

**Exemplo de Requisição:**
`GET /estatisticas?ano_escolar=3º ano`

**Resposta:**
```json
{
  "total_participantes": 45,
  "filtros_aplicados": {
    "genero": null,
    "ano_escolar": "3º ano",
    "universidade_pretendida": null,
    "idade_min": null,
    "idade_max": null
  },
  "demografia": {
    "genero": {
      "Homem": 20,
      "Mulher": 25
    },
    "ano_escolar": {
      "3º ano": 45
    },
    "universidade_pretendida": {
      "Pública": 30,
      "Privada": 10,
      "Não pretendo": 5
    },
    "idades": [17, 18, 17, 16, 18]
  },
  "avaliacoes": {
    "explicacoes_claras": {
      "Concordo totalmente": 30,
      "Concordo parcialmente": 15
    },
    "interesse_aplicacoes": { ... },
    "uso_tecnologias": { ... },
    "compreensao_curso": { ... },
    "experiencia_geral": { ... }
  }
}
```

## Documentação Interativa

Acesse `http://localhost:8000/docs` para a documentação interativa Swagger UI, onde você pode testar todos os endpoints e filtros diretamente no navegador.

## Exemplos de Uso no Front-end (JavaScript)

### Filtrando dados para Dashboard

```javascript
// Buscar estatísticas apenas de mulheres que querem universidade pública
const params = new URLSearchParams({
  genero: 'Mulher',
  universidade_pretendida: 'Pública'
});

fetch(`http://localhost:8000/estatisticas?${params}`)
  .then(response => response.json())
  .then(data => {
    console.log("Total filtrado:", data.total_participantes);
    console.log("Distribuição de satisfação:", data.avaliacoes.experiencia_geral);
  });
```

## Estrutura do Projeto

```
BackEnd/
├── main.py                  # API principal com endpoints e lógica de filtros
├── saveExcell.py           # (Legado) Funções de escrita
├── requirements.txt        # Dependências
└── Formulário de Avaliação da Oficina(1-51) (1).xlsx  # Fonte de dados
```
