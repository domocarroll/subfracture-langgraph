#!/usr/bin/env python3
"""
SUBFRACTURE Comprehensive Test Suite

Tests complete SUBFRACTURE v1 workflow with multiple brand scenarios.
Validates all four pillars, gravity system, human validation checkpoints,
Vesica Pisces breakthrough discovery, and brand world generation.

Test Categories:
- Unit tests for individual agents
- Integration tests for complete workflow
- Validation tests for human checkpoints
- Performance tests for large-scale execution
- Edge case tests for error handling
"""

import pytest
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.core.workflow import create_subfracture_workflow
from src.core.state import SubfractureGravityState, GravityType
from src.core.config import get_config
from src.agents.strategy_swarm import strategic_truth_discovery
from src.agents.creative_swarm import creative_insight_discovery
from src.agents.design_swarm import visual_gravity_synthesis
from src.agents.technology_swarm import user_experience_optimization
from src.agents.gravity_analyzer import comprehensive_gravity_analysis
from src.validation.heart_knows import intuitive_validation
from src.validation.emotional_resonance import authenticity_assessment
from src.validation.premium_value import boutique_quality_validation
from src.synthesis.vesica_pisces import breakthrough_intersection_finder
from src.synthesis.brand_world import comprehensive_output_creation


class TestSampleBrandBriefs:
    """Sample brand briefs for comprehensive testing"""
    
    @staticmethod
    def get_ai_consultancy_brief() -> Dict[str, Any]:
        """Conscious AI consultancy brand brief"""
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
                "personal_investment": "Building technology solutions that serve human flourishing",
                "vision": "Create a world where AI amplifies human wisdom rather than replacing it",
                "communication_preferences": "Sophisticated yet accessible, strategic depth with human warmth"
            },
            "target_outcome": "Establish market leadership in conscious AI consulting with premium positioning"
        }
    
    @staticmethod
    def get_sustainable_fashion_brief() -> Dict[str, Any]:
        """Sustainable fashion brand brief"""
        return {
            "brand_brief": """
            We're launching a sustainable fashion brand focused on timeless design and ethical production.
            The challenge: sustainable fashion is often seen as expensive, limited in style, or virtue signaling.
            We want to create a brand that makes sustainability aspirational and accessible, showing that
            ethical choices can be both beautiful and economically smart. Our target is conscious consumers
            who value both style and substance.
            """,
            "operator_context": {
                "role": "Creative Director & Co-Founder",
                "industry": "Fashion & Sustainability",
                "company_stage": "Startup",
                "personal_investment": "Creating beautiful products that don't harm the planet",
                "vision": "Make sustainable fashion the obvious choice for conscious consumers",
                "communication_preferences": "Aspirational yet approachable, aesthetic focus with ethical foundation"
            },
            "target_outcome": "Launch with strong brand differentiation and sustainable business model"
        }
    
    @staticmethod
    def get_fintech_startup_brief() -> Dict[str, Any]:
        """FinTech startup brand brief"""
        return {
            "brand_brief": """
            We're building a financial wellness platform that helps people develop healthier relationships with money.
            The challenge: most financial apps focus on tracking and optimization but ignore the emotional and
            psychological aspects of money management. We want to position ourselves as the holistic solution
            that addresses both practical financial management and emotional financial wellness.
            """,
            "operator_context": {
                "role": "CEO & Product Leader",
                "industry": "FinTech & Wellness",
                "company_stage": "Startup",
                "personal_investment": "Helping people build healthier relationships with money",
                "vision": "Transform how people think about and interact with their finances",
                "communication_preferences": "Trustworthy and empathetic, professional yet human"
            },
            "target_outcome": "Differentiate in crowded FinTech market through wellness positioning"
        }
    
    @staticmethod
    def get_b2b_saas_brief() -> Dict[str, Any]:
        """B2B SaaS platform brand brief"""
        return {
            "brand_brief": """
            We're a B2B SaaS platform that helps distributed teams collaborate more effectively through
            intelligent project management and communication tools. The challenge: the market is saturated
            with project management tools, and teams are experiencing tool fatigue. We need to position
            ourselves as the solution that reduces tool complexity while improving actual collaboration outcomes.
            """,
            "operator_context": {
                "role": "VP of Marketing",
                "industry": "B2B SaaS & Productivity",
                "company_stage": "Growth",
                "personal_investment": "Building tools that actually improve how teams work together",
                "vision": "Enable distributed teams to collaborate as effectively as co-located teams",
                "communication_preferences": "Clear and practical, results-focused with human understanding"
            },
            "target_outcome": "Break through tool fatigue and establish leadership in intelligent collaboration"
        }
    
    @staticmethod
    def get_all_sample_briefs() -> List[Dict[str, Any]]:
        """Get all sample brand briefs for testing"""
        return [
            TestSampleBrandBriefs.get_ai_consultancy_brief(),
            TestSampleBrandBriefs.get_sustainable_fashion_brief(),
            TestSampleBrandBriefs.get_fintech_startup_brief(),
            TestSampleBrandBriefs.get_b2b_saas_brief()
        ]


