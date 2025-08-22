import requests
import json
import os

def fetch_jobs(career="", skills=None):
    """Fetch jobs from Hiring.cafe API."""
    url = "https://hiring.cafe/api/search-jobs"
    
    # Use skills to enrich the search query if provided
    search_query = career
    if skills and isinstance(skills, list) and len(skills) > 0:
        search_query = f"{career} {' '.join(skills[:3])}"
    
    # Minimal search payload with dynamic query
    payload = {
        "size": 10,
        "page": 0,
        "searchState": {
            "locations": [{
                "formatted_address": "United States",
                "types": ["country"],
                "geometry": {"location": {"lat": "37.0902", "lon": "-95.7129"}},
                "id": "user_country",
                "address_components": [{"long_name": "United States", "short_name": "US", "types": ["country"]}],
                "options": {"flexible_regions": ["anywhere_in_continent", "anywhere_in_world"]}
            }],
            "workplaceTypes": ["Remote", "Hybrid", "Onsite"],
            "commitmentTypes": ["Full Time", "Part Time", "Contract", "Internship"],
            "seniorityLevel": ["No Prior Experience Required", "Entry Level", "Mid-Senior Level"],
            "sortBy": "default",
            "searchQuery": search_query
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        
        # Use backup data if API call fails
        backup_path = os.path.join(os.path.dirname(__file__), "static", "data", "response.json")
        if os.path.exists(backup_path):
            with open(backup_path, "r") as f:
                return json.load(f)
        return {"results": []}

def parse_jobs(raw_data, career=""):
    """Parse job data from API response."""
    jobs = []
    for job in raw_data.get("results", []):
        # Extract job title from the correct location in the response structure
        job_title = None
        if isinstance(job, dict):
            # First try to get title from job_information
            if "job_information" in job and isinstance(job["job_information"], dict):
                job_title = job["job_information"].get("title")
            
            # If not found in job_information, try other possible locations
            if not job_title:
                if "title" in job:
                    job_title = job.get("title")
                elif "v5_processed_job_data" in job:
                    job_title = job.get("v5_processed_job_data", {}).get("core_job_title")
        
        # Create a job object with basic information
        job_info = {
            "id": job.get("id", ""),
            "role": job_title or "Unknown Role",
            "company": job.get("company", {}).get("name", "Unknown Company") if isinstance(job.get("company"), dict) else job.get("v5_processed_company_data", {}).get("name", "Unknown Company"),
            "location": job.get("location", "Remote"),
            "type": job.get("commitmentType", job.get("v5_processed_job_data", {}).get("commitment", ["Full Time"])[0] if job.get("v5_processed_job_data", {}).get("commitment") else "Full Time"),
            "description": job.get("description", "") if isinstance(job.get("description"), str) else job.get("job_information", {}).get("description", ""),
            "link": job.get("externalApplyUrl") or job.get("apply_url") or f"https://hiring.cafe/job/{job.get('id')}"
        }
        
        # Extract additional information if available
        if "v5_processed_job_data" in job:
            job_data = job.get("v5_processed_job_data", {})
            
            # Extract requirements
            requirements = job_data.get("requirements_summary", "")
            job_info["requirements"] = requirements
            
            # Extract technical tools
            tools = job_data.get("technical_tools", [])
            job_info["tools"] = tools
            
            # Extract formatted location
            if job_data.get("formatted_workplace_location"):
                job_info["location"] = job_data.get("formatted_workplace_location")
        
        # Add company information if available
        if "v5_processed_company_data" in job:
            company_data = job.get("v5_processed_company_data", {})
            
            # Extract company activities
            job_info["company_activities"] = company_data.get("activities", [])
            
            # Extract company industry
            job_info["industry"] = company_data.get("industries", [])[0] if company_data.get("industries") else None
        
        jobs.append(job_info)
    
    return jobs

def match_jobs(career, user_skills, jobs):
    """Match jobs with user skills and career."""
    if not user_skills:
        user_skills = []
    
    # Add career as a skill to match against
    all_skills = user_skills + [career]
    
    matches = []
    for job in jobs:
        skill_overlap = 0
        role_match = False
        
        # Check if job role matches career
        if career.lower() in job["role"].lower():
            role_match = True
            skill_overlap += 2  # Higher weight for role match
        
        # Check for skill matches in title and description
        for skill in all_skills:
            skill_lower = skill.lower()
            if skill_lower in job["role"].lower() or skill_lower in job["description"].lower():
                skill_overlap += 1
        
        # Add jobs with any match, prioritizing role matches
        if skill_overlap > 0:
            # Calculate fit score (max 100%)
            max_possible = len(all_skills) + 2  # +2 for role match bonus
            fit_score = min(100, int((skill_overlap / max_possible) * 100))
            
            job["fit_score"] = fit_score
            job["role_match"] = role_match
            matches.append(job)
    
    # Sort by fit score descending, with role matches given priority
    sorted_matches = sorted(matches, key=lambda x: (x["role_match"], x["fit_score"]), reverse=True)
    return sorted_matches[:5]  # Return top 5 matches
