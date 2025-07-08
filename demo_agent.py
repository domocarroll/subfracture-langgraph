#!/usr/bin/env python3
"""
SUBFRACTURE Demo Agent for LangGraph Platform
Simplified version for testing without API keys
"""

import asyncio
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import json

from langgraph.graph import StateGraph, START, END


class SubfractureDemoAgent:
    """
    Demo version of SUBFRACTURE for LangGraph Platform testing
    Works without external API calls for demonstration
    """
    
    def __init__(self):
        """Initialize the demo agent"""
        print("🎭 Demo SUBFRACTURE Agent initialized")
    
    async def analyze_transcript(
        self,
        brand_brief: str,
        operator_context: Optional[Dict[str, Any]] = None,
        target_outcome: Optional[str] = None,
        deep_analysis: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze brand transcript and extract strategic insights
        Demo version with mock analysis
        """
        
        # Set defaults
        if operator_context is None:
            operator_context = {
                "role": "Brand Strategist",
                "industry": "Technology",
                "company_stage": "Growth",
                "years_experience": 5,
                "participant_id": str(uuid.uuid4())
            }
        
        if target_outcome is None:
            target_outcome = "Extract strategic brand insights and positioning opportunities"
        
        # Choose analysis mode
        if deep_analysis:
            print("🔬 Running DEEP ANALYSIS mode - showing the working...")
            return await self._run_deep_analysis(brand_brief, operator_context, target_outcome)
        else:
            print("⚡ Running STANDARD ANALYSIS mode - fast insights...")
            return await self._run_standard_analysis(brand_brief, operator_context, target_outcome)
    
    async def _run_standard_analysis(
        self,
        brand_brief: str,
        operator_context: Dict[str, Any],
        target_outcome: str
    ) -> Dict[str, Any]:
        """Run standard fast analysis"""
        
        # Extract key insights from the brand brief
        insights = self._extract_key_insights(brand_brief)
        
        # Calculate brand gravity index based on content
        gravity_index = self._calculate_gravity_index(brand_brief, insights)
        
        # Generate strategic recommendations
        recommendations = self._generate_recommendations(insights, operator_context)
        
        # Create standard analysis
        analysis = {
            "session_id": str(uuid.uuid4()),
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "brand_brief_length": len(brand_brief),
            "target_outcome": target_outcome,
            "analysis": {
                "key_insights": insights,
                "gravity_index": gravity_index,
                "strategic_positioning": self._analyze_positioning(brand_brief),
                "competitive_advantages": self._identify_advantages(brand_brief),
                "market_opportunities": self._find_opportunities(brand_brief),
                "brand_personality": self._extract_personality(brand_brief),
                "recommendations": recommendations
            },
            "business_metrics": {
                "market_readiness_score": gravity_index,
                "differentiation_strength": min(0.95, gravity_index + 0.1),
                "brand_coherence": gravity_index * 0.9,
                "launch_confidence": "High" if gravity_index > 0.7 else "Medium",
                "estimated_market_impact": f"${int(gravity_index * 500)}k-{int(gravity_index * 800)}k potential"
            }
        }
        
        return analysis
    
    async def _run_deep_analysis(
        self,
        brand_brief: str,
        operator_context: Dict[str, Any],
        target_outcome: str
    ) -> Dict[str, Any]:
        """Run comprehensive deep analysis with detailed working"""
        
        import re
        from collections import Counter
        
        print("🔬 Starting comprehensive brand intelligence analysis...")
        
        # 1. Content Structure Analysis
        content_stats = self._analyze_content_structure(brand_brief)
        
        # 2. Deep Theme Analysis  
        theme_analysis = self._detailed_theme_analysis(brand_brief)
        
        # 3. Key Phrase Extraction
        key_phrases = self._extract_key_phrases_deep(brand_brief)
        
        # 4. Sentiment Analysis
        sentiment_analysis = self._analyze_sentiment_deep(brand_brief)
        
        # 5. Strategic Framework Detection
        frameworks = self._detect_frameworks(brand_brief)
        
        # 6. Competitive Intelligence
        competitive_intel = self._extract_competitive_intelligence(brand_brief)
        
        # 7. Market Opportunity Mapping
        market_mapping = self._map_market_opportunities(brand_brief)
        
        # 8. Brand Architecture Analysis
        brand_architecture = self._analyze_brand_architecture_deep(brand_brief)
        
        # Calculate enhanced gravity index
        gravity_index = self._calculate_enhanced_gravity_index(
            brand_brief, theme_analysis, sentiment_analysis, market_mapping
        )
        
        # Generate enhanced recommendations
        recommendations = self._generate_enhanced_recommendations(
            theme_analysis, competitive_intel, market_mapping, operator_context
        )
        
        # Create comprehensive deep analysis
        deep_analysis = {
            "session_id": str(uuid.uuid4()),
            "status": "completed",
            "execution_time": datetime.now().isoformat(),
            "analysis_mode": "deep",
            "brand_brief_length": len(brand_brief),
            "target_outcome": target_outcome,
            "analysis": {
                "gravity_index": gravity_index,
                "content_analysis": content_stats,
                "theme_analysis": theme_analysis,
                "key_phrases": key_phrases,
                "sentiment_analysis": sentiment_analysis,
                "strategic_frameworks": frameworks,
                "competitive_intelligence": competitive_intel,
                "market_opportunities": market_mapping,
                "brand_architecture": brand_architecture,
                "strategic_positioning": self._generate_positioning_from_deep_analysis(
                    theme_analysis, competitive_intel, brand_brief
                ),
                "competitive_advantages": self._generate_advantages_from_deep_analysis(
                    theme_analysis, frameworks, brand_brief
                ),
                "brand_personality": self._extract_personality_deep(brand_brief, sentiment_analysis),
                "recommendations": recommendations
            },
            "business_metrics": {
                "market_readiness_score": gravity_index,
                "differentiation_strength": min(0.95, gravity_index + 0.1),
                "brand_coherence": theme_analysis.get("coherence_score", gravity_index * 0.9),
                "launch_confidence": "High" if gravity_index > 0.7 else "Medium",
                "estimated_market_impact": f"${int(gravity_index * 500)}k-{int(gravity_index * 800)}k potential",
                "competitive_readiness": competitive_intel.get("readiness_score", 0.8),
                "framework_sophistication": len(frameworks) / 10.0
            },
            "deep_insights": {
                "thematic_coherence": theme_analysis.get("coherence_score", 0.85),
                "strategic_sophistication": len(frameworks),
                "market_timing_alignment": market_mapping.get("timing_score", 0.8),
                "competitive_awareness": len(competitive_intel.get("mentioned_companies", [])),
                "brand_architecture_completeness": brand_architecture.get("completeness_score", 0.9)
            }
        }
        
        print("✅ Deep analysis completed with comprehensive insights!")
        return deep_analysis
    
    def _extract_key_insights(self, brand_brief: str) -> Dict[str, Any]:
        """Extract key insights from brand brief"""
        
        # Key phrases that indicate strategic themes
        key_themes = {
            "human_centered": ["human", "heart", "intuition", "personal", "authentic"],
            "technology_integration": ["AI", "technology", "tech", "digital", "cyborg"],
            "creative_methodology": ["creative", "design", "strategy", "methodology", "framework"],
            "brand_worlds": ["brand world", "immersive", "interactive", "experience"],
            "positioning": ["positioning", "different", "unique", "breakthrough"],
            "premium_value": ["premium", "boutique", "quality", "specialized", "high-touch"]
        }
        
        theme_scores = {}
        brief_length = max(1, len(brand_brief))  # Avoid division by zero
        for theme, keywords in key_themes.items():
            score = sum(brand_brief.lower().count(keyword) for keyword in keywords) / brief_length * 1000
            theme_scores[theme] = min(1.0, score)
        
        return {
            "primary_themes": theme_scores,
            "brand_essence": "Human-centered AI design studio" if theme_scores.get("human_centered", 0) > 0.3 else "Creative technology agency",
            "core_differentiator": "Keeping humans in the tech loop",
            "methodology": "Creative destructionism + vesica pisces",
            "confidence_level": sum(theme_scores.values()) / len(theme_scores)
        }
    
    def _calculate_gravity_index(self, brand_brief: str, insights: Dict[str, Any]) -> float:
        """Calculate brand gravity index"""
        
        # Base score from content length and depth
        base_score = min(0.6, len(brand_brief) / 20000)
        
        # Theme strength bonus
        theme_bonus = insights["confidence_level"] * 0.3
        
        # Strategic clarity bonus
        strategic_keywords = ["purpose", "personality", "positioning", "unique", "different"]
        clarity_bonus = sum(brand_brief.lower().count(word) for word in strategic_keywords) / 100
        
        gravity_index = base_score + theme_bonus + clarity_bonus
        return min(1.0, gravity_index)
    
    def _analyze_positioning(self, brand_brief: str) -> Dict[str, str]:
        """Analyze brand positioning from brief"""
        
        if "brand operators" in brand_brief.lower():
            target = "Brand operators and founders"
        elif "emerging brands" in brand_brief.lower():
            target = "Emerging and innovative brands"
        else:
            target = "Forward-thinking technology brands"
        
        return {
            "target_audience": target,
            "category": "Brand intelligence agency / Creative technology studio",
            "positioning_statement": "For brand operators who want breakthrough positioning, only SUBFRACTURE keeps humans in the tech loop because we start with the end in mind",
            "category_disruption": "Anti-slop, human-centered alternative to traditional agencies"
        }
    
    def _identify_advantages(self, brand_brief: str) -> List[str]:
        """Identify competitive advantages"""
        
        advantages = [
            "Cross-disciplinary integration: Strategy + Creative + Design + Technology",
            "Human-centered AI approach: Keeping humans in the tech loop",
            "Proprietary methodology: Creative destructionism + vesica pisces",
            "Living brand worlds: Interactive, breathing brand experiences",
            "Start with end in mind: Reverse engineering from desired outcomes"
        ]
        
        if "high-touch" in brand_brief.lower():
            advantages.append("High-touch, personalized service model")
        
        if "boutique" in brand_brief.lower():
            advantages.append("Boutique quality with technology scale")
        
        return advantages
    
    def _find_opportunities(self, brand_brief: str) -> List[str]:
        """Find market opportunities"""
        
        return [
            "AI slop fatigue: Market demand for human-centered AI solutions",
            "Emerging brands seeking differentiation from traditional agencies",
            "Technology integration gap in creative industry",
            "Premium positioning opportunity in commoditized market",
            "Brand world creation as new service category",
            "Founder-led brands wanting authentic positioning"
        ]
    
    def _extract_personality(self, brand_brief: str) -> Dict[str, str]:
        """Extract brand personality"""
        
        personality = {
            "core_traits": "Human, cool, rock star",
            "communication_style": "Authentic, messy truth-telling, anti-corporate",
            "brand_archetype": "The Rebel + The Magician",
            "emotional_tone": "Confident, innovative, slightly edgy"
        }
        
        if "rock star" in brand_brief.lower():
            personality["aspirational_identity"] = "Technology rock stars"
        
        return personality
    
    def _generate_recommendations(self, insights: Dict[str, Any], operator_context: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations"""
        
        recommendations = [
            "Lead with 'humans in the tech loop' positioning to differentiate from AI-first competitors",
            "Develop case studies demonstrating living brand worlds creation",
            "Target emerging brands and forward-thinking founders as primary market",
            "Build thought leadership around creative destructionism methodology",
            "Create high-impact spec work for target client list to demonstrate capabilities",
            "Position as premium alternative to traditional agencies and AI tools"
        ]
        
        if operator_context.get("company_stage") == "Launch Phase":
            recommendations.extend([
                "Focus on 10 high-value clients ($50k+ projects) rather than volume",
                "Leverage founder networks and relationships for initial client acquisition",
                "Create immersive first-touch experiences that demonstrate brand difference"
            ])
        
        return recommendations
    
    # Deep Analysis Helper Methods
    def _analyze_content_structure(self, text: str) -> dict:
        """Analyze the structural elements of the content"""
        import re
        
        char_count = len(text)
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        questions = re.findall(r'[^.!?]*\?', text)
        question_count = len(questions)
        
        return {
            "total_characters": char_count,
            "total_words": word_count,
            "total_sentences": sentence_count,
            "total_paragraphs": paragraph_count,
            "questions_asked": question_count,
            "avg_sentence_length": word_count / max(1, sentence_count),
            "conversation_density": question_count / max(1, paragraph_count)
        }
    
    def _detailed_theme_analysis(self, text: str) -> dict:
        """Deep theme analysis with frequency scoring"""
        import re
        
        theme_keywords = {
            "human_centered": ["human", "heart", "intuition", "personal", "authentic", "soul", "emotion"],
            "technology_integration": ["AI", "technology", "tech", "digital", "cyborg", "machine"],
            "creative_methodology": ["creative", "design", "strategy", "methodology", "framework", "process"],
            "brand_positioning": ["brand", "positioning", "identity", "personality", "voice", "essence"],
            "market_disruption": ["disruption", "different", "unique", "breakthrough", "innovation"],
            "business_strategy": ["business", "strategy", "market", "competitive", "advantage"]
        }
        
        theme_scores = {}
        theme_details = {}
        
        for theme, keywords in theme_keywords.items():
            matches = []
            for keyword in keywords:
                count = len(re.findall(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE))
                if count > 0:
                    matches.append((keyword, count))
            
            total_score = sum(count for _, count in matches) / len(text) * 10000
            theme_scores[theme] = min(1.0, total_score)
            theme_details[theme] = {
                "matches": matches,
                "raw_score": total_score,
                "normalized_score": theme_scores[theme]
            }
        
        coherence_score = sum(theme_scores.values()) / len(theme_scores)
        
        return {
            "theme_scores": theme_scores,
            "theme_details": theme_details,
            "coherence_score": coherence_score,
            "dominant_themes": sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _extract_key_phrases_deep(self, text: str) -> dict:
        """Extract and analyze key phrases and concepts"""
        import re
        
        brand_phrases = [
            "brand operator", "brand intelligence", "creative destructionism", 
            "vesica pisces", "humans in the tech loop", "brand worlds",
            "start with the end in mind", "heart knows", "anti-slop"
        ]
        
        strategic_concepts = [
            "positioning", "differentiation", "competitive advantage", 
            "market opportunity", "unique selling proposition", "target audience"
        ]
        
        phrase_analysis = {}
        
        for phrase_list, category in [
            (brand_phrases, "brand_specific"),
            (strategic_concepts, "strategic")
        ]:
            category_results = {}
            for phrase in phrase_list:
                count = len(re.findall(rf'\b{re.escape(phrase)}\b', text, re.IGNORECASE))
                if count > 0:
                    category_results[phrase] = count
            phrase_analysis[category] = category_results
        
        return phrase_analysis
    
    def _analyze_sentiment_deep(self, text: str) -> dict:
        """Analyze sentiment and communication tone"""
        import re
        
        positive_indicators = ["love", "great", "fantastic", "amazing", "cool", "awesome", "brilliant"]
        negative_indicators = ["hate", "bad", "terrible", "awful", "sucks", "problem", "issue"]
        confidence_indicators = ["confident", "sure", "certain", "definitely", "absolutely"]
        uncertainty_indicators = ["maybe", "perhaps", "might", "unsure", "don't know"]
        high_energy = ["fucking", "shit", "crazy", "wild", "insane", "massive"]
        
        sentiment_counts = {
            "positive": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in positive_indicators),
            "negative": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in negative_indicators),
            "confident": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in confidence_indicators),
            "uncertain": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in uncertainty_indicators),
            "high_energy": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in high_energy)
        }
        
        total_sentiment = sentiment_counts["positive"] + sentiment_counts["negative"]
        sentiment_ratio = sentiment_counts["positive"] / max(1, total_sentiment)
        
        total_confidence = sentiment_counts["confident"] + sentiment_counts["uncertain"]
        confidence_ratio = sentiment_counts["confident"] / max(1, total_confidence)
        
        return {
            "sentiment_counts": sentiment_counts,
            "sentiment_ratio": sentiment_ratio,
            "confidence_ratio": confidence_ratio,
            "energy_level": sentiment_counts["high_energy"],
            "overall_tone": "confident_energetic" if confidence_ratio > 0.6 and sentiment_counts['high_energy'] > 10 else "professional"
        }
    
    def _detect_frameworks(self, text: str) -> dict:
        """Detect mentions of strategic frameworks"""
        import re
        
        frameworks = {
            "Design Thinking": ["design thinking", "human-centered design", "empathy", "ideate", "prototype"],
            "Brand Strategy": ["brand positioning", "brand essence", "brand personality", "brand archetype"],
            "SUBFRACTURE Methods": ["creative destructionism", "vesica pisces", "four pillars", "gravity"]
        }
        
        detected_frameworks = {}
        for framework, keywords in frameworks.items():
            mentions = []
            for keyword in keywords:
                count = len(re.findall(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE))
                if count > 0:
                    mentions.append((keyword, count))
            
            if mentions:
                detected_frameworks[framework] = {
                    "total_mentions": sum(count for _, count in mentions),
                    "keywords_found": mentions
                }
        
        return detected_frameworks
    
    def _extract_competitive_intelligence(self, text: str) -> dict:
        """Extract competitive landscape insights"""
        import re
        from collections import Counter
        
        # Look for company mentions
        company_patterns = [
            r'\b([A-Z][a-z]+)\s+(?:agency|studio|company)\b',
            r'\b(Ogilvy|Wieden|Kennedy|IDEO|McKinsey)\b'
        ]
        
        mentioned_companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            mentioned_companies.extend(matches)
        
        competitive_terms = {
            "differentiation": ["different", "unique", "unlike", "alternative"],
            "superiority": ["better", "best", "superior", "outperform"],
            "innovation": ["first", "new", "innovative", "pioneering", "breakthrough"]
        }
        
        competitive_analysis = {}
        for category, terms in competitive_terms.items():
            count = sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in terms)
            competitive_analysis[category] = count
        
        return {
            "mentioned_companies": mentioned_companies,
            "competitive_positioning": competitive_analysis,
            "differentiation_focus": competitive_analysis["differentiation"] > competitive_analysis["superiority"],
            "readiness_score": min(1.0, (competitive_analysis["differentiation"] + competitive_analysis["innovation"]) / 20)
        }
    
    def _map_market_opportunities(self, text: str) -> dict:
        """Map market opportunities and gaps"""
        import re
        
        gap_indicators = ["no one", "nobody", "missing", "gap", "opportunity", "need", "demand"]
        timing_indicators = ["now", "timing", "moment", "ready", "ripe", "wave", "trend"]
        
        opportunity_signals = {
            "market_gaps": sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in gap_indicators),
            "timing_signals": sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in timing_indicators)
        }
        
        timing_score = min(1.0, opportunity_signals['timing_signals'] / 20)
        
        return {
            "opportunity_signals": opportunity_signals,
            "timing_score": timing_score,
            "market_readiness": timing_score > 0.5
        }
    
    def _analyze_brand_architecture_deep(self, text: str) -> dict:
        """Analyze brand architecture elements"""
        import re
        
        brand_elements = {
            "purpose": ["purpose", "mission", "why", "reason"],
            "vision": ["vision", "future", "aspiration", "dream"],
            "values": ["values", "principles", "beliefs"],
            "personality": ["personality", "character", "traits"],
            "positioning": ["positioning", "place", "category"],
            "promise": ["promise", "commitment", "deliver"]
        }
        
        architecture_strength = {}
        for element, keywords in brand_elements.items():
            count = sum(len(re.findall(rf'\b{keyword}\b', text, re.IGNORECASE)) for keyword in keywords)
            architecture_strength[element] = count
        
        defined_elements = sum(1 for count in architecture_strength.values() if count > 0)
        completeness_score = defined_elements / len(brand_elements)
        
        return {
            "architecture_strength": architecture_strength,
            "completeness_score": completeness_score,
            "strongest_elements": sorted(architecture_strength.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _calculate_enhanced_gravity_index(self, brand_brief: str, theme_analysis: dict, sentiment_analysis: dict, market_mapping: dict) -> float:
        """Calculate enhanced gravity index using deep analysis"""
        
        # Base score from content
        base_score = min(0.4, len(brand_brief) / 20000)
        
        # Theme coherence bonus
        theme_bonus = theme_analysis.get("coherence_score", 0.5) * 0.3
        
        # Sentiment strength bonus
        sentiment_bonus = sentiment_analysis.get("sentiment_ratio", 0.5) * 0.15
        
        # Market timing bonus
        timing_bonus = market_mapping.get("timing_score", 0.5) * 0.15
        
        gravity_index = base_score + theme_bonus + sentiment_bonus + timing_bonus
        return min(1.0, gravity_index)
    
    def _generate_enhanced_recommendations(self, theme_analysis: dict, competitive_intel: dict, market_mapping: dict, operator_context: dict) -> List[str]:
        """Generate enhanced recommendations from deep analysis"""
        
        recommendations = [
            "Lead with human-centered AI positioning to differentiate from purely technical competitors",
            "Develop comprehensive case studies demonstrating brand world creation methodology",
            "Target emerging brands seeking authentic, non-corporate agency alternatives"
        ]
        
        # Add theme-specific recommendations
        dominant_themes = theme_analysis.get("dominant_themes", [])
        if dominant_themes:
            top_theme = dominant_themes[0][0]
            if "human_centered" in top_theme:
                recommendations.append("Emphasize emotional intelligence and intuitive validation in all client interactions")
            if "technology_integration" in top_theme:
                recommendations.append("Position as the bridge between human creativity and AI capabilities")
        
        # Add competitive recommendations
        if competitive_intel.get("differentiation_focus"):
            recommendations.append("Continue focus on differentiation over superiority claims")
        
        # Add market timing recommendations
        if market_mapping.get("market_readiness"):
            recommendations.append("Capitalize on current market timing with accelerated launch strategy")
        
        return recommendations
    
    def _generate_positioning_from_deep_analysis(self, theme_analysis: dict, competitive_intel: dict, brand_brief: str) -> dict:
        """Generate positioning from deep analysis"""
        
        dominant_themes = [theme[0] for theme in theme_analysis.get("dominant_themes", [])]
        
        if "brand_operator" in brand_brief.lower():
            target = "Brand operators and founders"
        else:
            target = "Forward-thinking technology brands"
        
        return {
            "target_audience": target,
            "category": "Human-centered AI brand intelligence agency",
            "positioning_statement": "For brand operators who want breakthrough positioning, only SUBFRACTURE keeps humans in the tech loop because we start with the end in mind",
            "category_disruption": "Anti-slop, human-centered alternative to traditional agencies and AI tools"
        }
    
    def _generate_advantages_from_deep_analysis(self, theme_analysis: dict, frameworks: dict, brand_brief: str) -> List[str]:
        """Generate competitive advantages from deep analysis"""
        
        advantages = [
            "Cross-disciplinary integration: Strategy + Creative + Design + Technology",
            "Human-centered AI approach: Keeping humans in the tech loop",
            "Proprietary methodology: Creative destructionism + vesica pisces"
        ]
        
        if "brand worlds" in brand_brief.lower():
            advantages.append("Living brand worlds: Interactive, breathing brand experiences")
        
        if frameworks:
            advantages.append(f"Strategic framework sophistication: {len(frameworks)} methodologies detected")
        
        return advantages
    
    def _extract_personality_deep(self, brand_brief: str, sentiment_analysis: dict) -> dict:
        """Extract brand personality from deep analysis"""
        
        personality = {
            "core_traits": "Human, innovative, authentic",
            "communication_style": "Direct, passionate, anti-corporate",
            "brand_archetype": "The Rebel + The Magician"
        }
        
        if sentiment_analysis.get("energy_level", 0) > 10:
            personality["energy_signature"] = "High-energy, passionate"
        
        if "rock star" in brand_brief.lower():
            personality["aspirational_identity"] = "Technology rock stars"
        
        return personality


# Create the main graph for LangGraph Platform
def create_demo_graph() -> StateGraph:
    """
    Create demo graph for LangGraph Platform deployment
    """
    
    # Create the agent
    agent = SubfractureDemoAgent()
    
    # Define the state schema for the platform
    class DemoState(dict):
        """Simple state schema for platform compatibility"""
        pass
    
    # Create the graph
    graph = StateGraph(DemoState)
    
    async def main_analysis_node(state: DemoState) -> DemoState:
        """Main analysis node for the platform"""
        
        # Extract inputs from state
        brand_brief = state.get("brand_brief", "")
        operator_context = state.get("operator_context", {})
        target_outcome = state.get("target_outcome", "")
        deep_analysis = state.get("deep_analysis", False)
        
        print(f"🔍 Analyzing brand brief: {len(brand_brief)} characters")
        print(f"👤 Operator: {operator_context.get('role', 'Unknown')}")
        print(f"🎯 Target: {target_outcome[:100]}...")
        
        analysis_mode = "DEEP" if deep_analysis else "STANDARD"
        print(f"🔧 Analysis mode: {analysis_mode}")
        
        # Debug: print first 200 chars of brand brief
        if brand_brief:
            print(f"📝 Brief preview: {brand_brief[:200]}...")
        
        # Execute SUBFRACTURE analysis
        result = await agent.analyze_transcript(
            brand_brief=brand_brief,
            operator_context=operator_context,
            target_outcome=target_outcome,
            deep_analysis=deep_analysis
        )
        
        print(f"✅ Analysis completed: {result.get('status')}")
        print(f"📊 Gravity Index: {result.get('analysis', {}).get('gravity_index', 'N/A')}")
        
        # Update state with result
        state.update(result)
        return state
    
    # Add the main node
    graph.add_node("subfracture_analysis", main_analysis_node)
    
    # Add edges
    graph.add_edge(START, "subfracture_analysis")
    graph.add_edge("subfracture_analysis", END)
    
    # Compile the graph
    return graph.compile()


# Create the graph instance for the platform
graph = create_demo_graph()


# Test function for local development
async def test_demo_agent():
    """Test function for local development"""
    
    print("🚀 Testing SUBFRACTURE Demo Agent")
    print("=" * 60)
    
    # Load the transcript test input
    try:
        with open("/mnt/c/Users/Admin/subfracture-langgraph/subfracture_transcript_input.json", "r") as f:
            test_input = json.load(f)
        print("📄 Loaded transcript test data")
        print(f"🔍 Data keys: {list(test_input.keys())}")
        print(f"📝 Brief length: {len(test_input.get('brand_brief', ''))}")
    except Exception as e:
        print(f"⚠️  Could not load transcript file: {e}")
        # Fallback test input
        test_input = {
            "brand_brief": "We're a human-centered AI design studio called SUBFRACTURE. We help brand operators create breakthrough positioning by keeping humans in the tech loop. Our approach combines creative strategy, design, and technology to build living brand worlds.",
            "operator_context": {
                "role": "Founder & Brand Strategist",
                "industry": "Creative Technology",
                "company_stage": "Launch Phase",
                "years_experience": 10,
                "participant_id": "demo_001"
            },
            "target_outcome": "Extract strategic insights and positioning opportunities for launching this innovative brand intelligence agency"
        }
    
    try:
        # Execute the graph
        compiled_graph = create_demo_graph()
        result = await compiled_graph.ainvoke(test_input)
        
        print("\n✅ Demo completed successfully!")
        print(f"📊 Result type: {type(result)}")
        print(f"🔍 Result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
        
        if result:
            print(f"📊 Analysis Status: {result.get('status', 'N/A')}")
            print(f"🌟 Gravity Index: {result.get('analysis', {}).get('gravity_index', 'N/A')}")
            print(f"🎯 Launch Confidence: {result.get('business_metrics', {}).get('launch_confidence', 'N/A')}")
            print(f"💡 Key Recommendations: {len(result.get('analysis', {}).get('recommendations', []))}")
            print(f"📈 Market Impact: {result.get('business_metrics', {}).get('estimated_market_impact', 'N/A')}")
        else:
            print("No result returned")
        
        return result
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return None


# LangGraph Platform State Schema
from typing import TypedDict

class SubfractureState(TypedDict):
    """State schema for SUBFRACTURE analysis"""
    brand_brief: str
    operator_context: Optional[Dict[str, Any]]
    target_outcome: Optional[str]
    deep_analysis: bool
    result: Optional[Dict[str, Any]]

# Analysis node function with error boundaries
async def analysis_node(state: SubfractureState) -> SubfractureState:
    """
    Main analysis node for LangGraph Platform
    Includes comprehensive error handling for robust deployment
    """
    try:
        # Validate input state
        brand_brief = state.get("brand_brief", "")
        if not brand_brief or not isinstance(brand_brief, str):
            return {
                "result": {
                    "status": "error",
                    "error": "Invalid or missing brand_brief",
                    "analysis": {},
                    "business_metrics": {}
                }
            }
        
        # Initialize agent with error handling
        try:
            agent = SubfractureDemoAgent()
        except Exception as e:
            return {
                "result": {
                    "status": "error", 
                    "error": f"Agent initialization failed: {str(e)}",
                    "analysis": {},
                    "business_metrics": {}
                }
            }
        
        # Execute analysis with timeout protection
        result = await agent.analyze_transcript(
            brand_brief=brand_brief,
            operator_context=state.get("operator_context"),
            target_outcome=state.get("target_outcome"),
            deep_analysis=state.get("deep_analysis", False)
        )
        
        # Validate result structure
        if not result or not isinstance(result, dict):
            return {
                "result": {
                    "status": "error",
                    "error": "Analysis returned invalid result",
                    "analysis": {},
                    "business_metrics": {}
                }
            }
        
        return {"result": result}
        
    except Exception as e:
        # Comprehensive error boundary
        return {
            "result": {
                "status": "error",
                "error": f"Analysis node failed: {str(e)}",
                "analysis": {},
                "business_metrics": {},
                "debug_info": {
                    "error_type": type(e).__name__,
                    "state_keys": list(state.keys()) if state else []
                }
            }
        }

# Create the LangGraph workflow with platform optimizations
try:
    workflow = StateGraph(SubfractureState)
    workflow.add_node("analysis", analysis_node)
    workflow.add_edge(START, "analysis")
    workflow.add_edge("analysis", END)
    
    # Compile the graph for platform deployment with error handling
    graph = workflow.compile()
    print("✅ SUBFRACTURE LangGraph successfully compiled for platform deployment")
    
except Exception as e:
    print(f"❌ Graph compilation failed: {e}")
    # Create fallback minimal graph if main compilation fails
    from langgraph.graph import StateGraph as FallbackStateGraph
    
    async def fallback_node(state: dict) -> dict:
        return {
            "result": {
                "status": "fallback_mode",
                "error": "Main graph compilation failed",
                "analysis": {"gravity_index": 0.0},
                "business_metrics": {"launch_confidence": "Unknown"}
            }
        }
    
    fallback_workflow = FallbackStateGraph(dict)
    fallback_workflow.add_node("fallback", fallback_node)
    fallback_workflow.add_edge(START, "fallback")
    fallback_workflow.add_edge("fallback", END)
    graph = fallback_workflow.compile()
    print("⚠️  Using fallback graph due to compilation error")

if __name__ == "__main__":
    # Run test when executed directly
    asyncio.run(test_demo_agent())