@pytest.fixture
def config():
    """Get test configuration"""
    return get_config()


@pytest.fixture
async def workflow():
    """Create SUBFRACTURE workflow for testing"""
    return create_subfracture_workflow()


@pytest.fixture
def sample_state():
    """Create sample state for testing"""
    brief = TestSampleBrandBriefs.get_ai_consultancy_brief()
    return SubfractureGravityState(
        brand_brief=brief["brand_brief"],
        operator_context=brief["operator_context"],
        target_outcome=brief["target_outcome"]
    )


class TestIndividualAgents:
    """Test individual SUBFRACTURE agents"""
    
    @pytest.mark.asyncio
    async def test_strategy_swarm_execution(self, sample_state):
        """Test strategy swarm agent execution"""
        
        result = await strategic_truth_discovery(sample_state)
        
        assert "strategic_insights" in result
        assert "core_truths" in result["strategic_insights"]
        assert len(result["strategic_insights"]["core_truths"]) >= 3
        assert "strategic_summary" in result["strategic_insights"]
        
        # Validate strategic insights quality
        core_truths = result["strategic_insights"]["core_truths"]
        assert any("AI" in truth for truth in core_truths)  # Should contain industry insights
        assert any("human" in truth.lower() for truth in core_truths)  # Should reflect human-centered approach
    
    @pytest.mark.asyncio
    async def test_creative_swarm_execution(self, sample_state):
        """Test creative swarm agent execution"""
        
        # Add strategy insights to state for creative swarm
        sample_state.strategy_insights = {
            "core_truths": ["AI should amplify human capability", "Market seeks authentic solutions"],
            "strategic_summary": {"competitive_advantage": "Human-centered AI approach"}
        }
        
        result = await creative_insight_discovery(sample_state)
        
        assert "creative_directions" in result
        assert "target_insights" in result["creative_directions"]
        assert "creative_territories" in result["creative_directions"]
        assert len(result["creative_directions"]["target_insights"]) >= 3
        
        # Validate creative insights relevance
        insights = result["creative_directions"]["target_insights"]
        assert any("technology" in insight.lower() for insight in insights)
    
    @pytest.mark.asyncio
    async def test_design_swarm_execution(self, sample_state):
        """Test design swarm agent execution"""
        
        # Add prerequisite state
        sample_state.strategy_insights = {"core_truths": ["Human-centered AI"]}
        sample_state.creative_directions = {"target_insights": ["Seeking authentic solutions"]}
        
        result = await visual_gravity_synthesis(sample_state)
        
        assert "design_synthesis" in result
        assert "visual_languages" in result["design_synthesis"]
        assert "verbal_frameworks" in result["design_synthesis"]
        assert len(result["design_synthesis"]["visual_languages"]) >= 2
    
    @pytest.mark.asyncio
    async def test_technology_swarm_execution(self, sample_state):
        """Test technology swarm agent execution"""
        
        # Add prerequisite state
        sample_state.strategy_insights = {"core_truths": ["Human-centered approach"]}
        sample_state.creative_directions = {"target_insights": ["Technology anxiety"]}
        sample_state.design_synthesis = {"visual_languages": ["Professional warmth"]}
        
        result = await user_experience_optimization(sample_state)
        
        assert "technology_roadmap" in result
        assert "user_journeys" in result["technology_roadmap"]
        assert "funnel_physics" in result
        assert len(result["technology_roadmap"]["user_journeys"]) >= 2
    
    @pytest.mark.asyncio
    async def test_gravity_analyzer_execution(self, sample_state):
        """Test gravity analyzer agent execution"""
        
        # Add full prerequisite state
        sample_state.strategy_insights = {"core_truths": ["Human-centered AI"]}
        sample_state.creative_directions = {"target_insights": ["Authentic solutions"]}
        sample_state.design_synthesis = {"visual_languages": ["Professional warmth"]}
        sample_state.technology_roadmap = {"user_journeys": ["Discovery to trust"]}
        
        result = await comprehensive_gravity_analysis(sample_state)
        
        assert "gravity_analysis" in result
        assert "gravity_index" in result
        assert "world_rules" in result
        
        # Validate gravity types
        gravity_analysis = result["gravity_analysis"]
        for gravity_type in GravityType:
            assert gravity_type in gravity_analysis
            assert 0 <= gravity_analysis[gravity_type] <= 1
        
        # Validate overall gravity index
        assert 0 <= result["gravity_index"] <= 1


