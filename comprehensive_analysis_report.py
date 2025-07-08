#!/usr/bin/env python3
"""
SUBFRACTURE Comprehensive Analysis Report Generator
Shows the detailed "working" behind the brand intelligence analysis
"""

import asyncio
import json
import re
from collections import Counter
from demo_agent import SubfractureDemoAgent

class SubfractureAnalysisExplainer:
    """
    Explains the detailed working behind SUBFRACTURE's analysis
    Shows how insights are extracted from the transcript
    """
    
    def __init__(self):
        self.agent = SubfractureDemoAgent()
    
    def analyze_transcript_deeply(self, brand_brief: str) -> dict:
        """
        Deep analysis showing the working behind the scenes
        """
        
        print("🔬 SUBFRACTURE Deep Analysis - Showing The Working")
        print("=" * 80)
        
        # 1. Content Analysis
        content_stats = self._analyze_content_structure(brand_brief)
        
        # 2. Theme Detection
        theme_analysis = self._detailed_theme_analysis(brand_brief)
        
        # 3. Key Phrase Extraction
        key_phrases = self._extract_key_phrases(brand_brief)
        
        # 4. Sentiment and Tone Analysis
        sentiment_analysis = self._analyze_sentiment_and_tone(brand_brief)
        
        # 5. Strategic Framework Detection
        frameworks = self._detect_strategic_frameworks(brand_brief)
        
        # 6. Competitive Intelligence
        competitive_intel = self._extract_competitive_intelligence(brand_brief)
        
        # 7. Market Opportunity Mapping
        market_mapping = self._map_market_opportunities(brand_brief)
        
        # 8. Brand Architecture Analysis
        brand_architecture = self._analyze_brand_architecture(brand_brief)
        
        return {
            "content_analysis": content_stats,
            "theme_analysis": theme_analysis,
            "key_phrases": key_phrases,
            "sentiment_analysis": sentiment_analysis,
            "strategic_frameworks": frameworks,
            "competitive_intelligence": competitive_intel,
            "market_opportunities": market_mapping,
            "brand_architecture": brand_architecture
        }
    
    def _analyze_content_structure(self, text: str) -> dict:
        """Analyze the structural elements of the content"""
        
        print("\n📊 1. CONTENT STRUCTURE ANALYSIS")
        print("-" * 50)
        
        # Basic metrics
        char_count = len(text)
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        
        # Question analysis
        questions = re.findall(r'[^.!?]*\?', text)
        question_count = len(questions)
        
        # Speaker analysis (looking for conversation patterns)
        speaker_patterns = re.findall(r'(I|we|you|they)\s+(?:said|think|feel|believe|want)', text.lower())
        
        # Time references
        time_refs = re.findall(r'(yesterday|today|tomorrow|next|last|future|now|currently)', text.lower())
        
        stats = {
            "total_characters": char_count,
            "total_words": word_count,
            "total_sentences": sentence_count,
            "total_paragraphs": paragraph_count,
            "questions_asked": question_count,
            "speaker_references": len(speaker_patterns),
            "temporal_references": len(time_refs),
            "avg_sentence_length": word_count / max(1, sentence_count),
            "conversation_density": question_count / max(1, paragraph_count)
        }
        
        print(f"  📝 Content Volume: {char_count:,} characters, {word_count:,} words")
        print(f"  💬 Conversation Flow: {question_count} questions across {paragraph_count} sections")
        print(f"  🎯 Engagement Level: {stats['conversation_density']:.2f} questions per section")
        print(f"  ⏱️  Temporal Context: {len(time_refs)} time references")
        
        return stats
    
    def _detailed_theme_analysis(self, text: str) -> dict:
        """Deep theme analysis with frequency scoring"""
        
        print("\n🎨 2. THEMATIC ANALYSIS")
        print("-" * 50)
        
        # Enhanced theme detection with weighted keywords
        theme_keywords = {
            "human_centered": {
                "primary": ["human", "heart", "intuition", "personal", "authentic", "soul", "emotion"],
                "secondary": ["feel", "experience", "touch", "connection", "relationship"],
                "weight": 1.5
            },
            "technology_integration": {
                "primary": ["AI", "technology", "tech", "digital", "cyborg", "machine", "algorithm"],
                "secondary": ["automation", "intelligence", "smart", "system"],
                "weight": 1.3
            },
            "creative_methodology": {
                "primary": ["creative", "design", "strategy", "methodology", "framework", "process"],
                "secondary": ["approach", "method", "technique", "workflow"],
                "weight": 1.2
            },
            "brand_positioning": {
                "primary": ["brand", "positioning", "identity", "personality", "voice", "essence"],
                "secondary": ["message", "communication", "story", "narrative"],
                "weight": 1.4
            },
            "market_disruption": {
                "primary": ["disruption", "different", "unique", "breakthrough", "innovation"],
                "secondary": ["new", "novel", "revolutionary", "game-changing"],
                "weight": 1.3
            },
            "business_strategy": {
                "primary": ["business", "strategy", "market", "competitive", "advantage"],
                "secondary": ["opportunity", "growth", "scaling", "revenue"],
                "weight": 1.1
            }
        }
        
        theme_scores = {}
        theme_details = {}
        
        for theme, config in theme_keywords.items():
            primary_matches = []
            secondary_matches = []
            
            # Count primary keywords
            for keyword in config["primary"]:
                matches = len(re.findall(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE))
                if matches > 0:
                    primary_matches.append((keyword, matches))
            
            # Count secondary keywords  
            for keyword in config["secondary"]:
                matches = len(re.findall(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE))
                if matches > 0:
                    secondary_matches.append((keyword, matches))
            
            # Calculate weighted score
            primary_score = sum(count * config["weight"] for _, count in primary_matches)
            secondary_score = sum(count * 0.5 for _, count in secondary_matches)
            total_score = (primary_score + secondary_score) / len(text) * 10000
            
            theme_scores[theme] = min(1.0, total_score)
            theme_details[theme] = {
                "primary_matches": primary_matches,
                "secondary_matches": secondary_matches,
                "weighted_score": total_score,
                "normalized_score": theme_scores[theme]
            }
        
        # Show detailed results
        for theme, details in theme_details.items():
            score = details["normalized_score"]
            print(f"  🎯 {theme.replace('_', ' ').title()}: {score:.3f}")
            if details["primary_matches"]:
                top_matches = sorted(details["primary_matches"], key=lambda x: x[1], reverse=True)[:3]
                print(f"     Key terms: {', '.join([f'{term}({count})' for term, count in top_matches])}")
        
        return {
            "theme_scores": theme_scores,
            "theme_details": theme_details,
            "dominant_themes": sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        }
    
    def _extract_key_phrases(self, text: str) -> dict:
        """Extract and analyze key phrases and concepts"""
        
        print("\n🔑 3. KEY PHRASE EXTRACTION")
        print("-" * 50)
        
        # Brand-specific phrases
        brand_phrases = [
            "brand operator", "brand intelligence", "creative destructionism", 
            "vesica pisces", "humans in the tech loop", "brand worlds",
            "start with the end in mind", "heart knows", "anti-slop"
        ]
        
        # Strategic concepts
        strategic_concepts = [
            "positioning", "differentiation", "competitive advantage", 
            "market opportunity", "unique selling proposition", "target audience"
        ]
        
        # Methodology terms
        methodology_terms = [
            "methodology", "framework", "approach", "process", "system", "workflow"
        ]
        
        phrase_analysis = {}
        
        for phrase_list, category in [
            (brand_phrases, "brand_specific"),
            (strategic_concepts, "strategic"),
            (methodology_terms, "methodology")
        ]:
            category_results = {}
            for phrase in phrase_list:
                count = len(re.findall(rf'\b{re.escape(phrase)}\b', text, re.IGNORECASE))
                if count > 0:
                    category_results[phrase] = count
            phrase_analysis[category] = category_results
        
        # Show results
        for category, phrases in phrase_analysis.items():
            if phrases:
                print(f"  📋 {category.replace('_', ' ').title()}:")
                for phrase, count in sorted(phrases.items(), key=lambda x: x[1], reverse=True):
                    print(f"     • \"{phrase}\": {count} mentions")
        
        return phrase_analysis
    
    def _analyze_sentiment_and_tone(self, text: str) -> dict:
        """Analyze sentiment and communication tone"""
        
        print("\n😊 4. SENTIMENT & TONE ANALYSIS")
        print("-" * 50)
        
        # Sentiment indicators
        positive_indicators = ["love", "great", "fantastic", "amazing", "cool", "awesome", "brilliant"]
        negative_indicators = ["hate", "bad", "terrible", "awful", "sucks", "problem", "issue"]
        confidence_indicators = ["confident", "sure", "certain", "definitely", "absolutely"]
        uncertainty_indicators = ["maybe", "perhaps", "might", "unsure", "don't know"]
        
        # Energy level indicators
        high_energy = ["fucking", "shit", "crazy", "wild", "insane", "massive"]
        casual_tone = ["like", "you know", "I mean", "sort of", "kind of"]
        
        sentiment_counts = {
            "positive": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in positive_indicators),
            "negative": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in negative_indicators),
            "confident": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in confidence_indicators),
            "uncertain": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in uncertainty_indicators),
            "high_energy": sum(len(re.findall(rf'\b{word}\b', text, re.IGNORECASE)) for word in high_energy),
            "casual": sum(len(re.findall(rf'\b{phrase}\b', text, re.IGNORECASE)) for phrase in casual_tone)
        }
        
        # Calculate ratios
        total_sentiment = sentiment_counts["positive"] + sentiment_counts["negative"]
        sentiment_ratio = sentiment_counts["positive"] / max(1, total_sentiment)
        
        total_confidence = sentiment_counts["confident"] + sentiment_counts["uncertain"]
        confidence_ratio = sentiment_counts["confident"] / max(1, total_confidence)
        
        print(f"  😊 Sentiment Balance: {sentiment_ratio:.2f} (positive/total)")
        print(f"  💪 Confidence Level: {confidence_ratio:.2f} (confident/total)")
        print(f"  ⚡ Energy Level: {sentiment_counts['high_energy']} high-energy expressions")
        print(f"  💬 Conversational Style: {sentiment_counts['casual']} casual markers")
        
        return {
            "sentiment_counts": sentiment_counts,
            "sentiment_ratio": sentiment_ratio,
            "confidence_ratio": confidence_ratio,
            "overall_tone": "confident_casual" if confidence_ratio > 0.6 and sentiment_counts['casual'] > 10 else "professional"
        }
    
    def _detect_strategic_frameworks(self, text: str) -> dict:
        """Detect mentions of strategic frameworks and methodologies"""
        
        print("\n🏗️  5. STRATEGIC FRAMEWORKS DETECTED")
        print("-" * 50)
        
        frameworks = {
            "Design Thinking": ["design thinking", "human-centered design", "empathy", "ideate", "prototype"],
            "Lean Startup": ["lean", "MVP", "minimum viable product", "iterate", "pivot"],
            "Jobs to be Done": ["jobs to be done", "job to be done", "hire", "progress"],
            "Blue Ocean Strategy": ["blue ocean", "red ocean", "uncontested market"],
            "OKRs": ["OKR", "objectives", "key results", "quarterly"],
            "Growth Hacking": ["growth hack", "viral", "acquisition", "retention"],
            "Agile": ["agile", "sprint", "scrum", "iteration"],
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
        
        for framework, data in detected_frameworks.items():
            print(f"  📋 {framework}: {data['total_mentions']} mentions")
            top_keywords = sorted(data['keywords_found'], key=lambda x: x[1], reverse=True)[:2]
            print(f"     Key terms: {', '.join([f'{kw}({cnt})' for kw, cnt in top_keywords])}")
        
        return detected_frameworks
    
    def _extract_competitive_intelligence(self, text: str) -> dict:
        """Extract competitive landscape insights"""
        
        print("\n🎯 6. COMPETITIVE INTELLIGENCE")
        print("-" * 50)
        
        # Look for company/agency mentions
        company_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:agency|studio|company|brand)\b',
            r'\b(?:agency|studio|company)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\b(Ogilvy|Wieden|Kennedy|IDEO|McKinsey|Deloitte|Accenture)\b'
        ]
        
        mentioned_companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            mentioned_companies.extend(matches)
        
        # Competitive positioning keywords
        competitive_terms = {
            "differentiation": ["different", "unique", "unlike", "alternative", "opposite"],
            "superiority": ["better", "best", "superior", "outperform", "leading"],
            "innovation": ["first", "new", "innovative", "pioneering", "breakthrough"],
            "challenges": ["problem", "issue", "challenge", "difficulty", "struggle"]
        }
        
        competitive_analysis = {}
        for category, terms in competitive_terms.items():
            count = sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in terms)
            competitive_analysis[category] = count
        
        print(f"  🏢 Companies Mentioned: {len(set(mentioned_companies))}")
        if mentioned_companies:
            company_counts = Counter(mentioned_companies)
            for company, count in company_counts.most_common(3):
                print(f"     • {company}: {count} mentions")
        
        print(f"  🎯 Competitive Stance:")
        for category, count in competitive_analysis.items():
            print(f"     • {category.title()}: {count} references")
        
        return {
            "mentioned_companies": mentioned_companies,
            "competitive_positioning": competitive_analysis,
            "differentiation_focus": competitive_analysis["differentiation"] > competitive_analysis["superiority"]
        }
    
    def _map_market_opportunities(self, text: str) -> dict:
        """Map market opportunities and gaps"""
        
        print("\n🌟 7. MARKET OPPORTUNITY MAPPING")
        print("-" * 50)
        
        # Market gap indicators
        gap_indicators = [
            "no one", "nobody", "missing", "gap", "opportunity", "need", "demand", 
            "underserved", "overlooked", "ignored", "untapped"
        ]
        
        # Market size indicators
        size_indicators = [
            "million", "billion", "thousand", "huge", "massive", "large", "big",
            "growing", "expanding", "increasing"
        ]
        
        # Timing indicators
        timing_indicators = [
            "now", "timing", "moment", "opportunity", "ready", "ripe", "perfect time",
            "wave", "trend", "shift", "change"
        ]
        
        opportunity_signals = {
            "market_gaps": sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in gap_indicators),
            "market_size": sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in size_indicators),
            "timing_signals": sum(len(re.findall(rf'\b{term}\b', text, re.IGNORECASE)) for term in timing_indicators)
        }
        
        # Industry mentions
        industries = ["advertising", "marketing", "branding", "design", "technology", "AI", "startup"]
        industry_mentions = {}
        for industry in industries:
            count = len(re.findall(rf'\b{industry}\b', text, re.IGNORECASE))
            if count > 0:
                industry_mentions[industry] = count
        
        print(f"  🔍 Market Gap Signals: {opportunity_signals['market_gaps']} indicators")
        print(f"  📈 Market Size Signals: {opportunity_signals['market_size']} indicators")
        print(f"  ⏰ Timing Signals: {opportunity_signals['timing_signals']} indicators")
        print(f"  🏭 Industry Focus:")
        for industry, count in sorted(industry_mentions.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"     • {industry.title()}: {count} mentions")
        
        return {
            "opportunity_signals": opportunity_signals,
            "industry_mentions": industry_mentions,
            "market_readiness": opportunity_signals['timing_signals'] > 5
        }
    
    def _analyze_brand_architecture(self, text: str) -> dict:
        """Analyze brand architecture elements"""
        
        print("\n🏛️  8. BRAND ARCHITECTURE ANALYSIS")
        print("-" * 50)
        
        # Brand elements
        brand_elements = {
            "purpose": ["purpose", "mission", "why", "reason", "cause"],
            "vision": ["vision", "future", "aspiration", "dream", "goal"],
            "values": ["values", "principles", "beliefs", "standards"],
            "personality": ["personality", "character", "traits", "style"],
            "positioning": ["positioning", "place", "market position", "category"],
            "promise": ["promise", "commitment", "guarantee", "deliver"]
        }
        
        architecture_strength = {}
        for element, keywords in brand_elements.items():
            count = sum(len(re.findall(rf'\b{keyword}\b', text, re.IGNORECASE)) for keyword in keywords)
            architecture_strength[element] = count
        
        # Calculate completeness score
        defined_elements = sum(1 for count in architecture_strength.values() if count > 0)
        completeness_score = defined_elements / len(brand_elements)
        
        print(f"  📊 Brand Architecture Completeness: {completeness_score:.2f} ({defined_elements}/{len(brand_elements)} elements)")
        print(f"  🎯 Element Strength:")
        for element, count in sorted(architecture_strength.items(), key=lambda x: x[1], reverse=True):
            strength = "Strong" if count > 5 else "Moderate" if count > 2 else "Weak" if count > 0 else "Missing"
            print(f"     • {element.title()}: {strength} ({count} mentions)")
        
        return {
            "architecture_strength": architecture_strength,
            "completeness_score": completeness_score,
            "strongest_elements": sorted(architecture_strength.items(), key=lambda x: x[1], reverse=True)[:3]
        }

