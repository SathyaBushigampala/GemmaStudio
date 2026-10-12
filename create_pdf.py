"""
Generate GemmaStudio_Complete_User_Guide.pdf using ReportLab.
Exhaustive user guide and deep comparison with current AI solutions.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that computes total pages for 'Page X of Y' footers."""
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

        # Running header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "GemmaStudio | Complete User Manual & AI Comparative Analysis")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running footer
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * 72 - 54, 36, page_str)
        self.drawString(54, 36, "MLH & Google 'Build with Gemma' Project - Confidential & Open Source")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 8.5 * 72 - 54, 46)

        self.restoreState()


def build_pdf(filename="GemmaStudio_Complete_User_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1e40af")   # Deep Blue
    secondary_color = colors.HexColor("#6d28d9") # Purple
    dark_text = colors.HexColor("#0f172a")       # Slate 900
    muted_text = colors.HexColor("#475569")      # Slate 600

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=muted_text,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=dark_text,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=body_style,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor("#1e293b"),
        leading=13
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title Block
    story.append(Paragraph("GemmaStudio: Complete User Manual & Comparative Analysis", title_style))
    story.append(Paragraph("Everything You Need to Know: Step-by-Step Operations, Architecture, & How Gemma on Gemini API Differs from Current AI Models", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=15))

    # Executive Summary Callout Box
    summary_html = (
        "<b>EXECUTIVE OVERVIEW:</b> GemmaStudio is an interactive, full-stack AI development cockpit built for "
        "the <b>MLH & Google 'Build with Gemma'</b> challenge. It harnesses Google's hosted <b>Gemma 4</b> models "
        "(<code>gemma-4-26b-a4b-it</code> and <code>gemma-4-31b-it</code>) via the official <code>google-genai</code> SDK, "
        "enabling transparent step-by-step thinking, multimodal vision, system personas, and instant code generation—all "
        "with <b>zero local GPU requirements</b>."
    )
    summary_table = Table([[Paragraph(summary_html, callout_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93c5fd")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # SECTION 1: HOW USERS SHOULD USE THE PROJECT
    story.append(Paragraph("PART 1: Step-by-Step User Operations Guide", h1_style))
    story.append(Paragraph(
        "GemmaStudio was designed with an intuitive, developer-first interface. Follow this detailed "
        "step-by-step guide to utilize every control and capability:",
        body_style
    ))

    steps = [
        ("Step 1: Connecting Your Gemini API Key",
         "When you first load the studio (at <code>http://localhost:5000</code>), look at the bottom-left corner of the sidebar. "
         "If the status dot is yellow (<code>API Key Missing</code>), click the <b>Settings (Gear ⚙️)</b> icon. Enter your free API key "
         "from Google AI Studio (<code>aistudio.google.com/apikey</code>). You can check <i>'Save to local .env file'</i> so your key "
         "persists automatically across server restarts. Click <b>Save Key</b> to activate full model access."),

        ("Step 2: Selecting the Gemma 4 Model",
         "In the sidebar under <b>MODEL</b>, use the dropdown to choose your desired engine:<br/>"
         "• <b>Gemma 4 26B (a4b)</b> [<code>gemma-4-26b-a4b-it</code>]: Mixture-of-Experts (MoE) architecture. It activates only ~4B "
         "parameters per token, giving lightning-fast responses while retaining 26B parameter reasoning quality. Recommended for 90% of tasks.<br/>"
         "• <b>Gemma 4 31B</b> [<code>gemma-4-31b-it</code>]: Dense reasoning model. Contains 31B active parameters, optimized for deep "
         "mathematical proofs, algorithmic logic, and difficult competitive programming questions."),

        ("Step 3: Toggling Thinking Mode (Chain-of-Thought)",
         "Under <b>THINKING MODE</b>, choose between two levels:<br/>"
         "• <b>High Reasoning</b> (<code>thinking_level='high'</code>): Gemma runs an internal thought process before producing the response. "
         "GemmaStudio intercepts this reasoning stream and places it into an interactive purple collapsible box above the answer.<br/>"
         "• <b>Minimal</b> (<code>thinking_level='minimal'</code>): Disables chain-of-thought overhead for instant, concise outputs."),

        ("Step 4: Setting System Personas & Behavioral Constraints",
         "Under <b>SYSTEM PERSONA</b>, choose how Gemma should behave:<br/>"
         "• <b>Default Helpful Assistant</b>: Standard direct answers.<br/>"
         "• <b>Kyoto Tea Master</b>: Calms responses with nature metaphors in under 3 sentences (featured in Google's official tutorial).<br/>"
         "• <b>Senior Code Architect</b>: Delivers clean architectural code with Big-O time and space complexity analysis.<br/>"
         "• <b>Algorithmic Math & Proofs Tutor</b>: Methodical step-by-step mathematical proofs.<br/>"
         "• <b>Custom Persona</b>: Write your own explicit instructions directly in the text area."),

        ("Step 5: Multimodal Image Understanding (Vision)",
         "Gemma 4 is fully multimodal. You can upload an image in three easy ways:<br/>"
         "1. Click the <b>Paperclip (📎)</b> attachment button to browse for an image file.<br/>"
         "2. <b>Drag and drop</b> any image (PNG, JPG, WebP) directly onto the chat input box.<br/>"
         "3. <b>Paste from Clipboard</b>: Take a screenshot (Windows: <code>Win + Shift + S</code>) and press <code>Ctrl + V</code> in the input bar!<br/>"
         "Gemma will analyze diagrams, charts, UI screenshots, or handwritten notes alongside your text prompt."),

        ("Step 6: Inspecting the Internal Thinking Process",
         "When a response arrives with Thinking Mode enabled, click on the purple <b>'🧠 Gemma's Internal Thinking Process'</b> bar. "
         "This reveals the step-by-step reasoning steps the model took to deduce the answer before writing the response."),

        ("Step 7: Generating Production Code Snippets",
         "Click the <b>Code Snippet (&lt;/&gt;)</b> icon in the footer. A modal pops up showing the exact, executable code required "
         "to reproduce your current prompt, persona, and thinking configuration in <b>Python</b> (<code>google-genai</code>), "
         "<b>JavaScript/Node.js</b> (<code>@google/genai</code>), and <b>cURL (REST)</b>. Click <b>Copy</b> to paste it into your production codebase!"),

        ("Step 8: Exporting Conversation Transcripts",
         "Click the <b>Download (📥)</b> button in the footer to download the entire multi-turn conversation, timestamps, model metadata, "
         "and responses formatted as a GitHub-ready Markdown document."),

        ("Step 9: Starting a New Session",
         "Click the <b>+ New Session</b> button at the top of the sidebar anytime to clear chat history and reset your context window.")
    ]

    for title, desc in steps:
        step_p = Paragraph(f"<b>{title}</b>", h2_style)
        desc_p = Paragraph(desc, body_style)
        story.append(step_p)
        story.append(desc_p)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # SECTION 2: HOW GEMMA ON GEMINI API DIFFERS FROM PRESENT AI
    story.append(Paragraph("PART 2: How GemmaStudio Differs from Present AI", h1_style))
    story.append(Paragraph(
        "To understand what makes this project significant, we must compare it with existing AI paradigms: "
        "<b>Proprietary AI APIs (OpenAI/Anthropic)</b>, <b>Local AI (Ollama/LM Studio)</b>, and <b>Standard Cloud LLMs (Gemini Pro/Claude)</b>.",
        body_style
    ))

    # Comprehensive Comparison Table
    table_data = [
        [
            Paragraph("<b>Dimension</b>", body_bold),
            Paragraph("<b>GemmaStudio (This Project)</b>", body_bold),
            Paragraph("<b>Proprietary AI (ChatGPT / Claude)</b>", body_bold),
            Paragraph("<b>Local AI (Ollama / LM Studio)</b>", body_bold)
        ],
        [
            Paragraph("<b>Model Openness</b>", body_style),
            Paragraph("<b>Open Weights:</b> Inspectable, open weights developed by Google DeepMind.", body_style),
            Paragraph("<b>Closed Black-Box:</b> Proprietary weights; zero insight into architecture.", body_style),
            Paragraph("<b>Open Weights:</b> Downloaded and executed locally.", body_style)
        ],
        [
            Paragraph("<b>Hardware Needed</b>", body_style),
            Paragraph("<b>Zero GPU:</b> Runs on any standard laptop/PC. Google handles compute.", body_style),
            Paragraph("<b>Zero GPU:</b> Cloud hosted by OpenAI / Anthropic.", body_style),
            Paragraph("<b>Heavy GPU Required:</b> Requires 16GB-64GB VRAM GPU ($1,500+).", body_style)
        ],
        [
            Paragraph("<b>Reasoning Transparency</b>", body_style),
            Paragraph("<b>Direct Thinking Stream:</b> User can inspect internal reasoning steps via accordion.", body_style),
            Paragraph("<b>Hidden / Opaque:</b> Thought process is hidden or strictly sanitized.", body_style),
            Paragraph("<b>Varies:</b> Requires manual prompt crafting; often lacks native thinking support.", body_style)
        ],
        [
            Paragraph("<b>Architecture Efficiency</b>", body_style),
            Paragraph("<b>Mixture-of-Experts (MoE):</b> 26B total parameters with only 4B active per token for speed.", body_style),
            Paragraph("<b>Monolithic:</b> Unknown parameter allocation and high latency.", body_style),
            Paragraph("<b>Heavy Quantization:</b> Often forced to run heavily compressed 4-bit 7B models.", body_style)
        ],
        [
            Paragraph("<b>Developer Portability</b>", body_style),
            Paragraph("<b>Instant Code Generator:</b> Exports Python, JS, and cURL snippets in 1 click.", body_style),
            Paragraph("<b>Vendor Lock-in:</b> Tied to proprietary APIs and platform rate limits.", body_style),
            Paragraph("<b>Complex Integration:</b> Requires managing local daemon processes and ports.", body_style)
        ],
        [
            Paragraph("<b>Setup Time</b>", body_style),
            Paragraph("<b>&lt; 60 Seconds:</b> Double-click <code>run.bat</code>, paste free API key, done.", body_style),
            Paragraph("<b>Minutes:</b> Web browser sign up, but locked to web chat without API dev setup.", body_style),
            Paragraph("<b>Hours:</b> Gigabytes of weight downloads, driver conflicts, CUDA errors.", body_style)
        ]
    ]

    comp_table = Table(table_data, colWidths=[90, 140, 137, 137])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 14))

    # Deep Dive Points
    story.append(Paragraph("Key Differentiators in Detail:", h2_style))

    differentiators = [
        ("1. Democratized Access to Frontier Open Weights",
         "Historically, developers who wanted to experiment with open models like Gemma had to buy expensive high-VRAM "
         "NVIDIA graphics cards or spend hundreds of dollars provisioning cloud GPUs on AWS/GCP. Gemma on Gemini API breaks "
         "this barrier: you get access to <b>26B MoE and 31B Dense models</b> hosted at scale by Google with no hardware investment."),

        ("2. MoE Active Parameter Efficiency (a4b)",
         "Most AI systems run either full dense models (slow and power-hungry) or tiny quantized models (loss of accuracy). "
         "The <code>gemma-4-26b-a4b-it</code> model uses <b>Mixture-of-Experts</b>: while it holds 26 Billion parameters of knowledge, "
         "its routing network activates only <b>4 Billion parameters per token</b>. This gives it the raw intelligence of a massive model "
         "at the generation latency and throughput of a compact 4B model."),

        ("3. Visible Step-by-Step Reasoning Without Paywalls",
         "Leading commercial models (such as OpenAI o1 or Claude 3.5 Sonnet) hide or sanitize their reasoning steps behind high paywalls. "
         "GemmaStudio exposes Gemma's authentic internal reasoning stream in an interactive accordion, making it an invaluable "
         "educational and debugging tool for researchers, educators, and software engineers."),

        ("4. Seamless Developer Onboarding & Code Export",
         "Unlike consumer chat apps (like ChatGPT or Copilot) that trap conversations in a browser silo, GemmaStudio is a "
         "<b>developer cockpit</b>. Any configuration tested in the UI—whether vision inputs, personas, or thinking modes—can be "
         "immediately exported as working Python (<code>google-genai</code>), JavaScript (<code>@google/genai</code>), or cURL commands.")
    ]

    for d_title, d_desc in differentiators:
        story.append(Paragraph(f"<b>{d_title}</b>", body_bold))
        story.append(Paragraph(d_desc, body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # SECTION 3: SYSTEM ARCHITECTURE & CODE SNIPPET
    story.append(Paragraph("PART 3: Core API Integration Sample", h1_style))
    story.append(Paragraph(
        "Here is the exact production Python code that powers GemmaStudio under the hood:",
        body_style
    ))

    code_snippet = (
        "from google import genai\n"
        "from google.genai import types\n\n"
        "# 1. Initialize client with API key\n"
        "client = genai.Client(api_key='GEMINI_API_KEY')\n\n"
        "# 2. Configure thinking mode and system persona\n"
        "config = types.GenerateContentConfig(\n"
        "    thinking_config=types.ThinkingConfig(thinking_level='high'),\n"
        "    system_instruction='You are a wise Kyoto tea master. Speak calmly and poetically.'\n"
        ")\n\n"
        "# 3. Execute generation on Gemma 4 MoE model\n"
        "response = client.models.generate_content(\n"
        "    model='gemma-4-26b-a4b-it',\n"
        "    contents='What is the inner spiritual purpose of the tea ceremony?',\n"
        "    config=config\n"
        ")\n\n"
        "# 4. Access final text and thinking process\n"
        "print('Response:', response.text)\n"
    )

    code_table = Table([[Paragraph(f"<pre>{code_snippet}</pre>", code_style)]], colWidths=[504])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(code_table)
    story.append(Spacer(1, 14))

    # SECTION 4: HACKTOBERFEST SUBMISSION SUMMARY
    story.append(Paragraph("PART 4: Hacktoberfest & MLH Challenge Summary", h1_style))
    summary_bullets = [
        "<b>Track:</b> Build with Gemma on Google Gemini API.",
        "<b>Primary Technologies:</b> Python 3.14, Flask, Google GenAI SDK (<code>google-genai</code> v2.29), HTML5, CSS3 Glassmorphism, JavaScript ES6+.",
        "<b>Zero-GPU Portability:</b> Complete accessibility for any user without expensive hardware.",
        "<b>Educational Impact:</b> Transparent thinking process inspection for algorithmic learning.",
        "<b>License:</b> Open Source under the MIT License."
    ]
    for b in summary_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf("c:\\Users\\sathy\\OneDrive\\Documents\\Hacktoberfest\\GemmaStudio_Complete_User_Guide.pdf")