class TestValidationModules:
    """Test human validation modules"""
    
    @pytest.mark.asyncio
    async def test_heart_knows_validation(self, sample_state):
        """Test Heart Knows intuitive validation"""
        
        # Add prerequisite state
        sample_state.strategy_insights = {"core_truths": ["Human-centered AI"]}
        sample_state.creative_directions = {"target_insights": ["Authentic solutions"]}
        
        result = await intuitive_validation(sample_state)
        
        assert "intuitive_validation" in result
        assert "heart_knows_confidence" in result["intuitive_validation"]
        assert "validation_decision" in result["intuitive_validation"]
        assert 0 <= result["intuitive_validation"]["heart_knows_confidence"] <= 1
    
    @pytest.mark.asyncio
    async def test_emotional_resonance_validation(self, sample_state):
        """Test emotional resonance validation"""
        
        # Add prerequisite state
        sample_state.creative_directions = {"target_insights": ["Seeking authenticity"]}
        sample_state.design_synthesis = {"verbal_frameworks": ["Human-centered language"]}
        
        result = await authenticity_assessment(sample_state)
        
        assert "emotional_resonance" in result
        assert "authenticity_score" in result["emotional_resonance"]
        assert "validation_decision" in result["emotional_resonance"]
        assert 0 <= result["emotional_resonance"]["authenticity_score"] <= 1
    
    @pytest.mark.asyncio
    async def test_premium_value_validation(self, sample_state):
        """Test premium value validation"""
        
        # Add prerequisite state
        sample_state.gravity_index = 0.75
        sample_state.gravity_analysis = {GravityType.RECOGNITION: 0.8}
        sample_state.strategy_insights = {"core_truths": ["Unique methodology"]}
        
        result = await boutique_quality_validation(sample_state)
        
        assert "premium_value_validation" in result
        assert "value_confidence" in result["premium_value_validation"]
        assert "estimated_value" in result["premium_value_validation"]
        assert 0 <= result["premium_value_validation"]["value_confidence"] <= 1


