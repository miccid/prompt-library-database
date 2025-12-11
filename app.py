"""
Prompt Library Manager v2.0
A professional Streamlit application for managing AI prompts with advanced tagging.

Author: Michael Cid
License: MIT
"""

import streamlit as st
import sqlite3
import uuid
import json
import logging
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
import os

# Optional import with fallback
try:
    from st_copy_to_clipboard import st_copy_to_clipboard
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

# =============================================================================
# CONFIGURATION
# =============================================================================

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="Prompt Library Database",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- Database ---
DB_FILE = os.environ.get("PROMPT_DB_FILE", "prompts.db")

# --- Authentication ---
# Set environment variables USERNAME and PASSWORD in .env file
# Or update defaults below for local development
AUTH_USERNAME = os.environ.get("USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("PASSWORD", "admin")


# =============================================================================
# TAG SYSTEM CONFIGURATION v2.0
# =============================================================================
#
# Design Principles:
# 1. Mutually exclusive categories (minimal overlap)
# 2. Collectively exhaustive within each category
# 3. Alphabetical ordering (except Complexity which is hierarchical)
# 4. Consistent naming: lowercase-hyphenated (except proper nouns)
# 5. Single responsibility per category

TAG_CATEGORIES = {

    # === PROMPT METADATA ===

    "Abstraction Level": [
        "framework",
        "meta-prompt",
        "ready-to-use",
        "snippet",
        "template",
    ],

    "Complexity": [
        # Hierarchical order (not alphabetical)
        "basic",
        "simple",
        "intermediate",
        "advanced",
        "expert",
    ],

    "Language": [
        "de-DE",
        "en-GB",
        "en-US",
        "es-ES",
        "fr-FR",
        "nb-NO",
        "sv-SE",
    ],

    # === TASK & PURPOSE ===

    "Task Type": [
        "analysis",
        "automation",
        "brainstorming",
        "classification",
        "code-generation",
        "comparison",
        "conversation",
        "data-extraction",
        "debugging",
        "decision-support",
        "documentation",
        "editing",
        "evaluation",
        "explanation",
        "generation",
        "planning",
        "question-answering",
        "reasoning",
        "refactoring",
        "research",
        "summarization",
        "transformation",
        "translation",
        "validation",
        "writing",
    ],

    "Domain": [
        "agriculture",
        "business",
        "creative",
        "education",
        "engineering",
        "finance",
        "healthcare",
        "legal",
        "manufacturing",
        "marketing",
        "media",
        "non-profit",
        "real-estate",
        "retail",
        "sales",
        "science",
        "security",
        "software",
        "technology",
        "telecommunications",
    ],

    "Function": [
        "administration",
        "business-development",
        "communications",
        "consulting",
        "customer-support",
        "data-analysis",
        "design",
        "devops",
        "executive",
        "finance-accounting",
        "hr",
        "it-operations",
        "legal-compliance",
        "operations",
        "product-management",
        "project-management",
        "quality-assurance",
        "research-development",
        "sales-marketing",
        "strategy",
        "training",
    ],

    "Use Case": [
        "career-development",
        "code-review",
        "content-creation",
        "cover-letter",
        "crm-management",
        "data-pipeline",
        "email-drafting",
        "interview-prep",
        "job-application",
        "knowledge-management",
        "learning",
        "meeting-notes",
        "networking",
        "onboarding",
        "personal-assistant",
        "presentation",
        "process-automation",
        "proposal-writing",
        "report-generation",
        "resume-cv",
        "seo-optimization",
        "social-media",
        "system-design",
        "team-collaboration",
        "technical-writing",
        "time-management",
        "troubleshooting",
        "workflow-automation",
    ],

    # === PROMPTING METHODOLOGY ===

    "Prompt Technique": [
        "chain-of-draft",
        "chain-of-thought",
        "constrained-generation",
        "context-stuffing",
        "fabric-pattern",
        "few-shot",
        "instruction-following",
        "iterative-refinement",
        "least-to-most",
        "mega-prompt",
        "meta-prompting",
        "multi-agent",
        "persona-based",
        "RAG",
        "ReAct",
        "reflexion",
        "role-prompting",
        "self-consistency",
        "self-critique",
        "self-refinement",
        "tree-of-thought",
        "zero-shot",
    ],

    "Prompt Structure": [
        "atomic",
        "conditional",
        "conversational",
        "fabric-pattern",
        "hierarchical",
        "modular",
        "nate-prompt",
        "sequential",
        "system-user-assistant",
        "template-based",
    ],

    # === INPUT & OUTPUT ===

    "Input Type": [
        "audio",
        "code",
        "conversation-history",
        "document",
        "form-data",
        "image",
        "structured-data",
        "text",
        "url",
        "video",
    ],

    "Content Source": [
        "API",
        "blog",
        "book",
        "code-repository",
        "database",
        "documentation",
        "email",
        "general-knowledge",
        "news-article",
        "PDF",
        "podcast",
        "research-paper",
        "RSS-feed",
        "social-media",
        "spreadsheet",
        "transcript",
        "webpage",
        "wiki",
        "YouTube",
    ],

    "Output Format": [
        "bullet-list",
        "checklist",
        "code",
        "CSV",
        "diagram",
        "email",
        "HTML",
        "JSON",
        "JSONL",
        "markdown",
        "numbered-list",
        "plain-text",
        "report",
        "slides",
        "structured-plan",
        "table",
        "XML",
        "YAML",
    ],

    # === STYLE & TONE ===

    "Tone": [
        "assertive",
        "casual",
        "confident",
        "constructive",
        "diplomatic",
        "direct",
        "empathetic",
        "encouraging",
        "enthusiastic",
        "formal",
        "friendly",
        "humorous",
        "inquisitive",
        "neutral",
        "persuasive",
        "professional",
        "supportive",
        "technical",
        "witty",
    ],

    "Audience": [
        "beginner",
        "child",
        "colleague",
        "customer",
        "developer",
        "executive",
        "expert",
        "general-public",
        "investor",
        "manager",
        "non-technical",
        "recruiter",
        "student",
        "technical",
    ],

    # === MODEL & PLATFORM ===

    "Model Family": [
        "Claude",
        "DeepSeek",
        "Gemini",
        "GLM",
        "GPT",
        "Grok",
        "Kimi",
        "Llama",
        "Mistral",
        "Qwen",
        "Stable-Diffusion",
    ],

    "Model": [
        "Claude 3 Haiku",
        "Claude 3 Opus",
        "Claude 3 Sonnet",
        "Claude 3.5 Haiku",
        "Claude 3.5 Sonnet",
        "Claude 4 Opus",
        "Claude 4 Sonnet",
        "Claude 4.5 Haiku",
        "Claude 4.5 Opus",
        "Claude 4.5 Sonnet",
        "DeepSeek-R1",
        "DeepSeek-V3",
        "Gemini 2.0 Flash",
        "Gemini 2.5 Flash",
        "Gemini 2.5 Pro",
        "GLM-4",
        "GLM-4V",
        "GPT-3.5 Turbo",
        "GPT-4",
        "GPT-4 Turbo",
        "GPT-4.1",
        "GPT-4.1 mini",
        "GPT-4o",
        "GPT-4o mini",
        "GPT-o1",
        "GPT-o1 mini",
        "GPT-o3",
        "GPT-o3 mini",
        "GPT-o4 mini",
        "Grok-2",
        "Grok-3",
        "Kimi K2",
        "Llama 3.1",
        "Llama 3.2",
        "Llama 3.3",
        "Llama 4 Maverick",
        "Llama 4 Scout",
        "Mistral Large",
        "Mistral Medium",
        "Mistral Small",
        "Model-Agnostic",
        "Qwen 2.5",
        "Qwen 3",
        "Stable Diffusion 3.5",
        "Stable Diffusion XL",
    ],

    "Platform": [
        "Anthropic API",
        "AWS Bedrock",
        "Azure OpenAI",
        "Google AI Studio",
        "Google Vertex AI",
        "Groq",
        "Hugging Face",
        "LangChain",
        "LlamaIndex",
        "NotebookLM",
        "Ollama",
        "OpenAI API",
        "OpenRouter",
        "Perplexity",
        "Replicate",
        "Together AI",
    ],

    # === QUALITY & SAFETY ===

    "Safety & Guardrails": [
        "bias-mitigation",
        "content-filtering",
        "ethical-guardrails",
        "factual-grounding",
        "hallucination-prevention",
        "jailbreak-prevention",
        "output-validation",
        "pii-protection",
        "prompt-injection-defense",
        "rate-limiting",
        "source-citation",
        "toxicity-filtering",
        "uncertainty-flagging",
    ],

    "Quality Attributes": [
        "accuracy",
        "actionable",
        "clarity",
        "completeness",
        "conciseness",
        "consistency",
        "creativity",
        "depth",
        "objectivity",
        "originality",
        "relevance",
        "reproducibility",
        "specificity",
        "structured",
    ],

    # === MANAGEMENT ===

    "Status": [
        "archived",
        "deprecated",
        "draft",
        "experimental",
        "production",
        "review",
        "stable",
        "testing",
    ],
}

# Validation rules
REQUIRED_TAGS = ["Task Type", "Complexity", "Abstraction Level"]
SINGLE_VALUE_CATEGORIES = ["Complexity", "Abstraction Level", "Status"]


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class Prompt:
    """Data model for a prompt."""
    id: str
    title: str
    prompt_type: str = "structured"
    use_case: str = ""
    description: str = ""
    usage_notes: str = ""
    version: str = "v1.0"
    persona: str = ""
    context: str = ""
    task: str = ""
    style: str = ""
    variables: str = ""
    instructions: str = ""
    is_favorite: int = 0
    created_at: str = ""
    last_modified: str = ""
    tags: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Prompt":
        """Create Prompt from dictionary."""
        tags = data.pop("tags", {})
        # Filter out keys not in dataclass
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        prompt = cls(**filtered_data)
        prompt.tags = tags
        return prompt

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def get_copy_text(self) -> str:
        """Generate text for clipboard copy."""
        if self.prompt_type == "standard":
            return self.instructions or ""
        
        parts = []
        if self.persona:
            parts.append(f"### PERSONA\n{self.persona}")
        if self.context:
            parts.append(f"### CONTEXT\n{self.context}")
        if self.task:
            parts.append(f"### TASK\n{self.task}")
        if self.style:
            parts.append(f"### STYLE\n{self.style}")
        if self.variables:
            parts.append(f"### VARIABLES\n{self.variables}")
        return "\n\n---\n\n".join(parts)


# =============================================================================
# DATABASE LAYER
# =============================================================================

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database tables."""
    with get_db_connection() as conn:
        c = conn.cursor()
        
        # Main prompts table
        c.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                use_case TEXT DEFAULT '',
                description TEXT DEFAULT '',
                usage_notes TEXT DEFAULT '',
                version TEXT DEFAULT 'v1.0',
                created_at TEXT NOT NULL,
                last_modified TEXT NOT NULL,
                is_favorite INTEGER DEFAULT 0,
                prompt_type TEXT DEFAULT 'structured',
                instructions TEXT DEFAULT '',
                persona TEXT DEFAULT '',
                context TEXT DEFAULT '',
                task TEXT DEFAULT '',
                style TEXT DEFAULT '',
                variables TEXT DEFAULT ''
            )
        """)
        
        # Tags table
        c.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                UNIQUE(name, category)
            )
        """)
        
        # Prompt-Tags link table
        c.execute("""
            CREATE TABLE IF NOT EXISTS prompt_tags (
                prompt_id TEXT NOT NULL,
                tag_id INTEGER NOT NULL,
                PRIMARY KEY (prompt_id, tag_id),
                FOREIGN KEY (prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better performance
        c.execute("CREATE INDEX IF NOT EXISTS idx_prompts_title ON prompts(title)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_prompts_favorite ON prompts(is_favorite)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_tags_category ON tags(category)")
        
        logger.info("Database initialized successfully")


class PromptRepository:
    """Repository pattern for prompt data access."""

    @staticmethod
    def get_all() -> List[Prompt]:
        """Load all prompts with their tags."""
        with get_db_connection() as conn:
            c = conn.cursor()
            rows = c.execute("SELECT * FROM prompts ORDER BY title").fetchall()
            
            prompts = []
            for row in rows:
                prompt_dict = dict(row)
                
                # Load tags
                tags = c.execute("""
                    SELECT t.name, t.category FROM tags t
                    JOIN prompt_tags pt ON t.id = pt.tag_id
                    WHERE pt.prompt_id = ?
                """, (prompt_dict['id'],)).fetchall()
                
                prompt_dict['tags'] = {}
                for tag in tags:
                    category = tag['category']
                    if category not in prompt_dict['tags']:
                        prompt_dict['tags'][category] = []
                    prompt_dict['tags'][category].append(tag['name'])
                
                prompts.append(Prompt.from_dict(prompt_dict))
            
            return prompts

    @staticmethod
    def get_by_id(prompt_id: str) -> Optional[Prompt]:
        """Get a single prompt by ID."""
        with get_db_connection() as conn:
            c = conn.cursor()
            row = c.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,)).fetchone()
            
            if not row:
                return None
            
            prompt_dict = dict(row)
            
            # Load tags
            tags = c.execute("""
                SELECT t.name, t.category FROM tags t
                JOIN prompt_tags pt ON t.id = pt.tag_id
                WHERE pt.prompt_id = ?
            """, (prompt_dict['id'],)).fetchall()
            
            prompt_dict['tags'] = {}
            for tag in tags:
                category = tag['category']
                if category not in prompt_dict['tags']:
                    prompt_dict['tags'][category] = []
                prompt_dict['tags'][category].append(tag['name'])
            
            return Prompt.from_dict(prompt_dict)

    @staticmethod
    def save(prompt: Prompt, tags_data: Dict[str, List[str]]) -> None:
        """Save or update a prompt with tags."""
        with get_db_connection() as conn:
            c = conn.cursor()
            
            current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            
            # Check if exists
            exists = c.execute("SELECT id FROM prompts WHERE id = ?", (prompt.id,)).fetchone()
            
            if exists:
                c.execute("""
                    UPDATE prompts SET 
                        title=?, use_case=?, description=?, usage_notes=?, version=?,
                        persona=?, context=?, task=?, style=?, variables=?,
                        prompt_type=?, instructions=?, last_modified=?
                    WHERE id=?
                """, (
                    prompt.title, prompt.use_case, prompt.description, prompt.usage_notes,
                    prompt.version, prompt.persona, prompt.context, prompt.task,
                    prompt.style, prompt.variables, prompt.prompt_type, prompt.instructions,
                    current_time, prompt.id
                ))
                logger.info(f"Updated prompt: {prompt.title}")
            else:
                c.execute("""
                    INSERT INTO prompts (
                        id, title, use_case, description, usage_notes, version,
                        persona, context, task, style, variables, prompt_type,
                        instructions, is_favorite, created_at, last_modified
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    prompt.id, prompt.title, prompt.use_case, prompt.description,
                    prompt.usage_notes, prompt.version, prompt.persona, prompt.context,
                    prompt.task, prompt.style, prompt.variables, prompt.prompt_type,
                    prompt.instructions, 0, current_time, current_time
                ))
                logger.info(f"Created prompt: {prompt.title}")
            
            # Update tags
            c.execute("DELETE FROM prompt_tags WHERE prompt_id = ?", (prompt.id,))
            
            for category, tags in tags_data.items():
                for tag_name in tags:
                    c.execute(
                        "INSERT OR IGNORE INTO tags (name, category) VALUES (?, ?)",
                        (tag_name, category)
                    )
                    tag_id = c.execute(
                        "SELECT id FROM tags WHERE name = ? AND category = ?",
                        (tag_name, category)
                    ).fetchone()[0]
                    c.execute(
                        "INSERT INTO prompt_tags (prompt_id, tag_id) VALUES (?, ?)",
                        (prompt.id, tag_id)
                    )

    @staticmethod
    def delete(prompt_id: str) -> bool:
        """Delete a prompt."""
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM prompt_tags WHERE prompt_id = ?", (prompt_id,))
            c.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            logger.info(f"Deleted prompt: {prompt_id}")
            return True

    @staticmethod
    def toggle_favorite(prompt_id: str, current_status: int) -> None:
        """Toggle favorite status."""
        with get_db_connection() as conn:
            c = conn.cursor()
            new_status = 0 if current_status else 1
            c.execute(
                "UPDATE prompts SET is_favorite = ? WHERE id = ?",
                (new_status, prompt_id)
            )

    @staticmethod
    def duplicate(prompt_id: str) -> Optional[str]:
        """Duplicate a prompt and return new ID."""
        original = PromptRepository.get_by_id(prompt_id)
        if not original:
            return None
        
        new_id = str(uuid.uuid4())
        original.id = new_id
        original.title = f"{original.title} (Copy)"
        original.created_at = ""
        original.last_modified = ""
        original.is_favorite = 0
        
        PromptRepository.save(original, original.tags)
        logger.info(f"Duplicated prompt {prompt_id} to {new_id}")
        return new_id

    @staticmethod
    def export_all() -> str:
        """Export all prompts as JSON."""
        prompts = PromptRepository.get_all()
        data = [p.to_dict() for p in prompts]
        return json.dumps(data, indent=2)

    @staticmethod
    def import_from_json(json_str: str) -> int:
        """Import prompts from JSON. Returns count of imported prompts."""
        data = json.loads(json_str)
        count = 0
        
        for item in data:
            tags = item.pop('tags', {})
            # Generate new ID to avoid conflicts
            item['id'] = str(uuid.uuid4())
            prompt = Prompt.from_dict(item)
            PromptRepository.save(prompt, tags)
            count += 1
        
        logger.info(f"Imported {count} prompts")
        return count


def get_all_tags_by_category() -> Dict[str, List[str]]:
    """Get all tags organized by category, including custom tags from DB."""
    categorized_tags = {cat: list(tags) for cat, tags in TAG_CATEGORIES.items()}
    
    with get_db_connection() as conn:
        c = conn.cursor()
        db_tags = c.execute("SELECT name, category FROM tags ORDER BY name").fetchall()
        
        for tag in db_tags:
            name, category = tag['name'], tag['category']
            if category in categorized_tags and name not in categorized_tags[category]:
                categorized_tags[category].append(name)
    
    # Sort all tag lists
    for category in categorized_tags:
        if category != "Complexity":  # Keep Complexity in hierarchical order
            categorized_tags[category].sort()
    
    return categorized_tags


# =============================================================================
# AUTHENTICATION
# =============================================================================

def check_login() -> bool:
    """Handle login flow. Returns True if authenticated."""
    if st.session_state.get('logged_in'):
        return True
    
    st.title("🔐 Login to Prompt Library Database")
    st.markdown("---")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("Log In", use_container_width=True, type="primary")
        
        if submitted:
            if username == AUTH_USERNAME and password == AUTH_PASSWORD:
                st.session_state['logged_in'] = True
                logger.info(f"User logged in: {username}")
                st.rerun()
            else:
                st.error("❌ Incorrect username or password")
                logger.warning(f"Failed login attempt for: {username}")
    
    return False


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.title("💎 Prompt Library Database")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🔎 Browse Library", use_container_width=True):
            st.session_state.page = 'library'
            st.session_state.selected_prompt_id = None
            st.rerun()
        
        if st.button("✅ Add New Prompt", use_container_width=True):
            st.session_state.page = 'edit'
            st.session_state.selected_prompt_id = None
            st.rerun()
        
        st.markdown("---")
        
        # Export/Import section
        with st.expander("📦 Import / Export"):
            if st.button("📥 Export All Prompts", use_container_width=True):
                export_data = PromptRepository.export_all()
                st.download_button(
                    label="⬇️ Download JSON",
                    data=export_data,
                    file_name=f"prompts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            uploaded_file = st.file_uploader(
                "📤 Import from JSON",
                type=['json'],
                key="import_file"
            )
            if uploaded_file and st.button("Import", use_container_width=True):
                try:
                    content = uploaded_file.read().decode('utf-8')
                    count = PromptRepository.import_from_json(content)
                    st.success(f"✅ Imported {count} prompts!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Import failed: {e}")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state['logged_in'] = False
            logger.info("User logged out")
            st.rerun()
        
        # Info
        st.info("A professional library for structured and standard prompts with advanced tagging.")
        
        # Optional image
        image_path = Path("extract_wisdom.jpg")
        if image_path.is_file():
            st.image(str(image_path), use_container_width=True)


def render_tag_filters(all_tags_by_cat: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Render tag filter UI and return selected tags."""
    selected_tags = {}
    
    with st.expander("🏷️ Advanced Tag Filtering", expanded=False):
        # Group categories for better UX
        tab_names = ["Task & Domain", "Technique & Format", "Model & Platform", "Quality & Management"]
        tabs = st.tabs(tab_names)
        
        category_groups = {
            "Task & Domain": ["Task Type", "Domain", "Function", "Use Case"],
            "Technique & Format": ["Prompt Technique", "Prompt Structure", "Input Type", "Output Format", "Content Source"],
            "Model & Platform": ["Model Family", "Model", "Platform", "Language"],
            "Quality & Management": ["Tone", "Audience", "Complexity", "Abstraction Level", "Safety & Guardrails", "Quality Attributes", "Status"],
        }
        
        for tab, (group_name, categories) in zip(tabs, category_groups.items()):
            with tab:
                cols = st.columns(2)
                for i, cat_name in enumerate(categories):
                    if cat_name in all_tags_by_cat:
                        with cols[i % 2]:
                            options = all_tags_by_cat.get(cat_name, [])
                            selected_tags[cat_name] = st.multiselect(
                                f"{cat_name}:",
                                options=options,
                                key=f"filter_{cat_name}"
                            )
    
    return selected_tags


def render_prompt_card(prompt: Prompt):
    """Render a single prompt card in the library view."""
    fav_icon = "🔱" if prompt.is_favorite == 1 else "☆"
    type_badge = prompt.prompt_type.capitalize()
    
    with st.expander(f"**{fav_icon} {prompt.title}** `[{type_badge}]`"):
        # Copy button
        copy_text = prompt.get_copy_text()
        
        if HAS_CLIPBOARD:
            st_copy_to_clipboard(
                copy_text,
                "📋 Copy Prompt",
                "✅ Copied!",
                key=f"copy_{prompt.id}"
            )
        else:
            if st.button("📋 Copy to Clipboard", key=f"copy_btn_{prompt.id}"):
                st.code(copy_text, language=None)
                st.info("Select and copy the text above")
        
        # Description
        if prompt.description:
            st.markdown(f"**Description:** *{prompt.description}*")
        
        # Use case
        if prompt.use_case:
            st.markdown(f"**Use Case:** {prompt.use_case}")
        
        # Tags display
        if prompt.tags:
            tags_html = ""
            for category, tags in prompt.tags.items():
                if tags:
                    tag_spans = " ".join(
                        f"<span style='background-color:#2a3a57; color:white; "
                        f"padding: 2px 8px; border-radius: 12px; margin-right: 4px; "
                        f"font-size: 0.85em;'>{tag}</span>"
                        for tag in tags
                    )
                    tags_html += f"<div style='margin-bottom: 8px;'><b>{category}:</b> {tag_spans}</div>"
            st.markdown(tags_html, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1, 1, 3])
        
        with col1:
            if st.button(f"{'★' if prompt.is_favorite else '☆'} Favorite", key=f"fav_{prompt.id}"):
                PromptRepository.toggle_favorite(prompt.id, prompt.is_favorite)
                st.rerun()
        
        with col2:
            if st.button("✏️ Edit", key=f"edit_{prompt.id}"):
                st.session_state.page = 'edit'
                st.session_state.selected_prompt_id = prompt.id
                st.rerun()
        
        with col3:
            if st.button("📑 Duplicate", key=f"dup_{prompt.id}"):
                new_id = PromptRepository.duplicate(prompt.id)
                if new_id:
                    st.success(f"Duplicated: {prompt.title}")
                    st.rerun()
        
        with col4:
            # Delete with confirmation
            if f"confirm_delete_{prompt.id}" not in st.session_state:
                st.session_state[f"confirm_delete_{prompt.id}"] = False
            
            if st.session_state[f"confirm_delete_{prompt.id}"]:
                if st.button("⚠️ Confirm", key=f"confirm_{prompt.id}", type="primary"):
                    PromptRepository.delete(prompt.id)
                    st.session_state[f"confirm_delete_{prompt.id}"] = False
                    st.success(f"Deleted: {prompt.title}")
                    st.rerun()
            else:
                if st.button("🗑️ Delete", key=f"delete_{prompt.id}"):
                    st.session_state[f"confirm_delete_{prompt.id}"] = True
                    st.rerun()


