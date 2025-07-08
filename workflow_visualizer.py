#!/usr/bin/env python3
"""
SUBFRACTURE Workflow Visualizer

Visual progress tracking and workflow monitoring for SUBFRACTURE LangGraph system.
Provides real-time visualization of brand development process, gravity optimization,
and breakthrough discovery moments.

Features:
- Real-time workflow progress visualization
- Gravity system monitoring with physics metaphors
- Breakthrough moment highlighting
- Validation checkpoint tracking
- Performance metrics dashboard
- Export capabilities for presentations

Usage:
    python workflow_visualizer.py --live                # Live monitoring mode
    python workflow_visualizer.py --session "session_id" # Visualize specific session
    python workflow_visualizer.py --export              # Generate visualization exports
"""

import argparse
import asyncio
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.state import SubfractureGravityState, GravityType
from src.core.config import get_config


class WorkflowVisualizer:
    """
    Visual progress tracking for SUBFRACTURE workflow execution
    """
    
    def __init__(self):
        self.config = get_config()
        self.current_session: Optional[Dict[str, Any]] = None
        self.visualization_data = {}
        self.progress_history = []
        
    def initialize_visualization(self, session_data: Dict[str, Any]):
        """Initialize visualization with session data"""
        
        self.current_session = session_data
        self.visualization_data = {
            "session_id": session_data.get("session_id", "unknown"),
            "start_time": datetime.now().isoformat(),
            "phases": self._get_workflow_phases(),
            "gravity_tracking": self._initialize_gravity_tracking(),
            "validation_tracking": self._initialize_validation_tracking(),
            "breakthrough_tracking": self._initialize_breakthrough_tracking(),
            "progress_metrics": self._initialize_progress_metrics()
        }
        
        print(f"🎨 Workflow visualization initialized")
        print(f"📋 Session: {self.visualization_data['session_id']}")
        return self.visualization_data
    
    def _get_workflow_phases(self) -> List[Dict[str, Any]]:
        """Get workflow phases for visualization"""
        
        return [
            {
                "id": "strategy_discovery",
                "name": "Strategic Truth Mining",
                "icon": "📈",
                "description": "Extracting strategic truths and competitive insights",
                "estimated_duration": 180,  # seconds
                "status": "pending",
                "progress": 0,
                "outputs": ["core_truths", "strategic_frameworks", "competitive_analysis"]
            },
            {
                "id": "creative_exploration", 
                "name": "Creative Insight Hunting",
                "icon": "🎨",
                "description": "Discovering target insights and emotional territories",
                "estimated_duration": 180,
                "status": "pending",
                "progress": 0,
                "outputs": ["target_insights", "creative_territories", "human_breakthroughs"]
            },
            {
                "id": "design_synthesis",
                "name": "Design System Weaving",
                "icon": "🎭",
                "description": "Creating visual languages and gravity points",
                "estimated_duration": 150,
                "status": "pending", 
                "progress": 0,
                "outputs": ["visual_languages", "verbal_frameworks", "gravity_points"]
            },
            {
                "id": "technology_planning",
                "name": "Technology Experience Building",
                "icon": "⚙️",
                "description": "Designing user experiences with funnel physics",
                "estimated_duration": 150,
                "status": "pending",
                "progress": 0,
                "outputs": ["user_journeys", "friction_analysis", "velocity_optimization"]
            },
            {
                "id": "gravity_analysis",
                "name": "Gravity Analysis",
                "icon": "🌌",
                "description": "Calculating brand magnetism and optimization opportunities",
                "estimated_duration": 120,
                "status": "pending",
                "progress": 0,
                "outputs": ["gravity_index", "optimization_roadmap", "physics_analysis"]
            },
            {
                "id": "validation_checkpoints",
                "name": "Human Validation",
                "icon": "💝",
                "description": "Heart Knows validation and authenticity assessment",
                "estimated_duration": 90,
                "status": "pending",
                "progress": 0,
                "outputs": ["heart_knows_validation", "emotional_resonance", "authenticity_score"]
            },
            {
                "id": "breakthrough_discovery",
                "name": "Vesica Pisces Breakthrough",
                "icon": "✨",
                "description": "Truth + Insight intersection discovery",
                "estimated_duration": 120,
                "status": "pending",
                "progress": 0,
                "outputs": ["truth_insight_intersections", "primary_breakthrough", "applications"]
            },
            {
                "id": "brand_world_creation",
                "name": "Brand World Generation",
                "icon": "🌍",
                "description": "Comprehensive brand universe creation",
                "estimated_duration": 180,
                "status": "pending",
                "progress": 0,
                "outputs": ["strategic_foundation", "identity_system", "implementation_roadmap"]
            },
            {
                "id": "premium_value_validation",
                "name": "Premium Value Validation",
                "icon": "💎",
                "description": "$50k+ investment justification and ROI analysis",
                "estimated_duration": 90,
                "status": "pending",
                "progress": 0,
                "outputs": ["boutique_quality_assessment", "roi_projections", "competitive_advantage"]
            }
        ]
    
    def _initialize_gravity_tracking(self) -> Dict[str, Any]:
        """Initialize gravity system tracking"""
        
        return {
            "gravity_types": {
                GravityType.RECOGNITION: {
                    "name": "Recognition Gravity",
                    "icon": "👁️",
                    "description": "Visual distinctiveness and memorability",
                    "current_strength": 0.0,
                    "target_strength": 0.8,
                    "optimization_history": []
                },
                GravityType.COMPREHENSION: {
                    "name": "Comprehension Gravity", 
                    "icon": "🧠",
                    "description": "Verbal clarity and message stickiness",
                    "current_strength": 0.0,
                    "target_strength": 0.8,
                    "optimization_history": []
                },
                GravityType.ATTRACTION: {
                    "name": "Attraction Gravity",
                    "icon": "🧲",
                    "description": "Cultural relevance and natural pull",
                    "current_strength": 0.0,
                    "target_strength": 0.8,
                    "optimization_history": []
                },
                GravityType.AMPLIFICATION: {
                    "name": "Amplification Gravity",
                    "icon": "📢",
                    "description": "Partnership synergy and reach extension",
                    "current_strength": 0.0,
                    "target_strength": 0.8,
                    "optimization_history": []
                },
                GravityType.TRUST: {
                    "name": "Trust Gravity",
                    "icon": "🤝",
                    "description": "Experiential consistency and relationship building",
                    "current_strength": 0.0,
                    "target_strength": 0.8,
                    "optimization_history": []
                }
            },
            "total_gravity_index": 0.0,
            "gravity_optimization_opportunities": [],
            "physics_insights": []
        }
    
    def _initialize_validation_tracking(self) -> Dict[str, Any]:
        """Initialize validation checkpoint tracking"""
        
        return {
            "checkpoints": [
                {
                    "id": "heart_knows_strategy",
                    "name": "Heart Knows: Strategy + Creative",
                    "icon": "💝",
                    "description": "Gut check on strategy-creative synthesis",
                    "status": "pending",
                    "confidence": 0.0,
                    "timestamp": None
                },
                {
                    "id": "emotional_resonance",
                    "name": "Emotional Resonance",
                    "icon": "💫",
                    "description": "Authentic emotional connection validation",
                    "status": "pending",
                    "confidence": 0.0,
                    "timestamp": None
                },
                {
                    "id": "anti_ai_slop",
                    "name": "Anti-AI Slop Protection",
                    "icon": "🛡️",
                    "description": "Human authenticity vs. AI manipulation check",
                    "status": "pending",
                    "confidence": 0.0,
                    "timestamp": None
                },
                {
                    "id": "premium_value_confidence",
                    "name": "Premium Value Confidence",
                    "icon": "💎",
                    "description": "$50k+ investment justification validation",
                    "status": "pending",
                    "confidence": 0.0,
                    "timestamp": None
                }
            ],
            "overall_validation_score": 0.0,
            "validation_decision": "pending"
        }
    
    def _initialize_breakthrough_tracking(self) -> Dict[str, Any]:
        """Initialize breakthrough discovery tracking"""
        
        return {
            "truth_insight_intersections": [],
            "breakthrough_moments": [],
            "primary_breakthrough": None,
            "breakthrough_strength": 0.0,
            "vesica_pisces_discoveries": [],
            "application_opportunities": []
        }
    
    def _initialize_progress_metrics(self) -> Dict[str, Any]:
        """Initialize progress metrics tracking"""
        
        return {
            "overall_progress": 0.0,
            "estimated_completion_time": None,
            "elapsed_time": 0,
            "phases_completed": 0,
            "validation_checkpoints_passed": 0,
            "breakthrough_moments_discovered": 0,
            "current_phase": None,
            "performance_metrics": {
                "insights_per_minute": 0,
                "gravity_optimization_rate": 0,
                "validation_success_rate": 0
            }
        }
    
    def update_phase_progress(self, phase_id: str, progress: float, status: str = None, outputs: Dict[str, Any] = None):
        """Update progress for specific phase"""
        
        phases = self.visualization_data["phases"]
        phase = next((p for p in phases if p["id"] == phase_id), None)
        
        if phase:
            phase["progress"] = min(100, max(0, progress))
            if status:
                phase["status"] = status
            
            if outputs:
                phase["actual_outputs"] = outputs
            
            # Update overall progress
            total_progress = sum(p["progress"] for p in phases) / len(phases)
            self.visualization_data["progress_metrics"]["overall_progress"] = total_progress
            
            # Update current phase
            if status == "in_progress":
                self.visualization_data["progress_metrics"]["current_phase"] = phase_id
            elif status == "completed":
                self.visualization_data["progress_metrics"]["phases_completed"] += 1
            
            print(f"📊 {phase['icon']} {phase['name']}: {progress:.1f}% {status or ''}")
    
    def update_gravity_tracking(self, gravity_data: Dict[str, Any]):
        """Update gravity system tracking"""
        
        gravity_tracking = self.visualization_data["gravity_tracking"]
        
        if "gravity_analysis" in gravity_data:
            analysis = gravity_data["gravity_analysis"]
            
            # Update individual gravity strengths
            for gravity_type, strength in analysis.items():
                if gravity_type in gravity_tracking["gravity_types"]:
                    gravity_tracking["gravity_types"][gravity_type]["current_strength"] = strength
                    gravity_tracking["gravity_types"][gravity_type]["optimization_history"].append({
                        "timestamp": datetime.now().isoformat(),
                        "strength": strength
                    })
        
        if "gravity_index" in gravity_data:
            gravity_tracking["total_gravity_index"] = gravity_data["gravity_index"]
        
        if "physics_optimization" in gravity_data:
            gravity_tracking["physics_insights"].append({
                "timestamp": datetime.now().isoformat(),
                "insights": gravity_data["physics_optimization"]
            })
        
        print(f"🌌 Gravity Index Updated: {gravity_tracking['total_gravity_index']:.2f}")
    
    def update_validation_tracking(self, validation_data: Dict[str, Any]):
        """Update validation checkpoint tracking"""
        
        validation_tracking = self.visualization_data["validation_tracking"]
        
        for checkpoint_id, checkpoint_result in validation_data.items():
            checkpoint = next((c for c in validation_tracking["checkpoints"] if c["id"] == checkpoint_id), None)
            
            if checkpoint and isinstance(checkpoint_result, dict):
                checkpoint["status"] = "completed" if checkpoint_result.get("validated") else "failed"
                checkpoint["confidence"] = checkpoint_result.get("confidence", 0.0)
                checkpoint["timestamp"] = datetime.now().isoformat()
        
        # Update overall validation score
        completed_checkpoints = [c for c in validation_tracking["checkpoints"] if c["status"] == "completed"]
        if completed_checkpoints:
            validation_tracking["overall_validation_score"] = sum(c["confidence"] for c in completed_checkpoints) / len(completed_checkpoints)
            validation_tracking["validation_decision"] = "proceed" if validation_tracking["overall_validation_score"] >= 0.7 else "refine"
        
        self.visualization_data["progress_metrics"]["validation_checkpoints_passed"] = len(completed_checkpoints)
        
        print(f"💝 Validation Score: {validation_tracking['overall_validation_score']:.2f}")
    
    def update_breakthrough_tracking(self, breakthrough_data: Dict[str, Any]):
        """Update breakthrough discovery tracking"""
        
        breakthrough_tracking = self.visualization_data["breakthrough_tracking"]
        
        if "truth_insight_intersections" in breakthrough_data:
            breakthrough_tracking["truth_insight_intersections"] = breakthrough_data["truth_insight_intersections"]
        
        if "primary_breakthrough" in breakthrough_data:
            breakthrough_tracking["primary_breakthrough"] = breakthrough_data["primary_breakthrough"]
            breakthrough_tracking["breakthrough_strength"] = breakthrough_data["primary_breakthrough"].get("breakthrough_strength", 0.0)
        
        if "vesica_pisces_moments" in breakthrough_data:
            breakthrough_tracking["vesica_pisces_discoveries"] = breakthrough_data["vesica_pisces_moments"]
            breakthrough_tracking["breakthrough_moments"].append({
                "timestamp": datetime.now().isoformat(),
                "moment": breakthrough_data["vesica_pisces_moments"]
            })
        
        self.visualization_data["progress_metrics"]["breakthrough_moments_discovered"] = len(breakthrough_tracking["breakthrough_moments"])
        
        print(f"✨ Breakthrough Strength: {breakthrough_tracking['breakthrough_strength']:.2f}")
    
    def display_live_dashboard(self):
        """Display live ASCII dashboard"""
        
        self._clear_screen()
        print("🔮 SUBFRACTURE Live Workflow Dashboard")
        print("=" * 60)
        
        # Overall progress
        progress = self.visualization_data["progress_metrics"]["overall_progress"]
        progress_bar = self._create_progress_bar(progress, 30)
        print(f"\n📊 Overall Progress: {progress:.1f}% {progress_bar}")
        
        # Current phase
        current_phase = self.visualization_data["progress_metrics"]["current_phase"]
        if current_phase:
            phase = next((p for p in self.visualization_data["phases"] if p["id"] == current_phase), None)
            if phase:
                print(f"🎯 Current Phase: {phase['icon']} {phase['name']}")
        
        # Phase progress
        print(f"\n📋 Phase Progress:")
        for phase in self.visualization_data["phases"]:
            status_icon = self._get_status_icon(phase["status"])
            phase_bar = self._create_progress_bar(phase["progress"], 20)
            print(f"   {status_icon} {phase['icon']} {phase['name']:<25} {phase['progress']:>5.1f}% {phase_bar}")
        
        # Gravity tracking
        print(f"\n🌌 Gravity System:")
        gravity_tracking = self.visualization_data["gravity_tracking"]
        print(f"   🧲 Total Gravity Index: {gravity_tracking['total_gravity_index']:.2f}/1.0")
        
        for gravity_type, data in gravity_tracking["gravity_types"].items():
            strength = data["current_strength"]
            gravity_bar = self._create_progress_bar(strength * 100, 15)
            print(f"   {data['icon']} {data['name']:<20} {strength:.2f} {gravity_bar}")
        
        # Validation tracking
        print(f"\n💝 Validation Checkpoints:")
        validation_tracking = self.visualization_data["validation_tracking"]
        print(f"   🎯 Overall Score: {validation_tracking['overall_validation_score']:.2f}")
        
        for checkpoint in validation_tracking["checkpoints"]:
            status_icon = self._get_status_icon(checkpoint["status"])
            confidence = checkpoint["confidence"]
            print(f"   {status_icon} {checkpoint['icon']} {checkpoint['name']:<30} {confidence:.2f}")
        
        # Breakthrough tracking
        print(f"\n✨ Breakthrough Discovery:")
        breakthrough_tracking = self.visualization_data["breakthrough_tracking"]
        breakthrough_strength = breakthrough_tracking["breakthrough_strength"]
        breakthrough_count = len(breakthrough_tracking["breakthrough_moments"])
        
        print(f"   🔮 Breakthrough Strength: {breakthrough_strength:.2f}")
        print(f"   ⚡ Moments Discovered: {breakthrough_count}")
        
        if breakthrough_tracking["primary_breakthrough"]:
            concept = breakthrough_tracking["primary_breakthrough"].get("primary_breakthrough_concept", "Unknown")
            print(f"   💡 Primary Breakthrough: {concept[:50]}...")
        
        # Performance metrics
        print(f"\n⚡ Performance Metrics:")
        metrics = self.visualization_data["progress_metrics"]["performance_metrics"]
        elapsed = self.visualization_data["progress_metrics"]["elapsed_time"]
        
        print(f"   ⏰ Elapsed Time: {elapsed:.0f}s")
        print(f"   📊 Insights/Min: {metrics['insights_per_minute']:.1f}")
        print(f"   🌌 Gravity Optimization Rate: {metrics['gravity_optimization_rate']:.2f}")
        print(f"   💝 Validation Success Rate: {metrics['validation_success_rate']:.1%}")
        
        print(f"\n🔄 Dashboard updates every 2 seconds...")
    
    def _create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create ASCII progress bar"""
        
        filled = int(percentage / 100 * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"
    
    def _get_status_icon(self, status: str) -> str:
        """Get status icon for display"""
        
        status_icons = {
            "pending": "⏳",
            "in_progress": "🔄", 
            "completed": "✅",
            "failed": "❌",
            "skipped": "⏭️"
        }
        return status_icons.get(status, "❓")
    
    def _clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    async def monitor_live_session(self, session_id: str):
        """Monitor live workflow session"""
        
        print(f"🔴 Starting live monitoring for session: {session_id}")
        
        # Initialize with dummy data for demo
        self.initialize_visualization({"session_id": session_id})
        
        # Simulate workflow progress
        phases = self.visualization_data["phases"]
        start_time = time.time()
        
        try:
            for i, phase in enumerate(phases):
                # Update current phase
                self.update_phase_progress(phase["id"], 0, "in_progress")
                
                # Simulate phase execution with progress updates
                for progress in range(0, 101, 20):
                    self.update_phase_progress(phase["id"], progress)
                    
                    # Update elapsed time
                    self.visualization_data["progress_metrics"]["elapsed_time"] = time.time() - start_time
                    
                    # Simulate gravity updates
                    if phase["id"] == "gravity_analysis":
                        gravity_data = {
                            "gravity_analysis": {
                                GravityType.RECOGNITION: 0.6 + (progress / 100) * 0.2,
                                GravityType.COMPREHENSION: 0.7 + (progress / 100) * 0.1,
                                GravityType.ATTRACTION: 0.65 + (progress / 100) * 0.15,
                                GravityType.AMPLIFICATION: 0.5 + (progress / 100) * 0.3,
                                GravityType.TRUST: 0.8 + (progress / 100) * 0.1
                            },
                            "gravity_index": 0.66 + (progress / 100) * 0.14
                        }
                        self.update_gravity_tracking(gravity_data)
                    
                    # Simulate validation updates
                    if phase["id"] == "validation_checkpoints":
                        validation_data = {
                            "heart_knows_strategy": {"validated": True, "confidence": 0.85},
                            "emotional_resonance": {"validated": True, "confidence": 0.82}
                        }
                        self.update_validation_tracking(validation_data)
                    
                    # Simulate breakthrough updates
                    if phase["id"] == "breakthrough_discovery":
                        breakthrough_data = {
                            "primary_breakthrough": {
                                "primary_breakthrough_concept": "Brand Physics Laboratory",
                                "breakthrough_strength": 0.75 + (progress / 100) * 0.15
                            },
                            "vesica_pisces_moments": [{"discovery": "Truth + Insight intersection"}]
                        }
                        self.update_breakthrough_tracking(breakthrough_data)
                    
                    # Display dashboard
                    self.display_live_dashboard()
                    await asyncio.sleep(2)  # Update every 2 seconds
                
                # Mark phase complete
                self.update_phase_progress(phase["id"], 100, "completed")
        
        except KeyboardInterrupt:
            print(f"\n⏸️  Live monitoring stopped")
        
        print(f"\n🎉 Workflow monitoring completed!")
    
    def generate_visualization_export(self, output_dir: str = "visualizations"):
        """Generate visualization exports"""
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate JSON data export
        json_file = output_path / f"workflow_data_{self.visualization_data['session_id']}.json"
        with open(json_file, 'w') as f:
            json.dump(self.visualization_data, f, indent=2, default=str)
        
        # Generate markdown summary
        md_file = output_path / f"workflow_summary_{self.visualization_data['session_id']}.md"
        with open(md_file, 'w') as f:
            f.write(self._generate_markdown_summary())
        
        # Generate CSV data for external analysis
        csv_file = output_path / f"workflow_metrics_{self.visualization_data['session_id']}.csv"
        with open(csv_file, 'w') as f:
            f.write(self._generate_csv_metrics())
        
        print(f"📁 Visualization exports generated in: {output_path}")
        print(f"   📄 JSON Data: {json_file}")
        print(f"   📝 Summary: {md_file}")
        print(f"   📊 Metrics: {csv_file}")
        
        return output_path
    
    def _generate_markdown_summary(self) -> str:
        """Generate markdown summary of workflow"""
        
        session_id = self.visualization_data["session_id"]
        start_time = self.visualization_data["start_time"]
        progress = self.visualization_data["progress_metrics"]["overall_progress"]
        
        summary = f"""# SUBFRACTURE Workflow Visualization Summary