class TestSynthesisModules:
    """Test synthesis modules"""
    
    @pytest.mark.asyncio
    async def test_vesica_pisces_synthesis(self, sample_state):
        """Test Vesica Pisces breakthrough discovery"""
        
        # Add prerequisite state
        sample_state.strategy_insights = {
            "core_truths": ["Human-centered AI", "Market seeks authenticity"]
        }
        sample_state.creative_directions = {
            "target_insights": ["Technology anxiety", "Desire for genuine solutions"]
        }
        sample_state.design_synthesis = {"visual_languages": ["Professional warmth"]}
        sample_state.technology_roadmap = {"user_journeys": ["Trust building"]}
        
        result = await breakthrough_intersection_finder(sample_state)
        
        assert "vesica_pisces_synthesis" in result
        assert "primary_breakthrough" in result["vesica_pisces_synthesis"]
        assert "breakthrough_intersections" in result["vesica_pisces_synthesis"]
        
        # Validate breakthrough quality
        primary_breakthrough = result["vesica_pisces_synthesis"]["primary_breakthrough"]
        assert "breakthrough_strength" in primary_breakthrough
        assert 0 <= primary_breakthrough["breakthrough_strength"] <= 1
    
    @pytest.mark.asyncio
    async def test_brand_world_generation(self, sample_state):
        """Test brand world generation"""
        
        # Add full prerequisite state
        sample_state.strategy_insights = {"core_truths": ["Human-centered AI"]}
        sample_state.creative_directions = {"target_insights": ["Authentic solutions"]}
        sample_state.design_synthesis = {"visual_languages": ["Professional warmth"]}
        sample_state.technology_roadmap = {"user_journeys": ["Trust building"]}
        sample_state.gravity_index = 0.75
        sample_state.gravity_analysis = {GravityType.RECOGNITION: 0.8}
        sample_state.primary_breakthrough = {
            "primary_breakthrough_concept": "Human-AI Collaboration",
            "breakthrough_strength": 0.8
        }
        
        result = await comprehensive_output_creation(sample_state)
        
        assert "brand_world_package" in result
        assert "brand_world" in result["brand_world_package"]
        assert "implementation_plan" in result["brand_world_package"]
        
        # Validate brand world completeness
        brand_world = result["brand_world_package"]["brand_world"]
        assert "brand_world_overview" in brand_world
        assert "strategic_foundation" in brand_world
        assert "deliverables_summary" in brand_world


class TestCompleteWorkflows:
    """Test complete workflow execution with different brand briefs"""
    
    @pytest.mark.asyncio
    async def test_ai_consultancy_workflow(self, workflow):
        """Test complete workflow with AI consultancy brief"""
        
        brief = TestSampleBrandBriefs.get_ai_consultancy_brief()
        initial_state = SubfractureGravityState(
            brand_brief=brief["brand_brief"],
            operator_context=brief["operator_context"],
            target_outcome=brief["target_outcome"]
        )
        
        result = await workflow.ainvoke({"state": initial_state})
        
        assert result is not None
        assert "state" in result
        
        final_state = result["state"]
        assert hasattr(final_state, "brand_world")
        assert hasattr(final_state, "gravity_index")
        assert hasattr(final_state, "primary_breakthrough")
        
        # Validate workflow completeness
        assert final_state.gravity_index > 0
        assert len(final_state.validation_checkpoints) >= 3
    
    @pytest.mark.asyncio
    async def test_sustainable_fashion_workflow(self, workflow):
        """Test complete workflow with sustainable fashion brief"""
        
        brief = TestSampleBrandBriefs.get_sustainable_fashion_brief()
        initial_state = SubfractureGravityState(
            brand_brief=brief["brand_brief"],
            operator_context=brief["operator_context"],
            target_outcome=brief["target_outcome"]
        )
        
        result = await workflow.ainvoke({"state": initial_state})
        
        assert result is not None
        final_state = result["state"]
        
        # Validate industry-specific insights
        assert hasattr(final_state, "strategy_insights")
        if final_state.strategy_insights:
            core_truths = final_state.strategy_insights.get("core_truths", [])
            assert any("sustainable" in truth.lower() for truth in core_truths)
    
    @pytest.mark.asyncio
    async def test_fintech_workflow(self, workflow):
        """Test complete workflow with FinTech brief"""
        
        brief = TestSampleBrandBriefs.get_fintech_startup_brief()
        initial_state = SubfractureGravityState(
            brand_brief=brief["brand_brief"],
            operator_context=brief["operator_context"],
            target_outcome=brief["target_outcome"]
        )
        
        result = await workflow.ainvoke({"state": initial_state})
        
        assert result is not None
        final_state = result["state"]
        
        # Validate trust gravity should be high for FinTech
        if hasattr(final_state, "gravity_analysis") and final_state.gravity_analysis:
            trust_gravity = final_state.gravity_analysis.get(GravityType.TRUST, 0)
            assert trust_gravity > 0.5  # Trust should be prioritized for FinTech
    
    @pytest.mark.asyncio
    async def test_b2b_saas_workflow(self, workflow):
        """Test complete workflow with B2B SaaS brief"""
        
        brief = TestSampleBrandBriefs.get_b2b_saas_brief()
        initial_state = SubfractureGravityState(
            brand_brief=brief["brand_brief"],
            operator_context=brief["operator_context"],
            target_outcome=brief["target_outcome"]
        )
        
        result = await workflow.ainvoke({"state": initial_state})
        
        assert result is not None
        final_state = result["state"]
        
        # Validate comprehension gravity should be high for B2B
        if hasattr(final_state, "gravity_analysis") and final_state.gravity_analysis:
            comprehension_gravity = final_state.gravity_analysis.get(GravityType.COMPREHENSION, 0)
            assert comprehension_gravity > 0.5  # Clear communication critical for B2B


