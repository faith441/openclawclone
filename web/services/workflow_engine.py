"""
Workflow Engine - Natural Language to Automation
Converts user descriptions into executable workflow steps
"""
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class ActionType(Enum):
    """Types of automation actions"""
    # Web Actions
    SCRAPE_PAGE = "scrape_page"
    EXTRACT_DATA = "extract_data"
    CLICK_ELEMENT = "click_element"
    FILL_FORM = "fill_form"
    NAVIGATE_TO = "navigate_to"
    TAKE_SCREENSHOT = "take_screenshot"
    WAIT = "wait"

    # Data Actions
    FILTER_DATA = "filter_data"
    TRANSFORM_DATA = "transform_data"
    MERGE_DATA = "merge_data"
    DEDUPLICATE = "deduplicate"
    VALIDATE_DATA = "validate_data"

    # Output Actions
    SAVE_TO_SHEETS = "save_to_sheets"
    SAVE_TO_CSV = "save_to_csv"
    SAVE_TO_JSON = "save_to_json"
    SAVE_TO_DATABASE = "save_to_database"
    SEND_EMAIL = "send_email"
    SEND_WEBHOOK = "send_webhook"
    SEND_SLACK = "send_slack"

    # Control Flow
    LOOP = "loop"
    CONDITION = "condition"
    PARALLEL = "parallel"
    RETRY = "retry"

    # Scheduling
    SCHEDULE_DAILY = "schedule_daily"
    SCHEDULE_HOURLY = "schedule_hourly"
    SCHEDULE_CRON = "schedule_cron"

    # AI Actions
    AI_ANALYZE = "ai_analyze"
    AI_SUMMARIZE = "ai_summarize"
    AI_CLASSIFY = "ai_classify"
    AI_EXTRACT = "ai_extract"
    AI_GENERATE = "ai_generate"


@dataclass
class WorkflowStep:
    """A single step in a workflow"""
    action: ActionType
    params: Dict[str, Any]
    description: str
    depends_on: Optional[List[str]] = None
    retry_config: Optional[Dict] = None
    id: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "action": self.action.value,
            "params": self.params,
            "description": self.description,
            "depends_on": self.depends_on,
            "retry_config": self.retry_config
        }


@dataclass
class Workflow:
    """Complete workflow definition"""
    name: str
    description: str
    steps: List[WorkflowStep]
    schedule: Optional[Dict] = None
    variables: Optional[Dict] = None
    created_at: str = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        # Assign IDs to steps
        for i, step in enumerate(self.steps):
            if not step.id:
                step.id = f"step_{i+1}"

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "schedule": self.schedule,
            "variables": self.variables,
            "created_at": self.created_at
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)


# Action Block Templates
ACTION_BLOCKS = {
    ActionType.SCRAPE_PAGE: {
        "name": "Scrape Page",
        "icon": "🌐",
        "description": "Extract content from a web page",
        "params": {
            "url": {"type": "string", "required": True, "description": "URL to scrape"},
            "selector": {"type": "string", "required": False, "description": "CSS selector for specific elements"},
            "wait_for": {"type": "string", "required": False, "description": "Element to wait for before scraping"},
            "javascript": {"type": "boolean", "required": False, "default": True, "description": "Enable JavaScript rendering"}
        }
    },
    ActionType.EXTRACT_DATA: {
        "name": "Extract Data",
        "icon": "📊",
        "description": "Extract specific data points from content",
        "params": {
            "source": {"type": "string", "required": True, "description": "Source data or previous step output"},
            "fields": {"type": "array", "required": True, "description": "Fields to extract (e.g., emails, phones, names)"},
            "pattern": {"type": "string", "required": False, "description": "Regex pattern for custom extraction"}
        }
    },
    ActionType.FILL_FORM: {
        "name": "Fill Form",
        "icon": "✏️",
        "description": "Fill out a web form",
        "params": {
            "form_data": {"type": "object", "required": True, "description": "Field name to value mapping"},
            "submit": {"type": "boolean", "required": False, "default": True, "description": "Submit form after filling"}
        }
    },
    ActionType.SAVE_TO_SHEETS: {
        "name": "Save to Google Sheets",
        "icon": "📗",
        "description": "Save data to Google Sheets",
        "params": {
            "spreadsheet_id": {"type": "string", "required": True, "description": "Google Sheets ID"},
            "sheet_name": {"type": "string", "required": False, "default": "Sheet1", "description": "Sheet tab name"},
            "mode": {"type": "string", "required": False, "default": "append", "description": "append or replace"}
        }
    },
    ActionType.SEND_EMAIL: {
        "name": "Send Email",
        "icon": "📧",
        "description": "Send an email with results",
        "params": {
            "to": {"type": "string", "required": True, "description": "Recipient email"},
            "subject": {"type": "string", "required": True, "description": "Email subject"},
            "body": {"type": "string", "required": True, "description": "Email body (supports {{variables}})"},
            "attachments": {"type": "array", "required": False, "description": "Files to attach"}
        }
    },
    ActionType.SCHEDULE_DAILY: {
        "name": "Schedule Daily",
        "icon": "📅",
        "description": "Run workflow daily at specified time",
        "params": {
            "time": {"type": "string", "required": True, "description": "Time in HH:MM format (24h)"},
            "timezone": {"type": "string", "required": False, "default": "UTC", "description": "Timezone"}
        }
    },
    ActionType.AI_ANALYZE: {
        "name": "AI Analyze",
        "icon": "🤖",
        "description": "Use AI to analyze data",
        "params": {
            "data": {"type": "string", "required": True, "description": "Data to analyze"},
            "prompt": {"type": "string", "required": True, "description": "Analysis instructions"},
            "model": {"type": "string", "required": False, "default": "auto", "description": "AI model to use"}
        }
    },
    ActionType.LOOP: {
        "name": "Loop",
        "icon": "🔄",
        "description": "Repeat actions for each item",
        "params": {
            "items": {"type": "string", "required": True, "description": "Array of items to loop over"},
            "steps": {"type": "array", "required": True, "description": "Steps to execute for each item"}
        }
    },
    ActionType.CONDITION: {
        "name": "Condition",
        "icon": "❓",
        "description": "Execute steps based on condition",
        "params": {
            "condition": {"type": "string", "required": True, "description": "Condition to evaluate"},
            "if_true": {"type": "array", "required": True, "description": "Steps if condition is true"},
            "if_false": {"type": "array", "required": False, "description": "Steps if condition is false"}
        }
    }
}


