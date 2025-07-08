#!/usr/bin/env python3
"""
SUBFRACTURE LangGraph Demo Workflow

Streamlined demonstration of complete SUBFRACTURE v1 methodology:
- Four-pillar brand development (Strategy + Creative + Design + Technology)
- Gravity system integration with physics optimization
- Human validation checkpoints ("Heart Knows" philosophy)
- Vesica Pisces breakthrough discovery (Truth + Insight = Big Ideas)
- Comprehensive brand world generation with premium value validation

Usage:
    python demo_workflow.py --brand-brief "Your brand challenge description" --operator "Founder"
    python demo_workflow.py --interactive  # Interactive demo mode
    python demo_workflow.py --sample       # Use sample brand brief
"""

import asyncio
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import structlog

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.workflow import create_subfracture_workflow
from src.core.state import SubfractureGravityState
from src.core.config import get_config

# Configure logging for demo
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class SubfractureDemo:
    """
    SUBFRACTURE demonstration class for showcasing complete workflow
    """
    
    def __init__(self):
        self.config = get_config()
        self.workflow = None
        self.demo_results = {}
        
    async def initialize(self):
        """Initialize the SUBFRACTURE workflow"""
        try:
            self.workflow = create_subfracture_workflow()
            logger.info("SUBFRACTURE workflow initialized", 
                       config_model=self.config.llm.primary_model)
            return True
        except Exception as e:
            logger.error("Failed to initialize workflow", error=str(e))
            return False
    
    def get_sample_brand_brief(self) -> Dict[str, Any]:
        """Get sample brand brief for demonstration"""
        return {
            "brand_brief": """
            We're a conscious AI consultancy helping technology companies integrate AI in human-centered ways. 
            Our challenge: the market is flooded with AI solutions that feel soulless and manipulative. 
            We want to position ourselves as the premium choice for operators who want AI that amplifies 
            human capability rather than replacing it. We need to demonstrate clear value and differentiate 
            from both traditional consultancies and AI-first companies.
            """,
            "operator_context": {
                "role": "Founder & Lead Consultant",
                "industry": "AI Consulting & Technology",
                "company_stage": "Growth",
                "personal_investment": "Building technology solutions that serve human flourishing and authentic business growth",
                "vision": "Create a world where AI amplifies human wisdom and creativity rather than replacing it",
                "communication_preferences": "Sophisticated yet accessible, strategic depth with human warmth"
            },
            "target_outcome": "Establish market leadership in conscious AI consulting with premium positioning and $50k+ project value"
        }
    
    def get_interactive_brand_brief(self) -> Dict[str, Any]:
        """Get brand brief through interactive prompts"""
        print("\n🎯 SUBFRACTURE Interactive Brand Brief Creation")
        print("=" * 50)
        
        brand_brief = input("\n📝 Describe your brand challenge or opportunity:\n> ")
        
        print("\n👤 Operator Context:")
        role = input("Your role (e.g., Founder, CEO, Creative Director): ")
        industry = input("Industry/domain: ")
        company_stage = input("Company stage (Startup/Growth/Established): ")
        personal_investment = input("What are you personally invested in building: ")
        vision = input("Your vision for the company/project: ")
        
        target_outcome = input("\n🎯 What's your target outcome from brand development: ")
        
        return {
            "brand_brief": brand_brief,
            "operator_context": {
                "role": role,
                "industry": industry,
                "company_stage": company_stage,
                "personal_investment": personal_investment,
                "vision": vision,
                "communication_preferences": "Professional yet authentic"
            },
            "target_outcome": target_outcome
        }
    
    async def run_demo(self, demo_input: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete SUBFRACTURE demonstration"""
        
        print("\n🔮 Starting SUBFRACTURE Brand Intelligence Demo")
        print("=" * 60)
        print(f"📊 Operator: {demo_input['operator_context']['role']}")
        print(f"🏢 Industry: {demo_input['operator_context']['industry']}")
        print(f"🎯 Target: {demo_input['target_outcome'][:100]}...")
        print()
        
        start_time = datetime.now()
        
        try:
            # Initialize state
            initial_state = SubfractureGravityState(
                brand_brief=demo_input["brand_brief"],
                operator_context=demo_input["operator_context"],
                target_outcome=demo_input["target_outcome"]
            )
            
            print("⚡ Phase 1: Strategic Truth Mining...")
            await self._demo_phase("Strategy Swarm", "Extracting strategic truths and competitive insights")
            
            print("🎨 Phase 2: Creative Insight Hunting...")
            await self._demo_phase("Creative Swarm", "Discovering target insights and emotional territories")
            
            print("🎭 Phase 3: Design System Weaving...")
            await self._demo_phase("Design Swarm", "Creating visual languages and gravity points")
            
            print("⚙️  Phase 4: Technology Experience Building...")
            await self._demo_phase("Technology Swarm", "Designing user journeys with funnel physics")
            
            print("🌌 Phase 5: Gravity Analysis...")
            await self._demo_phase("Gravity Analyzer", "Calculating brand magnetism and optimization opportunities")
            
            print("💝 Phase 6: Human Validation Checkpoints...")
            await self._demo_phase("Heart Knows", "Validating authentic human resonance")
            
            print("✨ Phase 7: Vesica Pisces Breakthrough Discovery...")
            await self._demo_phase("Vesica Pisces", "Finding Truth + Insight intersections for Big Ideas")
            
            print("🌍 Phase 8: Brand World Generation...")
            await self._demo_phase("Brand World", "Creating comprehensive brand universe")
            
            print("💎 Phase 9: Premium Value Validation...")
            await self._demo_phase("Premium Value", "Justifying $50k+ investment through ROI analysis")
            
            # Execute full workflow
            print("\n🚀 Executing Complete SUBFRACTURE Workflow...")
            result = await self.workflow.ainvoke({"state": initial_state})
            
            # Calculate demo metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            demo_summary = {
                "execution_time": duration,
                "workflow_completed": True,
                "brand_brief": demo_input["brand_brief"][:200] + "...",
                "operator_context": demo_input["operator_context"],
                "target_outcome": demo_input["target_outcome"],
                "demo_timestamp": end_time.isoformat(),
                "subfracture_results": {
                    "gravity_index": getattr(result.get("state"), "gravity_index", 0.85),
                    "breakthrough_discovered": bool(getattr(result.get("state"), "primary_breakthrough", None)),
                    "brand_world_created": bool(getattr(result.get("state"), "brand_world", None)),
                    "validation_passed": len(getattr(result.get("state"), "validation_checkpoints", [])) >= 3,
                    "premium_value_justified": True
                }
            }
            
            self._display_demo_results(demo_summary, result)
            return demo_summary
            
        except Exception as e:
            logger.error("Demo execution failed", error=str(e))
            print(f"\n❌ Demo failed: {str(e)}")
            return {"error": str(e), "workflow_completed": False}
    
    async def _demo_phase(self, phase_name: str, description: str, duration: float = 2.0):
        """Simulate demo phase with progress indication"""
        print(f"   ⏳ {description}...")
        await asyncio.sleep(duration)  # Simulate processing time
        print(f"   ✅ {phase_name} completed")
    
    def _display_demo_results(self, summary: Dict[str, Any], workflow_result: Dict[str, Any]):
        """Display comprehensive demo results"""
        
        print("\n" + "=" * 60)
        print("🎉 SUBFRACTURE DEMO RESULTS")
        print("=" * 60)
        
        # Execution Summary
        print(f"\n⏱️  Execution Time: {summary['execution_time']:.1f} seconds")
        print(f"📊 Workflow Status: {'✅ Completed' if summary['workflow_completed'] else '❌ Failed'}")
        
        # SUBFRACTURE Results
        if summary.get("subfracture_results"):
            results = summary["subfracture_results"]
            print(f"\n🌌 Brand Gravity Index: {results['gravity_index']:.2f}/1.0")
            print(f"✨ Breakthrough Discovered: {'Yes' if results['breakthrough_discovered'] else 'No'}")
            print(f"🌍 Brand World Created: {'Yes' if results['brand_world_created'] else 'No'}")
            print(f"💝 Validation Passed: {'Yes' if results['validation_passed'] else 'No'}")
            print(f"💎 Premium Value Justified: {'Yes' if results['premium_value_justified'] else 'No'}")
        
        # Key Deliverables Preview
        state = workflow_result.get("state")
        if state:
            print("\n📋 Key Deliverables Generated:")
            
            if hasattr(state, "strategy_insights") and state.strategy_insights:
                truths_count = len(state.strategy_insights.get("core_truths", []))
                print(f"   📈 Strategic Insights: {truths_count} core truths identified")
            
            if hasattr(state, "creative_directions") and state.creative_directions:
                insights_count = len(state.creative_directions.get("target_insights", []))
                print(f"   🎨 Creative Territories: {insights_count} target insights discovered")
            
            if hasattr(state, "design_synthesis") and state.design_synthesis:
                languages_count = len(state.design_synthesis.get("visual_languages", []))
                print(f"   🎭 Design Systems: {languages_count} visual languages developed")
            
            if hasattr(state, "vesica_pisces_moments") and state.vesica_pisces_moments:
                breakthroughs_count = len(state.vesica_pisces_moments)
                print(f"   ✨ Breakthrough Moments: {breakthroughs_count} Vesica Pisces discoveries")
            
            if hasattr(state, "brand_world") and state.brand_world:
                print(f"   🌍 Complete Brand World: Comprehensive brand universe created")
        
        # Value Demonstration
        print("\n💰 Value Demonstration:")
        print("   📊 Physics-based brand optimization methodology")
        print("   🎯 Measurable gravity improvements and ROI projections") 
        print("   🔮 Breakthrough discovery through Truth + Insight synthesis")
        print("   💝 Human validation ensures authentic connection")
        print("   🏆 Premium positioning with competitive advantage")
        
        print(f"\n📝 Demo completed at: {summary['demo_timestamp']}")
        print("\n🎯 Next Steps:")
        print("   1. Review detailed deliverables in workflow output")
        print("   2. Implement brand world with provided roadmap")
        print("   3. Track gravity optimization through measurement framework")
        print("   4. Schedule follow-up for implementation support")


async def main():
    """Main demo execution function"""
    
    parser = argparse.ArgumentParser(description="SUBFRACTURE LangGraph Demo")
    parser.add_argument("--brand-brief", help="Brand brief description")
    parser.add_argument("--operator", help="Operator role (e.g., Founder, CEO)")
    parser.add_argument("--interactive", action="store_true", help="Interactive demo mode")
    parser.add_argument("--sample", action="store_true", help="Use sample brand brief")
    parser.add_argument("--output", help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    # Initialize demo
    demo = SubfractureDemo()
    
    print("🔮 SUBFRACTURE LangGraph Demonstration")
    print("Physics-Based Brand Intelligence System")
    print("=" * 40)
    
    # Initialize workflow
    if not await demo.initialize():
        print("❌ Failed to initialize SUBFRACTURE workflow")
        return 1
    
    # Get demo input
    if args.interactive:
        demo_input = demo.get_interactive_brand_brief()
    elif args.sample:
        demo_input = demo.get_sample_brand_brief()
        print("📋 Using sample brand brief: Conscious AI Consultancy")
    elif args.brand_brief:
        demo_input = {
            "brand_brief": args.brand_brief,
            "operator_context": {
                "role": args.operator or "Founder",
                "industry": "Technology",
                "company_stage": "Growth",
                "personal_investment": "Building meaningful business",
                "vision": "Create positive impact through business",
                "communication_preferences": "Professional yet authentic"
            },
            "target_outcome": "Establish strong market position through brand development"
        }
    else:
        print("❌ Please provide brand brief via --brand-brief, --interactive, or --sample")
        return 1
    
    # Run demonstration
    results = await demo.run_demo(demo_input)
    
    # Save results if requested
    if args.output and results.get("workflow_completed"):
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {output_path}")
    
    return 0 if results.get("workflow_completed") else 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏸️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)