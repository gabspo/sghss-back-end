#!/usr/bin/env python3
"""
Script para gerar diagrama DER em PNG e PDF
Requer: graphviz e pydot instalados
Instalar: pip install graphviz pydot
"""

import sys
from pathlib import Path

try:
    import pydot
except ImportError:
    print("❌ Erro: pydot não está instalado")
    print("Execute: pip install pydot")
    sys.exit(1)

# Definir o schema do banco de dados
DER_DOT = """
digraph SGHSS {
    rankdir=LR;
    splines=ortho;
    nodesep=2;
    
    // Estilos
    node [shape=plaintext];
    
    // Tabela: usuarios
    usuarios [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#4CAF50" COLSPAN="2"><B>usuarios</B></TD></TR>
            <TR><TD>id</TD><TD>int (PK)</TD></TR>
            <TR><TD>nome</TD><TD>varchar(255)</TD></TR>
            <TR><TD>email</TD><TD>varchar(255) UNIQUE</TD></TR>
            <TR><TD>senha</TD><TD>varchar(255)</TD></TR>
            <TR><TD>tipo</TD><TD>enum</TD></TR>
            <TR><TD>ativo</TD><TD>boolean</TD></TR>
            <TR><TD>criado_em</TD><TD>timestamp</TD></TR>
            <TR><TD>atualizado_em</TD><TD>timestamp</TD></TR>
        </TABLE>
    >];
    
    // Tabela: pacientes
    pacientes [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#2196F3" COLSPAN="2"><B>pacientes</B></TD></TR>
            <TR><TD>id</TD><TD>int (PK)</TD></TR>
            <TR><TD>usuario_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>cpf</TD><TD>varchar(14) UNIQUE</TD></TR>
            <TR><TD>data_nascimento</TD><TD>date</TD></TR>
            <TR><TD>telefone</TD><TD>varchar(20)</TD></TR>
            <TR><TD>endereco</TD><TD>varchar(500)</TD></TR>
            <TR><TD>cidade</TD><TD>varchar(100)</TD></TR>
            <TR><TD>estado</TD><TD>varchar(2)</TD></TR>
            <TR><TD>cep</TD><TD>varchar(9)</TD></TR>
            <TR><TD>condicoes_medicas</TD><TD>text</TD></TR>
            <TR><TD>alergias</TD><TD>text</TD></TR>
            <TR><TD>criado_em</TD><TD>timestamp</TD></TR>
            <TR><TD>atualizado_em</TD><TD>timestamp</TD></TR>
        </TABLE>
    >];
    
    // Tabela: profissionais
    profissionais [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#FF9800" COLSPAN="2"><B>profissionais</B></TD></TR>
            <TR><TD>id</TD><TD>int (PK)</TD></TR>
            <TR><TD>usuario_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>crm</TD><TD>varchar(20) UNIQUE</TD></TR>
            <TR><TD>especialidade</TD><TD>varchar(100)</TD></TR>
            <TR><TD>telefone_comercial</TD><TD>varchar(20)</TD></TR>
            <TR><TD>endereco_consultorio</TD><TD>varchar(500)</TD></TR>
            <TR><TD>cidade</TD><TD>varchar(100)</TD></TR>
            <TR><TD>estado</TD><TD>varchar(2)</TD></TR>
            <TR><TD>cep</TD><TD>varchar(9)</TD></TR>
            <TR><TD>horario_inicio</TD><TD>time</TD></TR>
            <TR><TD>horario_fim</TD><TD>time</TD></TR>
            <TR><TD>dias_atendimento</TD><TD>varchar(100)</TD></TR>
            <TR><TD>biografia</TD><TD>text</TD></TR>
            <TR><TD>criado_em</TD><TD>timestamp</TD></TR>
            <TR><TD>atualizado_em</TD><TD>timestamp</TD></TR>
        </TABLE>
    >];
    
    // Tabela: medicamentos
    medicamentos [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#9C27B0" COLSPAN="2"><B>medicamentos</B></TD></TR>
            <TR><TD>id</TD><TD>int (PK)</TD></TR>
            <TR><TD>nome</TD><TD>varchar(255)</TD></TR>
            <TR><TD>principio_ativo</TD><TD>varchar(255)</TD></TR>
            <TR><TD>fabricante</TD><TD>varchar(255)</TD></TR>
            <TR><TD>dosagem</TD><TD>varchar(100)</TD></TR>
            <TR><TD>forma_farmaceutica</TD><TD>varchar(100)</TD></TR>
            <TR><TD>lote</TD><TD>varchar(50)</TD></TR>
            <TR><TD>validade</TD><TD>date</TD></TR>
            <TR><TD>preco</TD><TD>decimal(10,2)</TD></TR>
            <TR><TD>estoque</TD><TD>int</TD></TR>
            <TR><TD>descricao</TD><TD>text</TD></TR>
            <TR><TD>contraindicacoes</TD><TD>text</TD></TR>
            <TR><TD>criado_em</TD><TD>timestamp</TD></TR>
            <TR><TD>atualizado_em</TD><TD>timestamp</TD></TR>
        </TABLE>
    >];
    
    // Tabela: consultas
    consultas [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#F44336" COLSPAN="2"><B>consultas</B></TD></TR>
            <TR><TD>id</TD><TD>int (PK)</TD></TR>
            <TR><TD>paciente_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>profissional_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>tipo</TD><TD>enum</TD></TR>
            <TR><TD>data_hora</TD><TD>datetime</TD></TR>
            <TR><TD>duracao_minutos</TD><TD>int</TD></TR>
            <TR><TD>motivo_consulta</TD><TD>varchar(500)</TD></TR>
            <TR><TD>sintomas</TD><TD>text</TD></TR>
            <TR><TD>diagnostico</TD><TD>text</TD></TR>
            <TR><TD>observacoes</TD><TD>text</TD></TR>
            <TR><TD>link_video</TD><TD>varchar(500)</TD></TR>
            <TR><TD>status</TD><TD>enum</TD></TR>
            <TR><TD>criado_em</TD><TD>timestamp</TD></TR>
            <TR><TD>atualizado_em</TD><TD>timestamp</TD></TR>
        </TABLE>
    >];
    
    // Tabela: prescricoes
    prescricoes [label=<
        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#00BCD4" COLSPAN="2"><B>prescricoes</B></TD></TR>
            <TR><TD>id</TD><TD>int (PK)</TD></TR>
            <TR><TD>consulta_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>medicamento_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>profissional_id</TD><TD>int (FK)</TD></TR>
            <TR><TD>dosagem</TD><TD>varchar(100)</TD></TR>
            <TR><TD>frequencia</TD><TD>varchar(100)</TD></TR>
            <TR><TD>duracao_dias</TD><TD>int</TD></TR>
            <TR><TD>data_inicio</TD><TD>date</TD></TR>
            <TR><TD>data_fim</TD><TD>date</TD></TR>
            <TR><TD>instrucoes_uso</TD><TD>text</TD></TR>
            <TR><TD>observacoes</TD><TD>text</TD></TR>
            <TR><TD>ativa</TD><TD>boolean</TD></TR>
            <TR><TD>criado_em</TD><TD>timestamp</TD></TR>
            <TR><TD>atualizado_em</TD><TD>timestamp</TD></TR>
        </TABLE>
    >];
    
    // Relacionamentos
    pacientes -> usuarios [label="1:1"];
    profissionais -> usuarios [label="1:1"];
    consultas -> pacientes [label="1:N"];
    consultas -> profissionais [label="1:N"];
    prescricoes -> consultas [label="1:N"];
    prescricoes -> medicamentos [label="1:N"];
    prescricoes -> profissionais [label="N:1"];
}
"""

