from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class LinkedInContentAnalyzerInput(BaseModel):
    """Input schema for LinkedInContentAnalyzer"""
    content: str = Field(..., description="LinkedIn post content that must be analyzed")
    topic: str = Field(..., description="Main topic of the content")
    
class LinkedInContentAnalyzer(BaseTool):
    name: str = "LinkedIn Content Quality Analyzer"
    description: str = (
        "Analyzes the quality of the LinkedIn content, including adequate emoji usage, storytelling "
        "structure, technical accuracy, and audience engagement potential. Thereafter, feedback is provided to improve "
        "the content quality based on industry best practices"
    )

    args_schema: Type[BaseModel] = LinkedInContentAnalyzerInput
    
    def _run(self, content: str, topic: str) -> str:
        # Implementation of the analytics logic
        analysis_points = []
        
        if not any(content.split('\n')[0].endswith(char) for char in ['?', '!']):
            analysis_points.append("❌ Missing strong opening hook (question/statement)")
        else:
            analysis_points.append("✅ Strong opening hook provided")
            
        # Check emoji usage
        emoji_count = sum(1 for char in content if ord(char) > 127)
        if 5 <= emoji_count <= 9:
            analysis_points.append("✅ Appropriate emoji usage")
        else:
            analysis_points.append("❌ Inappropriate emoji usage: 5-9 emojis expected")
            
        # Check content length
        words = len(content.split())
        if 200 <= words <= 300:
            analysis_points.append("✅ Appropriate content length")
        else:
            analysis_points.append("❌ Inappropriate content length: 201-300 words expected")
        
        # Check topic relevance
        topic_mentions = content.lower().count(topic.lower())
        
        if topic_mentions >= 2:
            analysis_points.append("✅ Topic relevance maintained (Topic mentioned at least twice)")
        else:
            analysis_points.append(f"❌ Topic relevance not maintained (only mentioned {topic_mentions} time(s), minimum 2 required)")
            
        return "\n".join(analysis_points)