def render_library_page():
    """Render the main library browsing page."""
    st.title("💎 Prompt Library Database 💎")
    
    # Load data
    all_prompts = PromptRepository.get_all()
    all_tags_by_cat = get_all_tags_by_category()
    
    # Search and filters
    st.subheader("🔍 Find Prompts")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input(
            "Search",
            key="search_bar",
            label_visibility="collapsed",
            placeholder="🔍 Search by title, description, use case, content..."
        )
    with col2:
        show_favorites = st.toggle("🔱 Favorites Only", key="favorites_toggle")
    with col3:
        sort_option = st.selectbox(
            "Sort by",
            ["Title (A-Z)", "Title (Z-A)", "Newest", "Oldest"],
            key="sort_option",
            label_visibility="collapsed"
        )
    
    # Tag filters
    selected_tags = render_tag_filters(all_tags_by_cat)
    
    # Apply filters
    filtered_prompts = all_prompts
    
    # Favorites filter
    if show_favorites:
        filtered_prompts = [p for p in filtered_prompts if p.is_favorite == 1]
    
    # Tag filters
    for category, tags in selected_tags.items():
        if tags:
            filtered_prompts = [
                p for p in filtered_prompts
                if p.tags and set(tags).issubset(set(p.tags.get(category, [])))
            ]
    
    # Search filter
    if search_query:
        query = search_query.lower()
        filtered_prompts = [
            p for p in filtered_prompts
            if query in p.title.lower()
            or query in p.use_case.lower()
            or query in p.description.lower()
            or query in p.instructions.lower()
            or query in p.task.lower()
            or query in p.persona.lower()
            or query in p.context.lower()
        ]
    
    # Sort
    if sort_option == "Title (A-Z)":
        filtered_prompts.sort(key=lambda p: p.title.lower())
    elif sort_option == "Title (Z-A)":
        filtered_prompts.sort(key=lambda p: p.title.lower(), reverse=True)
    elif sort_option == "Newest":
        filtered_prompts.sort(key=lambda p: p.last_modified or "", reverse=True)
    elif sort_option == "Oldest":
        filtered_prompts.sort(key=lambda p: p.created_at or "")
    
    # Results
    st.markdown("---")
    st.subheader(f"📋 Results ({len(filtered_prompts)})")
    
    if not filtered_prompts:
        st.warning("No prompts found. Try adjusting your search or filters!")
    else:
        for prompt in filtered_prompts:
            render_prompt_card(prompt)


