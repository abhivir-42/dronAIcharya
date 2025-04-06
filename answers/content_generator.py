from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
import os
import json
import uuid
import subprocess
import asyncio
from pathlib import Path

# In a production environment, you would properly import manim
# This is a simplified example that demonstrates the approach
# import manim as mn

app = FastAPI(title="DronAIcharya Content Generation Service")

# Directory for storing generated content
CONTENT_DIR = "generated_content"
os.makedirs(CONTENT_DIR, exist_ok=True)

class ContentRequest(BaseModel):
    topic: str
    grade: str
    subject: str
    language: str = "English"
    content_type: str  # "video", "interactive", "quiz"
    difficulty_level: int = 3  # 1-5
    additional_context: Optional[Dict] = None
    offline_capable: bool = True
    

class ContentMetadata(BaseModel):
    id: str
    topic: str
    grade: str
    subject: str
    language: str
    content_type: str
    difficulty_level: int
    files: List[Dict[str, str]]  # List of files with type and path
    status: str = "pending"
    error: Optional[str] = None


# Simplified manim script generation
def generate_manim_script(request: ContentRequest) -> str:
    """Generate a Python script for manim animation based on the request"""
    
    if request.subject == "Mathematics" and "equation" in request.topic.lower():
        # Example: Generate a script for equation solving
        script = """
from manim import *

class SolveEquation(Scene):
    def construct(self):
        # Initial equation
        equation = MathTex("2x + 3 = 7")
        self.play(Write(equation))
        self.wait(1)
        
        # Step 1: Subtract 3 from both sides
        step1 = MathTex("2x + 3 - 3 = 7 - 3")
        self.play(TransformMatchingTex(equation, step1))
        self.wait(1)
        
        # Step 2: Simplify
        step2 = MathTex("2x = 4")
        self.play(TransformMatchingTex(step1, step2))
        self.wait(1)
        
        # Step 3: Divide by 2
        step3 = MathTex("\\\\frac{2x}{2} = \\\\frac{4}{2}")
        self.play(TransformMatchingTex(step2, step3))
        self.wait(1)
        
        # Final step
        final = MathTex("x = 2")
        self.play(TransformMatchingTex(step3, final))
        
        # Highlight the solution
        box = SurroundingRectangle(final, color=YELLOW)
        self.play(Create(box))
        self.wait(2)
"""
    elif request.subject == "Science" and "photosynthesis" in request.topic.lower():
        # Example: Generate a script for photosynthesis animation
        script = """
from manim import *

class Photosynthesis(Scene):
    def construct(self):
        # Title
        title = Text("Photosynthesis", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        
        # Equation
        equation = MathTex("6CO_2 + 6H_2O \\\\xrightarrow{\\\\text{sunlight}} C_6H_{12}O_6 + 6O_2")
        self.play(Write(equation))
        self.wait(2)
        self.play(equation.animate.to_edge(DOWN))
        
        # Plant cell
        cell = Circle(radius=2, color=GREEN)
        chloroplast = Circle(radius=0.5, color=DARK_GREEN)
        chloroplast.move_to([0.5, 0.5, 0])
        
        self.play(Create(cell), Create(chloroplast))
        
        # Sun rays
        sun = Dot(point=[3, 3, 0], radius=0.5, color=YELLOW)
        rays = VGroup(*[Line(sun.get_center(), cell.point_at_angle(angle), color=YELLOW) 
                      for angle in np.arange(0, TAU, TAU/8)])
        
        self.play(Create(sun), Create(rays))
        self.wait(1)
        
        # Arrow for CO2 entering
        co2_arrow = Arrow([-4, 0, 0], [-2, 0, 0], color=BLUE)
        co2_text = Text("CO2", font_size=20).next_to(co2_arrow, UP)
        
        # Arrow for O2 exiting
        o2_arrow = Arrow([2, 0, 0], [4, 0, 0], color=RED)
        o2_text = Text("O2", font_size=20).next_to(o2_arrow, UP)
        
        self.play(Create(co2_arrow), Write(co2_text))
        self.wait(1)
        self.play(Create(o2_arrow), Write(o2_text))
        self.wait(2)
"""
    else:
        # Default simple animation
        script = """
from manim import *

class DefaultAnimation(Scene):
    def construct(self):
        title = Text("{}".format(""" + f'"{request.topic}"' + """))
        self.play(Write(title))
        self.wait(1)
        
        # Animated subtitle
        subtitle = Text("Grade {} - {}".format(""" + f'"{request.grade}", "{request.subject}"' + """), font_size=30)
        subtitle.next_to(title, DOWN)
        self.play(Write(subtitle))
        self.wait(2)
        
        # Sample content
        content = Text("Interactive content would appear here", font_size=24)
        content.next_to(subtitle, DOWN, buff=1)
        self.play(Write(content))
        self.wait(1)
        
        # Highlight
        highlight = SurroundingRectangle(content, color=YELLOW)
        self.play(Create(highlight))
        self.wait(2)
"""
    
    return script


