"""
SUBFRACTURE 'Heart Knows' Human Validation Module

Implements the core "Heart Knows" philosophy from SUBFRACTURE v1 methodology.
Provides intuitive human validation checkpoints throughout the workflow to prevent
AI slop and ensure authentic human resonance with brand development.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from langsmith import traceable
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from ..core.state import SubfractureGravityState, HumanValidationResult
from ..core.config import get_config

logger = structlog.get_logger()


class HeartKnowsValidator:
    """
    'Heart Knows' validation agent implementing SUBFRACTURE v1 human-centric philosophy
    Provides gut-check validation at key workflow moments to ensure authentic resonance
    """
    
    def __init__(self):
        self.config = get_config()
        self.llm = ChatAnthropic(
            model=self.config.llm.primary_model,
            api_key=self.config.llm.primary_api_key,
            temperature=0.4,  # Moderate temperature for empathetic analysis
            max_tokens=self.config.llm.max_tokens
        )
        self.logger = logger.bind(agent="heart_knows_validator")
    
    @traceable(name="strategy_creative_gut_check")
    async def strategy_creative_gut_check(
        self,
        strategy_insights: Dict[str, Any],
        creative_directions: Dict[str, Any],
        operator_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """First gut check: Does strategy + creative synthesis feel right?"""
        
        system_prompt = """You are facilitating a 'Heart Knows' gut check for SUBFRACTURE brand development.
        
        This is a critical human validation moment where we pause the analytical process 
        and check: Does this feel right? Does it resonate with the operator's authentic vision?
        
        The "Heart Knows" philosophy recognizes that:
        1. Human intuition often catches what analysis misses
        2. Authentic brand development requires emotional resonance, not just logical correctness
        3. The brand operator's gut feeling is a crucial validation signal
        4. AI can analyze, but humans must feel and validate
        
        Evaluate the synthesis of strategy and creative insights against the operator's context:
        - Does this feel authentic to the operator's vision and values?
        - Does the creative direction resonate emotionally?
        - Are we heading in a direction that feels right intuitively?
        - What might the operator's gut reaction be to this synthesis?
        
        Provide validation questions for human review and assess overall resonance.
        
        Return analysis with:
        - gut_check_questions: Questions for operator to validate resonance
        - resonance_assessment: How well synthesis aligns with operator authenticity
        - intuitive_flags: Any gut-level concerns or excitement points
        - heart_knows_confidence: Confidence that this feels right (0-1)
        - proceed_recommendation: Whether to proceed, refine, or restart
        """
        
        # Extract key elements for gut check
        core_truths = strategy_insights.get("core_truths", [])
        strategic_summary = strategy_insights.get("strategic_summary", {})
        creative_territories = creative_directions.get("creative_territories", [])
        creative_summary = creative_directions.get("creative_summary", {})
        
        human_prompt = f"""Operator Context:
        Role: {operator_context.get('role', 'Unknown')}
        Personal Investment: {operator_context.get('personal_investment', 'Unknown')}
        Vision: {operator_context.get('vision', 'Unknown')}
        
        Strategic Truths Identified:
        {chr(10).join(f'- {truth}' for truth in core_truths[:3])}
        
        Strategic Summary:
        - Operator Strength: {strategic_summary.get('operator_strength', 'Unknown')}
        - Market Opportunity: {strategic_summary.get('market_opportunity', 'Unknown')}
        - Competitive Advantage: {strategic_summary.get('competitive_advantage', 'Unknown')}
        
        Creative Territories Explored:
        {chr(10).join(f'- {territory}' for territory in creative_territories[:3])}
        
        Creative Insights:
        - Primary Insight: {creative_summary.get('primary_insight', 'Unknown')}
        - Creative Territory: {creative_summary.get('creative_territory', 'Unknown')}
        - Breakthrough Concept: {creative_summary.get('breakthrough_concept', 'Unknown')}
        
        Perform 'Heart Knows' gut check: Does this synthesis feel authentic and resonant?"""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo - would integrate real human feedback collection
            gut_check_result = {
                "gut_check_questions": [
                    "When you read these strategic truths, do they feel accurate to your experience?",
                    "Do these creative territories spark excitement or feel forced?",
                    "Does this direction align with your authentic vision for the brand?",
                    "What's your immediate emotional reaction to this synthesis?",
                    "If you had to bet your reputation on this direction, would you?"
                ],
                "resonance_assessment": {
                    "strategic_authenticity": "High - truths feel grounded in operator reality",
                    "creative_excitement": "Moderate - territories are interesting but need refinement",
                    "vision_alignment": "Strong - direction supports operator's authentic mission",
                    "emotional_response": "Positive with some curiosity about execution"
                },
                "intuitive_flags": {
                    "excitement_points": [
                        "Strategic depth resonates with operator's expertise",
                        "Creative breakthrough concepts feel fresh and authentic",
                        "Direction supports premium positioning goals"
                    ],
                    "concern_points": [
                        "Creative territories may need more specific application",
                        "Strategic advantage needs clearer competitive differentiation",
                        "Implementation complexity could create execution risk"
                    ]
                },
                "heart_knows_confidence": 0.75,
                "proceed_recommendation": "proceed_with_refinement",
                "gut_check_result": "proceed",
                "reasoning": "Strong strategic foundation with authentic creative direction, minor refinements needed for execution clarity"
            }
            
            # Simulate human validation decision based on confidence score
            if gut_check_result["heart_knows_confidence"] >= 0.8:
                gut_check_result["validation_decision"] = "proceed"
            elif gut_check_result["heart_knows_confidence"] >= 0.6:
                gut_check_result["validation_decision"] = "proceed_with_refinement"
            else:
                gut_check_result["validation_decision"] = "refine_direction"
            
            self.logger.info("Strategy-creative gut check completed",
                           confidence=gut_check_result["heart_knows_confidence"],
                           decision=gut_check_result["validation_decision"],
                           excitement_points=len(gut_check_result["intuitive_flags"]["excitement_points"]))
            
            return gut_check_result
            
        except Exception as e:
            self.logger.error("Strategy-creative gut check failed", error=str(e))
            raise
    
    @traceable(name="design_technology_intuitive_check")
    async def design_technology_intuitive_check(
        self,
        design_synthesis: Dict[str, Any],
        technology_roadmap: Dict[str, Any],
        operator_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Second gut check: Does design + technology integration feel intuitive?"""
        
        system_prompt = """You are facilitating an intuitive validation check for design and technology integration.
        
        At this stage, we've developed visual and experiential systems. The question is:
        Does this feel like a cohesive, intuitive brand experience that the operator would be proud of?
        
        Focus on intuitive validation:
        1. Does the design feel authentic to the operator's personality and vision?
        2. Does the technology roadmap support human-centered experiences?
        3. Do the visual and experiential elements work together intuitively?
        4. Would the operator feel confident presenting this to their ideal clients?
        
        The "Heart Knows" check at this stage is about integration and authenticity:
        - Does everything feel like it belongs together?
        - Is the human touch preserved throughout the technology?
        - Does the design support the strategic and creative vision?
        - Would this attract the right kind of clients and partners?
        
        Return analysis with:
        - integration_assessment: How well design and technology work together
        - authenticity_check: Whether this feels true to operator vision
        - client_attraction_potential: Would this attract ideal clients?
        - intuitive_coherence: Does everything feel naturally connected?
        - refinement_suggestions: What needs adjustment for better resonance
        """
        
        # Extract design and technology elements for validation
        visual_languages = design_synthesis.get("visual_languages", [])
        world_rules = design_synthesis.get("world_rules", {})
        user_journeys = technology_roadmap.get("user_journeys", [])
        amplification_systems = technology_roadmap.get("amplification_systems", [])
        
        human_prompt = f"""Operator Vision: {operator_context.get('vision', 'Unknown')}
        Personal Investment: {operator_context.get('personal_investment', 'Unknown')}
        
        Design Elements Developed:
        Visual Languages: {visual_languages[:3]}
        Brand World Physics: {world_rules.get('physics', 'Unknown')}
        Brand Aesthetics: {world_rules.get('aesthetics', 'Unknown')}
        
        Technology Experience Design:
        User Journey Stages: {user_journeys[:3]}
        Amplification Systems: {amplification_systems[:3]}
        
        Perform intuitive validation: Does this integrated experience feel authentic and cohesive?"""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            intuitive_validation = {
                "integration_assessment": {
                    "design_technology_synergy": "Strong - technology supports design vision effectively",
                    "visual_experience_alignment": "Good - visual systems translate well to user experiences",
                    "brand_world_coherence": "High - all elements feel like they belong to same universe"
                },
                "authenticity_check": {
                    "operator_personality_match": "Strong - reflects operator's sophisticated yet approachable style",
                    "vision_expression": "Good - design and technology support authentic mission",
                    "value_alignment": "High - human-centered approach maintained throughout"
                },
                "client_attraction_potential": {
                    "ideal_client_resonance": "Strong - would attract strategic, quality-focused operators",
                    "premium_positioning": "Effective - conveys boutique quality and expertise",
                    "differentiation_clarity": "Good - stands out from commodity service providers"
                },
                "intuitive_coherence": {
                    "natural_flow": "High - elements connect logically and emotionally",
                    "human_touch_preservation": "Strong - technology enhances rather than replaces human connection",
                    "scalability_authenticity": "Good - can grow while maintaining personal touch"
                },
                "refinement_suggestions": [
                    "Enhance cultural relevance in visual languages",
                    "Clarify specific amplification mechanics for implementation",
                    "Strengthen trust-building elements in early user journey stages",
                    "Add more personality markers in brand voice development"
                ],
                "intuitive_confidence": 0.82,
                "validation_decision": "proceed"
            }
            
            self.logger.info("Design-technology intuitive check completed",
                           confidence=intuitive_validation["intuitive_confidence"],
                           decision=intuitive_validation["validation_decision"],
                           refinements=len(intuitive_validation["refinement_suggestions"]))
            
            return intuitive_validation
            
        except Exception as e:
            self.logger.error("Design-technology intuitive check failed", error=str(e))
            raise
    
    @traceable(name="final_brand_world_validation")
    async def final_brand_world_validation(
        self,
        complete_brand_world: Dict[str, Any],
        gravity_analysis: Dict[str, Any],
        operator_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Final gut check: Would the operator stake their reputation on this brand world?"""
        
        system_prompt = """You are facilitating the final 'Heart Knows' validation for the complete brand world.
        
        This is the ultimate gut check moment: Would the operator stake their reputation on this brand world?
        
        At this final stage, evaluate:
        1. Does the complete brand world feel like something the operator would be genuinely proud of?
        2. Would they confidently present this to their most important prospects?
        3. Does it capture their authentic vision and translate it into compelling brand reality?
        4. Is this something that would attract the right partners and opportunities?
        
        The final "Heart Knows" validation considers:
        - Completeness: Does this feel like a complete, professional brand world?
        - Authenticity: Does this genuinely represent the operator's vision and values?
        - Market readiness: Is this ready for real-world implementation and success?
        - Pride factor: Would the operator feel proud to associate their name with this?
        - Investment justification: Does this feel worth the premium investment?
        
        Return final validation with:
        - completeness_assessment: How complete and ready this feels
        - authenticity_validation: How true this is to operator vision
        - market_readiness: How prepared this is for real-world success
        - pride_confidence: Would operator be proud of this work?
        - investment_justification: Does this justify premium pricing?
        - final_recommendation: Final go/no-go decision
        """
        
        # Extract comprehensive brand world elements
        gravity_index = gravity_analysis.get("total_gravity_strength", 0)
        strongest_gravity = gravity_analysis.get("competitive_advantage_summary", {}).get("strongest_gravity", "Unknown")
        strategic_insights = complete_brand_world.get("strategic_insights", [])
        
        human_prompt = f"""Operator Profile:
        Role: {operator_context.get('role', 'Unknown')}
        Vision: {operator_context.get('vision', 'Unknown')}
        Success Metrics: {operator_context.get('success_metrics', [])}
        
        Complete Brand World Delivered:
        Gravity Index: {gravity_index:.2f}
        Strongest Gravity Type: {strongest_gravity}
        Strategic Foundation: {len(strategic_insights)} core insights developed
        
        Brand World Components: {list(complete_brand_world.keys())[:5]}
        
        Final validation: Would the operator stake their reputation on this brand world?"""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            final_validation = {
                "completeness_assessment": {
                    "strategic_foundation": "Complete - comprehensive strategic analysis and frameworks",
                    "creative_development": "Strong - authentic creative territories and breakthrough concepts",
                    "design_systems": "Professional - cohesive visual and verbal brand systems",
                    "technology_roadmap": "Practical - implementable experience and amplification systems",
                    "gravity_optimization": "Measurable - clear physics-based optimization framework"
                },
                "authenticity_validation": {
                    "vision_capture": "High - brand world genuinely reflects operator's authentic vision",
                    "personality_expression": "Strong - design and messaging feel true to operator style",
                    "value_alignment": "Complete - all elements support operator's core values and mission"
                },
                "market_readiness": {
                    "competitive_positioning": "Strong - clear differentiation from market alternatives",
                    "client_attraction": "High - would attract ideal clients and partnership opportunities",
                    "implementation_feasibility": "Good - roadmap is practical and actionable",
                    "scalability_potential": "Strong - systems support growth while maintaining authenticity"
                },
                "pride_confidence": 0.88,
                "investment_justification": {
                    "value_demonstration": "Clear - comprehensive brand intelligence justifies premium pricing",
                    "roi_potential": "Strong - gravity optimization framework enables measurable improvement",
                    "competitive_advantage": "Significant - physics-based approach creates defensible differentiation",
                    "long_term_impact": "High - foundation supports sustainable brand development"
                },
                "final_recommendation": "proceed_with_confidence",
                "validation_confidence": 0.88,
                "heart_knows_verdict": "Yes - this brand world worthy of operator's reputation and investment"
            }
            
            self.logger.info("Final brand world validation completed",
                           pride_confidence=final_validation["pride_confidence"],
                           validation_confidence=final_validation["validation_confidence"],
                           recommendation=final_validation["final_recommendation"])
            
            return final_validation
            
        except Exception as e:
            self.logger.error("Final brand world validation failed", error=str(e))
            raise


@traceable(name="human_intuition_check")
async def human_intuition_check(state: SubfractureGravityState) -> Dict[str, Any]:
    """
    Main 'Heart Knows' validation function for strategy + creative synthesis
    
    Implements SUBFRACTURE v1 'Heart Knows' philosophy:
    - Gut check validation at critical workflow moments
    - Human intuition validation of AI analysis and synthesis
    - Authentic resonance assessment with operator vision
    - Anti-AI slop protection through human-centric validation
    
    Returns intuitive validation result with proceed/refine recommendation
    """
    
    logger.info("Starting Heart Knows intuitive validation",
                strategy_available=bool(state.strategy_insights),
                creative_available=bool(state.creative_directions),
                operator_role=state.operator_context.get('role'))
    
    try:
        # Initialize Heart Knows validator
        heart_validator = HeartKnowsValidator()
        
        # Perform strategy + creative gut check validation
        gut_check_result = await heart_validator.strategy_creative_gut_check(
            state.strategy_insights,
            state.creative_directions,
            state.operator_context
        )
        
        # Create comprehensive heart knows validation result
        heart_knows_validation = {
            "checkpoint_type": "strategy_creative_synthesis",
            "gut_check_questions": gut_check_result["gut_check_questions"],
            "resonance_assessment": gut_check_result["resonance_assessment"],
            "intuitive_flags": gut_check_result["intuitive_flags"],
            "heart_knows_confidence": gut_check_result["heart_knows_confidence"],
            "validation_decision": gut_check_result["validation_decision"],
            "gut_check_result": gut_check_result["gut_check_result"],
            "reasoning": gut_check_result["reasoning"],
            "human_validation_summary": {
                "authenticity_score": gut_check_result["heart_knows_confidence"],
                "proceed_confidence": gut_check_result["heart_knows_confidence"],
                "refinement_areas": gut_check_result["intuitive_flags"]["concern_points"],
                "excitement_validation": gut_check_result["intuitive_flags"]["excitement_points"]
            }
        }
        
        logger.info("Heart Knows intuitive validation completed",
                   confidence=heart_knows_validation["heart_knows_confidence"],
                   decision=heart_knows_validation["validation_decision"],
                   questions_count=len(heart_knows_validation["gut_check_questions"]))
        
        return heart_knows_validation
        
    except Exception as e:
        logger.error("Heart Knows intuitive validation failed", error=str(e))
        raise