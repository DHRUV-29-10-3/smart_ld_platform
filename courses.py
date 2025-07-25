import os

base_dir = "course_materials"
videos = [
    "ai_basics.mp4", "ai_bootcamp.mp4", "ds_ai.mp4", "cv_course.mp4", "transformers.mp4",
    "intro_dotnet.mp4", "ef_core.mp4", "dotnet_core.mp4", "winforms.mp4", "dotnet_projects.mp4",
    "uiux_fundamentals.mp4", "user_research.mp4", "design_thinking.mp4", "color_theory.mp4", "ux_case_studies.mp4"
]

documents = [
    "ml_python.pdf", "nlp_basics.pdf", "ai_ethics.pdf", "csharp_basics.pdf", "dotnet_api.pdf", "linq.pdf",
    "figma_tutorial.pdf", "typography.pdf", "accessibility.pdf"
]

assignments = [
    "dl_assignment.docx", "ai_real_world.docx", "aspnet_mvc.docx", "dotnet_security.docx",
    "wireframing.docx", "ui_trends_2025.docx"
]

# Create directories
os.makedirs(os.path.join(base_dir, "videos"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "documents"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "assignments"), exist_ok=True)

# Create dummy files
for file in videos:
    with open(os.path.join(base_dir, "videos", file), "w") as f:
        f.write(f"Dummy content for {file}")

for file in documents:
    with open(os.path.join(base_dir, "documents", file), "w") as f:
        f.write(f"Dummy content for {file}")

for file in assignments:
    with open(os.path.join(base_dir, "assignments", file), "w") as f:
        f.write(f"Dummy content for {file}")

print("All dummy files created successfully!")
