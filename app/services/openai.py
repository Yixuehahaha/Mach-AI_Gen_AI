import os
from fastapi import HTTPException
from openai import AsyncOpenAI
from collections import defaultdict, deque
from dotenv import load_dotenv
import json


#openai api key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
client = AsyncOpenAI(
    api_key=api_key
)

#system prompt library
SYSTEM_PROMPT_LIBRARY = {
    "recommend":"""
        You are an expert project management assistant. Your task is to generate a detailed project plan based on the user's description of their project.\n\n"
        1. **Your Core Task**:
            - Generate a detailed project plan based on the user's initial input.
            - If the user provides feedback, modify the existing project plan to address their new requirements.
            - Ensure the recommendations remain clear, concise, and actionable.
        2. **Understand the User Prompt**:
           - Analyze the user's description of the project.
           - Identify the type of project (e.g., job, home improvement, school, commercial).
           - Break down the description into key objectives and requirements.
        3. **Generate Recommendations**:
           Based on the project type and description, provide recommendations that include:
           - A list of sub-projects and their corresponding tasks.
           - Suggested start- and end-dates for each task (based on typical project timelines, please provide specific dates).
           - Task interdependencies to ensure logical sequencing.
           - Recommended talent or roles for each task.
        4. **How to Handle Modification**:
           - Always reference the last recommendation.
           - Retain the parts of the recommendation that are not affected by the feedback.
           - For example, if the user says "The timeline is too long," shorten the timeline while keeping the project phases intact.

        !!! Important!!! This is the format:
        ### **Project Plan Summary**
            - **Project Name**: [If provided, include it; otherwise infer based on context]
            - **Project Type**: [Type of project, e.g., Job Planning, Home Improvement, School, Commercial]
            - **Description**:  [Provide an overview of what this project is about]
        **Main Goals**:  
            - [Goal 1]  
            - [Goal 2]  
        **Estimated Timeline**: [Start Date] to [End Date]  
    
    
        #### Phase 1: [Phase Name]
            - **Description**:  [Provide an overview of what this phase is about and why it is important.]  
            - **Start Date**: [Start Date]  
            - **End Date**: [End Date]  
            
            [this part should not be shown to the user
            [Key Tasks]
            [LLM should determine the appropriate number of tasks based on project complexity]  
            [Each task should be concise and specific, with clear descriptions]]
                
            ##### Task 1: [Task Name]
                - **Start Date**: [Start Date]  
                - **End Date**: [End Date]  
                - **Description**: [Brief summary of the task]  
                - **Responsible Team**: [Roles involved, e.g., Developers, Designers]
                
            ##### Task 2: [Task Name]
                - **Start Date**: [Start Date]  
                - **End Date**: [End Date]  
                - **Description**: [Brief summary of the task]  
                - **Responsible Team**: [Roles involved] 
                 
            [this part should not be shown to the user
            [Continue adding tasks as necessary]]
        
            
        #### Phase 2: [Phase Name]
            - **Description**:  [Overview of this phase]  
            - **Start Date**: [Start Date]  
            - **End Date**: [End Date]  
            
            ##### Task 1: [Task Name]
                - **Start Date**: [Start Date]  
                - **End Date**: [End Date]  
                - **Description**: [Brief summary]  
                - **Responsible Team**: [Roles involved]  
            
            [this part should not be shown to the user
            [Continue for more tasks if needed]  
            
            [Repeat for additional phases as necessary. The number of phases should be determined based on project complexity.]]
            
        ### **Interdependencies Summary**
            - Highlight how tasks and phases depend on each other. Use a simple sequence, e.g.,Feasibility Study → Land Acquisition → Architectural Design → Permitting → Construction.
              
        ### **Key Insights and Recommendations**
            - Provide additional insights or potential risks to consider for the project. For example:
                - [Insight 1: Allocate buffer time for permit approvals.]
                - [Insight 2: Early stakeholder alignment is critical for success.]
"""
}

project_schema = {
  "name": "parse_project_plan",
  "description": "Extract a structured project plan from recommendation text. The project plan includes a high-level project overview, its key phases, and associated tasks for each phase.",
  "parameters": {
    "type": "object",
    "properties": {
      "project": {
        "type": "object",
        "description": "The root project structure, including project-level details and phases.",
        "properties": {
          "name": {
            "type": "string",
            "description": "The title or name of the overall project (e.g., 'AI Product Expansion Plan')"
          },
          "description": {
            "type": "string",
            "description": "A concise summary describing the purpose and goal of this project."
          },
          "start_date": {
            "type": "string",
            "description": "Project start date in MM/DD/YYYY format."
          },
          "end_date": {
            "type": "string",
            "description": "Project end date in MM/DD/YYYY format."
          },
          "phases": {
            "type": "array",
            "description": "A list of phases representing major parts or milestones of the project.",
            "items": {
              "type": "object",
              "description": "Each phase includes its own name, description, timeline, and tasks.",
              "properties": {
                "name": {
                  "type": "string",
                  "description": "Title of the phase (e.g., 'Phase 1: Market Research')."
                },
                "description": {
                  "type": "string",
                  "description": "Brief overview of the purpose of this phase."
                },
                "start_date": {
                  "type": "string",
                  "description": "Phase start date in MM/DD/YYYY format."
                },
                "end_date": {
                  "type": "string",
                  "description": "Phase end date in MM/DD/YYYY format."
                },
                "tasks": {
                  "type": "array",
                  "description": "A list of specific tasks under this phase.",
                  "items": {
                    "type": "object",
                    "description": "Each task includes a name, timeline, description, and responsible team.",
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "Short name of the task (e.g., 'Create landing page layout')."
                      },
                      "description": {
                        "type": "string",
                        "description": "Brief summary of what the task entails or why it's needed."
                      },
                      "start_date": {
                        "type": "string",
                        "description": "Task start date in MM/DD/YYYY format."
                      },
                      "end_date": {
                        "type": "string",
                        "description": "Task end date in MM/DD/YYYY format."
                      },
                      "team": {
                        "type": "string",
                        "description": "Team or role responsible for this task (e.g., 'Designers', 'LLM Engineers')."
                      }
                    },
                    "required": ["name", "start_date", "end_date"]
                  }
                }
              },
              "required": ["name", "start_date", "end_date"]
            }
          }
        },
        "required": ["name", "start_date", "end_date"]
      }
    },
    "required": ["project"]
  }
}


class ChatHistoryManager:
    def __init__(self, max_cache: int = 10):
        self.max_cache = max_cache
        self.chat_history = defaultdict(deque)

    def add_message(self, user_id: str, role: str, content: str):
        if len(self.chat_history[user_id]) >= self.max_cache:
            self.chat_history[user_id].popleft()
        self.chat_history[user_id].append({"role": role, "content": content})
    def get_context(self, user_id: str):
        return list(self.chat_history[user_id])
#define chat_history_manager
chat_history_manager = ChatHistoryManager(max_cache=10)


#api call
async def call_openai_api(user_id: str, user_input: str, system_prompt: str):
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    messages.extend(chat_history_manager.get_context(user_id))
    messages.append({"role": "user", "content": user_input})
    try:
        response = await client.chat.completions.create(
            messages = messages,
            model = "gpt-3.5-turbo",
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")


async def call_openai_with_function(content: str, schema: dict, function_name: str, system_prompt: str = "You are a structured data extraction assistant.") -> dict:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content}
    ]

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=[schema],
        function_call={"name": function_name}
    )
    return json.loads(response.choices[0].message.function_call.arguments)

