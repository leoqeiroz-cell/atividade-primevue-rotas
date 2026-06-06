from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "Relatorio_Cloud_Docker_PrimeShop.pdf"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitlePrime",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=20,
        textColor=colors.HexColor("#1F4E79"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="SubPrime",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#444444"),
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="H1Prime",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyPrime",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.9,
        leading=11.2,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallPrime",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=10,
    )
)


def p(text, style="BodyPrime"):
    return Paragraph(text, styles[style])


def h(text):
    return Paragraph(text, styles["H1Prime"])


doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=1.45 * cm,
    leftMargin=1.45 * cm,
    topMargin=1.15 * cm,
    bottomMargin=1.15 * cm,
)

story = [
    Paragraph("Relatorio tecnico - Aplicacao containerizada em nuvem", styles["TitlePrime"]),
    Paragraph("PrimeShop | Docker, PaaS, escalabilidade e responsabilidade compartilhada", styles["SubPrime"]),
]

meta = Table(
    [
        ["Nome completo do aluno", "[inserir nome completo]"],
        ["Projeto", "PrimeShop - vitrine web com area administrativa simulada"],
        ["Modelo de servico", "PaaS - Platform as a Service"],
    ],
    colWidths=[4.3 * cm, 12.2 * cm],
)
meta.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D9EAF7")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F4E79")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.4),
            ("LEADING", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#AFC9DB")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)
story += [meta, Spacer(1, 6)]

sections = [
    (
        "1. Apresentacao do projeto",
        [
            "Este projeto simula a entrega de uma aplicacao web para um cliente que precisa de uma solucao segura, escalavel, hospedada em nuvem e baseada em containers. A aplicacao escolhida foi a PrimeShop, uma loja demonstrativa em Vue 3 com vitrine de produtos, carrinho, checkout protegido por login simulado e area administrativa restrita ao perfil de administrador.",
            "A proposta aproxima a atividade de um cenario real: a equipe entrega uma aplicacao pronta para producao, empacotada em Docker e servida por Nginx, em vez de depender de configuracoes manuais em cada ambiente.",
        ],
    ),
    (
        "2. Modelo de servico escolhido",
        [
            "O modelo escolhido foi PaaS, usando como referencia Azure App Service for Containers, AWS Elastic Beanstalk com Docker ou Google Cloud Run. O PaaS reduz a carga operacional porque a equipe publica a imagem Docker e a plataforma gerenciada cuida de boa parte da execucao, disponibilidade, logs, HTTPS e escalabilidade.",
            "A mesma solucao poderia rodar em IaaS, como uma maquina virtual EC2, mas isso exigiria maior responsabilidade sobre sistema operacional, patches e configuracao do servidor. Para este projeto, PaaS e a opcao mais equilibrada.",
        ],
    ),
    (
        "3. Componentes utilizados",
        [
            "Vue 3, Vite, PrimeVue e Tailwind CSS; Docker; Node.js 20 Alpine na etapa de build; Nginx 1.27 Alpine na etapa de producao; Docker Compose para simular porta, rede isolada e volumes persistentes; volumes para cache e logs do Nginx.",
        ],
    ),
    (
        "4. Preparacao do ambiente com Docker",
        [
            "O Dockerfile usa uma estrategia multi-stage. A primeira etapa instala dependencias e gera o build da aplicacao. A segunda copia apenas os arquivos finais para o Nginx, reduzindo o tamanho da imagem e evitando dependencias de desenvolvimento em producao.",
            "Porta simulada: localhost:8080 -> container:80. Rede Docker: primeshop-net. Volumes persistentes: primeshop-nginx-cache e primeshop-nginx-logs.",
        ],
    ),
]

for title, paragraphs in sections:
    story.append(h(title))
    for text in paragraphs:
        story.append(p(text))

story.append(h("5. Diagrama simplificado da arquitetura"))
diagram_rows = [
    ["Usuario acessa por HTTPS"],
    ["Plataforma PaaS em nuvem recebe a requisicao"],
    ["Servico executa a imagem Docker"],
    ["Container PrimeShop responde pela porta 80"],
    ["Nginx entrega os arquivos estaticos Vue/Vite"],
    ["Rede Docker isolada + volumes de cache e logs"],
]
diagram = Table(diagram_rows, colWidths=[15.8 * cm])
diagram.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF3F8")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9CBBD0")),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#C5D8E5")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.3),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
)
story += [diagram, Spacer(1, 4)]

more_sections = [
    (
        "6. Simulacao de deploy",
        "A estrategia recomendada e automatizada com CI/CD. O pipeline instalaria dependencias, executaria validacoes, geraria o build, construiria a imagem Docker, publicaria em um registry e atualizaria o servico na nuvem. Em uma implantacao na Azure App Service for Containers, a plataforma buscaria a imagem no registry e executaria o container com HTTPS, variaveis de ambiente, monitoramento e possibilidade de aumento de instancias. Para reduzir riscos, o deploy pode ser escalonado: homologacao primeiro, producao depois.",
    ),
    (
        "7. Escalabilidade e elasticidade",
        "A escalabilidade acontece porque o container nao guarda estado interno relevante. Assim, a plataforma pode executar varias instancias identicas atras de um balanceador de carga. A elasticidade complementa esse comportamento: em horarios de pico, a nuvem aumenta recursos ou instancias; quando a demanda diminui, reduz novamente, mantendo disponibilidade sem desperdicar custo com capacidade ociosa.",
    ),
    (
        "8. Seguranca e responsabilidade compartilhada",
        "Na nuvem, a seguranca e compartilhada. O provedor cuida da infraestrutura fisica, rede base, datacenter e parte da plataforma. A equipe do projeto cuida do codigo, imagem Docker, configuracoes, credenciais, permissoes e atualizacoes. Neste projeto foram considerados: imagens oficiais e pequenas, separacao entre build e execucao, publicacao apenas da porta necessaria, healthcheck, logs persistidos e controle de acesso simulado.",
    ),
    (
        "9. Beneficios, desafios e conclusao",
        "Os beneficios principais sao portabilidade, padronizacao, facilidade de deploy e melhor aproveitamento dos recursos da nuvem. Os desafios envolvem manter imagens atualizadas, proteger segredos, observar logs e definir limites de recursos. A solucao atende ao enunciado porque apresenta Dockerfile funcional, porta de acesso, rede, volume persistente, deploy em nuvem e aplicacao dos conceitos de escalabilidade, elasticidade e responsabilidade compartilhada.",
    ),
    (
        "10. Execucao local",
        "Com Docker instalado: docker compose up --build. Acesso: http://localhost:8080. Para parar a aplicacao: docker compose down.",
    ),
]

for title, text in more_sections:
    story.append(h(title))
    story.append(p(text))


def add_page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(19.5 * cm, 0.65 * cm, f"Pagina {document.page}")
    canvas.restoreState()


doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(OUTPUT)
