import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_README = os.path.join(ROOT_DIR, "README.md")

START_MARKER = '<!-- PROJECTS-LIST:START -->'
END_MARKER = '<!-- PROJECTS-LIST:END -->'

def extract_project_info(readme_path):
    """Extracts the first H1 title and the following paragraph from a README.md."""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the first H1 header
        title_match = re.search(r'^#\s+(.*?)\s*$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "Untitled Project"

        # Find the first non-empty line after the title that isn't a heading
        description = ""
        lines = content.split('\n')
        title_passed = False
        
        for line in lines:
            line = line.strip()
            if not title_passed:
                if line.startswith('#'):
                    title_passed = True
                continue
            
            if line:
                if line.startswith('#'):
                    # another heading started before description found
                    break
                # found the first paragraph line
                description = line
                break

        return title, description
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return "Untitled Project", "No description provided."

def generate_projects_list():
    """Scans subdirectories for projects and generates the Markdown list."""
    projects = []

    # Get all subdirectories in root, ignoring dotfiles like .git, .github, etc.
    subdirs = [d for d in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, d)) and not d.startswith('.')]
    
    # Sort subdirectories alphabetically for consistent ordering
    subdirs.sort()

    for subdir in subdirs:
        dir_path = os.path.join(ROOT_DIR, subdir)
        readme_path = os.path.join(dir_path, "README.md")

        if os.path.exists(readme_path):
            title, description = extract_project_info(readme_path)
            
            # Format: '1. Project Title:\nDescription' or '- **[Project Title](./subdir/)**: Description'
            # The prompt requested:
            # 1. Beatport Automation Tool:
            # Automated Beatport account creation...
            projects.append((title, subdir, description))

    
    # Format the markdown list
    lines = []
    for idx, (title, subdir, desc) in enumerate(projects, 1):
        lines.append(f"{idx}. [{title}](./{subdir}):")
        lines.append(f"{desc}")
        lines.append("") # Blank line between entries

    return '\n'.join(lines)

def update_root_readme(projects_markdown):
    """Injects the generated list into the root README.md."""
    if not os.path.exists(ROOT_README):
        print(f"Root README not found at {ROOT_README}")
        return False

    with open(ROOT_README, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create the replacement block with markers
    replacement = f"{START_MARKER}\n{projects_markdown}\n{END_MARKER}"
    
    # Replace between markers
    pattern = re.compile(f"{START_MARKER}.*?{END_MARKER}", re.DOTALL)
    
    if not pattern.search(content):
        print("Markers not found in root README.md")
        return False
        
    updated_content = pattern.sub(replacement, content)

    if updated_content != content:
        with open(ROOT_README, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("Successfully updated README.md with new projects.")
        return True
    else:
        print("README.md is already up-to-date.")
        return False

if __name__ == '__main__':
    print("Scanning for projects...")
    projects_md = generate_projects_list()
    
    if not projects_md:
        print("No projects found.")
    else:
        print("Generated Projects Markdown:\n")
        print(projects_md)
        update_root_readme(projects_md)