def render_edit_page():
    """Render the add/edit prompt page."""
    prompt_to_edit = None
    if st.session_state.selected_prompt_id:
        prompt_to_edit = PromptRepository.get_by_id(st.session_state.selected_prompt_id)
    
    if prompt_to_edit:
        st.title(f"✏️ Edit Prompt: `{prompt_to_edit.title}`")
    else:
        st.title("✅ Add New Prompt")
    
    # Default values
    defaults = {
        'title': '',
        'use_case': '',
        'description': '',
        'usage_notes': '',
        'version': 'v1.0',
        'persona': '',
        'context': '',
        'task': '',
        'style': '',
        'variables': '# {VAR_NAME}: Description of variable',
        'prompt_type': 'structured',
        'instructions': '',
        'tags': {}
    }
    
    if prompt_to_edit:
        defaults.update({
            'title': prompt_to_edit.title or '',
            'use_case': prompt_to_edit.use_case or '',
            'description': prompt_to_edit.description or '',
            'usage_notes': prompt_to_edit.usage_notes or '',
            'version': prompt_to_edit.version or 'v1.0',
            'persona': prompt_to_edit.persona or '',
            'context': prompt_to_edit.context or '',
            'task': prompt_to_edit.task or '',
            'style': prompt_to_edit.style or '',
            'variables': prompt_to_edit.variables or '',
            'prompt_type': prompt_to_edit.prompt_type or 'structured',
            'instructions': prompt_to_edit.instructions or '',
            'tags': prompt_to_edit.tags or {}
        })
    
    # Prompt type selection
    prompt_type = st.radio(
        "Prompt Type",
        ('Structured', 'Standard'),
        index=0 if defaults['prompt_type'] == 'structured' else 1,
        horizontal=True,
        help="Structured: PCTS format (Persona, Context, Task, Style). Standard: Free-form instructions."
    )
    
    st.markdown("---")
    
    # Form
    with st.form("prompt_form"):
        st.subheader("✨ Prompt Details")
        
        # Basic info
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Prompt Title *", value=defaults['title'])
            use_case = st.text_input("Use Case", value=defaults['use_case'])
        with col2:
            version = st.text_input("Version", value=defaults['version'])
            # Status could be added here
        
        description = st.text_area(
            "Description / Purpose",
            value=defaults['description'],
            height=100
        )
        usage_notes = st.text_area(
            "Usage Notes",
            value=defaults['usage_notes'],
            height=80,
            help="Tips for using this prompt effectively"
        )
        
        st.markdown("---")
        
        # Content fields based on type
        if prompt_type == 'Structured':
            st.subheader("📝 PCTS Framework")
            
            persona = st.text_area(
                "Persona",
                value=defaults['persona'],
                height=100,
                help="Who should the AI act as?"
            )
            context = st.text_area(
                "Context",
                value=defaults['context'],
                height=100,
                help="Background information and constraints"
            )
            task = st.text_area(
                "Task",
                value=defaults['task'],
                height=150,
                help="What should the AI do?"
            )
            style = st.text_area(
                "Style",
                value=defaults['style'],
                height=100,
                help="How should the output be formatted/toned?"
            )
            variables = st.text_area(
                "Variables",
                value=defaults['variables'],
                height=100,
                help="Placeholder variables like {VAR_NAME}"
            )
            instructions = None
        else:
            st.subheader("📝 Instructions")
            instructions = st.text_area(
                "Prompt Instructions",
                value=defaults['instructions'],
                height=400,
                help="The complete prompt text"
            )
            persona = context = task = style = variables = None
        
        st.markdown("---")
        
        # Tags
        st.subheader("🏷️ Tags")
        
        all_tags_by_cat = get_all_tags_by_category()
        tags_data = {}
        
        # Group tags into tabs for better organization
        tag_tabs = st.tabs(["Core", "Methodology", "Format", "Model", "Quality"])
        
        tag_groups = {
            "Core": ["Task Type", "Domain", "Function", "Use Case"],
            "Methodology": ["Prompt Technique", "Prompt Structure", "Complexity", "Abstraction Level"],
            "Format": ["Input Type", "Output Format", "Content Source", "Language"],
            "Model": ["Model Family", "Model", "Platform"],
            "Quality": ["Tone", "Audience", "Safety & Guardrails", "Quality Attributes", "Status"],
        }
        
        for tab, (group_name, categories) in zip(tag_tabs, tag_groups.items()):
            with tab:
                cols = st.columns(2)
                for i, cat in enumerate(categories):
                    if cat in all_tags_by_cat:
                        with cols[i % 2]:
                            tags_data[cat] = st.multiselect(
                                cat,
                                options=all_tags_by_cat[cat],
                                default=defaults['tags'].get(cat, []),
                                key=f"tag_{cat}"
                            )
        
        st.markdown("---")
        
        # Submit
        col1, col2 = st.columns([1, 4])
        with col1:
            submitted = st.form_submit_button(
                "💾 Save Prompt",
                use_container_width=True,
                type="primary"
            )
        
        if submitted:
            # Validation
            if not title.strip():
                st.error("❌ Title is required!")
            else:
                # Create prompt object
                prompt = Prompt(
                    id=prompt_to_edit.id if prompt_to_edit else str(uuid.uuid4()),
                    title=title.strip(),
                    prompt_type=prompt_type.lower(),
                    use_case=use_case,
                    description=description,
                    usage_notes=usage_notes,
                    version=version,
                    persona=persona or "",
                    context=context or "",
                    task=task or "",
                    style=style or "",
                    variables=variables or "",
                    instructions=instructions or "",
                )
                
                # Save
                PromptRepository.save(prompt, tags_data)
                st.success(f"✅ Prompt saved: {title}")
                
                # Return to library
                st.session_state.page = 'library'
                st.session_state.selected_prompt_id = None
                st.rerun()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize database
    init_db()
    
    # Check authentication
    if not check_login():
        return
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'library'
    if 'selected_prompt_id' not in st.session_state:
        st.session_state.selected_prompt_id = None
    
    # Render sidebar
    render_sidebar()
    
    # Render main content
    if st.session_state.page == 'library':
        render_library_page()
    elif st.session_state.page == 'edit':
        render_edit_page()


if __name__ == "__main__":
    main()