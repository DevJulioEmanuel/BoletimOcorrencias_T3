from typing import List, Optional
from datetime import date, datetime
from enum import Enum
from beanie import Document, Link
from pydantic import BaseModel, Field

from models.autor import Autor
from models.declarante import Declarante

class TipoOcorrencia(str, Enum):
    FURTO = "Furto"
    ROUBO = "Roubo"
    HOMICIDIO = "Homicídio"
    LESAO_CORPORAL = "Lesão Corporal"
    AMEACA = "Ameaça"
    VIOLENCIA_DOMESTICA = "Violência Doméstica"
    ESTELIONATO = "Estelionato"
    DANOS_MATERIAIS = "Danos Materiais"
    ACIDENTE_TRANSITO = "Acidente de Trânsito"
    EMBRIAGUEZ_AO_VOLANTE = "Embriaguez ao Volante"
    DESAPARECIMENTO_PESSOA = "Desaparecimento de Pessoa"
    ENCONTRO_CADAVER = "Encontro de Cadáver"
    ENCONTRO_PESSOA = "Encontro de Pessoa"
    PERTURBACAO_TRANQUILIDADE = "Perturbação do Sossego/Tranquilidade"
    VIOLACAO_DOMICILIO = "Violação de Domicílio"
    DANO = "Dano"
    POSSE_DROGAS = "Posse de Drogas"
    TRAFICO_DROGAS = "Tráfico de Drogas"
    PORTE_ARMA = "Porte Ilegal de Arma"
    RECEPTACAO = "Receptação"
    CRIME_CIBERNETICO = "Crime Cibernético"
    FRAUDE = "Fraude"
    DIFAMACAO = "Difamação"
    INJURIA = "Injúria"
    CALUNIA = "Calúnia"
    DESOBEDIENCIA = "Desobediência"
    DESACATO = "Desacato"
    VIOLACAO_MEDIDA_PROTETIVA = "Violação de Medida Protetiva"
    TENTATIVA_SUICIDIO = "Tentativa de Suicídio"
    MAUS_TRATOS_ANIMAIS = "Maus-tratos a Animais"
    OUTROS = "Outros"

class StatusBoletim(Enum):
    REGISTRADO = "Registrado"                  
    EM_ANALISE = "Em Análise"                 
    EM_INVESTIGACAO = "Em Investigação"        
    COMPLEMENTADO = "Complementado"            
    ENCAMINHADO = "Encaminhado"               
    SUSPENSO = "Suspenso"                      
    ARQUIVADO = "Arquivado"                    
    CONCLUIDO = "Concluído"                    
    CANCELADO = "Cancelado"                   
    AGUARDANDO_VALIDACAO = "Aguardando Validação"
    REABERTO = "Reaberto"

class BoletimOcorrencia(Document):
    data_registro: date
    tipo_ocorrencia: TipoOcorrencia
    status: StatusBoletim
    
    autor: Link[Autor] 
    declarantes: List[Link[Declarante]] = [] 
    

    class Settings:
        name = "boletins"
        indexes = [
            [("tipo_ocorrencia", "text")]
        ]