class TestPerformanceAndEdgeCases:
    """Test performance and edge cases"""
    
    @pytest.mark.asyncio
    async def test_minimal_brand_brief(self, workflow):
        """Test workflow with minimal brand brief"""
        
        minimal_state = SubfractureGravityState(
            brand_brief="We need better brand positioning",
            operator_context={"role": "Founder"},
            target_outcome="Improve market position"
        )
        
        # Should complete without errors even with minimal input
        result = await workflow.ainvoke({"state": minimal_state})
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_complex_brand_brief(self, workflow):
        """Test workflow with complex, detailed brand brief"""
        
        complex_brief = """
        We are a multi-stakeholder cooperative developing regenerative agriculture technology 
        that combines IoT sensors, machine learning, and traditional farming wisdom to help 
        small-scale farmers increase yields while improving soil health. Our challenge is 
        that we operate in a complex ecosystem with farmers, investors, technology partners, 
        and environmental organizations, each with different values and communication preferences. 
        We need a brand that can speak authentically to all stakeholders while maintaining 
        our core mission of environmental regeneration and social justice.
        """
        
        complex_state = SubfractureGravityState(
            brand_brief=complex_brief,
            operator_context={
                "role": "Cooperative Director",
                "industry": "AgTech & Sustainability",
                "company_stage": "Growth",
                "personal_investment": "Regenerative agriculture and social justice",
                "vision": "Transform agriculture to heal the planet and support farmers",
                "communication_preferences": "Authentic, inclusive, scientifically grounded"
            },
            target_outcome="Unite diverse stakeholders around shared regenerative vision"
        )
        
        result = await workflow.ainvoke({"state": complex_state})
        assert result is not None
        
        # Complex brief should generate rich insights
        final_state = result["state"]
        if hasattr(final_state, "strategy_insights") and final_state.strategy_insights:
            core_truths = final_state.strategy_insights.get("core_truths", [])
            assert len(core_truths) >= 3  # Should extract multiple truths from complex brief
    
    @pytest.mark.asyncio
    async def test_workflow_error_handling(self, workflow):
        """Test workflow error handling"""
        
        # Test with invalid state structure
        try:
            invalid_state = SubfractureGravityState(
                brand_brief="",  # Empty brief
                operator_context={},  # Empty context
                target_outcome=""  # Empty outcome
            )
            
            result = await workflow.ainvoke({"state": invalid_state})
            # Should handle gracefully rather than crashing
            assert result is not None
        except Exception as e:
            # If it does throw an exception, it should be informative
            assert str(e) is not None