## Session Details
- **Session ID**: {session_id}
- **Start Time**: {start_time}
- **Overall Progress**: {progress:.1f}%

## Phase Progress
"""
        
        for phase in self.visualization_data["phases"]:
            summary += f"- {phase['icon']} **{phase['name']}**: {phase['progress']:.1f}% ({phase['status']})\n"
        
        summary += f"""
## Gravity System Analysis
- **Total Gravity Index**: {self.visualization_data['gravity_tracking']['total_gravity_index']:.2f}/1.0

"""
        
        for gravity_type, data in self.visualization_data["gravity_tracking"]["gravity_types"].items():
            summary += f"- {data['icon']} **{data['name']}**: {data['current_strength']:.2f}\n"
        
        summary += f"""
## Validation Results
- **Overall Validation Score**: {self.visualization_data['validation_tracking']['overall_validation_score']:.2f}
- **Checkpoints Passed**: {self.visualization_data['progress_metrics']['validation_checkpoints_passed']}

## Breakthrough Discovery
- **Breakthrough Strength**: {self.visualization_data['breakthrough_tracking']['breakthrough_strength']:.2f}
- **Moments Discovered**: {len(self.visualization_data['breakthrough_tracking']['breakthrough_moments'])}

---
Generated by SUBFRACTURE Workflow Visualizer
"""
        
        return summary
    
    def _generate_csv_metrics(self) -> str:
        """Generate CSV metrics data"""
        
        csv_lines = ["Category,Metric,Value"]
        
        # Progress metrics
        metrics = self.visualization_data["progress_metrics"]
        csv_lines.append(f"Progress,Overall Progress,{metrics['overall_progress']}")
        csv_lines.append(f"Progress,Phases Completed,{metrics['phases_completed']}")
        csv_lines.append(f"Progress,Validation Checkpoints Passed,{metrics['validation_checkpoints_passed']}")
        csv_lines.append(f"Progress,Breakthrough Moments,{metrics['breakthrough_moments_discovered']}")
        
        # Gravity metrics
        gravity_tracking = self.visualization_data["gravity_tracking"]
        csv_lines.append(f"Gravity,Total Index,{gravity_tracking['total_gravity_index']}")
        
        for gravity_type, data in gravity_tracking["gravity_types"].items():
            csv_lines.append(f"Gravity,{data['name']},{data['current_strength']}")
        
        # Validation metrics
        validation_tracking = self.visualization_data["validation_tracking"]
        csv_lines.append(f"Validation,Overall Score,{validation_tracking['overall_validation_score']}")
        
        for checkpoint in validation_tracking["checkpoints"]:
            csv_lines.append(f"Validation,{checkpoint['name']},{checkpoint['confidence']}")
        
        return "\n".join(csv_lines)


async def main():
    """Main visualizer execution"""
    
    parser = argparse.ArgumentParser(description="SUBFRACTURE Workflow Visualizer")
    parser.add_argument("--live", action="store_true", help="Live monitoring mode")
    parser.add_argument("--session", help="Monitor specific session ID")
    parser.add_argument("--export", action="store_true", help="Generate visualization exports")
    parser.add_argument("--demo", action="store_true", help="Run demo visualization")
    
    args = parser.parse_args()
    
    visualizer = WorkflowVisualizer()
    
    print("🎨 SUBFRACTURE Workflow Visualizer")
    print("Real-time Brand Intelligence Progress Tracking")
    print("=" * 50)
    
    try:
        if args.live or args.demo:
            session_id = args.session or f"demo_{int(time.time())}"
            await visualizer.monitor_live_session(session_id)
            
            if args.export:
                visualizer.generate_visualization_export()
        
        elif args.session:
            # Load existing session data
            print(f"📂 Loading session: {args.session}")
            # This would load real session data in production
            visualizer.initialize_visualization({"session_id": args.session})
            visualizer.display_live_dashboard()
            
            if args.export:
                visualizer.generate_visualization_export()
        
        elif args.export:
            # Generate exports from current visualization data
            if not visualizer.visualization_data:
                print("❌ No visualization data available. Run with --live or --session first.")
                return 1
            
            visualizer.generate_visualization_export()
        
        else:
            print("❓ No visualization mode specified. Use --help for options.")
            print("💡 Try: python workflow_visualizer.py --demo")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏸️  Visualization interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Visualization failed: {e}")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ Visualizer startup failed: {e}")
        sys.exit(1)