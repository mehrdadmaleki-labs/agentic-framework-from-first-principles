from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

agents = {}


class AgentRegistration(BaseModel):
    name: str
    url: str
    capabilities: list[str]


@app.post("/register")
async def register_agent(agent: AgentRegistration):

    # Step 1: Add agent information to the dictionary
    agents[agent.name]=agent.model_dump()  #model_dump() converts the Pydantic object into a dictionary.

    # Step 2: Return a registration confirmation
    return {
        "status":"success",
        "message":f"Agent {agent.name} registered successfully"
    }


@app.get("/agents")
async def list_agents():

    # Step 3: Return all registered agents
    return agents


@app.get("/discover/{capability}")
async def discover_agent(capability: str):

    
    # Step 4: Search agents for the requested capability
    # Step 5: Return the matching agent's information
    for agent in agents.values():
        if capability in agent["capabilities"]:
            return agent
    # Step 6: If no agent is found, raise HTTPException(404)
    raise HTTPException(404, f"Agent not found to support {capability}")
        
    
    