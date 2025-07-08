#!/usr/bin/env python3
"""
Direct API test for SUBFRACTURE analysis
Bypasses LangGraph Studio UI issues
"""

import asyncio
import json
import requests
import time

async def test_direct_api():
    """Test SUBFRACTURE via direct API call"""
    
    print("🚀 Testing SUBFRACTURE via Direct API")
    print("=" * 60)
    
    # Load the transcript test input
    try:
        with open("/mnt/c/Users/Admin/subfracture-langgraph/subfracture_transcript_input.json", "r") as f:
            test_input = json.load(f)
        print("📄 Loaded transcript test data")
        print(f"📝 Brief length: {len(test_input.get('brand_brief', ''))}")
    except Exception as e:
        print(f"❌ Could not load transcript file: {e}")
        return
    
    # Test the API endpoint
    api_url = "http://localhost:2024"
    
    # Test if server is reachable
    try:
        response = requests.get(f"{api_url}/docs", timeout=5)
        print(f"✅ Server is accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        print("💡 Try: https://smith.langchain.com/studio/?baseUrl=http://localhost:2024")
        return
    
    # Test thread creation and execution
    try:
        # Create a thread
        thread_response = requests.post(
            f"{api_url}/threads",
            json={"metadata": {"test": "subfracture_transcript"}}
        )
        thread_id = thread_response.json()["thread_id"]
        print(f"📝 Created thread: {thread_id}")
        
        # Submit the job
        run_response = requests.post(
            f"{api_url}/threads/{thread_id}/runs",
            json={
                "assistant_id": "subfracture",
                "input": test_input
            }
        )
        run_id = run_response.json()["run_id"]
        print(f"🚀 Started run: {run_id}")
        
        # Poll for completion
        for i in range(30):  # 30 second timeout
            status_response = requests.get(f"{api_url}/threads/{thread_id}/runs/{run_id}")
            status = status_response.json().get("status")
            print(f"📊 Status: {status}")
            
            if status == "success":
                result = status_response.json()
                print("✅ Analysis completed successfully!")
                
                # Extract key results
                output = result.get("output", {})
                if "analysis" in output:
                    analysis = output["analysis"]
                    print(f"🌟 Gravity Index: {analysis.get('gravity_index', 'N/A')}")
                    print(f"🎯 Brand Essence: {analysis.get('key_insights', {}).get('brand_essence', 'N/A')}")
                    print(f"🚀 Launch Confidence: {output.get('business_metrics', {}).get('launch_confidence', 'N/A')}")
                    print(f"💡 Recommendations: {len(analysis.get('recommendations', []))}")
                
                return result
            elif status == "error":
                print(f"❌ Analysis failed: {status_response.json()}")
                return None
            
            time.sleep(1)
        
        print("⏰ Analysis timed out")
        return None
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_direct_api())