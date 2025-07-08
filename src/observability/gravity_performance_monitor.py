"""
SUBFRACTURE Gravity Optimization Performance Monitor

Real-time monitoring and optimization tracking for the five-gravity system.
Provides continuous measurement of brand magnetism improvements, physics
optimization opportunities, and competitive advantage development.

Monitors:
- Recognition Gravity: Visual distinctiveness optimization
- Comprehension Gravity: Verbal clarity improvements  
- Attraction Gravity: Cultural relevance enhancement
- Amplification Gravity: Partnership synergy development
- Trust Gravity: Experiential consistency building

Features:
- Real-time gravity strength tracking
- Optimization opportunity identification
- Physics-based improvement recommendations
- Competitive benchmarking
- ROI attribution for gravity improvements
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import structlog
from dataclasses import dataclass, asdict
from enum import Enum

from langsmith import traceable

from ..core.state import SubfractureGravityState, GravityType
from ..core.config import get_config

logger = structlog.get_logger()


class GravityOptimizationLevel(Enum):
    """Gravity optimization levels"""
    CRITICAL = "critical"      # < 0.3 - Requires immediate attention
    LOW = "low"               # 0.3-0.5 - Needs improvement 
    MODERATE = "moderate"     # 0.5-0.7 - Good with optimization potential
    HIGH = "high"            # 0.7-0.9 - Strong performance
    EXCEPTIONAL = "exceptional"  # > 0.9 - Outstanding performance


@dataclass
class GravityMetrics:
    """Individual gravity type metrics"""
    gravity_type: GravityType
    current_strength: float
    baseline_strength: float
    optimization_potential: float
    improvement_rate: float
    target_strength: float
    optimization_level: GravityOptimizationLevel
    recommendations: List[str]
    roi_attribution: float
    competitive_advantage: float
    measurement_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "gravity_type": self.gravity_type.value,
            "optimization_level": self.optimization_level.value,
            "measurement_timestamp": self.measurement_timestamp.isoformat()
        }


@dataclass
class SystemGravityMetrics:
    """Overall gravity system performance metrics"""
    total_gravity_index: float
    baseline_gravity_index: float
    improvement_percentage: float
    optimization_velocity: float
    physics_coherence_score: float
    competitive_gravity_advantage: float
    roi_attribution_total: float
    system_optimization_recommendations: List[str]
    priority_optimization_areas: List[GravityType]
    measurement_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "priority_optimization_areas": [gt.value for gt in self.priority_optimization_areas],
            "measurement_timestamp": self.measurement_timestamp.isoformat()
        }


class GravityPerformanceMonitor:
    """
    Real-time gravity optimization performance monitoring system
    """
    
    def __init__(self):
        self.config = get_config()
        self.logger = logger.bind(component="gravity_performance_monitor")
        
        # Performance tracking state
        self.gravity_history: Dict[GravityType, List[GravityMetrics]] = {
            gravity_type: [] for gravity_type in GravityType
        }
        self.system_history: List[SystemGravityMetrics] = []
        self.optimization_targets: Dict[GravityType, float] = self._initialize_optimization_targets()
        self.competitive_benchmarks: Dict[GravityType, float] = self._initialize_competitive_benchmarks()
        
    def _initialize_optimization_targets(self) -> Dict[GravityType, float]:
        """Initialize optimization targets for each gravity type"""
        
        return {
            GravityType.RECOGNITION: 0.85,    # Visual distinctiveness target
            GravityType.COMPREHENSION: 0.90,  # Verbal clarity target
            GravityType.ATTRACTION: 0.80,     # Cultural relevance target
            GravityType.AMPLIFICATION: 0.75,  # Partnership synergy target
            GravityType.TRUST: 0.95          # Experiential consistency target
        }
    
    def _initialize_competitive_benchmarks(self) -> Dict[GravityType, float]:
        """Initialize competitive benchmarks for gravity performance"""
        
        return {
            GravityType.RECOGNITION: 0.60,    # Industry average visual distinctiveness
            GravityType.COMPREHENSION: 0.65,  # Industry average message clarity
            GravityType.ATTRACTION: 0.55,     # Industry average cultural relevance
            GravityType.AMPLIFICATION: 0.45,  # Industry average partnership leverage
            GravityType.TRUST: 0.70          # Industry average trust building
        }
    
    @traceable(name="measure_gravity_performance")
    async def measure_gravity_performance(
        self,
        state: SubfractureGravityState,
        baseline_metrics: Optional[Dict[GravityType, float]] = None
    ) -> Dict[GravityType, GravityMetrics]:
        """Measure current gravity performance across all types"""
        
        current_time = datetime.now()
        gravity_metrics = {}
        
        try:
            # Extract current gravity analysis
            current_gravity = state.gravity_analysis or {}
            baseline_gravity = baseline_metrics or {gt: 0.5 for gt in GravityType}
            
            for gravity_type in GravityType:
                current_strength = current_gravity.get(gravity_type, 0.5)
                baseline_strength = baseline_gravity.get(gravity_type, 0.5)
                
                # Calculate metrics
                metrics = await self._calculate_gravity_metrics(
                    gravity_type=gravity_type,
                    current_strength=current_strength,
                    baseline_strength=baseline_strength,
                    measurement_time=current_time
                )
                
                # Store metrics
                gravity_metrics[gravity_type] = metrics
                self.gravity_history[gravity_type].append(metrics)
                
                # Log individual gravity performance
                self.logger.info(f"{gravity_type.value}_gravity_measured",
                               current_strength=current_strength,
                               optimization_level=metrics.optimization_level.value,
                               improvement_rate=metrics.improvement_rate,
                               optimization_potential=metrics.optimization_potential)
            
            return gravity_metrics
            
        except Exception as e:
            self.logger.error("Gravity performance measurement failed", error=str(e))
            raise
    
    @traceable(name="calculate_system_gravity_performance") 
    async def calculate_system_gravity_performance(
        self,
        individual_metrics: Dict[GravityType, GravityMetrics],
        baseline_system_index: Optional[float] = None
    ) -> SystemGravityMetrics:
        """Calculate overall system gravity performance"""
        
        current_time = datetime.now()
        
        try:
            # Calculate total gravity index
            total_gravity_index = sum(metrics.current_strength for metrics in individual_metrics.values()) / len(individual_metrics)
            baseline_index = baseline_system_index or 0.5
            
            # Calculate system-level metrics
            improvement_percentage = ((total_gravity_index - baseline_index) / baseline_index) * 100 if baseline_index > 0 else 0
            optimization_velocity = self._calculate_optimization_velocity(individual_metrics)
            physics_coherence_score = self._calculate_physics_coherence(individual_metrics)
            competitive_advantage = self._calculate_competitive_advantage(individual_metrics)
            roi_attribution = self._calculate_system_roi_attribution(individual_metrics)
            
            # Identify priority optimization areas
            priority_areas = self._identify_priority_optimization_areas(individual_metrics)
            
            # Generate system recommendations
            system_recommendations = await self._generate_system_recommendations(
                individual_metrics, total_gravity_index, priority_areas
            )
            
            # Create system metrics
            system_metrics = SystemGravityMetrics(
                total_gravity_index=total_gravity_index,
                baseline_gravity_index=baseline_index,
                improvement_percentage=improvement_percentage,
                optimization_velocity=optimization_velocity,
                physics_coherence_score=physics_coherence_score,
                competitive_gravity_advantage=competitive_advantage,
                roi_attribution_total=roi_attribution,
                system_optimization_recommendations=system_recommendations,
                priority_optimization_areas=priority_areas,
                measurement_timestamp=current_time
            )
            
            # Store system metrics
            self.system_history.append(system_metrics)
            
            self.logger.info("System gravity performance calculated",
                           total_gravity_index=total_gravity_index,
                           improvement_percentage=improvement_percentage,
                           optimization_velocity=optimization_velocity,
                           physics_coherence=physics_coherence_score,
                           priority_areas=[area.value for area in priority_areas])
            
            return system_metrics
            
        except Exception as e:
            self.logger.error("System gravity performance calculation failed", error=str(e))
            raise
    
    async def _calculate_gravity_metrics(
        self,
        gravity_type: GravityType,
        current_strength: float,
        baseline_strength: float,
        measurement_time: datetime
    ) -> GravityMetrics:
        """Calculate detailed metrics for individual gravity type"""
        
        # Calculate optimization potential
        target_strength = self.optimization_targets[gravity_type]
        optimization_potential = max(0, target_strength - current_strength)
        
        # Calculate improvement rate
        improvement_rate = self._calculate_improvement_rate(gravity_type, current_strength)
        
        # Determine optimization level
        optimization_level = self._determine_optimization_level(current_strength)
        
        # Generate recommendations
        recommendations = await self._generate_gravity_recommendations(gravity_type, current_strength, optimization_potential)
        
        # Calculate ROI attribution
        roi_attribution = self._calculate_gravity_roi_attribution(gravity_type, current_strength, baseline_strength)
        
        # Calculate competitive advantage
        competitive_benchmark = self.competitive_benchmarks[gravity_type]
        competitive_advantage = max(0, current_strength - competitive_benchmark)
        
        return GravityMetrics(
            gravity_type=gravity_type,
            current_strength=current_strength,
            baseline_strength=baseline_strength,
            optimization_potential=optimization_potential,
            improvement_rate=improvement_rate,
            target_strength=target_strength,
            optimization_level=optimization_level,
            recommendations=recommendations,
            roi_attribution=roi_attribution,
            competitive_advantage=competitive_advantage,
            measurement_timestamp=measurement_time
        )
    
    def _calculate_improvement_rate(self, gravity_type: GravityType, current_strength: float) -> float:
        """Calculate improvement rate based on historical data"""
        
        history = self.gravity_history[gravity_type]
        if len(history) < 2:
            return 0.0
        
        # Calculate improvement over last few measurements
        recent_measurements = history[-3:]  # Last 3 measurements
        if len(recent_measurements) >= 2:
            start_strength = recent_measurements[0].current_strength
            end_strength = recent_measurements[-1].current_strength
            time_delta = (recent_measurements[-1].measurement_timestamp - recent_measurements[0].measurement_timestamp).total_seconds()
            
            if time_delta > 0:
                return (end_strength - start_strength) / (time_delta / 3600)  # Per hour rate
        
        return 0.0
    
    def _determine_optimization_level(self, strength: float) -> GravityOptimizationLevel:
        """Determine optimization level based on strength"""
        
        if strength < 0.3:
            return GravityOptimizationLevel.CRITICAL
        elif strength < 0.5:
            return GravityOptimizationLevel.LOW
        elif strength < 0.7:
            return GravityOptimizationLevel.MODERATE
        elif strength < 0.9:
            return GravityOptimizationLevel.HIGH
        else:
            return GravityOptimizationLevel.EXCEPTIONAL
    
    async def _generate_gravity_recommendations(
        self,
        gravity_type: GravityType,
        current_strength: float,
        optimization_potential: float
    ) -> List[str]:
        """Generate specific recommendations for gravity optimization"""
        
        recommendations = []
        
        if gravity_type == GravityType.RECOGNITION:
            if current_strength < 0.6:
                recommendations.extend([
                    "Develop distinctive visual identity system with unique color palette",
                    "Create memorable brand mark that stands out in category",
                    "Establish consistent visual language across all touchpoints"
                ])
            elif current_strength < 0.8:
                recommendations.extend([
                    "Refine visual distinctiveness through advanced design systems",
                    "Optimize visual recognition across digital and physical applications",
                    "Test visual recall and memorability with target audience"
                ])
            else:
                recommendations.append("Maintain visual distinctiveness while exploring premium applications")
        
        elif gravity_type == GravityType.COMPREHENSION:
            if current_strength < 0.6:
                recommendations.extend([
                    "Simplify core messaging for immediate understanding",
                    "Develop clear value proposition statements",
                    "Create message hierarchy for different audience segments"
                ])
            elif current_strength < 0.8:
                recommendations.extend([
                    "Optimize message clarity through A/B testing",
                    "Develop compelling storytelling frameworks",
                    "Enhance verbal identity system consistency"
                ])
            else:
                recommendations.append("Focus on advanced message sophistication and thought leadership")
        
        elif gravity_type == GravityType.ATTRACTION:
            if current_strength < 0.6:
                recommendations.extend([
                    "Research cultural relevance and audience alignment",
                    "Develop authentic connection points with target culture",
                    "Create culturally resonant content and experiences"
                ])
            elif current_strength < 0.8:
                recommendations.extend([
                    "Deepen cultural integration through community engagement",
                    "Develop cultural leadership position in relevant spaces",
                    "Optimize cultural relevance across different audience segments"
                ])
            else:
                recommendations.append("Establish cultural thought leadership and trendsetting position")
        
        elif gravity_type == GravityType.AMPLIFICATION:
            if current_strength < 0.6:
                recommendations.extend([
                    "Identify strategic partnership opportunities",
                    "Develop referral and word-of-mouth systems",
                    "Create shareable content and experiences"
                ])
            elif current_strength < 0.8:
                recommendations.extend([
                    "Optimize partnership leverage and collaboration frameworks",
                    "Develop systematic amplification through network effects",
                    "Create compelling partnership value propositions"
                ])
            else:
                recommendations.append("Build ecosystem leadership and platform amplification capabilities")
        
        elif gravity_type == GravityType.TRUST:
            if current_strength < 0.6:
                recommendations.extend([
                    "Establish consistent experience delivery across touchpoints",
                    "Develop transparent communication and feedback systems", 
                    "Create trust-building content and social proof"
                ])
            elif current_strength < 0.8:
                recommendations.extend([
                    "Optimize trust signals and credibility markers",
                    "Develop systematic trust-building through customer success",
                    "Create premium trust experiences for key relationships"
                ])
            else:
                recommendations.append("Establish trust leadership and become category trust benchmark")
        
        return recommendations
    
    def _calculate_optimization_velocity(self, individual_metrics: Dict[GravityType, GravityMetrics]) -> float:
        """Calculate overall optimization velocity across gravity types"""
        
        improvement_rates = [metrics.improvement_rate for metrics in individual_metrics.values()]
        if improvement_rates:
            return sum(improvement_rates) / len(improvement_rates)
        return 0.0
    
    def _calculate_physics_coherence(self, individual_metrics: Dict[GravityType, GravityMetrics]) -> float:
        """Calculate physics coherence score (how well gravity types work together)"""
        
        strengths = [metrics.current_strength for metrics in individual_metrics.values()]
        if not strengths:
            return 0.0
        
        # Calculate standard deviation (lower = more coherent)
        mean_strength = sum(strengths) / len(strengths)
        variance = sum((s - mean_strength) ** 2 for s in strengths) / len(strengths)
        std_deviation = variance ** 0.5
        
        # Convert to coherence score (1.0 = perfect coherence, 0.0 = no coherence)
        coherence_score = max(0.0, 1.0 - (std_deviation * 2))  # Scale std dev to 0-1
        
        return coherence_score
    
    def _calculate_competitive_advantage(self, individual_metrics: Dict[GravityType, GravityMetrics]) -> float:
        """Calculate overall competitive advantage from gravity performance"""
        
        competitive_advantages = [metrics.competitive_advantage for metrics in individual_metrics.values()]
        if competitive_advantages:
            return sum(competitive_advantages) / len(competitive_advantages)
        return 0.0
    
    def _calculate_system_roi_attribution(self, individual_metrics: Dict[GravityType, GravityMetrics]) -> float:
        """Calculate total ROI attribution from gravity improvements"""
        
        roi_attributions = [metrics.roi_attribution for metrics in individual_metrics.values()]
        return sum(roi_attributions)
    
    def _calculate_gravity_roi_attribution(
        self,
        gravity_type: GravityType,
        current_strength: float,
        baseline_strength: float
    ) -> float:
        """Calculate ROI attribution for specific gravity improvement"""
        
        improvement = max(0, current_strength - baseline_strength)
        
        # ROI attribution factors by gravity type
        roi_factors = {
            GravityType.RECOGNITION: 0.15,    # Visual improvements drive 15% of brand ROI
            GravityType.COMPREHENSION: 0.25,  # Message clarity drives 25% of conversion ROI
            GravityType.ATTRACTION: 0.20,     # Cultural relevance drives 20% of engagement ROI
            GravityType.AMPLIFICATION: 0.30,  # Partnership leverage drives 30% of growth ROI
            GravityType.TRUST: 0.35          # Trust building drives 35% of retention ROI
        }
        
        base_roi_factor = roi_factors.get(gravity_type, 0.2)
        return improvement * base_roi_factor
    
    def _identify_priority_optimization_areas(
        self,
        individual_metrics: Dict[GravityType, GravityMetrics]
    ) -> List[GravityType]:
        """Identify priority areas for optimization"""
        
        # Sort by optimization potential (highest first)
        sorted_by_potential = sorted(
            individual_metrics.items(),
            key=lambda x: x[1].optimization_potential,
            reverse=True
        )
        
        # Return top 3 optimization priorities
        priority_areas = [gravity_type for gravity_type, metrics in sorted_by_potential[:3]]
        
        return priority_areas
    
    async def _generate_system_recommendations(
        self,
        individual_metrics: Dict[GravityType, GravityMetrics],
        total_gravity_index: float,
        priority_areas: List[GravityType]
    ) -> List[str]:
        """Generate system-level optimization recommendations"""
        
        recommendations = []
        
        # Overall system recommendations
        if total_gravity_index < 0.6:
            recommendations.append("Focus on foundational gravity building across all types for systemic improvement")
        elif total_gravity_index < 0.8:
            recommendations.append("Optimize gravity coherence and focus on top 2 priority areas for accelerated growth")
        else:
            recommendations.append("Maintain gravity excellence while exploring advanced optimization opportunities")
        
        # Priority-specific recommendations
        if GravityType.RECOGNITION in priority_areas:
            recommendations.append("Prioritize visual distinctiveness development for immediate market impact")
        
        if GravityType.COMPREHENSION in priority_areas:
            recommendations.append("Focus on message clarity optimization for conversion improvement")
        
        if GravityType.ATTRACTION in priority_areas:
            recommendations.append("Invest in cultural relevance development for authentic audience connection")
        
        if GravityType.AMPLIFICATION in priority_areas:
            recommendations.append("Develop strategic partnerships and referral systems for growth acceleration")
        
        if GravityType.TRUST in priority_areas:
            recommendations.append("Build systematic trust experiences for sustainable relationship development")
        
        # Physics coherence recommendations
        physics_coherence = self._calculate_physics_coherence(individual_metrics)
        if physics_coherence < 0.7:
            recommendations.append("Improve gravity type coherence through integrated brand experience design")
        
        return recommendations
    
    @traceable(name="generate_gravity_performance_report")
    async def generate_gravity_performance_report(
        self,
        individual_metrics: Dict[GravityType, GravityMetrics],
        system_metrics: SystemGravityMetrics
    ) -> Dict[str, Any]:
        """Generate comprehensive gravity performance report"""
        
        try:
            # Create performance summary
            performance_summary = {
                "overall_performance": {
                    "total_gravity_index": system_metrics.total_gravity_index,
                    "improvement_percentage": system_metrics.improvement_percentage,
                    "optimization_velocity": system_metrics.optimization_velocity,
                    "physics_coherence_score": system_metrics.physics_coherence_score,
                    "competitive_advantage": system_metrics.competitive_gravity_advantage,
                    "roi_attribution": system_metrics.roi_attribution_total
                },
                "individual_gravity_performance": {
                    gravity_type.value: metrics.to_dict()
                    for gravity_type, metrics in individual_metrics.items()
                },
                "optimization_roadmap": {
                    "priority_areas": [area.value for area in system_metrics.priority_optimization_areas],
                    "system_recommendations": system_metrics.system_optimization_recommendations,
                    "individual_recommendations": {
                        gravity_type.value: metrics.recommendations
                        for gravity_type, metrics in individual_metrics.items()
                    }
                },
                "competitive_analysis": {
                    gravity_type.value: {
                        "current_strength": metrics.current_strength,
                        "competitive_benchmark": self.competitive_benchmarks[gravity_type],
                        "competitive_advantage": metrics.competitive_advantage,
                        "market_position": "leading" if metrics.competitive_advantage > 0.2 else "competitive" if metrics.competitive_advantage > 0 else "below_market"
                    }
                    for gravity_type, metrics in individual_metrics.items()
                },
                "roi_attribution_breakdown": {
                    gravity_type.value: metrics.roi_attribution
                    for gravity_type, metrics in individual_metrics.items()
                },
                "performance_trends": self._calculate_performance_trends(),
                "report_metadata": {
                    "generation_timestamp": datetime.now().isoformat(),
                    "measurement_timestamp": system_metrics.measurement_timestamp.isoformat(),
                    "measurement_count": len(self.system_history),
                    "tracking_duration_hours": self._calculate_tracking_duration()
                }
            }
            
            self.logger.info("Gravity performance report generated",
                           total_gravity_index=system_metrics.total_gravity_index,
                           priority_areas=len(system_metrics.priority_optimization_areas),
                           recommendations=len(system_metrics.system_optimization_recommendations))
            
            return performance_summary
            
        except Exception as e:
            self.logger.error("Gravity performance report generation failed", error=str(e))
            raise
    
    def _calculate_performance_trends(self) -> Dict[str, Any]:
        """Calculate performance trends from historical data"""
        
        if len(self.system_history) < 2:
            return {"trend_data_insufficient": True}
        
        # Calculate trends from last 5 measurements
        recent_history = self.system_history[-5:]
        
        # Gravity index trend
        gravity_indices = [metrics.total_gravity_index for metrics in recent_history]
        gravity_trend = "improving" if gravity_indices[-1] > gravity_indices[0] else "declining"
        
        # Optimization velocity trend
        velocities = [metrics.optimization_velocity for metrics in recent_history]
        velocity_trend = "accelerating" if velocities[-1] > velocities[0] else "decelerating"
        
        return {
            "gravity_index_trend": gravity_trend,
            "optimization_velocity_trend": velocity_trend,
            "measurement_count": len(recent_history),
            "trend_reliability": "high" if len(recent_history) >= 5 else "moderate"
        }
    
    def _calculate_tracking_duration(self) -> float:
        """Calculate total tracking duration in hours"""
        
        if not self.system_history:
            return 0.0
        
        start_time = self.system_history[0].measurement_timestamp
        end_time = self.system_history[-1].measurement_timestamp
        duration = (end_time - start_time).total_seconds() / 3600  # Convert to hours
        
        return duration


# Global gravity performance monitor instance
gravity_monitor = GravityPerformanceMonitor()


@traceable(name="monitor_gravity_performance")
async def monitor_gravity_performance(
    state: SubfractureGravityState,
    baseline_metrics: Optional[Dict[GravityType, float]] = None
) -> Dict[str, Any]:
    """
    Main function to monitor gravity performance and generate optimization insights
    """
    
    try:
        # Measure individual gravity performance
        individual_metrics = await gravity_monitor.measure_gravity_performance(
            state=state,
            baseline_metrics=baseline_metrics
        )
        
        # Calculate system performance
        system_metrics = await gravity_monitor.calculate_system_gravity_performance(
            individual_metrics=individual_metrics,
            baseline_system_index=0.5  # Default baseline
        )
        
        # Generate comprehensive performance report
        performance_report = await gravity_monitor.generate_gravity_performance_report(
            individual_metrics=individual_metrics,
            system_metrics=system_metrics
        )
        
        return {
            "gravity_performance_monitoring": performance_report,
            "individual_gravity_metrics": {gt.value: metrics.to_dict() for gt, metrics in individual_metrics.items()},
            "system_gravity_metrics": system_metrics.to_dict(),
            "monitoring_summary": {
                "total_gravity_index": system_metrics.total_gravity_index,
                "optimization_velocity": system_metrics.optimization_velocity,
                "priority_optimization_count": len(system_metrics.priority_optimization_areas),
                "competitive_advantage": system_metrics.competitive_gravity_advantage,
                "roi_attribution": system_metrics.roi_attribution_total
            }
        }
        
    except Exception as e:
        logger.error("Gravity performance monitoring failed", error=str(e))
        raise