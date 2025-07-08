#!/usr/bin/env python3
"""
SUBFRACTURE User Options Demo
Shows how users can choose between Standard and Deep analysis modes
"""

import asyncio
import json
from demo_agent import SubfractureDemoAgent

def show_user_interface():
    """Show the user interface options"""
    
    print("🎭 SUBFRACTURE Brand Intelligence Platform")
    print("=" * 60)
    print()
    print("Choose your analysis mode:")
    print()
    print("⚡ STANDARD MODE")
    print("  • Fast strategic insights (2-3 seconds)")
    print("  • Core positioning and recommendations")
    print("  • Business metrics and gravity index")
    print("  • Perfect for quick decision making")
    print()
    print("🔬 DEEP MODE")
    print("  • Comprehensive analysis with 'showing the working'")
    print("  • 8-step analytical process revealed")
    print("  • Detailed thematic scoring and competitive intelligence")
    print("  • Content structure, sentiment, and framework detection")
    print("  • Perfect for methodology demonstration and thorough insights")
    print()

async def demonstrate_user_choice():
    """Demonstrate how users choose analysis modes"""
    
    show_user_interface()
    
    # Load the full transcript
    with open("/mnt/c/Users/Admin/subfracture-langgraph/subfracture_transcript_input.json", "r") as f:
        full_data = json.load(f)
    
    # Simulate user choosing Standard Mode first
    print("👤 User Selection: Standard Mode")
    print("-" * 30)
    
    agent = SubfractureDemoAgent()
    
    standard_result = await agent.analyze_transcript(
        brand_brief=full_data["brand_brief"],
        operator_context=full_data["operator_context"],
        target_outcome=full_data["target_outcome"],
        deep_analysis=False  # User choice: Standard
    )
    
    print(f"📊 Standard Analysis Results:")
    print(f"  • Gravity Index: {standard_result['analysis']['gravity_index']:.3f}")
    print(f"  • Launch Confidence: {standard_result['business_metrics']['launch_confidence']}")
    print(f"  • Key Recommendations: {len(standard_result['analysis']['recommendations'])}")
    print(f"  • Analysis Time: ~2 seconds")
    
    print("\n" + "="*60)
    
    # Simulate user choosing Deep Mode
    print("👤 User Selection: Deep Mode")
    print("-" * 30)
    
    deep_result = await agent.analyze_transcript(
        brand_brief=full_data["brand_brief"],
        operator_context=full_data["operator_context"],
        target_outcome=full_data["target_outcome"],
        deep_analysis=True  # User choice: Deep
    )
    
    print(f"📊 Deep Analysis Results:")
    print(f"  • Enhanced Gravity Index: {deep_result['analysis']['gravity_index']:.3f}")
    print(f"  • Thematic Coherence: {deep_result['deep_insights']['thematic_coherence']:.3f}")
    print(f"  • Competitive Awareness: {deep_result['deep_insights']['competitive_awareness']} companies")
    print(f"  • Brand Architecture: {deep_result['deep_insights']['brand_architecture_completeness']:.3f} completeness")
    print(f"  • Framework Sophistication: {deep_result['deep_insights']['strategic_sophistication']} methodologies")
    print(f"  • Analysis Components: {len(deep_result['analysis'])} detailed sections")
    
    print(f"\n🎯 VALUE PROPOSITION:")
    print(f"Standard Mode: Perfect for clients needing quick strategic direction")
    print(f"Deep Mode: Perfect for demonstrating SUBFRACTURE methodology depth")
    
    print(f"\n💡 BUSINESS APPLICATION:")
    print(f"• Sales presentations: Use Deep Mode to show analytical sophistication")
    print(f"• Client workshops: Use Standard Mode for rapid insights during sessions")
    print(f"• Methodology training: Use Deep Mode to teach SUBFRACTURE approach")
    print(f"• Competitive differentiation: Deep Mode shows 'how we think' vs 'what we think'")

async def langgraph_platform_usage():
    """Show how this works in LangGraph Platform"""
    
    print(f"\n🚀 LANGGRAPH PLATFORM USAGE")
    print("=" * 60)
    print()
    print("For STANDARD analysis, use this JSON input:")
    print("```json")
    
    standard_input = {
        "brand_brief": "Your brand strategy conversation...",
        "operator_context": {
            "role": "Brand Strategist",
            "industry": "Technology",
            "company_stage": "Growth"
        },
        "target_outcome": "Quick strategic insights",
        "deep_analysis": False
    }
    
    print(json.dumps(standard_input, indent=2))
    print("```")
    
    print("\nFor DEEP analysis, use this JSON input:")
    print("```json")
    
    deep_input = {
        "brand_brief": "Your brand strategy conversation...",
        "operator_context": {
            "role": "Brand Strategist",
            "industry": "Technology", 
            "company_stage": "Growth"
        },
        "target_outcome": "Comprehensive analysis with working shown",
        "deep_analysis": True
    }
    
    print(json.dumps(deep_input, indent=2))
    print("```")
    
    print(f"\n🔧 INTEGRATION STATUS:")
    print(f"✅ Both modes integrated into demo_agent.py")
    print(f"✅ LangGraph Platform configuration updated")
    print(f"✅ JSON input parameters support deep_analysis flag")
    print(f"✅ User can choose analysis depth via simple boolean")

if __name__ == "__main__":
    asyncio.run(demonstrate_user_choice())
    asyncio.run(langgraph_platform_usage())