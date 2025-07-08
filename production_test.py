#!/usr/bin/env python3
"""
SUBFRACTURE Production Testing Suite

Comprehensive testing with realistic brand scenarios to validate
production-ready system performance and business value delivery.
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.workflow import create_subfracture_workflow
from src.core.state import SubfractureGravityState
from src.core.memory_manager import memory_manager, initialize_memory_management
from src.core.cognee_integration import cognee_manager, initialize_cognee_memory
from src.core.error_handling import error_handler
from src.core.async_optimizer import async_optimizer

import structlog

# Configure logging
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
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class ProductionTester:
    """Production testing coordinator for SUBFRACTURE system"""
    
    def __init__(self):
        self.test_results = []
        self.test_start_time = None
        self.workflow = None
        
    async def initialize(self):
        """Initialize all system components for testing"""
        logger.info("Initializing production testing environment")
        
        # Initialize memory management
        await initialize_memory_management()
        
        # Initialize Cognee if available
        try:
            await initialize_cognee_memory()
        except Exception as e:
            logger.warning("Cognee initialization skipped", error=str(e))
        
        # Create workflow
        self.workflow = create_subfracture_workflow()
        
        logger.info("Production testing environment ready")
    
    def get_realistic_test_scenarios(self) -> List[Dict[str, Any]]:
        """Generate realistic brand scenarios for comprehensive testing"""
        
        return [
            {
                "name": "AI Consultancy Disruption",
                "brand_brief": "We're a conscious AI consultancy helping technology companies integrate AI in human-centered ways. Our challenge: the market is flooded with AI solutions that feel soulless and manipulative. Most consultancies either oversell AI's capabilities or underestimate its transformative potential. We need to establish ourselves as the trusted guide for companies wanting to implement AI that serves human flourishing rather than replacing it. Our clients range from Series A startups to Fortune 500 companies, all struggling with the same question: How do we harness AI's power while maintaining our humanity?",
                "operator_context": {
                    "role": "Founder & Lead Consultant",
                    "industry": "AI Consulting & Technology",
                    "company_stage": "Growth",
                    "years_experience": 8,
                    "team_size": 12,
                    "personal_investment": "Building technology solutions that serve human flourishing",
                    "vision": "Create a world where AI amplifies human wisdom rather than replacing it",
                    "biggest_challenge": "Differentiating in oversaturated AI consulting market",
                    "current_revenue": "$2.4M ARR",
                    "target_revenue": "$10M ARR in 24 months"
                },
                "target_outcome": "Establish market leadership in conscious AI consulting with premium positioning that justifies 3x higher rates than competitors",
                "expected_gravity_index": 0.75,
                "expected_roi": "$300k-500k"
            },
            
            {
                "name": "Sustainable Fashion Revolution",
                "brand_brief": "We're pioneering a circular fashion platform that transforms waste into luxury. The fashion industry creates 92 million tons of waste annually, yet sustainable fashion is still perceived as boring or expensive. We've developed revolutionary technology that converts textile waste into high-performance luxury fabrics that outperform traditional materials. Our challenge: the sustainable fashion space is crowded with well-meaning but underwhelming brands. Consumers want sustainability but won't compromise on style, quality, or status. We need to position ourselves not as 'sustainable fashion' but as the future of luxury itself.",
                "operator_context": {
                    "role": "Co-Founder & Creative Director",
                    "industry": "Fashion Technology & Sustainability",
                    "company_stage": "Series A",
                    "years_experience": 12,
                    "team_size": 35,
                    "personal_investment": "Revolutionizing fashion through regenerative innovation",
                    "vision": "Make sustainability the ultimate luxury",
                    "biggest_challenge": "Overcoming sustainability perception as compromise",
                    "current_revenue": "$5.8M ARR",
                    "target_revenue": "$25M ARR in 18 months"
                },
                "target_outcome": "Redefine luxury fashion category with sustainability as premium advantage, commanding 40% higher margins than traditional luxury brands",
                "expected_gravity_index": 0.80,
                "expected_roi": "$400k-650k"
            },
            
            {
                "name": "FinTech Mental Wellness",
                "brand_brief": "We're building the first financial wellness platform that treats money stress as a public health crisis. 72% of Americans report being stressed about money, yet traditional financial apps focus on budgeting without addressing the psychological barriers to financial health. Our platform combines AI-powered financial coaching with evidence-based mental health interventions. The challenge: FinTech is oversaturated with apps promising to 'fix your finances,' while mental health apps treat money as taboo. We're creating an entirely new category that requires shifting fundamental beliefs about the relationship between money and wellbeing.",
                "operator_context": {
                    "role": "CEO & Behavioral Economist",
                    "industry": "FinTech & Mental Health",
                    "company_stage": "Seed",
                    "years_experience": 6,
                    "team_size": 18,
                    "personal_investment": "Healing the toxic relationship between money and mental health",
                    "vision": "Financial wellness as fundamental human right",
                    "biggest_challenge": "Creating new category at intersection of finance and therapy",
                    "current_revenue": "$800K ARR",
                    "target_revenue": "$5M ARR in 30 months"
                },
                "target_outcome": "Establish financial wellness as essential health category, capturing early market leadership with premium B2B2C partnerships",
                "expected_gravity_index": 0.85,
                "expected_roi": "$250k-400k"
            }
        ]
    
    async def run_scenario_test(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow test for specific scenario"""
        
        scenario_name = scenario["name"]
        logger.info("Starting scenario test", scenario=scenario_name)
        
        start_time = time.time()
        
        try:
            # Create initial state
            initial_state = SubfractureGravityState(
                brand_brief=scenario["brand_brief"],
                operator_context=scenario["operator_context"],
                target_outcome=scenario["target_outcome"]
            )
            
            # Execute workflow
            result = await self.workflow.ainvoke({"state": initial_state})
            final_state = result.get("state")
            
            execution_time = time.time() - start_time
            
            # Analyze results
            gravity_index = getattr(final_state, "gravity_index", 0.0)
            breakthrough_discovered = bool(getattr(final_state, "primary_breakthrough", None))
            brand_world_created = bool(getattr(final_state, "brand_world", None))
            validation_passed = len(getattr(final_state, "validation_checkpoints", [])) >= 3
            
            # Quality assessment
            gravity_performance = gravity_index / scenario["expected_gravity_index"] if scenario["expected_gravity_index"] > 0 else 1.0
            
            test_result = {
                "scenario_name": scenario_name,
                "status": "success",
                "execution_time": execution_time,
                "gravity_index": gravity_index,
                "expected_gravity": scenario["expected_gravity_index"],
                "gravity_performance": gravity_performance,
                "breakthrough_discovered": breakthrough_discovered,
                "brand_world_created": brand_world_created,
                "validation_passed": validation_passed,
                "quality_score": (
                    int(breakthrough_discovered) +
                    int(brand_world_created) +
                    int(validation_passed) +
                    int(gravity_performance > 0.8)
                ) / 4,
                "deliverables": {
                    "strategy_insights": bool(getattr(final_state, "strategy_insights", None)),
                    "creative_directions": bool(getattr(final_state, "creative_directions", None)),
                    "design_synthesis": bool(getattr(final_state, "design_synthesis", None)),
                    "technology_roadmap": bool(getattr(final_state, "technology_roadmap", None)),
                    "primary_breakthrough": bool(getattr(final_state, "primary_breakthrough", None)),
                    "brand_world": bool(getattr(final_state, "brand_world", None))
                },
                "business_metrics": {
                    "expected_roi": scenario["expected_roi"],
                    "premium_justified": gravity_index > 0.7,
                    "market_differentiation": breakthrough_discovered,
                    "implementation_ready": brand_world_created
                }
            }
            
            logger.info("Scenario test completed", 
                       scenario=scenario_name,
                       execution_time=execution_time,
                       gravity_index=gravity_index,
                       quality_score=test_result["quality_score"])
            
            return test_result
            
        except Exception as e:
            logger.error("Scenario test failed", scenario=scenario_name, error=str(e))
            
            return {
                "scenario_name": scenario_name,
                "status": "failed",
                "error": str(e),
                "execution_time": time.time() - start_time,
                "quality_score": 0.0
            }
    
    async def run_system_performance_test(self) -> Dict[str, Any]:
        """Test system performance under load"""
        
        logger.info("Running system performance test")
        
        # Memory performance
        memory_summary = memory_manager.get_memory_summary()
        
        # Error handling performance
        error_summary = error_handler.get_error_summary()
        
        # Async optimization performance
        async_summary = async_optimizer.get_performance_summary()
        
        # Cognee performance (if available)
        cognee_status = {}
        if cognee_manager.initialized:
            cognee_status = cognee_manager.get_memory_status()
        
        performance_metrics = {
            "memory_management": {
                "monitoring_active": memory_summary.get("monitoring_active", False),
                "total_checkpoints": memory_summary.get("total_checkpoints", 0),
                "memory_efficiency": memory_summary.get("memory_usage_mb", 0) < 2048
            },
            "error_handling": {
                "error_count": error_summary.get("total_errors", 0),
                "recovery_rate": error_summary.get("recovery_success_rate", 1.0),
                "circuit_breaker_active": error_summary.get("circuit_breaker_active", False)
            },
            "async_optimization": {
                "total_optimizations": async_summary.get("total_optimizations", 0),
                "average_speedup": async_summary.get("average_speedup", 1.0),
                "parallel_efficiency": async_summary.get("parallel_efficiency", 1.0)
            },
            "cognee_integration": {
                "initialized": cognee_manager.initialized,
                "knowledge_entries": cognee_status.get("knowledge_entries", 0) if cognee_status else 0
            }
        }
        
        # Overall system health score
        health_score = (
            int(performance_metrics["memory_management"]["monitoring_active"]) +
            int(performance_metrics["error_handling"]["recovery_rate"] > 0.95) +
            int(performance_metrics["async_optimization"]["average_speedup"] > 1.2) +
            int(performance_metrics["memory_management"]["memory_efficiency"])
        ) / 4
        
        performance_metrics["overall_health_score"] = health_score
        
        logger.info("System performance test completed", health_score=health_score)
        
        return performance_metrics
    
    async def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Execute complete production test suite"""
        
        logger.info("Starting comprehensive production test suite")
        self.test_start_time = time.time()
        
        # Initialize system
        await self.initialize()
        
        # Get test scenarios
        scenarios = self.get_realistic_test_scenarios()
        
        # Run scenario tests
        scenario_results = []
        for scenario in scenarios:
            result = await self.run_scenario_test(scenario)
            scenario_results.append(result)
            self.test_results.append(result)
        
        # Run system performance test
        performance_results = await self.run_system_performance_test()
        
        # Calculate overall results
        total_execution_time = time.time() - self.test_start_time
        successful_tests = [r for r in scenario_results if r.get("status") == "success"]
        
        overall_quality_score = sum(r.get("quality_score", 0) for r in successful_tests) / len(scenario_results) if scenario_results else 0
        average_gravity_index = sum(r.get("gravity_index", 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
        comprehensive_results = {
            "test_summary": {
                "total_scenarios": len(scenarios),
                "successful_tests": len(successful_tests),
                "failed_tests": len(scenario_results) - len(successful_tests),
                "success_rate": len(successful_tests) / len(scenario_results) if scenario_results else 0,
                "total_execution_time": total_execution_time,
                "average_scenario_time": sum(r.get("execution_time", 0) for r in scenario_results) / len(scenario_results) if scenario_results else 0
            },
            "quality_metrics": {
                "overall_quality_score": overall_quality_score,
                "average_gravity_index": average_gravity_index,
                "breakthrough_discovery_rate": sum(1 for r in successful_tests if r.get("breakthrough_discovered")) / len(successful_tests) if successful_tests else 0,
                "brand_world_creation_rate": sum(1 for r in successful_tests if r.get("brand_world_created")) / len(successful_tests) if successful_tests else 0,
                "validation_pass_rate": sum(1 for r in successful_tests if r.get("validation_passed")) / len(successful_tests) if successful_tests else 0
            },
            "business_validation": {
                "premium_justification_rate": sum(1 for r in successful_tests if r.get("business_metrics", {}).get("premium_justified")) / len(successful_tests) if successful_tests else 0,
                "market_differentiation_rate": sum(1 for r in successful_tests if r.get("business_metrics", {}).get("market_differentiation")) / len(successful_tests) if successful_tests else 0,
                "implementation_readiness_rate": sum(1 for r in successful_tests if r.get("business_metrics", {}).get("implementation_ready")) / len(successful_tests) if successful_tests else 0
            },
            "system_performance": performance_results,
            "scenario_results": scenario_results,
            "production_readiness": {
                "system_stability": performance_results.get("overall_health_score", 0) > 0.8,
                "quality_threshold": overall_quality_score > 0.75,
                "performance_threshold": total_execution_time < 600,  # 10 minutes for all tests
                "business_value_validated": overall_quality_score > 0.8 and average_gravity_index > 0.7
            }
        }
        
        # Determine production readiness
        readiness_score = (
            int(comprehensive_results["production_readiness"]["system_stability"]) +
            int(comprehensive_results["production_readiness"]["quality_threshold"]) +
            int(comprehensive_results["production_readiness"]["performance_threshold"]) +
            int(comprehensive_results["production_readiness"]["business_value_validated"])
        ) / 4
        
        comprehensive_results["overall_production_readiness"] = readiness_score
        comprehensive_results["recommendation"] = "PRODUCTION READY" if readiness_score > 0.8 else "NEEDS OPTIMIZATION"
        
        logger.info("Comprehensive test suite completed",
                   success_rate=comprehensive_results["test_summary"]["success_rate"],
                   overall_quality=overall_quality_score,
                   production_readiness=readiness_score,
                   recommendation=comprehensive_results["recommendation"])
        
        return comprehensive_results
    
    def save_test_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to JSON file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"production_test_results_{timestamp}.json"
        
        results_path = Path("test_results") / filename
        results_path.parent.mkdir(exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info("Test results saved", filename=str(results_path))
        return str(results_path)
    
    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable test report"""
        
        report = []
        report.append("=" * 80)
        report.append("SUBFRACTURE PRODUCTION TEST RESULTS")
        report.append("=" * 80)
        report.append(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Execution Time: {results['test_summary']['total_execution_time']:.2f} seconds")
        report.append(f"Production Readiness: {results['recommendation']} ({results['overall_production_readiness']:.1%})")
        report.append("")
        
        # Test Summary
        report.append("TEST SUMMARY")
        report.append("-" * 40)
        summary = results["test_summary"]
        report.append(f"Scenarios Tested: {summary['total_scenarios']}")
        report.append(f"Successful Tests: {summary['successful_tests']}")
        report.append(f"Failed Tests: {summary['failed_tests']}")
        report.append(f"Success Rate: {summary['success_rate']:.1%}")
        report.append(f"Average Scenario Time: {summary['average_scenario_time']:.2f} seconds")
        report.append("")
        
        # Quality Metrics
        report.append("QUALITY METRICS")
        report.append("-" * 40)
        quality = results["quality_metrics"]
        report.append(f"Overall Quality Score: {quality['overall_quality_score']:.1%}")
        report.append(f"Average Gravity Index: {quality['average_gravity_index']:.2f}")
        report.append(f"Breakthrough Discovery Rate: {quality['breakthrough_discovery_rate']:.1%}")
        report.append(f"Brand World Creation Rate: {quality['brand_world_creation_rate']:.1%}")
        report.append(f"Validation Pass Rate: {quality['validation_pass_rate']:.1%}")
        report.append("")
        
        # Business Validation
        report.append("BUSINESS VALIDATION")
        report.append("-" * 40)
        business = results["business_validation"]
        report.append(f"Premium Justification Rate: {business['premium_justification_rate']:.1%}")
        report.append(f"Market Differentiation Rate: {business['market_differentiation_rate']:.1%}")
        report.append(f"Implementation Readiness Rate: {business['implementation_readiness_rate']:.1%}")
        report.append("")
        
        # System Performance
        report.append("SYSTEM PERFORMANCE")
        report.append("-" * 40)
        perf = results["system_performance"]
        report.append(f"Overall Health Score: {perf['overall_health_score']:.1%}")
        report.append(f"Memory Management: {'Active' if perf['memory_management']['monitoring_active'] else 'Inactive'}")
        report.append(f"Error Recovery Rate: {perf['error_handling']['recovery_rate']:.1%}")
        report.append(f"Async Speedup: {perf['async_optimization']['average_speedup']:.1f}x")
        report.append(f"Cognee Integration: {'Active' if perf['cognee_integration']['initialized'] else 'Inactive'}")
        report.append("")
        
        # Individual Scenario Results
        report.append("SCENARIO RESULTS")
        report.append("-" * 40)
        for scenario in results["scenario_results"]:
            if scenario.get("status") == "success":
                report.append(f"✅ {scenario['scenario_name']}")
                report.append(f"   Gravity Index: {scenario['gravity_index']:.2f}")
                report.append(f"   Quality Score: {scenario['quality_score']:.1%}")
                report.append(f"   Execution Time: {scenario['execution_time']:.2f}s")
            else:
                report.append(f"❌ {scenario['scenario_name']}")
                report.append(f"   Error: {scenario.get('error', 'Unknown')}")
                report.append(f"   Execution Time: {scenario['execution_time']:.2f}s")
            report.append("")
        
        # Production Readiness Assessment
        report.append("PRODUCTION READINESS ASSESSMENT")
        report.append("-" * 40)
        readiness = results["production_readiness"]
        report.append(f"System Stability: {'✅' if readiness['system_stability'] else '❌'}")
        report.append(f"Quality Threshold: {'✅' if readiness['quality_threshold'] else '❌'}")
        report.append(f"Performance Threshold: {'✅' if readiness['performance_threshold'] else '❌'}")
        report.append(f"Business Value Validated: {'✅' if readiness['business_value_validated'] else '❌'}")
        report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)


async def main():
    """Main entry point for production testing"""
    
    print("🚀 SUBFRACTURE Production Testing Suite")
    print("=" * 60)
    
    # Create tester
    tester = ProductionTester()
    
    try:
        # Run comprehensive test suite
        results = await tester.run_comprehensive_test_suite()
        
        # Save results
        results_file = tester.save_test_results(results)
        
        # Generate and display report
        report = tester.generate_test_report(results)
        print(report)
        
        # Save report
        report_file = results_file.replace('.json', '_report.txt')
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\n📊 Detailed results saved to: {results_file}")
        print(f"📋 Test report saved to: {report_file}")
        
        # Final recommendation
        if results["overall_production_readiness"] > 0.8:
            print("\n🎉 SYSTEM IS PRODUCTION READY!")
            print("The SUBFRACTURE system has passed all production tests.")
        else:
            print("\n⚠️  SYSTEM NEEDS OPTIMIZATION")
            print("Review test results for improvement recommendations.")
        
    except Exception as e:
        logger.error("Production testing failed", error=str(e))
        print(f"\n❌ Production testing failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())