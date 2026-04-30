#!/usr/bin/env python3
"""
Seed Agent Catalog - Populate database with agents from /industries/
"""
import sys
from pathlib import Path
import yaml
import re

# Add web directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'web'))

from app import app, HAS_NEW_MODULES
if not HAS_NEW_MODULES:
    print("❌ Error: New authentication modules not loaded. Run setup.sh first.")
    sys.exit(1)

from models import db
from models.agent import AgentCatalog
from slugify import slugify


def parse_skill_md(skill_md_path):
    """Parse SKILL.md file to extract metadata"""
    try:
        with open(skill_md_path, 'r') as f:
            content = f.read()

        # Extract YAML frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            metadata = yaml.safe_load(yaml_match.group(1))
            return metadata
        return {}
    except Exception as e:
        print(f"Failed to parse {skill_md_path}: {e}")
        return {}


def extract_env_vars(skill_md_path, script_path):
    """Extract required environment variables from SKILL.md or script"""
    env_vars = []

    # Try SKILL.md first
    if skill_md_path.exists():
        metadata = parse_skill_md(skill_md_path)
        if metadata.get('metadata', {}).get('openclaw', {}).get('requires', {}).get('env'):
            env_vars = metadata['metadata']['openclaw']['requires']['env']

    # Also scan the Python script
    if script_path.exists():
        try:
            with open(script_path, 'r') as f:
                script_content = f.read()

            # Find os.environ.get() calls
            env_pattern = r"os\.environ\.get\(['\"]([A-Z_]+)['\"]"
            found_vars = re.findall(env_pattern, script_content)
            env_vars.extend(found_vars)

        except Exception as e:
            print(f"Failed to scan script {script_path}: {e}")

    return list(set(env_vars))  # Remove duplicates


def parse_requirements(requirements_path):
    """Parse requirements.txt file"""
    try:
        with open(requirements_path, 'r') as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
            return requirements
    except Exception:
        return []


def scan_agents():
    """Scan /industries/ directory for agents"""
    industries_dir = Path(__file__).parent.parent / 'industries'

    if not industries_dir.exists():
        print(f"Industries directory not found: {industries_dir}")
        return []

    agents = []

    # Scan all agent directories
    for agent_dir in industries_dir.rglob('*/agents/*'):
        if not agent_dir.is_dir():
            continue

        # Find the main script
        scripts_dir = agent_dir / 'scripts'
        if not scripts_dir.exists():
            continue

        # Find Python script
        script_files = list(scripts_dir.glob('*.py'))
        if not script_files:
            continue

        script_path = script_files[0]

        # Get metadata
        skill_md_path = agent_dir / 'SKILL.md'
        readme_path = agent_dir / 'README.md'
        requirements_path = agent_dir / 'requirements.txt'

        # Extract info
        agent_name = agent_dir.name.replace('-', ' ').title()
        industry = agent_dir.parent.parent.name
        category = 'industry' if industry in ['finance', 'real-estate', 'ecommerce', 'legal', 'hospitality', 'construction', 'marketing', 'healthcare'] else 'automation'

        # Get description from README or SKILL.md
        description = ''
        if skill_md_path.exists():
            metadata = parse_skill_md(skill_md_path)
            description = metadata.get('description', '')

        if not description and readme_path.exists():
            try:
                with open(readme_path, 'r') as f:
                    lines = f.readlines()
                    # Get first non-empty, non-title line
                    for line in lines[1:]:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            description = line
                            break
            except Exception:
                pass

        # Get icon (emoji)
        icon_map = {
            'finance': '💰',
            'real-estate': '🏠',
            'ecommerce': '🛒',
            'legal': '⚖️',
            'hospitality': '🏨',
            'construction': '🏗️',
            'marketing': '📊',
            'healthcare': '🏥',
            'email': '📧',
            'sms': '📱',
            'pdf': '📄',
            'web-scraper': '🌐',
            'data-converter': '🔄',
            'image-optimizer': '🖼️',
            'slack': '💬'
        }
        icon = icon_map.get(agent_dir.name, '⚡')

        # Extract environment variables
        env_vars = extract_env_vars(skill_md_path, script_path)

        # Parse requirements
        requirements = parse_requirements(requirements_path)

        agents.append({
            'slug': slugify(f"{industry}-{agent_name}"),
            'name': agent_name,
            'description': description or f"AI-powered {agent_name.lower()}",
            'category': category,
            'industry': industry,
            'icon': icon,
            'file_path': str(script_path.relative_to(Path(__file__).parent.parent)),
            'skill_md_path': str(skill_md_path.relative_to(Path(__file__).parent.parent)) if skill_md_path.exists() else None,
            'requirements_json': requirements,
            'env_vars_required': env_vars,
            'is_published': True,
            'is_featured': category == 'industry'  # Feature industry agents
        })

    return agents


def seed_catalog():
    """Seed the agent catalog"""
    print("\n" + "="*60)
    print("  🌱 Seeding Agent Catalog")
    print("="*60 + "\n")

    # Scan agents
    print("📂 Scanning /industries/ directory...")
    agents = scan_agents()
    print(f"   Found {len(agents)} agents\n")

    if not agents:
        print("❌ No agents found. Check your /industries/ directory structure.")
        return

    # Populate database
    with app.app_context():
        print("💾 Populating database...")

        added = 0
        updated = 0

        for agent_data in agents:
            existing = AgentCatalog.query.filter_by(slug=agent_data['slug']).first()

            if existing:
                # Update existing
                for key, value in agent_data.items():
                    if key not in ['id', 'created_at', 'install_count', 'rating_avg', 'rating_count']:
                        setattr(existing, key, value)
                db.session.commit()
                updated += 1
                print(f"   ✓ Updated: {agent_data['name']}")
            else:
                # Create new
                agent = AgentCatalog(**agent_data)
                db.session.add(agent)
                db.session.commit()
                added += 1
                print(f"   ✓ Added: {agent_data['name']}")

        print(f"\n✅ Complete! Added: {added}, Updated: {updated}")
        print(f"   Total agents in catalog: {AgentCatalog.query.count()}")

    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    seed_catalog()
