#!/usr/bin/env python3
"""
Test both STANDARD and DEEP analysis modes
"""

import asyncio
import json
from demo_agent import SubfractureDemoAgent

async def test_both_modes():
    """Test both analysis modes"""
    
    print("🚀 SUBFRACTURE Analysis Mode Comparison")
    print("=" * 80)
    
    agent = SubfractureDemoAgent()
    
    # Test 1: Standard Mode
    print("\n📈 TESTING STANDARD MODE")
    print("-" * 40)
    
    with open("/mnt/c/Users/Admin/subfracture-langgraph/test_standard_mode.json", "r") as f:
        standard_input = json.load(f)
    
    standard_result = await agent.analyze_transcript(
        brand_brief=standard_input["brand_brief"],
        operator_context=standard_input["operator_context"],
        target_outcome=standard_input["target_outcome"],
        deep_analysis=False
    )
    
    print(f"✅ Standard Analysis Complete")
    print(f"📊 Gravity Index: {standard_result['analysis']['gravity_index']}")
    print(f"🎯 Recommendations: {len(standard_result['analysis']['recommendations'])}")
    
    # Test 2: Deep Mode
    print("\n🔬 TESTING DEEP MODE")
    print("-" * 40)
    
    with open("/mnt/c/Users/Admin/subfracture-langgraph/test_deep_mode.json", "r") as f:
        deep_input = json.load(f)
    
    deep_result = await agent.analyze_transcript(
        brand_brief=deep_input["brand_brief"],
        operator_context=deep_input["operator_context"],
        target_outcome=deep_input["target_outcome"],
        deep_analysis=True
    )
    
    print(f"✅ Deep Analysis Complete")
    print(f"📊 Gravity Index: {deep_result['analysis']['gravity_index']}")
    print(f"🎯 Recommendations: {len(deep_result['analysis']['recommendations'])}")
    
    # Comparison
    print(f"\n📋 MODE COMPARISON")
    print("=" * 40)
    print(f"Standard Mode:")
    print(f"  • Analysis Keys: {list(standard_result['analysis'].keys())}")
    print(f"  • Response Size: {len(str(standard_result))} characters")
    
    print(f"\nDeep Mode:")
    print(f"  • Analysis Keys: {list(deep_result['analysis'].keys())}")
    print(f"  • Response Size: {len(str(deep_result))} characters")
    print(f"  • Additional Insights: {list(deep_result.get('deep_insights', {}).keys())}")
    
    # Save results
    with open("/mnt/c/Users/Admin/subfracture-langgraph/standard_mode_result.json", "w") as f:
        json.dump(standard_result, f, indent=2)
    
    with open("/mnt/c/Users/Admin/subfracture-langgraph/deep_mode_result.json", "w") as f:
        json.dump(deep_result, f, indent=2)
    
    print(f"\n💾 Results saved to standard_mode_result.json and deep_mode_result.json")
    
    print(f"\n🎉 Both analysis modes are now integrated into the SUBFRACTURE agent!")
    print(f"Users can choose between fast insights or comprehensive analysis.")

if __name__ == "__main__":
    asyncio.run(test_both_modes())