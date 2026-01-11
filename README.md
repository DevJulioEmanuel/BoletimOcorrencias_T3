# API de Gestão de Boletins de Ocorrência (NoSQL)

API Web assíncrona desenvolvida com **FastAPI** e **MongoDB** para o gerenciamento de Boletins de Ocorrência, Autores e Declarantes. Este projeto foi migrado de uma arquitetura relacional para orientada a documentos, utilizando **Beanie** como ODM.

## 📋 Sobre o Projeto

Este projeto compõe a avaliação da disciplina de Persistência de Dados (UFC - Quixadá). O objetivo é implementar uma API robusta que realize operações CRUD completas e consultas complexas (Aggregation Pipelines) em um banco de dados NoSQL.

### 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
* **Banco de Dados:** [MongoDB](https://www.mongodb.com/) (Motor Assíncrono)
* **ODM (Object Document Mapper):** [Beanie](https://beanie-odm.dev/) (Baseado no Pydantic)
* **Gerenciador de Dependências:** [uv](https://github.com/astral-sh/uv)
* **Documentação:** OpenAPI (Swagger UI)

---

## 🏗️ Modelagem de Dados (NoSQL)

Abaixo está o diagrama de classes representando a estrutura dos documentos no MongoDB. 
*Nota: Diferente do modelo relacional, as relações N:N são resolvidas através de listas de referências (Links) dentro dos documentos, e não por tabelas associativas.*

```mermaid
classDiagram
    direction LR

    class Autor {
        +id: PydanticObjectId
        +nome: str
        +matricula: str
        +posto: str
        +lotacao: str
    }

    class Declarante {
        +id: PydanticObjectId
        +nome: str
        +cpf: str
        +endereco: str
        +tipo_envolvimento: Enum
    }

    class BoletimOcorrencia {
        +id: PydanticObjectId
        +data_registro: date
        +tipo_ocorrencia: Enum
        +status: Enum
        +autor: Link[Autor]
        +declarantes: List[Link[Declarante]]
        +historico_alteracoes: List[Embedded]
    }

    %% Relacionamentos
    BoletimOcorrencia --> "1" Autor : Referencia (Link)
    BoletimOcorrencia --> "0..*" Declarante : Referencia (Lista de Links)