def main():
    print("🔄 Gerando DER em PNG e PDF...")
    
    try:
        # Criar grafo
        graphs = pydot.graph_from_dot_data(DER_DOT)
        graph = graphs[0]
        
        # Caminhos de saída
        png_path = Path("DER_SGHSS.png")
        pdf_path = Path("DER_SGHSS.pdf")
        
        # Gerar PNG
        print(f"📝 Gerando PNG: {png_path}")
        graph.write_png(str(png_path))
        print(f"✅ PNG gerado com sucesso: {png_path}")
        
        # Gerar PDF
        print(f"📝 Gerando PDF: {pdf_path}")
        graph.write_pdf(str(pdf_path))
        print(f"✅ PDF gerado com sucesso: {pdf_path}")
        
        print("\n✨ DER gerado com sucesso!")
        print(f"📍 Arquivos criados:")
        print(f"   - {png_path.absolute()}")
        print(f"   - {pdf_path.absolute()}")
        
    except Exception as e:
        print(f"❌ Erro ao gerar DER: {e}")
        print("\nVerifique se você tem graphviz instalado:")
        print("  Windows: choco install graphviz")
        print("  macOS: brew install graphviz")
        print("  Linux: sudo apt-get install graphviz")
        sys.exit(1)

if __name__ == "__main__":
    main()
