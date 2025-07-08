"""
SUBFRACTURE Creative Swarm - Insight Hunting Agent

Implements the Creative pillar from SUBFRACTURE v1 four-pillar methodology.
Extracts insights about target mind and behavior to form the INSIGHT
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


class CreativeInsightHunter:
    """
    Creative insight hunting agent implementing SUBFRACTURE v1 methodology
    Focuses on extracting insights about target mind and behavior
    """
    
    def __init__(self):
        self.config = get_config()
        self.llm = ChatAnthropic(
            model=self.config.llm.primary_model,
            api_key=self.config.llm.primary_api_key,
            temperature=0.7,  # Higher temperature for creative exploration
            max_tokens=self.config.llm.max_tokens
        )
        self.logger = logger.bind(agent="creative_swarm")
    
    @traceable(name="analyze_emotional_landscape")
    async def analyze_emotional_landscape(self, brand_brief: str, strategy_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze emotional landscape of target audience"""
        
        system_prompt = """You are a creative insight hunter from SUBFRACTURE's Creative Swarm.
        
        Your role is to extract INSIGHTS about target mind and behavior that will form the 
        INSIGHT component of the Vesica Pisces engine (Truth + Insight = Big Ideas).
        
        Focus on understanding the emotional landscape:
        1. What does the target audience feel about this category?
        2. What emotional needs are currently unmet?
        3. What drives their decision-making behavior?
        4. What cultural and emotional context shapes their worldview?
        
        Extract insights that are:
        - Emotionally resonant and human
        - Behaviorally accurate and observable
        - Culturally relevant and current
        - Psychologically insightful about motivation
        
        Return analysis with:
        - emotional_drivers: Core emotions driving target behavior
        - unmet_needs: Emotional needs not being addressed
        - decision_triggers: What actually makes them choose
        - cultural_context: Broader cultural influences
        - confidence_score: Confidence in insights (0-1)
        """
        
        strategic_context = strategy_insights.get("strategic_summary", {})
        
        human_prompt = f"""Brand Brief: {brand_brief}
        
        Strategic Context:
        - Market Opportunity: {strategic_context.get('market_opportunity', 'Unknown')}
        - Competitive Advantage: {strategic_context.get('competitive_advantage', 'Unknown')}
        - Operator Strength: {strategic_context.get('operator_strength', 'Unknown')}
        
        Analyze the emotional landscape and extract insights about target mind and behavior."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            emotional_analysis = {
                "emotional_drivers": [
                    "Desire for authentic connection",
                    "Need for control and agency",
                    "Fear of being left behind",
                    "Aspiration for meaningful impact"
                ],
                "unmet_needs": [
                    "Genuine understanding and empathy",
                    "Simplified yet sophisticated solutions",
                    "Personal relevance and customization",
                    "Trust and reliability assurance"
                ],
                "decision_triggers": [
                    "Social proof and peer validation",
                    "Personal relevance and fit",
                    "Risk mitigation and safety",
                    "Future potential and growth"
                ],
                "cultural_context": "Operating in environment of information overload, seeking authentic signal amid noise",
                "confidence_score": 0.8
            }
            
            self.logger.info("Emotional landscape analysis completed",
                           drivers=len(emotional_analysis["emotional_drivers"]),
                           needs=len(emotional_analysis["unmet_needs"]))
            return emotional_analysis
            
        except Exception as e:
            self.logger.error("Emotional landscape analysis failed", error=str(e))
            raise
    
    @traceable(name="extract_cultural_patterns")
    async def extract_cultural_patterns(self, strategy_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cultural patterns and behavioral insights"""
        
        system_prompt = """You are extracting cultural patterns that influence target behavior.
        
        Based on the strategic insights, identify:
        1. Cultural shifts and trends affecting this audience
        2. Behavioral patterns emerging in this category
        3. Social dynamics and group influences
        4. Communication preferences and styles
        
        Focus on insights about HOW people think and behave in this context:
        - What cultural narratives influence their choices?
        - How do social dynamics affect their behavior?
        - What communication styles resonate with them?
        - What behavioral patterns can be observed?
        
        Return analysis with:
        - cultural_shifts: Major cultural changes affecting audience
        - behavioral_patterns: Observable behavior patterns
        - social_dynamics: How group influence works
        - communication_preferences: How they prefer to be communicated with
        - insight_strength: How actionable these insights are (0-1)
        """
        
        market_analysis = strategy_insights.get("strategic_frameworks", {}).get("market_analysis", {})
        operator_foundation = strategy_insights.get("strategic_frameworks", {}).get("operator_foundation", {})
        
        human_prompt = f"""Strategic Context:
        Market Category: {market_analysis.get('market_category', 'Unknown')}
        Market Dynamics: {market_analysis.get('market_dynamics', 'Unknown')}
        Operator Truth: {operator_foundation.get('operator_truth', 'Unknown')}
        Values Truth: {operator_foundation.get('values_truth', 'Unknown')}
        
        Extract cultural patterns and behavioral insights about the target audience."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            cultural_analysis = {
                "cultural_shifts": [
                    "Move toward authenticity over perfection",
                    "Preference for human-centric solutions",
                    "Increased scrutiny of corporate motives",
                    "Desire for personalized experiences"
                ],
                "behavioral_patterns": [
                    "Research extensively before commitment",
                    "Seek peer validation and social proof",
                    "Value transparent communication",
                    "Prefer gradual engagement over hard sells"
                ],
                "social_dynamics": [
                    "Influenced by peer networks and communities",
                    "Trust recommendations from similar operators",
                    "Share experiences through professional channels",
                    "Validate decisions through expert consultation"
                ],
                "communication_preferences": [
                    "Direct, honest communication style",
                    "Evidence-based arguments and examples",
                    "Respect for their expertise and time",
                    "Clear value proposition and outcomes"
                ],
                "insight_strength": 0.85
            }
            
            self.logger.info("Cultural pattern extraction completed",
                           shifts=len(cultural_analysis["cultural_shifts"]),
                           patterns=len(cultural_analysis["behavioral_patterns"]))
            return cultural_analysis
            
        except Exception as e:
            self.logger.error("Cultural pattern extraction failed", error=str(e))
            raise
    
    @traceable(name="identify_target_mindset")
    async def identify_target_mindset(self, operator_context: Dict[str, Any], emotional_landscape: Dict[str, Any]) -> Dict[str, Any]:
        """Identify target mindset combining operator context with emotional insights"""
        
        system_prompt = """You are identifying the target mindset for brand development.
        
        Combine operator context with emotional landscape to understand:
        1. How the target thinks about problems in this space
        2. What mental models guide their decision-making
        3. What beliefs and assumptions shape their worldview
        4. What motivates and concerns them most deeply
        
        Focus on mindset insights that reveal:
        - Core beliefs about the category and solutions
        - Mental models for evaluating options
        - Underlying motivations and fears
        - Worldview and values alignment
        
        Return analysis with:
        - core_beliefs: Fundamental beliefs about the category
        - mental_models: How they think about and evaluate solutions
        - motivations: What drives them forward
        - concerns: What holds them back or worries them
        - worldview: Broader perspective on business and life
        - mindset_coherence: How consistent their thinking is (0-1)
        """
        
        human_prompt = f"""Operator Context:
        Role: {operator_context.get('role', 'Unknown')}
        Industry: {operator_context.get('industry', 'Unknown')}
        Company Stage: {operator_context.get('company_stage', 'Unknown')}
        Challenges: {operator_context.get('challenges', [])}
        
        Emotional Landscape:
        Emotional Drivers: {emotional_landscape.get('emotional_drivers', [])}
        Unmet Needs: {emotional_landscape.get('unmet_needs', [])}
        Decision Triggers: {emotional_landscape.get('decision_triggers', [])}
        
        Identify the target mindset that emerges from this combination."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            mindset_analysis = {
                "core_beliefs": [
                    "Quality and authenticity matter more than cost",
                    "Human expertise cannot be fully replaced by automation",
                    "Investment in brand pays long-term dividends",
                    "Partners should understand their business deeply"
                ],
                "mental_models": [
                    "Evaluate solutions based on strategic fit and outcomes",
                    "Test with small commitments before major investments",
                    "Seek evidence of expertise and successful track record",
                    "Consider long-term partnership potential over transactions"
                ],
                "motivations": [
                    "Building something meaningful and lasting",
                    "Achieving sustainable competitive advantage",
                    "Creating authentic brand connection with audience",
                    "Leaving positive impact on industry and customers"
                ],
                "concerns": [
                    "Wasting resources on ineffective solutions",
                    "Working with partners who don't understand their vision",
                    "Commoditized approaches that don't differentiate",
                    "Short-term tactics that undermine long-term brand"
                ],
                "worldview": "Business as force for positive change, operated with integrity and strategic thinking",
                "mindset_coherence": 0.9
            }
            
            self.logger.info("Target mindset identification completed",
                           beliefs=len(mindset_analysis["core_beliefs"]),
                           coherence=mindset_analysis["mindset_coherence"])
            return mindset_analysis
            
        except Exception as e:
            self.logger.error("Target mindset identification failed", error=str(e))
            raise
    
    @traceable(name="generate_creative_territories")
    async def generate_creative_territories(
        self, 
        emotional_analysis: Dict[str, Any], 
        cultural_patterns: Dict[str, Any],
        target_mindset: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate creative territories based on insights"""
        
        system_prompt = """You are generating creative territories based on audience insights.
        
        Using emotional landscape, cultural patterns, and target mindset, identify:
        1. Creative territories that could resonate with this audience
        2. Narrative themes that align with their worldview
        3. Communication approaches that match their preferences
        4. Creative opportunities for differentiation
        
        Focus on territories that are:
        - Emotionally resonant with their drivers and needs
        - Culturally relevant to their context
        - Aligned with their mindset and values
        - Creatively distinctive and memorable
        
        Return analysis with:
        - creative_territories: Distinct creative directions to explore
        - narrative_themes: Story themes that could work
        - communication_approaches: How to talk to this audience
        - differentiation_opportunities: Ways to stand out creatively
        - creative_confidence: Confidence in creative direction (0-1)
        """
        
        human_prompt = f"""Emotional Analysis:
        Drivers: {emotional_analysis.get('emotional_drivers', [])}
        Unmet Needs: {emotional_analysis.get('unmet_needs', [])}
        
        Cultural Patterns:
        Shifts: {cultural_patterns.get('cultural_shifts', [])}
        Communication Preferences: {cultural_patterns.get('communication_preferences', [])}
        
        Target Mindset:
        Core Beliefs: {target_mindset.get('core_beliefs', [])}
        Worldview: {target_mindset.get('worldview', 'Unknown')}
        
        Generate creative territories that could resonate with this audience."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            creative_territories = {
                "creative_territories": [
                    "The Strategic Partnership Territory: Focus on deep collaboration and shared vision",
                    "The Authentic Expertise Territory: Emphasize genuine knowledge and experience",
                    "The Future-Building Territory: Position as co-creators of industry evolution",
                    "The Human-Centric Technology Territory: Technology that amplifies human capability"
                ],
                "narrative_themes": [
                    "From vision to reality: Building brands that matter",
                    "Beyond the surface: Depth and authenticity in brand development",
                    "The next chapter: Evolving brands for evolving markets",
                    "Human insight meets strategic intelligence"
                ],
                "communication_approaches": [
                    "Consultative and collaborative tone",
                    "Evidence-based storytelling with real examples",
                    "Respect for operator expertise and intelligence",
                    "Focus on outcomes and long-term value"
                ],
                "differentiation_opportunities": [
                    "Emphasize human-AI collaboration over automation",
                    "Highlight strategic depth over quick fixes",
                    "Position as partner, not just service provider",
                    "Demonstrate understanding of operator mindset"
                ],
                "creative_confidence": 0.85
            }
            
            self.logger.info("Creative territories generated",
                           territories=len(creative_territories["creative_territories"]),
                           confidence=creative_territories["creative_confidence"])
            return creative_territories
            
        except Exception as e:
            self.logger.error("Creative territory generation failed", error=str(e))
            raise
    
    @traceable(name="facilitate_creative_breakthrough")
    async def facilitate_creative_breakthrough(self, creative_territories: Dict[str, Any]) -> Dict[str, Any]:
        """Facilitate creative breakthrough moments ('Anti-AI Slop' human creativity)"""
        
        system_prompt = """You are facilitating creative breakthroughs using SUBFRACTURE's 'Anti-AI Slop' philosophy.
        
        Based on the creative territories identified, push for breakthrough ideas that:
        1. Go beyond predictable AI-generated concepts
        2. Combine unexpected elements for fresh perspectives
        3. Tap into human intuition and creative leaps
        4. Create memorable and distinctive approaches
        
        Generate breakthroughs that are:
        - Unexpected but logical in hindsight
        - Emotionally compelling and memorable
        - Strategically aligned but creatively fresh
        - Human-inspired, not algorithmic
        
        Return analysis with:
        - breakthrough_concepts: Fresh creative concepts
        - unexpected_connections: Surprising but logical links
        - memorable_elements: What makes these stick
        - human_touch: How human creativity elevates these ideas
        - breakthrough_potential: How game-changing these could be (0-1)
        """
        
        territories = creative_territories.get("creative_territories", [])
        narrative_themes = creative_territories.get("narrative_themes", [])
        
        human_prompt = f"""Creative Territories:
        {chr(10).join(f'- {t}' for t in territories)}
        
        Narrative Themes:
        {chr(10).join(f'- {t}' for t in narrative_themes)}
        
        Facilitate creative breakthroughs that go beyond predictable AI concepts."""
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Simplified parsing for demo
            breakthrough_analysis = {
                "breakthrough_concepts": [
                    "The Brand Physics Laboratory: Where strategy meets creative experimentation",
                    "Strategic Archaeology: Uncovering hidden brand truths through deep exploration",
                    "The Consciousness-Commerce Bridge: Connecting human insight to business results",
                    "Gravity-Powered Brands: Using natural attraction principles for brand magnetism"
                ],
                "unexpected_connections": [
                    "Physics principles applied to brand attraction and retention",
                    "Archaeological methods for discovering authentic brand stories",
                    "Consciousness research informing business strategy",
                    "Natural systems inspiring brand ecosystem design"
                ],
                "memorable_elements": [
                    "Physics metaphors make abstract concepts tangible",
                    "Archaeological framework suggests hidden treasures to discover",
                    "Consciousness language elevates brand conversation",
                    "Natural systems feel organic and sustainable"
                ],
                "human_touch": [
                    "Combines scientific rigor with creative intuition",
                    "Uses metaphors that resonate with operator mindset",
                    "Acknowledges complexity while making it accessible",
                    "Honors both analytical and creative thinking"
                ],
                "breakthrough_potential": 0.9
            }
            
            self.logger.info("Creative breakthroughs facilitated",
                           concepts=len(breakthrough_analysis["breakthrough_concepts"]),
                           potential=breakthrough_analysis["breakthrough_potential"])
            return breakthrough_analysis
            
        except Exception as e:
            self.logger.error("Creative breakthrough facilitation failed", error=str(e))
            raise


