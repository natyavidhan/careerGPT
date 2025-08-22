from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables (for API key)
load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("home.html")

# New route for the roadmap page
@app.route("/roadmap/<career>")
def roadmap(career):
    return render_template("roadmap.html", career=career)

@app.route("/api/suggest_careers", methods=["POST"])
def suggest_careers():
    user_input = request.json.get("user_input", "")
    
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    
    CONF = {
        "temperature": 1,
        "max_completion_tokens": 8192,
        "top_p": 1,
        "reasoning_effort": "medium",
        "stream": False,
        "stop": None,
    }
    
    # Prepare the prompt for Groq
    system_message = "You are a career advisor AI that provides career suggestions based on user input."
    
    user_prompt = f"""
    Based on the following user description, suggest 3 suitable careers.
    For each career, provide a confidence score (1-5) and a brief reason why it's suitable.
    Return the results in the following JSON format:
    {{
      "user_input": "User's input text",
      "career_suggestions": [
        {{
          "career": "Career Title",
          "confidence": confidence_score,
          "reason": "Reason text"
        }},
        ...
      ]
    }}
    
    User description: {user_input}
    """
    
    # Call Groq API
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            **CONF
        )
        
        # Extract the JSON response from the AI
        ai_response = response.choices[0].message.content
        ai_response = ai_response.replace("```json", "").replace("```", "")
        try:
            result = json.loads(ai_response)
            return jsonify(result)
        except json.JSONDecodeError:
            # Fallback if the AI doesn't return valid JSON
            return jsonify({"error": "Failed to parse AI response"}), 500
        
    except Exception as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500

# New API endpoint for generating roadmaps
@app.route("/api/generate_roadmap", methods=["POST"])
def generate_roadmap():
    career = request.json.get("career", "")
    
    if not career:
        return jsonify({"error": "No career provided"}), 400
    
    CONF = {
        "temperature": 1,
        "max_completion_tokens": 8192,
        "top_p": 1,
        "reasoning_effort": "medium",
        "stream": False,
        "stop": None,
    }
    
    # Prepare the prompt for Groq
    system_message = "You are a career development expert that creates detailed career roadmaps."
    
    user_prompt = f"""
        You are an expert career mentor AI.  
        Your task is to generate a detailed, structured career roadmap for someone aspiring to become a {career}.  

        The roadmap must:  
        - Contain at least 4–5 progressive phases (e.g., Beginner, Intermediate, Advanced, Professional, Expert).  
        - Each phase must include:  
        1. **Specific skills** to learn (technical + soft skills).  
        2. **Projects or hands-on experiences** to complete.  
        3. **Recommended certifications, courses, or education paths** (if relevant).  
        4. A **clear, actionable goal description** that guides the user.  
        - Ensure logical progression from absolute beginner to advanced/professional readiness.  
        - Keep all outputs highly practical and directly usable and concise.  

        ⚠️ Important:  
        - Return ONLY valid JSON, nothing else.  
        - Avoid extra commentary outside the JSON structure.  

        Format to return:  
        
        {{
        "career": "{career}",
        "roadmap": [
            {{
            "phase": "Phase name (e.g., Short-term, Beginner, etc.)",
            "duration": "Estimated time frame",
            "goal": "Detailed description of learning objectives or milestones"
            }},
            ...
        ]
        }}

    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            **CONF
        )
        
        # Extract the JSON response from the AI
        ai_response = response.choices[0].message.content
        print(ai_response)
        ai_response = ai_response.replace("```json", "").replace("```", "")
        
        try:
            result = json.loads(ai_response)
            return jsonify(result)
        except json.JSONDecodeError:
            # Fallback if the AI doesn't return valid JSON
            return jsonify({"error": "Failed to parse AI response"}), 500
        
    except Exception as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)