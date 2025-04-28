"""
Example of how the manager agent would use the delegation tool:

The manager can delegate work using this format:

{
    "task": "Revise LinkedIn post to improve engagement",
    "context": "Current post: [original content here]\n\nRequired improvements:\n1. Add a stronger opening hook\n2. Include the research statistics about [topic]\n3. End with a clear call-to-action",
    "coworker": "Content Creation Specialist"
}

The tool will automatically:
1. Route the task to the correct agent
2. Provide the context and requirements
3. Return the revised content for review
"""