from flask import Flask, render_template, request, redirect
from fpdf import FPDF
from flask import send_file

app =  Flask(__name__)

users = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        
        users.append({
            "name" : name,
            "email" : email,
            "password": password
        })
        
        return redirect("/login")
    
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        for user in users:
            if user["email"] == email and user["password"] == password:
                return redirect("/form")
            
        return "Invalid Email or Password"
    
    return render_template("login.html")  

@app.route("/form")
def form():
    return render_template("form.html")  

@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    global user_data
    
    name=request.form["name"]
    email=request.form["email"]
    phone=request.form["phone"]
    address=request.form["address"]
    
    degree=request.form["degree"]
    college=request.form["college"]
    year=request.form["year"]
    
    skills=request.form["skills"]
    projects=request.form["projects"]
    experience=request.form["experience"]
    template = request.form["template"]
    suggestions = resume_suggestions(skills, projects, experience)
    

    user_data = {
    "name" : name,
    "email" : email,
    "phone" : phone,
    "address" : address,
    "degree" : degree,
    "college" : college,
    "year" : year,
    "skills" : skills,
    "projects" : projects,
    "experience" : experience
}
    
    jobs = suggest_jobs(skills)
    analysis = skill_gap_analysis(skills)
    
    return render_template(
        "resume.html",
        name=name,
        email=email,
        phone=phone,
        address=address,
        degree=degree,
        college=college,
        year=year,
        skills=skills,
        projects=projects,
        experience=experience,
        jobs=jobs,
        analysis=analysis,
        template=template,
        suggestions=suggestions
    )
    
def suggest_jobs(skills):
    
    skills=skills.lower().split(",")
    
    jobs=[]
    
    if "html" in skills or "css" in skills:
        jobs.append("Fronted Developer")
        
    if "python" in skills:
        jobs.append("Python Developer")
        
    if "java" in skills:
        jobs.append("Software Developer")
        
    if "sql" in skills:
        jobs.append("Database Administrator")
        
    if "javascript" in skills:
        jobs.append("Web Developer")
    
    return jobs  

job_skills = {
    "Fronted Developer" : ["html", "css", "javascript", "react"],
    "Python Developer" : ["python", "django", "flask", "sql"],
    "Software Developer" : ["java", "oop", "sql", "data structures"],
    "Database Administrator": ["sql", "database", "mysql"]
}

def skill_gap_analysis(user_skills):
    
    user_skills = user_skills.lower().split(",")
    
    results = []
    
    for job, skills in job_skills.items():
        
        matched =[]
        missing = []
        
        for skill in skills:
            if skill in user_skills:
                matched.append(skill)
            else:
                missing.append(skill)
                
        match_percent = int((len(matched) / len(skills)) * 100)
        
        results.append({
            "job" : job,
            "match": match_percent,
            "missing": missing
        })       
        
    return results   

def create_pdf(name,email,phone,address,degree,college,year,skills,projects,experience):
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200,10,txt=name,ln=True)
    
    pdf.cell(200,10,txt="Email: " + email,ln=True)
    pdf.cell(200,10,txt="Phone: " + phone,ln=True)
    pdf.cell(200,10,txt="Address: " + address,ln=True)
    
    pdf.cell(200,10,txt=" ",ln=True)
    
    pdf.cell(200,10,txt="Education",ln=True)
    pdf.cell(200,10,txt=degree + " - " + college + " (" + year + ")",ln=True)  
    
    pdf.cell(200,10,txt=" ",ln=True)
    
    pdf.cell(200,10,txt="Skills",ln=True)
    pdf.cell(200,10,txt=skills,ln=True)
    
    pdf.cell(200,10,txt=" ",ln=True)
    
    pdf.cell(200,10,txt="Projects",ln=True)
    pdf.multi_cell(0,10,projects)
    
    pdf.cell(200,10,txt=" ",ln=True)
    
    pdf.cell(200,10,txt="Experience",ln=True)
    pdf.multi_cell(0,10,experience)
    
    pdf.output("resume.pdf")   
    
@app.route("/download")
def download():
    create_pdf(
        user_data["name"],
        user_data["email"],
        user_data["phone"],
        user_data["address"],
        user_data["degree"],
        user_data["college"],
        user_data["year"],
        user_data["skills"],
        user_data["projects"],
        user_data["experience"]
        
    ) 
    return send_file("resume.pdf", as_attachment=True) 

def resume_suggestions(skills, projects, experience):
    suggestions = []
    skill_list = skills.split(",")
    
    if len(skill_list) < 3:
        suggestions.append("Add more technical skills to strengthen your resume.")
        
    if projects.strip() == "":
        suggestions.append("Include at least one project to show practical experience")
    
    if experience.strip() == "":
        suggestions.append("Mention internships, training, or volunteer work.")
    
    if len(projects) < 20:            
            suggestions.append("Explain your projects with more details.")
            
    return suggestions        

if __name__ == "__main__":
    app.run(debug=True)