class WorkflowEngine:
    """
    Engine for generating and executing workflows from natural language
    """

    # System prompt for workflow generation
    WORKFLOW_SYSTEM_PROMPT = """You are an automation workflow generator. Convert user requests into structured JSON workflows.

Available action types:
- scrape_page: Extract content from web pages
- extract_data: Extract specific data (emails, phones, names, etc.)
- click_element: Click on page elements
- fill_form: Fill out web forms
- navigate_to: Go to a URL
- filter_data: Filter data based on criteria
- transform_data: Transform/format data
- save_to_sheets: Save to Google Sheets
- save_to_csv: Export as CSV
- send_email: Send email with results
- send_webhook: Send data to webhook
- send_slack: Send Slack notification
- schedule_daily: Run daily at specific time
- schedule_hourly: Run every N hours
- ai_analyze: Use AI to analyze data
- ai_summarize: Use AI to summarize
- ai_extract: Use AI to extract structured data
- loop: Repeat for each item
- condition: If/else logic

Respond ONLY with valid JSON in this format:
{
  "name": "Workflow name",
  "description": "What this workflow does",
  "steps": [
    {
      "action": "action_type",
      "params": {...},
      "description": "What this step does"
    }
  ],
  "schedule": {
    "type": "daily|hourly|cron",
    "time": "09:00",
    "timezone": "UTC"
  }
}"""

    @staticmethod
    def get_action_blocks() -> List[Dict]:
        """Get all available action blocks"""
        return [
            {
                "type": action_type.value,
                **block_def
            }
            for action_type, block_def in ACTION_BLOCKS.items()
        ]

    @staticmethod
    async def generate_workflow(
        user_prompt: str,
        ai_router,
        api_keys: Dict[str, str],
        model_id: str = None
    ) -> Tuple[Workflow, Dict]:
        """
        Generate a workflow from natural language description

        Args:
            user_prompt: User's description of what they want to automate
            ai_router: AI router instance
            api_keys: User's API keys
            model_id: Specific model to use (or auto-select)

        Returns:
            Tuple of (Workflow, usage_info)
        """
        # Auto-select model if not specified
        if not model_id:
            model_id = ai_router.select_best_model("complex", api_keys)

        messages = [
            {"role": "system", "content": WorkflowEngine.WORKFLOW_SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a workflow for: {user_prompt}"}
        ]

        response, usage, cost = await ai_router.chat(
            messages=messages,
            model_id=model_id,
            api_keys=api_keys
        )

        # Parse JSON from response
        try:
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response

            workflow_data = json.loads(json_str.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse workflow: {e}")

        # Convert to Workflow object
        steps = []
        for step_data in workflow_data.get("steps", []):
            action_str = step_data.get("action", "")
            try:
                action = ActionType(action_str)
            except ValueError:
                # Unknown action, skip or use a default
                continue

            steps.append(WorkflowStep(
                action=action,
                params=step_data.get("params", {}),
                description=step_data.get("description", "")
            ))

        workflow = Workflow(
            name=workflow_data.get("name", "Untitled Workflow"),
            description=workflow_data.get("description", ""),
            steps=steps,
            schedule=workflow_data.get("schedule")
        )

        return workflow, {
            "usage": usage,
            "cost": cost,
            "model": model_id
        }

    @staticmethod
    def validate_workflow(workflow: Workflow) -> Tuple[bool, List[str]]:
        """
        Validate a workflow for completeness and correctness

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not workflow.name:
            errors.append("Workflow must have a name")

        if not workflow.steps:
            errors.append("Workflow must have at least one step")

        for i, step in enumerate(workflow.steps):
            # Check required params
            block_def = ACTION_BLOCKS.get(step.action)
            if block_def:
                for param_name, param_def in block_def.get("params", {}).items():
                    if param_def.get("required") and param_name not in step.params:
                        errors.append(f"Step {i+1}: Missing required param '{param_name}'")

        return len(errors) == 0, errors

    @staticmethod
    async def explain_workflow(
        workflow: Workflow,
        ai_router,
        api_keys: Dict[str, str]
    ) -> str:
        """Generate a human-readable explanation of the workflow"""
        model_id = ai_router.select_best_model("simple", api_keys)

        messages = [
            {"role": "system", "content": "Explain this automation workflow in simple, friendly terms. Be concise."},
            {"role": "user", "content": f"Workflow: {workflow.to_json()}"}
        ]

        response, _, _ = await ai_router.chat(
            messages=messages,
            model_id=model_id,
            api_keys=api_keys
        )

        return response

    @staticmethod
    async def optimize_workflow(
        workflow: Workflow,
        ai_router,
        api_keys: Dict[str, str]
    ) -> Workflow:
        """Use AI to optimize and improve the workflow"""
        model_id = ai_router.select_best_model("complex", api_keys)

        messages = [
            {"role": "system", "content": """Optimize this workflow for efficiency and reliability.
Consider:
- Combining steps where possible
- Adding error handling
- Parallelizing independent steps
- Adding appropriate waits/retries

Return ONLY the optimized JSON workflow."""},
            {"role": "user", "content": f"Optimize this: {workflow.to_json()}"}
        ]

        response, _, _ = await ai_router.chat(
            messages=messages,
            model_id=model_id,
            api_keys=api_keys
        )

        # Parse optimized workflow
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response

        workflow_data = json.loads(json_str.strip())

        # Convert back to Workflow
        steps = []
        for step_data in workflow_data.get("steps", []):
            try:
                action = ActionType(step_data.get("action", ""))
                steps.append(WorkflowStep(
                    action=action,
                    params=step_data.get("params", {}),
                    description=step_data.get("description", ""),
                    retry_config=step_data.get("retry_config")
                ))
            except ValueError:
                continue

        return Workflow(
            name=workflow_data.get("name", workflow.name),
            description=workflow_data.get("description", workflow.description),
            steps=steps,
            schedule=workflow_data.get("schedule", workflow.schedule)
        )


# Workflow Storage (database model would go here)
class WorkflowStorage:
    """In-memory workflow storage (replace with database in production)"""

    _workflows: Dict[str, Dict[str, Workflow]] = {}  # user_id -> workflow_id -> workflow

    @classmethod
    def save(cls, user_id: str, workflow: Workflow) -> str:
        """Save workflow and return ID"""
        import uuid
        workflow_id = str(uuid.uuid4())

        if user_id not in cls._workflows:
            cls._workflows[user_id] = {}

        cls._workflows[user_id][workflow_id] = workflow
        return workflow_id

    @classmethod
    def get(cls, user_id: str, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID"""
        return cls._workflows.get(user_id, {}).get(workflow_id)

    @classmethod
    def list(cls, user_id: str) -> List[Dict]:
        """List all workflows for user"""
        workflows = cls._workflows.get(user_id, {})
        return [
            {"id": wf_id, **wf.to_dict()}
            for wf_id, wf in workflows.items()
        ]

    @classmethod
    def delete(cls, user_id: str, workflow_id: str) -> bool:
        """Delete a workflow"""
        if user_id in cls._workflows and workflow_id in cls._workflows[user_id]:
            del cls._workflows[user_id][workflow_id]
            return True
        return False


# Convenience functions
engine = WorkflowEngine()

def get_action_blocks():
    return WorkflowEngine.get_action_blocks()

async def generate_workflow(prompt, ai_router, api_keys, model_id=None):
    return await WorkflowEngine.generate_workflow(prompt, ai_router, api_keys, model_id)

def validate_workflow(workflow):
    return WorkflowEngine.validate_workflow(workflow)
