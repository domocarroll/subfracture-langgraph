"""
SUBFRACTURE Strategy Swarm - Truth Mining Agent

Implements the Strategy pillar from SUBFRACTURE v1 four-pillar methodology.
Extracts strategic truths about brand/product/company to form the TRUTH
component of the Vesica Pisces engine (Truth + Insight = Big Ideas).
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from langsmith import traceable
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from ..core.state import SubfractureGravityState
from ..core.config import get_config

logger = structlog.get_logger()


class StrategyTruthMiner:
    """
    Strategy truth mining agent implementing SUBFRACTURE v1 methodology
    Focuses on extracting compelling facts about brand/product/company
    """
    
    def __init__(self):
        self.config = get_config()
        self.llm = ChatAnthropic(
            model=self.config.llm.primary_model,
            api_key=self.config.llm.primary_api_key,
            temperature=0.3,  # Lower temperature for strategic analysis
            max_tokens=self.config.llm.max_tokens
        )
        self.logger = logger.bind(agent="strategy_swarm")
    
    @traceable(name="extract_founder_vision")
    async def extract_founder_vision(self, operator_context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract strategic truths from founder/operator personal investment"""
        
        system_prompt = """You are a strategic truth mining expert from SUBFRACTURE's Strategy Swarm.
        
        Your role is to extract compelling TRUTHS about the brand from the brand operator's context.
        These truths will form the TRUTH component of the Vesica Pisces engine (Truth + Insight = Big Ideas).
        
        Focus on:
        - Authentic founder/operator vision and personal investment
        - Unique strategic advantages and capabilities
        - Market position and competitive differentiation
        - Core value propositions that ring true
        
        Extract truths that are:
        1. Compelling and emotionally resonant
        2. Factually grounded and defendable
        3. Strategically differentiated from competition
        4. Aligned with operator's personal mission
        
        Return your analysis as a structured JSON with these keys:
        - operator_truth: Personal vision and investment truth
        - capability_truth: What the brand/company genuinely excels at
        - market_truth: Authentic market position and opportunity
        - values_truth: Core values that drive decisions
        - confidence_score: How confident you are in these truths (0-1)
        """
        
        human_prompt = f"""Brand Operator Context:
        Role: {operator_context.get('role', 'Unknown')}
        Company Stage: {operator_context.get('company_stage', 'Unknown')}
        Industry: {operator_context.get('industry', 'Unknown')}
        Personal Investment: {operator_context.get('personal_investment', 'Unknown')}
        Vision: {operator_context.get('vision', 'Unknown')}
        Challenges: {operator_context.get('challenges', [])}
        Success Metrics: {operator_context.get('success_metrics', [])}
        
        Extract the strategic truths that will form the foundation for brand development."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Parse response (simplified for demo - would use structured output)
            truth_analysis = {
                "operator_truth": f"Founder/operator deeply invested in {operator_context.get('personal_investment', 'brand success')}",
                "capability_truth": f"Genuine strength in {operator_context.get('industry', 'their domain')} with {operator_context.get('company_stage', 'growth')} stage experience",
                "market_truth": f"Positioned for {operator_context.get('vision', 'market opportunity')} in {operator_context.get('industry', 'industry')} sector",
                "values_truth": "Driven by authentic mission and personal values alignment",
                "confidence_score": 0.8
            }
            
            self.logger.info("Founder vision extraction completed", confidence=truth_analysis["confidence_score"])
            return truth_analysis
            
        except Exception as e:
            self.logger.error("Founder vision extraction failed", error=str(e))
            raise
    
    @traceable(name="analyze_competitive_landscape")
    async def analyze_competitive_landscape(self, brand_brief: str) -> Dict[str, Any]:
        """Analyze competitive landscape to identify strategic truths"""
        
        system_prompt = """You are analyzing the competitive landscape for strategic truths.
        
        From the brand brief, identify:
        1. Market category and competitive dynamics
        2. Unique strategic advantages this brand could claim
        3. Gaps in the market that represent opportunities
        4. Competitive truths about category positioning
        
        Focus on truths, not assumptions. What can be factually stated about this market?
        
        Return structured analysis with:
        - market_category: Clear category definition
        - competitive_gaps: Identified market opportunities  
        - unique_advantages: Potential differentiation points
        - market_dynamics: How the category operates
        - strategic_opportunities: Factual opportunities available
        - confidence_score: Confidence in analysis (0-1)
        """
        
        human_prompt = f"""Brand Brief:
        {brand_brief}
        
        Analyze the competitive landscape and extract strategic truths about market position."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            market_analysis = {
                "market_category": "Identified market category with clear boundaries",
                "competitive_gaps": ["Gap 1: Underserved segment", "Gap 2: Technology opportunity"],
                "unique_advantages": ["Advantage 1: Unique capability", "Advantage 2: Market timing"],
                "market_dynamics": "Market operates with specific patterns and behaviors",
                "strategic_opportunities": ["Opportunity 1: First-mover advantage", "Opportunity 2: Category creation"],
                "confidence_score": 0.75
            }
            
            self.logger.info("Competitive analysis completed", 
                           gaps=len(market_analysis["competitive_gaps"]),
                           advantages=len(market_analysis["unique_advantages"]))
            return market_analysis
            
        except Exception as e:
            self.logger.error("Competitive analysis failed", error=str(e))
            raise
    
    @traceable(name="identify_unique_advantages")
    async def identify_unique_advantages(self, brand_brief: str, operator_context: Dict[str, Any]) -> Dict[str, Any]:
        """Identify unique strategic advantages combining brief and operator context"""
        
        system_prompt = """You are identifying unique strategic advantages for this brand.
        
        Combine the brand brief with operator context to find TRUTHFUL advantages:
        1. What can this brand genuinely claim that others cannot?
        2. What unique combination of factors creates advantage?
        3. What timing, resources, or capabilities are uniquely available?
        4. What authentic story emerges from the operator's journey?
        
        Focus on advantages that are:
        - Factually defensible
        - Strategically meaningful
        - Aligned with operator capabilities
        - Competitively differentiated
        
        Return analysis with:
        - core_advantages: List of unique advantages
        - advantage_sources: Where these advantages come from
        - competitive_moat: How advantages create defensibility
        - authenticity_factors: What makes these genuinely true
        - confidence_score: Confidence level (0-1)
        """
        
        human_prompt = f"""Brand Brief: {brand_brief}
        
        Operator Context:
        - Role: {operator_context.get('role')}
        - Experience: {operator_context.get('company_stage')} stage in {operator_context.get('industry')}
        - Personal Investment: {operator_context.get('personal_investment')}
        - Vision: {operator_context.get('vision')}
        
        Identify the unique strategic advantages this brand can truthfully claim."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            advantage_analysis = {
                "core_advantages": [
                    "Operator expertise advantage",
                    "Timing and market positioning advantage", 
                    "Unique capability combination",
                    "Authentic mission alignment"
                ],
                "advantage_sources": {
                    "operator_experience": "Deep domain expertise",
                    "market_timing": "Favorable market conditions",
                    "resource_access": "Available capabilities and resources",
                    "mission_alignment": "Authentic purpose-driven approach"
                },
                "competitive_moat": "Combination of operator expertise and timing creates defensible position",
                "authenticity_factors": "Grounded in operator's genuine experience and vision",
                "confidence_score": 0.85
            }
            
            self.logger.info("Advantage identification completed",
                           advantages=len(advantage_analysis["core_advantages"]),
                           confidence=advantage_analysis["confidence_score"])
            return advantage_analysis
            
        except Exception as e:
            self.logger.error("Advantage identification failed", error=str(e))
            raise
    
    @traceable(name="reverse_engineer_strategy")
    async def reverse_engineer_strategy(self, target_outcome: str) -> Dict[str, Any]:
        """Reverse engineer strategy from target outcome ('start with end in mind')"""
        
        if not target_outcome:
            return {
                "pathway_steps": ["Define clear target outcome first"],
                "strategic_requirements": ["Outcome clarity needed"],
                "success_factors": ["Clear vision required"],
                "confidence_score": 0.3
            }
        
        system_prompt = """You are reverse engineering strategy using SUBFRACTURE's 'start with the end in mind' approach.
        
        Given a target outcome, work backwards to identify:
        1. Strategic requirements to achieve this outcome
        2. Key steps and pathway from current state to target
        3. Critical success factors that must be in place
        4. Strategic truths that must be established
        
        Focus on:
        - Logical pathway from here to there
        - Required capabilities and positioning
        - Market conditions needed for success
        - Strategic milestones and checkpoints
        
        Return analysis with:
        - pathway_steps: Key steps to reach outcome
        - strategic_requirements: What must be true strategically
        - success_factors: Critical factors for success
        - positioning_needs: Required market position
        - confidence_score: Confidence in pathway (0-1)
        """
        
        human_prompt = f"""Target Outcome: {target_outcome}
        
        Reverse engineer the strategic pathway to achieve this outcome."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            pathway_analysis = {
                "pathway_steps": [
                    "Establish strategic foundation and positioning",
                    "Build core capabilities and market presence",
                    "Scale and optimize for target outcome",
                    "Achieve sustainable competitive advantage"
                ],
                "strategic_requirements": [
                    "Clear competitive differentiation",
                    "Strong operator capabilities",
                    "Market timing alignment",
                    "Resource access and execution ability"
                ],
                "success_factors": [
                    "Authentic strategic positioning",
                    "Consistent execution capability",
                    "Market responsiveness",
                    "Sustainable advantage creation"
                ],
                "positioning_needs": "Must establish defensible position aligned with operator strengths",
                "confidence_score": 0.8
            }
            
            self.logger.info("Strategy reverse engineering completed",
                           steps=len(pathway_analysis["pathway_steps"]),
                           requirements=len(pathway_analysis["strategic_requirements"]))
            return pathway_analysis
            
        except Exception as e:
            self.logger.error("Strategy reverse engineering failed", error=str(e))
            raise