# Simplified function to generate content
async def generate_content(content_id: str, request: ContentRequest):
    """Background task to generate content based on the request"""
    content_path = os.path.join(CONTENT_DIR, content_id)
    os.makedirs(content_path, exist_ok=True)
    
    metadata = ContentMetadata(
        id=content_id,
        topic=request.topic,
        grade=request.grade,
        subject=request.subject,
        language=request.language,
        content_type=request.content_type,
        difficulty_level=request.difficulty_level,
        files=[],
        status="processing"
    )
    
    # Save initial metadata
    with open(os.path.join(content_path, "metadata.json"), "w") as f:
        f.write(metadata.json())
    
    try:
        if request.content_type == "video":
            # Generate manim script
            script = generate_manim_script(request)
            script_path = os.path.join(content_path, "animation.py")
            
            with open(script_path, "w") as f:
                f.write(script)
            
            # In a real implementation, we would call manim here
            # This is a simplified example
            """
            result = subprocess.run(
                ["manim", "-pql", script_path, "SolveEquation"],
                capture_output=True,
                text=True
            )
            """
            
            # For demo, let's simulate the manim output
            await asyncio.sleep(3)  # Simulate processing time
            
            # Add the output file to metadata
            metadata.files.append({
                "type": "video",
                "path": f"{content_path}/animation.mp4",
                "description": f"Animation of {request.topic}"
            })
            
            # Generate supporting materials
            if request.offline_capable:
                # For offline use, generate images and transcripts
                transcript_path = os.path.join(content_path, "transcript.txt")
                with open(transcript_path, "w") as f:
                    f.write(f"Transcript for {request.topic} animation\n")
                    f.write(f"This video explains {request.topic} for grade {request.grade} {request.subject}\n")
                
                metadata.files.append({
                    "type": "transcript",
                    "path": transcript_path,
                    "description": f"Transcript for {request.topic}"
                })
                
        elif request.content_type == "interactive":
            # Generate an HTML interactive content
            html_path = os.path.join(content_path, "interactive.html")
            
            # Simple HTML template for interactive content
            html_content = f"""
<!DOCTYPE html>
<html lang="{request.language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{request.topic} - Interactive</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .interactive {{ border: 1px solid #ccc; padding: 20px; margin-top: 20px; }}
        button {{ padding: 10px; background: #4CAF50; color: white; border: none; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{request.topic}</h1>
        <p>Grade {request.grade} - {request.subject}</p>
        
        <div class="interactive">
            <!-- Interactive elements would be inserted here -->
            <p>This is an interactive learning module for {request.topic}.</p>
            <div id="interactive-content">
                <button onclick="showNextStep()">Start Learning</button>
                <div id="steps"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Simple interactive script
        const steps = [
            "Step 1: Introduction to {request.topic}",
            "Step 2: Key concepts exploration",
            "Step 3: Interactive exercises",
            "Step 4: Assessment and feedback"
        ];
        
        let currentStep = 0;
        
        function showNextStep() {{
            if (currentStep < steps.length) {{
                const stepElement = document.createElement('p');
                stepElement.textContent = steps[currentStep];
                document.getElementById('steps').appendChild(stepElement);
                currentStep++;
            }}
            
            if (currentStep >= steps.length) {{
                document.querySelector('button').textContent = 'Completed!';
                document.querySelector('button').disabled = true;
            }}
        }}
    </script>
</body>
</html>
"""
            with open(html_path, "w") as f:
                f.write(html_content)
            
            metadata.files.append({
                "type": "interactive",
                "path": html_path,
                "description": f"Interactive content for {request.topic}"
            })
            
        elif request.content_type == "quiz":
            # Generate a quiz JSON
            quiz_path = os.path.join(content_path, "quiz.json")
            
            # Sample quiz generation - in real implementation, this would use AI
            quiz = {
                "title": f"Quiz on {request.topic}",
                "description": f"Test your knowledge of {request.topic}",
                "grade": request.grade,
                "subject": request.subject,
                "questions": [
                    {
                        "id": "q1",
                        "text": f"What is the main concept of {request.topic}?",
                        "options": [
                            "Option A", "Option B", "Option C", "Option D"
                        ],
                        "correct": 0,
                        "difficulty": 1
                    },
                    {
                        "id": "q2",
                        "text": f"How does {request.topic} relate to other concepts?",
                        "options": [
                            "Option A", "Option B", "Option C", "Option D"
                        ],
                        "correct": 2,
                        "difficulty": 2
                    }
                ]
            }
            
            with open(quiz_path, "w") as f:
                json.dump(quiz, f, indent=2)
            
            metadata.files.append({
                "type": "quiz",
                "path": quiz_path,
                "description": f"Quiz for {request.topic}"
            })
        
        # Update metadata with success status
        metadata.status = "completed"
        
    except Exception as e:
        # Update metadata with error information
        metadata.status = "error"
        metadata.error = str(e)
    
    # Save final metadata
    with open(os.path.join(content_path, "metadata.json"), "w") as f:
        f.write(metadata.json())


