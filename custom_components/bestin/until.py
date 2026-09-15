def formatted_name(name: str) -> str:
    """Format the given name by capitalizing and removing any text after a colon."""
    if ':' in name:
        return name.split(":")[0].title()
    return name.title()