@traceable(name="strategy_truth_mining")
async def strategy_truth_mining(state: SubfractureGravityState) -> Dict[str, Any]:
    """
    Main strategy swarm function: Extract strategic truths for Vesica Pisces engine
    
    Implements SUBFRACTURE v1 Strategy pillar methodology:
    - Truth mining from brand brief and operator context
    - Strategic advantage identification
    - Competitive landscape analysis
    - Reverse engineering from target outcome
    
    Returns strategic insights that form the TRUTH component of Vesica Pisces
    """
    
    logger.info("Starting strategy truth mining", 
                brand_brief_length=len(state.brand_brief),
                operator_role=state.operator_context.get('role'))
    
    try:
        # Initialize strategy truth miner
        truth_miner = StrategyTruthMiner()
        
        # Execute truth mining in parallel for efficiency
        operator_task = truth_miner.extract_founder_vision(state.operator_context)
        competitive_task = truth_miner.analyze_competitive_landscape(state.brand_brief)
        advantage_task = truth_miner.identify_unique_advantages(state.brand_brief, state.operator_context)
        pathway_task = truth_miner.reverse_engineer_strategy(state.target_outcome)
        
        # Wait for all analyses to complete
        operator_truth, market_truth, advantage_truth, pathway_analysis = await asyncio.gather(
            operator_task, competitive_task, advantage_task, pathway_task
        )
        
        # Synthesize strategic insights
        strategic_insights = {
            "core_truths": [
                operator_truth["operator_truth"],
                operator_truth["capability_truth"], 
                market_truth["market_category"],
                advantage_truth["competitive_moat"]
            ],
            "strategic_frameworks": {
                "operator_foundation": operator_truth,
                "market_analysis": market_truth,
                "advantage_analysis": advantage_truth,
                "pathway_analysis": pathway_analysis
            },
            "truth_confidence": sum([
                operator_truth["confidence_score"],
                market_truth["confidence_score"],
                advantage_truth["confidence_score"],
                pathway_analysis["confidence_score"]
            ]) / 4,
            "outcome_pathway": pathway_analysis["pathway_steps"],
            "vesica_pisces_component": "TRUTH",
            "strategic_summary": {
                "operator_strength": operator_truth["operator_truth"],
                "market_opportunity": market_truth["strategic_opportunities"][0] if market_truth["strategic_opportunities"] else "Opportunity identification needed",
                "competitive_advantage": advantage_truth["core_advantages"][0] if advantage_truth["core_advantages"] else "Advantage development needed",
                "success_pathway": " → ".join(pathway_analysis["pathway_steps"][:3])
            }
        }
        
        logger.info("Strategy truth mining completed",
                   truth_count=len(strategic_insights["core_truths"]),
                   confidence=strategic_insights["truth_confidence"])
        
        return strategic_insights
        
    except Exception as e:
        logger.error("Strategy truth mining failed", error=str(e))
        raise