@app.get("/")
async def root():
    return {"message": "DronAIcharya Content Generation Service"}

@app.post("/generate/", response_model=ContentMetadata)
async def request_content(request: ContentRequest, background_tasks: BackgroundTasks):
    """Request generation of educational content"""
    content_id = str(uuid.uuid4())
    
    # Create initial metadata
    metadata = ContentMetadata(
        id=content_id,
        topic=request.topic,
        grade=request.grade,
        subject=request.subject,
        language=request.language,
        content_type=request.content_type,
        difficulty_level=request.difficulty_level,
        files=[],
        status="pending"
    )
    
    # Start generation in background
    background_tasks.add_task(generate_content, content_id, request)
    
    return metadata

@app.get("/status/{content_id}", response_model=ContentMetadata)
async def get_content_status(content_id: str):
    """Get the status of content generation"""
    try:
        metadata_path = os.path.join(CONTENT_DIR, content_id, "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        return metadata
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Content not found")

@app.get("/download/{content_id}/{file_index}")
async def download_content(content_id: str, file_index: int):
    """Download generated content"""
    try:
        metadata_path = os.path.join(CONTENT_DIR, content_id, "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        
        if file_index >= len(metadata["files"]):
            raise HTTPException(status_code=404, detail="File not found")
        
        file_info = metadata["files"][file_index]
        file_path = file_info["path"]
        
        return {"file_info": file_info, "download_url": f"/static/{content_id}/{Path(file_path).name}"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Content not found")

@app.post("/translate/{content_id}")
async def translate_content(content_id: str, target_language: str):
    """Translate content to another language"""
    # This would handle translation of content to different languages
    # For simplicity, we're returning a mock response
    return {"message": f"Content {content_id} will be translated to {target_language}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 