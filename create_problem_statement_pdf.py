"""
Generate GemmaStudio_Problem_Statement_and_Solution.pdf using ReportLab.
Includes Problem Statement, How It Was Built, and Open Source Tools Used.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))

        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "GemmaStudio | Problem Statement, Methodology & Open Source Stack")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * 72 - 54, 36, page_str)
        self.drawString(54, 36, "Hacktoberfest / Google DeepMind: Best Use of Gemma 4 Track")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * 72 - 54, 46)

        self.restoreState()


def build_problem_solution_pdf(filename="GemmaStudio_Problem_Statement_and_Solution.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1e3a8a")   # Navy / Blue 900
    accent_color = colors.HexColor("#2563eb")    # Blue 600
    purple_accent = colors.HexColor("#7c3aed")   # Purple 600
    dark_text = colors.HexColor("#0f172a")       # Slate 900
    muted_text = colors.HexColor("#475569")      # Slate 600

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=muted_text,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=purple_accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.5,
        textColor=dark_text,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    callout_style = ParagraphStyle(
        'Callout_Style',
        parent=body_style,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor("#1e293b"),
        leading=13
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("GemmaStudio: Problem Statement, Methodology & Open Source Stack", title_style))
    story.append(Paragraph("Official Hackathon Project Submission for 'Best Use of Gemma 4' (Google DeepMind Track)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=12))

    # Abstract Callout Box
    abstract_text = (
        "<b>PROJECT ESSENCE:</b> This document outlines the formal problem statement addressed by "
        "<b>GemmaStudio</b>, the technical methodology employed to solve it, and the full catalog of "
        "open-source technologies utilized. GemmaStudio democratizes frontier open-weights AI by bridging "
        "Google's Gemma 4 models on the Gemini API with a zero-friction developer cockpit featuring visible reasoning, "
        "multimodal vision, and instant multi-language code generation."
    )
    abstract_table = Table([[Paragraph(abstract_text, callout_style)]], colWidths=[504])
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#bfdbfe")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 10))

    # SECTION 1: PROBLEM STATEMENT
    story.append(Paragraph("1. The Problem Statement", h1_style))
    story.append(Paragraph(
        "While open-weights AI models have made tremendous strides, their practical adoption by everyday developers, "
        "students, and researchers faces four critical barriers:",
        body_style
    ))

    problems = [
        ("Problem 1: The Massive Hardware & GPU Barrier",
         "Frontier open models like Gemma 4 come in 26-Billion and 31-Billion parameter sizes. Running these models locally "
         "requires enterprise-grade GPUs (e.g., NVIDIA RTX 4090 or A100 with 24GB-80GB VRAM) costing upwards of $1,500-$10,000. "
         "Students, indie hackers, and developers on standard consumer laptops are completely locked out of experimenting with "
         "state-of-the-art open models."),

        ("Problem 2: The 'Black-Box' Reasoning Dilemma",
         "Modern reasoning models (such as OpenAI o1 or proprietary chat systems) perform internal chain-of-thought thinking, "
         "but their actual thought steps are hidden, sanitized, or placed behind expensive subscription paywalls. Developers and "
         "educators cannot inspect how the model deconstructs algorithms, logic puzzles, or mathematical proofs."),

        ("Problem 3: The Gap Between Web Chatting & Software Engineering",
         "Consumer chat interfaces allow users to ask questions, but they do not help developers integrate AI into real software. "
         "When an engineer tests a prompt, vision input, or persona that works well, they still have to manually research the SDK, "
         "read documentation, and write boilerplate code in Python or JavaScript to integrate it."),

        ("Problem 4: Environment & Setup Friction",
         "Setting up local open-weights inference (configuring Ollama, vLLM, HuggingFace transformers, CUDA drivers, and Python virtual environments) "
         "often takes hours and frequently fails due to OS-specific dependency conflicts, discouraging developers from ever building.")
    ]

    for p_title, p_desc in problems:
        story.append(Paragraph(f"• <b>{p_title}</b>", body_bold))
        story.append(Paragraph(p_desc, body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 8))

    # SECTION 2: HOW WE WORKED ON IT (METHODOLOGY & SOLUTION)
    story.append(Paragraph("2. How We Worked on It (The Technical Solution)", h1_style))
    story.append(Paragraph(
        "To solve these four challenges, we designed and built <b>GemmaStudio</b> as a full-stack, "
        "developer-first cockpit following Google's official <i>'Run Gemma with the Gemini API'</i> specification:",
        body_style
    ))

    solutions = [
        ("A. Hosted Gemma 4 Inference with Zero Hardware Overhead",
         "Rather than demanding local GPUs, GemmaStudio connects directly to Google's hosted infrastructure via the Gemini API "
         "using the official <code>google-genai</code> SDK (v2.29). This allows users to run both <b>Gemma 4 26B (a4b MoE)</b> and "
         "<b>Gemma 4 31B (Dense)</b> on any standard computer with 100% cloud inference acceleration."),

        ("B. Transparent Thinking Stream Parser",
         "We engineered a specialized response extraction pipeline in <code>app.py</code>. When Gemma 4 executes in thinking mode "
         "(<code>thinking_level='high'</code>), our backend separates intermediate <code>part.thought</code> tokens from final text "
         "and renders them inside an interactive, collapsible purple accordion in the UI. Users can visually dissect every reasoning step."),

        ("C. Multimodal Vision Pipeline",
         "We implemented an asynchronous image ingestion system. Users can attach images via file picker, drag-and-drop, or "
         "direct clipboard pasting (<code>Ctrl+V</code>). The client encodes the image into base64 data URIs, which our backend converts "
         "into binary <code>types.Part.from_bytes</code> blobs for multimodal Gemma 4 processing."),

        ("D. 1-Click Multi-Language Code Generator",
         "We built a dynamic code generation engine. Whenever a user configures a prompt, persona, image, or thinking level, "
         "the app dynamically generates production-ready, copy-pasteable snippets in <b>Python</b> (<code>google-genai</code>), "
         "<b>JavaScript / Node.js</b> (<code>@google/genai</code>), and <b>cURL (REST)</b>."),

        ("E. One-Click Zero-Friction Launchers",
         "We automated the setup process with <code>run.bat</code> and <code>run.ps1</code>. A single click automatically validates "
         "dependencies, verifies the Python runtime, and starts the server on <code>localhost:5000</code> in under 10 seconds.")
    ]

    for s_title, s_desc in solutions:
        story.append(Paragraph(f"<b>{s_title}</b>", h2_style))
        story.append(Paragraph(s_desc, body_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # SECTION 3: OPEN SOURCE TECHNOLOGIES USED
    story.append(Paragraph("3. Open Source Stack & Technologies Used", h1_style))
    story.append(Paragraph(
        "GemmaStudio was built exclusively with high-quality open-source libraries, open models, and open web standards:",
        body_style
    ))

    tech_table_data = [
        [
            Paragraph("<b>Component / Library</b>", body_bold),
            Paragraph("<b>Type / License</b>", body_bold),
            Paragraph("<b>Exact Role in Solving the Problem</b>", body_bold)
        ],
        [
            Paragraph("<b>Google Gemma 4</b><br/>(<code>26b-a4b-it</code> & <code>31b-it</code>)", body_style),
            Paragraph("Open-Weights Model<br/>(Gemma Terms)", body_style),
            Paragraph("Provides state-of-the-art open intelligence, multimodal image reasoning, and thinking process.", body_style)
        ],
        [
            Paragraph("<b>google-genai SDK</b><br/>(v2.29.0)", body_style),
            Paragraph("Open Source<br/>(Apache 2.0)", body_style),
            Paragraph("Official unified client library connecting Python to Gemma hosted on Gemini API.", body_style)
        ],
        [
            Paragraph("<b>Python 3.14</b>", body_style),
            Paragraph("Open Source<br/>(PSF License)", body_style),
            Paragraph("Core backend runtime driving server logic, payload serialization, and API calls.", body_style)
        ],
        [
            Paragraph("<b>Flask & Werkzeug</b><br/>(v3.1.3)", body_style),
            Paragraph("Open Source<br/>(BSD-3-Clause)", body_style),
            Paragraph("Lightweight WSGI web server handling REST endpoints, session state, and static assets.", body_style)
        ],
        [
            Paragraph("<b>Marked.js</b>", body_style),
            Paragraph("Open Source<br/>(MIT License)", body_style),
            Paragraph("Client-side markdown compiler rendering headings, lists, tables, and formatted text in chat.", body_style)
        ],
        [
            Paragraph("<b>Highlight.js</b>", body_style),
            Paragraph("Open Source<br/>(BSD-3-Clause)", body_style),
            Paragraph("Performs real-time syntax highlighting on code blocks returned by Gemma across 180+ languages.", body_style)
        ],
        [
            Paragraph("<b>Font Awesome Free</b>", body_style),
            Paragraph("Open Source<br/>(CC BY 4.0 / SIL OFL)", body_style),
            Paragraph("Vector icon library for intuitive UI navigation, badges, buttons, and status indicators.", body_style)
        ],
        [
            Paragraph("<b>Google Fonts</b><br/>(Plus Jakarta Sans & JetBrains Mono)", body_style),
            Paragraph("Open Source<br/>(OFL)", body_style),
            Paragraph("Modern developer typography ensuring clear readability for prose and monospaced code blocks.", body_style)
        ],
        [
            Paragraph("<b>python-dotenv</b>", body_style),
            Paragraph("Open Source<br/>(BSD-3-Clause)", body_style),
            Paragraph("Secures API keys by loading environment variables from local <code>.env</code> files.", body_style)
        ],
        [
            Paragraph("<b>ReportLab</b>", body_style),
            Paragraph("Open Source<br/>(BSD License)", body_style),
            Paragraph("Programmatic document generation engine used to compile high-quality PDF user manuals.", body_style)
        ]
    ]

    tech_table = Table(tech_table_data, colWidths=[120, 100, 284])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 12))

    # SECTION 4: IMPACT & CONCLUSION
    story.append(Paragraph("4. Impact & Alignment with 'Best Use of Gemma 4'", h1_style))
    impact_points = [
        ("Accessibility:", "Enables any student or engineer on any laptop to build with Gemma 4 without buying expensive hardware."),
        ("Transparency:", "Demystifies AI decision-making by making Gemma's internal chain-of-thought visible and inspectable."),
        ("Production Velocity:", "Turns prompt experiments into production code (Python, JS, cURL) in a single click."),
        ("Open-Source Heritage:", "Built entirely with open technologies and open weights, licensed under the MIT License.")
    ]
    for label, desc in impact_points:
        story.append(Paragraph(f"• <b>{label}</b> {desc}", body_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    build_problem_solution_pdf("c:\\Users\\sathy\\OneDrive\\Documents\\Hacktoberfest\\GemmaStudio_Problem_Statement_and_Solution.pdf")