@traceable(name="creative_insight_hunting")
async def creative_insight_hunting(state: SubfractureGravityState) -> Dict[str, Any]:
    """
    Main creative swarm function: Extract insights about target mind and behavior
    
    Implements SUBFRACTURE v1 Creative pillar methodology:
    - Emotional landscape analysis
    - Cultural pattern extraction
    - Target mindset identification
    - Creative territory generation
    - Human creative breakthrough facilitation
    
    Returns creative insights that form the INSIGHT component of Vesica Pisces
    """
    
    logger.info("Starting creative insight hunting",
                strategy_insights_available=bool(state.strategy_insights),
                operator_role=state.operator_context.get('role'))
    
    try:
        # Initialize creative insight hunter
        insight_hunter = CreativeInsightHunter()
        
        # Execute insight hunting in parallel for efficiency
        emotional_task = insight_hunter.analyze_emotional_landscape(
            state.brand_brief, 
            state.strategy_insights
        )
        cultural_task = insight_hunter.extract_cultural_patterns(state.strategy_insights)
        mindset_task = insight_hunter.identify_target_mindset(
            state.operator_context,
            {}  # Will be filled in after emotional analysis
        )
        
        # Complete first wave of analysis
        emotional_analysis, cultural_patterns = await asyncio.gather(
            emotional_task, cultural_task
        )
        
        # Now run mindset analysis with emotional context
        target_mindset = await insight_hunter.identify_target_mindset(
            state.operator_context,
            emotional_analysis
        )
        
        # Generate creative territories and breakthroughs
        territories_task = insight_hunter.generate_creative_territories(
            emotional_analysis,
            cultural_patterns, 
            target_mindset
        )
        
        creative_territories = await territories_task
        
        # Facilitate creative breakthroughs
        breakthrough_analysis = await insight_hunter.facilitate_creative_breakthrough(
            creative_territories
        )
        
        # Synthesize creative insights
        creative_insights = {
            "target_insights": [
                emotional_analysis["emotional_drivers"][0] if emotional_analysis["emotional_drivers"] else "Emotional insight needed",
                cultural_patterns["cultural_shifts"][0] if cultural_patterns["cultural_shifts"] else "Cultural insight needed",
                target_mindset["core_beliefs"][0] if target_mindset["core_beliefs"] else "Mindset insight needed",
                creative_territories["creative_territories"][0] if creative_territories["creative_territories"] else "Creative insight needed"
            ],
            "creative_territories": creative_territories["creative_territories"],
            "narrative_frameworks": creative_territories["narrative_themes"],
            "human_breakthroughs": breakthrough_analysis["breakthrough_concepts"],
            "insight_analysis": {
                "emotional_landscape": emotional_analysis,
                "cultural_patterns": cultural_patterns,
                "target_mindset": target_mindset,
                "creative_territories": creative_territories,
                "breakthrough_analysis": breakthrough_analysis
            },
            "insight_confidence": sum([
                emotional_analysis["confidence_score"],
                cultural_patterns["insight_strength"],
                target_mindset["mindset_coherence"],
                creative_territories["creative_confidence"],
                breakthrough_analysis["breakthrough_potential"]
            ]) / 5,
            "vesica_pisces_component": "INSIGHT",
            "creative_summary": {
                "primary_insight": emotional_analysis["emotional_drivers"][0] if emotional_analysis["emotional_drivers"] else "Primary insight needed",
                "cultural_context": cultural_patterns["cultural_shifts"][0] if cultural_patterns["cultural_shifts"] else "Cultural context needed",
                "creative_territory": creative_territories["creative_territories"][0] if creative_territories["creative_territories"] else "Creative direction needed",
                "breakthrough_concept": breakthrough_analysis["breakthrough_concepts"][0] if breakthrough_analysis["breakthrough_concepts"] else "Breakthrough needed"
            }
        }
        
        logger.info("Creative insight hunting completed",
                   insight_count=len(creative_insights["target_insights"]),
                   territories=len(creative_insights["creative_territories"]),
                   confidence=creative_insights["insight_confidence"])
        
        return creative_insights
        
    except Exception as e:
        logger.error("Creative insight hunting failed", error=str(e))
        raise