async def generate_comprehensive_report():
    """Generate the comprehensive analysis report"""
    
    # Load the transcript
    try:
        with open("/mnt/c/Users/Admin/subfracture-langgraph/subfracture_transcript_input.json", "r") as f:
            data = json.load(f)
        brand_brief = data["brand_brief"]
    except Exception as e:
        print(f"❌ Failed to load transcript: {e}")
        return
    
    # Initialize the analyzer
    analyzer = SubfractureAnalysisExplainer()
    
    # Perform deep analysis
    deep_analysis = analyzer.analyze_transcript_deeply(brand_brief)
    
    # Generate final summary
    print("\n" + "="*80)
    print("🎯 COMPREHENSIVE ANALYSIS SUMMARY")
    print("="*80)
    
    print(f"\n📊 **CONTENT METRICS**:")
    content = deep_analysis["content_analysis"]
    print(f"  • Volume: {content['total_words']:,} words in {content['total_paragraphs']} sections")
    print(f"  • Engagement: {content['conversation_density']:.2f} questions per section")
    print(f"  • Complexity: {content['avg_sentence_length']:.1f} words per sentence")
    
    print(f"\n🎨 **THEMATIC STRENGTH**:")
    themes = deep_analysis["theme_analysis"]["dominant_themes"]
    for theme, score in themes:
        print(f"  • {theme.replace('_', ' ').title()}: {score:.3f} strength")
    
    print(f"\n🔑 **KEY STRATEGIC CONCEPTS**:")
    key_phrases = deep_analysis["key_phrases"]
    for category, phrases in key_phrases.items():
        if phrases:
            top_phrase = max(phrases.items(), key=lambda x: x[1])
            print(f"  • {category.replace('_', ' ').title()}: \"{top_phrase[0]}\" ({top_phrase[1]} mentions)")
    
    print(f"\n😊 **COMMUNICATION STYLE**:")
    sentiment = deep_analysis["sentiment_analysis"]
    print(f"  • Sentiment Balance: {sentiment['sentiment_ratio']:.2f} (positive-leaning)")
    print(f"  • Confidence Level: {sentiment['confidence_ratio']:.2f}")
    print(f"  • Overall Tone: {sentiment['overall_tone'].replace('_', ' ').title()}")
    
    print(f"\n🏗️ **STRATEGIC FRAMEWORKS**:")
    frameworks = deep_analysis["strategic_frameworks"]
    for framework, data in list(frameworks.items())[:3]:
        print(f"  • {framework}: {data['total_mentions']} mentions")
    
    print(f"\n🎯 **COMPETITIVE POSITIONING**:")
    competitive = deep_analysis["competitive_intelligence"]
    print(f"  • Companies Referenced: {len(set(competitive['mentioned_companies']))}")
    print(f"  • Differentiation Focus: {'Yes' if competitive['differentiation_focus'] else 'No'}")
    
    print(f"\n🌟 **MARKET OPPORTUNITY STRENGTH**:")
    market = deep_analysis["market_opportunities"]
    signals = market["opportunity_signals"]
    print(f"  • Gap Identification: {signals['market_gaps']} signals")
    print(f"  • Timing Indicators: {signals['timing_signals']} signals")
    print(f"  • Market Readiness: {'High' if market['market_readiness'] else 'Moderate'}")
    
    print(f"\n🏛️ **BRAND ARCHITECTURE COMPLETENESS**:")
    architecture = deep_analysis["brand_architecture"]
    print(f"  • Overall Completeness: {architecture['completeness_score']:.2f}")
    strongest = architecture["strongest_elements"][:3]
    for element, strength in strongest:
        print(f"  • Strongest Element: {element.title()} ({strength} mentions)")
    
    # Save comprehensive analysis
    with open("/mnt/c/Users/Admin/subfracture-langgraph/comprehensive_analysis.json", "w") as f:
        json.dump(deep_analysis, f, indent=2)
    
    print(f"\n💾 **DETAILED ANALYSIS SAVED**: comprehensive_analysis.json")
    print(f"\n🎉 **CONCLUSION**: This analysis demonstrates SUBFRACTURE's ability to extract")
    print(f"deep strategic insights from unstructured brand conversations, revealing")
    print(f"positioning opportunities and competitive advantages that traditional")
    print(f"analysis methods might miss.")

if __name__ == "__main__":
    asyncio.run(generate_comprehensive_report())