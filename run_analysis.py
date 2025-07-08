#!/usr/bin/env python3
"""
Direct SUBFRACTURE analysis runner
Runs the analysis directly without LangGraph Platform
"""

import asyncio
import json
from demo_agent import SubfractureDemoAgent

async def run_subfracture_analysis():
    """Run SUBFRACTURE analysis on the transcript"""
    
    print("🚀 SUBFRACTURE Brand Intelligence Analysis")
    print("=" * 60)
    
    # Load the transcript
    try:
        with open("/mnt/c/Users/Admin/subfracture-langgraph/subfracture_transcript_input.json", "r") as f:
            data = json.load(f)
        print("📄 Loaded transcript data successfully")
        print(f"📝 Transcript length: {len(data['brand_brief']):,} characters")
    except Exception as e:
        print(f"❌ Failed to load transcript: {e}")
        return
    
    # Initialize SUBFRACTURE agent
    agent = SubfractureDemoAgent()
    
    # Run the analysis
    try:
        print("\n🔍 Starting brand intelligence analysis...")
        result = await agent.analyze_transcript(
            brand_brief=data["brand_brief"],
            operator_context=data["operator_context"],
            target_outcome=data["target_outcome"]
        )
        
        print("\n✅ Analysis Complete!")
        print("=" * 60)
        
        # Display key results
        analysis = result["analysis"]
        metrics = result["business_metrics"]
        
        print(f"📊 **BRAND GRAVITY INDEX**: {analysis['gravity_index']:.3f}")
        print(f"🎯 **BRAND ESSENCE**: {analysis['key_insights']['brand_essence']}")
        print(f"🚀 **MARKET READINESS**: {metrics['launch_confidence']}")
        print(f"💰 **MARKET IMPACT**: {metrics['estimated_market_impact']}")
        
        print(f"\n🧠 **KEY INSIGHTS**:")
        insights = analysis['key_insights']
        print(f"  • Core Differentiator: {insights['core_differentiator']}")
        print(f"  • Methodology: {insights['methodology']}")
        print(f"  • Confidence Level: {insights['confidence_level']:.2f}")
        
        print(f"\n🎯 **STRATEGIC POSITIONING**:")
        positioning = analysis['strategic_positioning']
        print(f"  • Target: {positioning['target_audience']}")
        print(f"  • Category: {positioning['category']}")
        print(f"  • Disruption: {positioning['category_disruption']}")
        
        print(f"\n⚡ **COMPETITIVE ADVANTAGES**:")
        for i, advantage in enumerate(analysis['competitive_advantages'][:5], 1):
            print(f"  {i}. {advantage}")
        
        print(f"\n🌟 **MARKET OPPORTUNITIES**:")
        for i, opportunity in enumerate(analysis['market_opportunities'][:5], 1):
            print(f"  {i}. {opportunity}")
        
        print(f"\n🎭 **BRAND PERSONALITY**:")
        personality = analysis['brand_personality']
        print(f"  • Core Traits: {personality['core_traits']}")
        print(f"  • Style: {personality['communication_style']}")
        print(f"  • Archetype: {personality['brand_archetype']}")
        
        print(f"\n💡 **STRATEGIC RECOMMENDATIONS**:")
        for i, rec in enumerate(analysis['recommendations'][:8], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n📈 **BUSINESS METRICS**:")
        print(f"  • Market Readiness Score: {metrics['market_readiness_score']:.3f}")
        print(f"  • Differentiation Strength: {metrics['differentiation_strength']:.3f}")
        print(f"  • Brand Coherence: {metrics['brand_coherence']:.3f}")
        
        print(f"\n🎉 **SUMMARY**:")
        print(f"SUBFRACTURE has analyzed {len(data['brand_brief']):,} characters of brand strategy")
        print(f"conversation and identified a {metrics['launch_confidence'].lower()} confidence")
        print(f"opportunity for launching this human-centered AI design studio.")
        
        # Save detailed results
        with open("/mnt/c/Users/Admin/subfracture-langgraph/analysis_results.json", "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Detailed results saved to: analysis_results.json")
        
        return result
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(run_subfracture_analysis())