class TestMetrics:
    """Test metrics and quality assessment"""
    
    @pytest.mark.asyncio
    async def test_gravity_index_consistency(self):
        """Test that gravity index calculations are consistent"""
        
        brief = TestSampleBrandBriefs.get_ai_consultancy_brief()
        
        # Run workflow multiple times
        gravity_indices = []
        for _ in range(3):
            workflow = create_subfracture_workflow()
            initial_state = SubfractureGravityState(
                brand_brief=brief["brand_brief"],
                operator_context=brief["operator_context"],
                target_outcome=brief["target_outcome"]
            )
            
            result = await workflow.ainvoke({"state": initial_state})
            final_state = result["state"]
            gravity_indices.append(final_state.gravity_index)
        
        # Gravity indices should be similar (within 0.2 range)
        gravity_range = max(gravity_indices) - min(gravity_indices)
        assert gravity_range <= 0.2
    
    @pytest.mark.asyncio
    async def test_breakthrough_quality_assessment(self):
        """Test breakthrough discovery quality"""
        
        brief = TestSampleBrandBriefs.get_sustainable_fashion_brief()
        workflow = create_subfracture_workflow()
        initial_state = SubfractureGravityState(
            brand_brief=brief["brand_brief"],
            operator_context=brief["operator_context"],
            target_outcome=brief["target_outcome"]
        )
        
        result = await workflow.ainvoke({"state": initial_state})
        final_state = result["state"]
        
        if hasattr(final_state, "primary_breakthrough") and final_state.primary_breakthrough:
            breakthrough = final_state.primary_breakthrough
            
            # Breakthrough should have key components
            assert "primary_breakthrough_concept" in breakthrough
            assert "breakthrough_strength" in breakthrough
            assert breakthrough["breakthrough_strength"] > 0.5  # Should be reasonably strong
    
    def test_sample_brief_quality(self):
        """Test that sample briefs meet quality standards"""
        
        briefs = TestSampleBrandBriefs.get_all_sample_briefs()
        
        for brief in briefs:
            # Each brief should have required components
            assert "brand_brief" in brief
            assert "operator_context" in brief
            assert "target_outcome" in brief
            
            # Brand brief should be substantial
            assert len(brief["brand_brief"]) > 100
            
            # Operator context should have key fields
            assert "role" in brief["operator_context"]
            assert "industry" in brief["operator_context"]
            assert "vision" in brief["operator_context"]
            
            # Target outcome should be clear
            assert len(brief["target_outcome"]) > 20


# Test execution utilities
def run_performance_test():
    """Run performance test with timing"""
    
    async def performance_test():
        start_time = datetime.now()
        
        brief = TestSampleBrandBriefs.get_ai_consultancy_brief()
        workflow = create_subfracture_workflow()
        initial_state = SubfractureGravityState(
            brand_brief=brief["brand_brief"],
            operator_context=brief["operator_context"],
            target_outcome=brief["target_outcome"]
        )
        
        result = await workflow.ainvoke({"state": initial_state})
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"Workflow execution time: {duration:.2f} seconds")
        return duration, result
    
    return asyncio.run(performance_test())


if __name__ == "__main__":
    # Run specific tests or performance evaluation
    import argparse
    
    parser = argparse.ArgumentParser(description="SUBFRACTURE Test Suite")
    parser.add_argument("--performance", action="store_true", help="Run performance test")
    parser.add_argument("--brief", choices=["ai", "fashion", "fintech", "saas"], 
                       help="Test specific brief type")
    
    args = parser.parse_args()
    
    if args.performance:
        duration, result = run_performance_test()
        print(f"Performance test completed in {duration:.2f}s")
        
    elif args.brief:
        brief_map = {
            "ai": TestSampleBrandBriefs.get_ai_consultancy_brief,
            "fashion": TestSampleBrandBriefs.get_sustainable_fashion_brief,
            "fintech": TestSampleBrandBriefs.get_fintech_startup_brief,
            "saas": TestSampleBrandBriefs.get_b2b_saas_brief
        }
        
        async def test_specific_brief():
            brief = brief_map[args.brief]()
            workflow = create_subfracture_workflow()
            initial_state = SubfractureGravityState(
                brand_brief=brief["brand_brief"],
                operator_context=brief["operator_context"],
                target_outcome=brief["target_outcome"]
            )
            
            result = await workflow.ainvoke({"state": initial_state})
            print(f"Test completed for {args.brief} brief")
            return result
        
        asyncio.run(test_specific_brief())
        
    else:
        # Run pytest
        pytest.main([__file__, "-v"])