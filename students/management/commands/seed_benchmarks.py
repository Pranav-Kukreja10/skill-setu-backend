from django.core.management.base import BaseCommand
from students.models import IndustrySector, JobBenchmark

class Command(BaseCommand):
    help = "Seeds database with multi-department industry standards"

    def handle(self, *args, **options):
        self.stdout.write("Clearing previous benchmarks...")
        JobBenchmark.objects.all().delete()
        IndustrySector.objects.all().delete()

        # Define 3 departments
        # it_sector = IndustrySector.objects.create(name="Information Technology", description="Software Development and Cloud Engineering")
        # mech_sector = IndustrySector.objects.create(name="Mechanical Engineering", description="Industrial CAD, Fluid Mechanics, and Aerospace Systems")
        # finance_sector = IndustrySector.objects.create(name="Finance & Commerce", description="Accounting, Corporate Finance, and Banking Analytics")

        # ==============================================================================
        # CORE COMPUTING, ENGINEERING & TECHNOLOGY SECTORS
        # ==============================================================================

        it_sector = IndustrySector.objects.create(
            name="Information Technology & Software Engineering",
            description="Fullstack Development, Cloud Architecture, DevOps, Cybersecurity, Data Engineering, and Artificial Intelligence"
        )

        mech_sector = IndustrySector.objects.create(
            name="Mechanical & Manufacturing Engineering",
            description="CAD/CAM Design, Finite Element Analysis (FEA), Computational Fluid Dynamics (CFD), Robotics, and EV Powertrains"
        )

        ece_sector = IndustrySector.objects.create(
            name="Electrical & Electronics Engineering",
            description="VLSI Physical Design, Embedded Systems, Power Systems Engineering, and RF/Microwave Circuit Design"
        )

        civil_sector = IndustrySector.objects.create(
            name="Civil & Infrastructure Engineering",
            description="Structural Analysis, Geotechnical Engineering, Highway Design, Water Resources, and Construction Management"
        )

        chem_sector = IndustrySector.objects.create(
            name="Chemical & Process Engineering",
            description="Process Simulation, Plant Design, Thermodynamics, Separation Techniques, and Industrial Process Safety"
        )

        aero_sector = IndustrySector.objects.create(
            name="Aerospace & Aeronautical Engineering",
            description="Aerodynamics, Flight Mechanics, Propulsion Systems, and Avionics Systems Integration"
        )

        bme_sector = IndustrySector.objects.create(
            name="Biomedical Engineering & Healthcare Tech",
            description="Medical Device Design, Biomechanics, Clinical Instrumentation, and Biosignal Processing"
        )

        materials_sector = IndustrySector.objects.create(
            name="Materials Science & Metallurgical Engineering",
            description="Physical Metallurgy, Phase Transformations, Crystallography, Failure Analysis, and Advanced Materials"
        )

        enviro_sector = IndustrySector.objects.create(
            name="Environmental & Sustainability Engineering",
            description="Water Treatment Engineering, Air Dispersion Modeling, Site Remediation, and Environmental Impact Assessment"
        )

        industrial_sector = IndustrySector.objects.create(
            name="Industrial & Systems Engineering",
            description="Operations Research, Discrete Event Simulation, Facility Planning, Ergonomics, and Supply Chain Optimization"
        )

        marine_sector = IndustrySector.objects.create(
            name="Marine Engineering & Naval Architecture",
            description="Hydrostatics, Ship Resistance and Propulsion, Seakeeping, Mooring Systems, and Offshore Structural Design"
        )

        petro_sector = IndustrySector.objects.create(
            name="Petroleum & Energy Reservoir Engineering",
            description="Reservoir Simulation, Petrophysics, Well Logging, Enhanced Oil Recovery (EOR), and Directional Drilling"
        )

        # ==============================================================================
        # BUSINESS, FINANCE, LAW & COMMERCE SECTORS
        # ==============================================================================

        finance_sector = IndustrySector.objects.create(
            name="Finance, Banking & Commerce",
            description="Financial Modeling, Valuation, Corporate Accounting, Investment Banking, Quantitative Finance, and Risk Management"
        )

        management_sector = IndustrySector.objects.create(
            name="Business Administration & Management",
            description="Digital Marketing, Human Resource Management, Enterprise Sales, and Supply Chain Operations"
        )

        law_sector = IndustrySector.objects.create(
            name="Legal Studies & Corporate Law",
            description="Corporate Legal Advisory, Contract Drafting, Due Diligence, Arbitration, and Intellectual Property Rights (IPR)"
        )

        policy_sector = IndustrySector.objects.create(
            name="Public Policy, CSR & Sustainability",
            description="Corporate Social Responsibility (CSR), ESG Reporting Frameworks, Policy Evaluation, and Impact Assessment"
        )

        actuarial_sector = IndustrySector.objects.create(
            name="Actuarial Science & Insurance Analytics",
            description="Life Contingencies, Claims Reserving, Loss Modeling, Insurance Pricing GLMs, and IFRS 17 Compliance"
        )

        # ==============================================================================
        # PHARMACEUTICAL, HEALTHCARE & LIFE SCIENCES SECTORS
        # ==============================================================================

        pharma_sector = IndustrySector.objects.create(
            name="Pharmacy & Pharmaceutical Sciences",
            description="Formulation & Development (F&D), Drug Regulatory Affairs, Pharmacovigilance, and Quality Control Chemistry"
        )

        healthcare_sector = IndustrySector.objects.create(
            name="Allied Healthcare Sciences & Nursing",
            description="Critical Care Nursing, Physiotherapy, Clinical Optometry, Medical Laboratory Tech (MLT), and Radiology"
        )

        biotech_sector = IndustrySector.objects.create(
            name="Biotechnology & Food Technology",
            description="Bioprocess Engineering, Industrial Fermentation, Downstream Processing, and Food Safety & Quality Standards"
        )

        dental_sector = IndustrySector.objects.create(
            name="Dental Surgery & Oral Healthcare",
            description="Endodontics, Prosthodontics, Periodontology, Oral Surgery, and Clinical Dental Practice Operations"
        )

        veterinary_sector = IndustrySector.objects.create(
            name="Veterinary Medicine & Animal Sciences",
            description="Veterinary Clinical Practice, Animal Pathology, Zoonotic Disease Surveillance, and Livestock Health Operations"
        )

        ayush_sector = IndustrySector.objects.create(
            name="Ayurvedic Medicine & Traditional Healthcare",
            description="Kayachikitsa, Dravyaguna Pharmacology, Panchakarma Therapies, Nadi Pariksha, and AYUSH Clinical Documentation"
        )

        # ==============================================================================
        # DESIGN, MEDIA, ARCHITECTURE & HOSPITALITY SECTORS
        # ==============================================================================

        design_sector = IndustrySector.objects.create(
            name="Design, Animation & Game Development",
            description="UI/UX Product Design, Graphic Branding, 3D Character Animation, VFX Pipeline, and Game Level Architecture"
        )

        architecture_sector = IndustrySector.objects.create(
            name="Architecture & Interior Design",
            description="Architectural Working Drawings, Building Information Modeling (BIM), Interior Detailing, and Spatial Planning"
        )

        media_sector = IndustrySector.objects.create(
            name="Media, Journalism & Mass Communication",
            description="Public Relations (PR), Corporate Communications, Investigative Journalism, and Digital Broadcast Production"
        )

        hospitality_sector = IndustrySector.objects.create(
            name="Hospitality & Culinary Arts Management",
            description="Front Office Operations, Room Division Management, Food & Beverage (F&B) Service, and Culinary Production"
        )

        fashion_sector = IndustrySector.objects.create(
            name="Fashion Design & Textile Merchandising",
            description="Apparel Product Development, Garment Construction, Tech Pack Drafting, Fashion Merchandising, and Fabric Sourcing"
        )

        education_sector = IndustrySector.objects.create(
            name="Education, Pedagogy & Instructional Design",
            description="Curriculum Architecture, ADDIE Framework, LMS Course Development, Learning Analytics, and EdTech Design"
        )

        events_sector = IndustrySector.objects.create(
            name="Event Management & Experiential Marketing",
            description="Experiential Live Event Production, Technical Rider Vetting, Crowd Safety Operations, and Stage Rigging"
        )

        sports_sector = IndustrySector.objects.create(
            name="Sports Science & Sports Management",
            description="Exercise Physiology, Sports Biomechanics, Athlete Conditioning, Match-Day Operations, and League Management"
        )

        audio_sector = IndustrySector.objects.create(
            name="Sound Engineering & Audio Production",
            description="Multitrack Audio Recording, Studio Mixing & Mastering, Dolby Atmos Spatial Audio, and Acoustics Design"
        )

        # ==============================================================================
        # SPECIALIZED, EARTH & APPLIED APPLIED SCIENCES SECTORS
        # ==============================================================================

        agri_sector = IndustrySector.objects.create(
            name="Agriculture, Agritech & Horticulture",
            description="Agronomic Field Production, Integrated Pest Management (IPM), Precision Agritech, and GIS Crop Telemetry"
        )

        aviation_sector = IndustrySector.objects.create(
            name="Aviation & Airport Operations",
            description="Flight Dispatch Operations, Weight & Balance Planning, Ramp Operations, and Airport Passenger Flow Logistics"
        )

        psych_sector = IndustrySector.objects.create(
            name="Psychology & Behavioral Sciences",
            description="Clinical Psychological Assessment, Psychometric Testing, Cognitive Behavioral Therapy, and I/O Psychology"
        )

        nautical_sector = IndustrySector.objects.create(
            name="Nautical Science & Maritime Operations",
            description="Marine Passage Planning, Terrestrial & Celestial Navigation, Bridge Resource Management, and Ship Stability"
        )

        geosciences_sector = IndustrySector.objects.create(
            name="Applied Geology, Mining & Earth Sciences",
            description="Mineral Exploration, Structural Geology, Core Logging, Lithological Mapping, and Subsurface Modeling"
        )

        geoinformatics_sector = IndustrySector.objects.create(
            name="Geoinformatics, Cartography & LiDAR",
            description="Photogrammetry, Satellite Remote Sensing, LiDAR Point Cloud Processing, Spatial GIS, and DEM Modeling"
        )

        forensic_sector = IndustrySector.objects.create(
            name="Forensic Science & Criminology",
            description="Crime Scene Investigation, Forensic Toxicology, Serology, Ballistics, and Digital Evidence Custody"
        )

        bioinfo_sector = IndustrySector.objects.create(
            name="Bioinformatics & Computational Biology",
            description="Genomic Sequence Alignment, Next-Generation Sequencing (NGS) Pipelines, Molecular Docking, and Proteomics"
        )

        audiology_sector = IndustrySector.objects.create(
            name="Audiology & Speech-Language Pathology",
            description="Diagnostic Audiometry, Tympanometry, Hearing Aid Programming, and Neurogenic Speech Rehabilitation"
        )

        cosmetic_sector = IndustrySector.objects.create(
            name="Cosmetic Technology & Formulation Science",
            description="Cosmetic Emulsion Formulation, Skin Rheology, Preservative Efficacy Testing (PET), and Regulatory Claims"
        )

        dairy_sector = IndustrySector.objects.create(
            name="Dairy Science & Processing Technology",
            description="Thermal Milk Processing, HTST Pasteurization, Dairy Plant Clean-in-Place (CIP), and Quality Assurance"
        )

        fisheries_sector = IndustrySector.objects.create(
            name="Fisheries Science & Aquaculture",
            description="Aquaculture Engineering, Hatchery Management, Fish Pathology, Biofloc Systems, and Feed Optimization"
        )

        packaging_sector = IndustrySector.objects.create(
            name="Packaging Technology & Sustainable Materials",
            description="Barrier Properties Testing, Corrugated Packaging Structural Mechanics, Drop/Transit Testing, and Polymer Selection"
        )

        nuclear_sector = IndustrySector.objects.create(
            name="Medical Physics & Radiation Safety",
            description="Radiotherapy Treatment Planning, Linac Dosimetry Quality Assurance, Radiobiology, and AERB Compliance"
        )

        disaster_sector = IndustrySector.objects.create(
            name="Disaster Management & Humanitarian Relief",
            description="Hazard Vulnerability Assessment, Emergency Operations Center (EOC) Operations, and Relief Logistics"
        )

        # 1. Seed Computer Science and Engineering and Information Technology
        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Backend Engineer",
            core_skills=["python", "django", "fastapi", "postgresql", "sql", "flask", "c"],
            methodology_skills=["rest api", "mvc", "docker", "gunicorn", "jwt", "quality assurance"],
            tooling_skills=["git", "trello", "jira", "postman"]
        )
         
        # ==============================================================================
        # 1. FRONTEND ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Frontend Engineer (React / Next.js)",
            core_skills=["javascript", "typescript", "html5", "css3", "dom manipulation", "browser internals"],
            methodology_skills=["responsive design", "component-driven development", "state management", "server-side rendering", "web performance optimization"],
            tooling_skills=["react", "next.js", "tailwind css", "redux toolkit", "vite", "jest"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Frontend Engineer (Vue.js)",
            core_skills=["javascript", "typescript", "html5", "css3", "composition api", "dom manipulation"],
            methodology_skills=["single page applications", "responsive design", "state management", "web performance optimization", "cross-browser compatibility"],
            tooling_skills=["vue.js", "nuxt.js", "pinia", "vite", "tailwind css", "vitest"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Web Core & UI/UX Engineer",
            core_skills=["javascript", "html5", "css3", "css grid", "flexbox", "web animations"],
            methodology_skills=["web accessibility", "design systems", "responsive design", "cross-browser testing", "seo fundamentals"],
            tooling_skills=["figma", "storybook", "sass", "framer motion", "webpack", "lighthouse"]
        )

        # ==============================================================================
        # 2. BACKEND ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Backend Engineer (Python / FastAPI / Django)",
            core_skills=["python", "sql", "data structures", "asyncio", "concurrency", "rest apis"],
            methodology_skills=["object-oriented programming", "microservices", "api design", "test-driven development", "database indexing"],
            tooling_skills=["fastapi", "django", "postgresql", "redis", "celery", "docker"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Backend Engineer (Node.js / TypeScript)",
            core_skills=["javascript", "typescript", "node.js", "event loop", "sql", "nosql"],
            methodology_skills=["rest apis", "microservices", "event-driven architecture", "caching strategies", "unit testing"],
            tooling_skills=["express.js", "nest.js", "postgresql", "mongodb", "redis", "prisma"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Backend Engineer (Go)",
            core_skills=["go", "goroutines", "channels", "sql", "data structures", "networking fundamentals"],
            methodology_skills=["microservices", "concurrency patterns", "grpc communication", "rest apis", "system design"],
            tooling_skills=["gin", "gorm", "grpc", "postgresql", "docker", "prometheus"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Backend Engineer (Java / Spring Boot)",
            core_skills=["java", "jvm internals", "sql", "multithreading", "data structures", "collections framework"],
            methodology_skills=["object-oriented design", "microservices", "domain-driven design", "test-driven development", "database transactions"],
            tooling_skills=["spring boot", "spring cloud", "hibernate", "postgresql", "kafka", "maven"]
        )

        # ==============================================================================
        # 3. FULLSTACK ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Full Stack Engineer (MERN)",
            core_skills=["javascript", "html5", "css3", "node.js", "nosql", "rest apis"],
            methodology_skills=["mvc architecture", "state management", "api design", "full-lifecycle development", "authentication and authorization"],
            tooling_skills=["react", "express.js", "mongodb", "redux", "git", "docker"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Full Stack Engineer (PERN / Python)",
            core_skills=["python", "javascript", "typescript", "sql", "html5", "css3"],
            methodology_skills=["relational data modeling", "api integration", "state management", "responsive design", "test automation"],
            tooling_skills=["react", "fastapi", "postgresql", "tailwind css", "docker", "git"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Full Stack Engineer (Next.js / TypeScript)",
            core_skills=["typescript", "javascript", "react", "sql", "serverless architecture", "browser internals"],
            methodology_skills=["server-side rendering", "jamstack architecture", "database migrations", "performance optimization", "api security"],
            tooling_skills=["next.js", "prisma", "postgresql", "tailwind css", "trpc", "vercel"]
        )

        # ==============================================================================
        # 4. CLOUD, DEVOPS & SITE RELIABILITY ENGINEERING (SRE)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="DevOps Engineer",
            core_skills=["linux", "bash scripting", "networking fundamentals", "python", "system administration"],
            methodology_skills=["ci/cd pipelines", "infrastructure as code", "configuration management", "release engineering", "site reliability engineering"],
            tooling_skills=["docker", "kubernetes", "terraform", "github actions", "ansible", "aws"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Site Reliability Engineer (SRE)",
            core_skills=["linux internals", "networking protocols", "python", "go", "troubleshooting"],
            methodology_skills=["incident management", "chaos engineering", "observability", "capacity planning", "sla/slo management"],
            tooling_skills=["prometheus", "grafana", "kubernetes", "opentelemetry", "datadog", "terraform"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Cloud Infrastructure Engineer (AWS / Multi-Cloud)",
            core_skills=["cloud computing", "linux", "ip networking", "dns", "identity and access management"],
            methodology_skills=["infrastructure as code", "cloud security", "high availability architecture", "disaster recovery", "cost optimization"],
            tooling_skills=["aws", "terraform", "docker", "cloudformation", "packer", "vault"]
        )

        # ==============================================================================
        # 5. DATA ENGINEERING & BIG DATA
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Data Engineer",
            core_skills=["python", "sql", "data structures", "distributed computing", "linux"],
            methodology_skills=["etl pipeline design", "data warehousing", "data modeling", "stream processing", "batch processing"],
            tooling_skills=["apache spark", "apache airflow", "postgresql", "snowflake", "dbt", "kafka"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Big Data Engineer",
            core_skills=["java", "scala", "python", "sql", "distributed systems", "operating systems"],
            methodology_skills=["massively parallel processing", "lakehouse architecture", "data pipeline automation", "partitioning strategies", "real-time streaming"],
            tooling_skills=["apache spark", "apache kafka", "hadoop", "databricks", "apache flink", "hive"]
        )

        # ==============================================================================
        # 6. ARTIFICIAL INTELLIGENCE, MACHINE LEARNING & MLOPS
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Machine Learning Engineer",
            core_skills=["python", "linear algebra", "calculus", "probability and statistics", "algorithms"],
            methodology_skills=["supervised learning", "unsupervised learning", "feature engineering", "model evaluation", "cross-validation"],
            tooling_skills=["scikit-learn", "pytorch", "tensorflow", "pandas", "numpy", "jupyter"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Generative AI / LLM Engineer",
            core_skills=["python", "natural language processing", "deep learning", "vector embeddings", "information retrieval"],
            methodology_skills=["prompt engineering", "retrieval augmented generation", "model fine-tuning", "quantization", "semantic search"],
            tooling_skills=["langchain", "llamaindex", "hugging face", "pinecone", "chromadb", "openai api"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="MLOps Engineer",
            core_skills=["python", "linux", "cloud computing", "machine learning fundamentals", "bash scripting"],
            methodology_skills=["continuous delivery for ml", "model monitoring", "model drift detection", "feature store architecture", "data versioning"],
            tooling_skills=["mlflow", "kubeflow", "dvc", "docker", "kubernetes", "feast"]
        )

        # ==============================================================================
        # 7. CYBERSECURITY & INFORMATION SECURITY
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Application Security Engineer",
            core_skills=["cryptography", "web protocols", "python", "javascript", "linux"],
            methodology_skills=["owasp top 10", "threat modeling", "secure code review", "vulnerability assessment", "devsecops"],
            tooling_skills=["burp suite", "snyk", "sonarqube", "owasp zap", "git", "postman"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Penetration Tester / Ethical Hacker",
            core_skills=["network protocols", "linux internals", "tcp/ip", "python", "bash scripting", "operating systems"],
            methodology_skills=["penetration testing", "vulnerability scanning", "privilege escalation", "reverse engineering", "red teaming"],
            tooling_skills=["metasploit", "nmap", "wireshark", "burp suite", "kali linux", "aircrack-ng"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Security Operations Center (SOC) Analyst",
            core_skills=["networking fundamentals", "log analysis", "linux", "windows internals", "incident response"],
            methodology_skills=["threat detection", "incident handling", "siem management", "forensic analysis", "mitre att&ck framework"],
            tooling_skills=["splunk", "elastic siem", "wireshark", "snort", "suricata", "crowdstrike"]
        )

        # ==============================================================================
        # 8. MOBILE APPLICATION DEVELOPMENT
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Mobile Engineer (React Native)",
            core_skills=["javascript", "typescript", "react", "mobile ui design", "dom manipulation"],
            methodology_skills=["cross-platform development", "state management", "mobile performance optimization", "native bridge integration", "offline storage"],
            tooling_skills=["react native", "expo", "redux toolkit", "react navigation", "jest", "android studio"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Mobile Engineer (Flutter)",
            core_skills=["dart", "object-oriented programming", "mobile ui design", "widget lifecycle", "reactive programming"],
            methodology_skills=["cross-platform development", "state management", "rest api integration", "app store deployment", "performance profiling"],
            tooling_skills=["flutter", "bloc", "provider", "firebase", "android studio", "xcode"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Android Developer (Kotlin)",
            core_skills=["kotlin", "java", "android sdk", "concurrency", "memory management", "data structures"],
            methodology_skills=["mvvm architecture", "jetpack components", "reactive architecture", "clean architecture", "dependency injection"],
            tooling_skills=["android studio", "jetpack compose", "coroutines", "dagger hilt", "retrofit", "room"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="iOS Developer (Swift)",
            core_skills=["swift", "objective-c", "ios sdk", "memory management", "concurrency"],
            methodology_skills=["mvvm architecture", "apple human interface guidelines", "clean architecture", "unit testing", "rest api integration"],
            tooling_skills=["xcode", "swiftui", "uikit", "combine", "cocoapods", "core data"]
        )

        # ==============================================================================
        # 9. SYSTEMS & LOW-LATENCY PROGRAMMING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Systems Software Engineer (C++)",
            core_skills=["c++", "c", "data structures", "memory management", "multithreading", "pointers and references"],
            methodology_skills=["object-oriented design", "concurrency patterns", "cache optimization", "low-latency design", "hardware-software interfacing"],
            tooling_skills=["gdb", "cmake", "valgrind", "git", "linux", "llvm"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Systems & Low-Latency Engineer (Rust)",
            core_skills=["rust", "ownership and borrowing", "concurrency", "memory safety", "data structures", "network sockets"],
            methodology_skills=["zero-cost abstractions", "low-latency design", "concurrent programming", "systems design", "unit testing"],
            tooling_skills=["cargo", "tokio", "git", "linux", "gdb", "perf"]
        )



        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Blockchain & Smart Contract Developer",
            core_skills=["solidity", "ethereum", "cryptography", "javascript", "data structures"],
            methodology_skills=["smart contract security", "gas optimization", "decentralized architecture", "evm execution model", "token standards"],
            tooling_skills=["hardhat", "truffle", "ethers.js", "web3.js", "metamask", "openzeppelin"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="SDET / QA Automation Engineer",
            core_skills=["java", "python", "javascript", "data structures", "api testing", "test automation"],
            methodology_skills=["behavior-driven development (bdd)", "test-driven development (tdd)", "ci/cd test integration", "page object model", "regression testing"],
            tooling_skills=["selenium", "cypress", "playwright", "postman", "pytest", "testng"]
        )

        JobBenchmark.objects.create(
            sector=it_sector,
            role_title="Database Administrator / SQL Developer",
            core_skills=["sql", "relational algebra", "database design", "indexing", "stored procedures", "acid transactions"],
            methodology_skills=["query optimization", "database normalization", "backup and disaster recovery", "data replication", "partitioning"],
            tooling_skills=["postgresql", "mysql", "oracle database", "sql server", "redis", "dbeaver"]
        )

        # 2. Seed Mechanical Design Benchmark
        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="CAD Design Engineer",
            core_skills=["autocad", "solidworks", "catia", "ansys", "thermodynamics", "fluid mechanics"],
            methodology_skills=["gd&t", "fea", "geometric dimensioning", "stress analysis"],
            tooling_skills=["matlab", "msc nasran", "fusion 360"]
        )

        # ==============================================================================
        # MECHANICAL & MANUFACTURING ENGINEERING BENCHMARKS
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="CAD/CAM Design Engineer",
            core_skills=["engineering drawing", "mechanics of materials", "machine design", "metallurgy", "gd&t", "kinematics"],
            methodology_skills=["design for manufacturing (dfm)", "design for assembly (dfa)", "tolerance stackup analysis", "sheet metal design", "reverse engineering"],
            tooling_skills=["solidworks", "catia", "autocad", "mastercam", "creo", "ptc windchill"]
        )

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="FEA & Structural Analysis Engineer",
            core_skills=["finite element analysis", "solid mechanics", "strength of materials", "structural dynamics", "vibration analysis", "fatigue analysis"],
            methodology_skills=["mesh refinement", "static structural analysis", "dynamic analysis", "modal analysis", "fmea"],
            tooling_skills=["ansys mechanical", "abaqus", "hypermesh", "nastran", "solidworks simulation", "ls-dyna"]
        )

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="CFD & Thermal Systems Engineer",
            core_skills=["computational fluid dynamics", "thermodynamics", "heat transfer", "fluid mechanics", "aerodynamics", "turbomachinery"],
            methodology_skills=["turbulence modeling", "thermal management", "grid independence study", "conjugate heat transfer", "multiphase flow analysis"],
            tooling_skills=["ansys fluent", "openfoam", "star-ccm+", "ansys cfx", "pointwise", "matlab"]
        )

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="EV Powertrain & Battery Systems Engineer",
            core_skills=["electrochemistry", "thermodynamics", "electric motor theory", "battery management systems", "heat transfer", "powertrain dynamics"],
            methodology_skills=["thermal runaway mitigation", "state of charge estimation", "cell balancing", "powertrain sizing", "hardware-in-the-loop testing"],
            tooling_skills=["matlab", "simulink", "ansys fluent", "canalyzer", "solidworks", "comsol multiphysics"]
        )

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="Robotics & Mechatronics Engineer",
            core_skills=["kinematics", "dynamics", "control systems", "microcontrollers", "actuators", "signal processing"],
            methodology_skills=["motion planning", "sensor fusion", "plc programming", "trajectory generation", "feedback loop tuning"],
            tooling_skills=["ros", "matlab", "simulink", "arduino", "stm32", "siemens tia portal"]
        )

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="HVAC & MEP Design Engineer",
            core_skills=["psychrometrics", "thermodynamics", "fluid flow", "heat load calculation", "refrigeration cycles", "building physics"],
            methodology_skills=["ashrae standards", "duct sizing", "pipe sizing", "bim workflows", "indoor air quality compliance"],
            tooling_skills=["revit mep", "carrier hap", "autocad mep", "trace 700", "bluebeam revu"]
        )

        JobBenchmark.objects.create(
            sector=mech_sector,
            role_title="Quality & Manufacturing Engineer",
            core_skills=["manufacturing processes", "engineering metrology", "statistical process control", "material science", "destructive testing"],
            methodology_skills=["six sigma", "lean manufacturing", "dfma", "root cause analysis", "apqp/ppap", "kaizen"],
            tooling_skills=["cmm", "minitab", "sap erp", "autocad", "optical comparator", "calipers"]
        )

        # ==============================================================================
        # 1. ELECTRICAL & ELECTRONICS ENGINEERING (EEE / ECE)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=ece_sector,
            role_title="VLSI & ASIC Physical Design Engineer",
            core_skills=["digital logic design", "static timing analysis", "cmos technology", "semiconductor physics", "verilog", "systemverilog"],
            methodology_skills=["floorplanning", "place and route", "clock tree synthesis", "design rule checking (drc)", "layout versus schematic (lvs)"],
            tooling_skills=["synopsys design compiler", "cadence innovus", "primetime", "cadence virtuoso", "tcl", "modelism"]
        )

        JobBenchmark.objects.create(
            sector=ece_sector,
            role_title="Embedded Firmware Engineer",
            core_skills=["embedded c", "microcontrollers", "computer architecture", "interrupt handling", "rtos concepts", "digital electronics"],
            methodology_skills=["hardware-software codesign", "communication protocols (i2c/spi/uart)", "firmware debugging", "bare-metal programming", "hardware abstraction layers"],
            tooling_skills=["keil uvision", "stm32cubeide", "oscilloscope", "logic analyzer", "jtag", "git"]
        )

        JobBenchmark.objects.create(
            sector=ece_sector,
            role_title="Power Systems & High-Voltage Engineer",
            core_skills=["power systems analysis", "electrical machines", "high voltage engineering", "power electronics", "electromagnetics", "circuit theory"],
            methodology_skills=["load flow analysis", "short circuit analysis", "protective relay coordination", "substation design", "grid code compliance"],
            tooling_skills=["etap", "pscad", "matlab/simulink", "autocad electrical", "digsilent powerfactory"]
        )

        JobBenchmark.objects.create(
            sector=ece_sector,
            role_title="RF & Microwave Design Engineer",
            core_skills=["electromagnetic field theory", "transmission line theory", "rf circuit design", "s-parameters", "antenna theory", "smith charts"],
            methodology_skills=["impedance matching", "em simulation", "rf link budget analysis", "pcb layout design", "spectrum analysis"],
            tooling_skills=["keysight ads", "ansys hfss", "cst studio suite", "spectrum analyzer", "vector network analyzer (vna)"]
        )

        JobBenchmark.objects.create(
            sector=ece_sector,
            role_title="IoT Solutions & Edge Computing Engineer",
            core_skills=["microcontrollers", "embedded systems", "sensor interfacing", "c", "c++", "networking protocols"],
            methodology_skills=["mqtt communication", "low-power system design", "edge telemetry", "ota firmware updates", "hardware prototyping"],
            tooling_skills=["esp32", "arduino", "raspberry pi", "nodered", "thingsboard", "kicad"]
        )

        # ==============================================================================
        # 2. CIVIL, STRUCTURAL & INFRASTRUCTURE ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=civil_sector,
            role_title="Structural Design Engineer",
            core_skills=["structural mechanics", "reinforced concrete design", "structural steel design", "seismic analysis", "mechanics of solids", "soil-structure interaction"],
            methodology_skills=["finite element modeling", "load path calculation", "building code compliance", "wind load analysis", "value engineering"],
            tooling_skills=["etabs", "staad pro", "sap2000", "autocad", "revit structure", "safe"]
        )

        JobBenchmark.objects.create(
            sector=civil_sector,
            role_title="Geotechnical Engineer",
            core_skills=["soil mechanics", "rock mechanics", "foundation engineering", "geology", "hydrogeology", "shear strength of soils"],
            methodology_skills=["slope stability analysis", "soil settlement estimation", "site investigation", "retaining wall design", "deep foundation design"],
            tooling_skills=["plaxis", "geostudio", "gint", "autocad", "slide2", "ssettle"]
        )

        JobBenchmark.objects.create(
            sector=civil_sector,
            role_title="Transportation & Highway Design Engineer",
            core_skills=["highway engineering", "traffic flow theory", "pavement design", "surveying", "geometric design of roads", "transportation planning"],
            methodology_skills=["traffic impact assessment", "pavement distress evaluation", "horizontal and vertical alignment", "intersection design", "drainage design"],
            tooling_skills=["autodesk civil 3d", "synchro", "vissim", "bentley openroads", "arcgis"]
        )

        JobBenchmark.objects.create(
            sector=civil_sector,
            role_title="Water Resources & Hydrologic Engineer",
            core_skills=["fluid mechanics", "hydrology", "open channel hydraulics", "groundwater flow", "water quality modeling", "sediment transport"],
            methodology_skills=["flood risk assessment", "watershed modeling", "stormwater management design", "hydraulic structure sizing", "dam safety evaluation"],
            tooling_skills=["hec-ras", "hec-hms", "epanet", "swmm", "arcgis hydro", "flow-3d"]
        )

        JobBenchmark.objects.create(
            sector=civil_sector,
            role_title="Construction Project & Planning Engineer",
            core_skills=["construction materials", "estimation and costing", "surveying", "building codes", "project economics", "structural fundamentals"],
            methodology_skills=["critical path method (cpm)", "earned value management (evm)", "bim coordination", "site safety protocols", "quality assurance and quality control (qa/qc)"],
            tooling_skills=["primavera p6", "ms project", "autodesk navisworks", "procore", "bluebeam revu", "autocad"]
        )

        # ==============================================================================
        # 3. CHEMICAL & PROCESS ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=chem_sector,
            role_title="Chemical Process Design Engineer",
            core_skills=["chemical engineering thermodynamics", "mass transfer", "heat transfer", "fluid dynamics", "chemical reaction engineering", "separation processes"],
            methodology_skills=["process flow diagram (pfd) design", "piping and instrumentation diagram (p&id)", "mass and energy balances", "equipment sizing", "pinch analysis"],
            tooling_skills=["aspen hysys", "aspen plus", "pro/ii", "autocad", "matlab", "chemcad"]
        )

        JobBenchmark.objects.create(
            sector=chem_sector,
            role_title="Process Safety & Risk Engineer",
            core_skills=["process safety fundamentals", "thermodynamics", "chemical reaction hazard analysis", "flammability and explosion dynamics", "fluid mechanics"],
            methodology_skills=["hazop analysis", "layer of protection analysis (lopa)", "fault tree analysis", "quantitative risk assessment (qra)", "safety integrity level (sil) determination"],
            tooling_skills=["phast", "pha-pro", "bowtiexp", "exsilentia", "aloha", "flacs"]
        )

        # ==============================================================================
        # 4. AEROSPACE & AERONAUTICAL ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=aero_sector,
            role_title="Aerodynamics & Flight Dynamics Engineer",
            core_skills=["compressible flow", "viscous aerodynamics", "flight dynamics", "orbital mechanics", "propulsion theory", "aircraft stability and control"],
            methodology_skills=["airfoil and wing design", "wind tunnel testing", "flight trajectory optimization", "computational aerodynamic analysis", "flight envelope estimation"],
            tooling_skills=["ansys fluent", "matlab", "simulink", "xflr5", "openfoam", "cart3d"]
        )

        JobBenchmark.objects.create(
            sector=aero_sector,
            role_title="Avionics Systems Integration Engineer",
            core_skills=["avionics architecture", "radar fundamentals", "digital communication", "navigation systems", "control theory", "sensor fusion"],
            methodology_skills=["do-178c standards", "do-254 standards", "mil-std-1553 bus architecture", "arinc 429 communication", "fault-tolerant design"],
            tooling_skills=["matlab/simulink", "vector canalyzer", "labview", "dspace", "ibm doors", "oscilloscope"]
        )

        JobBenchmark.objects.create(
            sector=aero_sector,
            role_title="Aerospace Propulsion Engineer",
            core_skills=["gas turbine theory", "rocket propulsion", "combustion thermodynamics", "turbomachinery", "aerospace materials", "aerothermodynamics"],
            methodology_skills=["thrust chamber design", "combustion stability analysis", "cycle analysis", "thermal protection system sizing", "engine performance matching"],
            tooling_skills=["npss", "ansys cfx", "cea (chemical equilibrium with applications)", "matlab", "creo", "simulink"]
        )

        # ==============================================================================
        # 5. BIOMEDICAL & BIOENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=bme_sector,
            role_title="Medical Device Design Engineer",
            core_skills=["biomechanics", "biocompatibility", "biomaterials", "human anatomy and physiology", "mechanics of biomaterials", "fatigue testing"],
            methodology_skills=["iso 13485 compliance", "fda 510(k) documentation", "design controls", "medical risk management (iso 14971)", "dfma for medical devices"],
            tooling_skills=["solidworks", "ansys mechanical", "materialise mimics", "autocad", "minitab", "instron testmaster"]
        )

        JobBenchmark.objects.create(
            sector=bme_sector,
            role_title="Biomedical Instrumentation & Biosignals Engineer",
            core_skills=["biosignals processing", "analog circuit design", "digital signal processing", "transducer theory", "electrophysiology", "embedded systems"],
            methodology_skills=["analog signal filtering", "iec 60601 safety standards", "sensor calibration", "clinical trial data acquisition", "noise reduction techniques"],
            tooling_skills=["matlab", "labview", "altium designer", "biopac systems", "ltspice", "oscilloscope"]
        )

        # ==============================================================================
        # 6. MATERIALS SCIENCE & METALLURGICAL ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=materials_sector,
            role_title="Materials Characterization & Metallurgical Engineer",
            core_skills=["phase transformations", "physical metallurgy", "crystallography", "fracture mechanics", "thermodynamics of materials", "solid state physics"],
            methodology_skills=["metallographic examination", "heat treatment optimization", "failure analysis", "fractography", "corrosion assessment"],
            tooling_skills=["scanning electron microscopy (sem)", "x-ray diffraction (xrd)", "thermo-calc", "optical emission spectrometer", "instron hardness tester"]
        )

        # ==============================================================================
        # 7. ENVIRONMENTAL & SUSTAINABILITY ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=enviro_sector,
            role_title="Water & Wastewater Treatment Process Engineer",
            core_skills=["environmental chemistry", "biological wastewater treatment", "fluid mechanics", "water quality analytics", "contaminant transport"],
            methodology_skills=["biological nutrient removal", "sludge management and disposal", "membrane bioreactor design", "environmental regulations compliance", "treatment plant sizing"],
            tooling_skills=["biowin", "gps-x", "epanet", "autocad", "arcgis", "hach wims"]
        )

        JobBenchmark.objects.create(
            sector=enviro_sector,
            role_title="Environmental Compliance & Remediation Engineer",
            core_skills=["environmental chemistry", "hydrogeology", "soil science", "toxicology", "fate and transport modeling"],
            methodology_skills=["site contamination assessment", "in-situ groundwater remediation", "environmental impact assessment (eia)", "air dispersion modeling", "regulatory compliance audit"],
            tooling_skills=["aermod", "modflow", "arcgis", "gint", "procore"]
        )

        # ==============================================================================
        # 8. INDUSTRIAL & SYSTEMS ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=industrial_sector,
            role_title="Industrial & Supply Chain Systems Engineer",
            core_skills=["operations research", "linear programming", "applied probability and statistics", "queuing theory", "engineering economics", "ergonomics"],
            methodology_skills=["discrete event simulation", "facility layout planning", "value stream mapping", "inventory optimization", "time and motion study"],
            tooling_skills=["arena simulation", "anylogic", "sap erp", "minitab", "gurobi", "microsoft excel solver"]
        )

        # ==============================================================================
        # 9. MARINE & NAVAL ARCHITECTURE ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=marine_sector,
            role_title="Naval Architect & Marine Structural Engineer",
            core_skills=["hydrostatics", "marine hydrodynamics", "ship resistance and propulsion", "marine structural mechanics", "seakeeping and wave mechanics"],
            methodology_skills=["hull form optimization", "intact and damage stability calculation", "imo/marpol standards", "mooring system design", "scantling calculations"],
            tooling_skills=["maxsurf", "rhino 3d", "ansys aqwa", "orcaflex", "autocad", "gasp"]
        )

        # ==============================================================================
        # 10. PETROLEUM & ENERGY RESERVOIR ENGINEERING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=petro_sector,
            role_title="Petroleum Reservoir & Subsurface Engineer",
            core_skills=["reservoir fluid mechanics", "petrophysics", "rock properties", "well logging", "phase behavior of hydrocarbons", "reservoir thermodynamics"],
            methodology_skills=["enhanced oil recovery (eor)", "decline curve analysis", "material balance analysis", "well test analysis", "geological modeling integration"],
            tooling_skills=["slb petrel", "slb eclipse", "prosper", "techlog", "kappa sapphire", "cmg suite"]
        )

        JobBenchmark.objects.create(
            sector=petro_sector,
            role_title="Drilling & Well Completion Engineer",
            core_skills=["drilling hydraulics", "rock mechanics", "fluid mechanics", "wellbore integrity", "metallurgy of drillstrings"],
            methodology_skills=["directional drilling trajectory design", "casing and cementing design", "well control procedures", "hydraulic fracturing design", "drill bit selection"],
            tooling_skills=["landmark compass", "halliburton wellplan", "prosper", "autocad", "slb techlog"]
        )

        # 3. Seed Finance Analyst Benchmark
        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Financial Analyst",
            core_skills=["accounting", "valuation", "corporate finance", "excel", "tableau", "statistics"],
            methodology_skills=["dcf", "financial modeling", "portfolio management", "trend analysis"],
            tooling_skills=["powerbi", "ms office", "bloomberg terminal"]
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded multi-department job benchmarks!"))

            # ==============================================================================
        # FINANCE, BANKING & COMMERCE BENCHMARKS
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Financial Analyst & Valuation Associate",
            core_skills=["corporate finance", "discounted cash flow (dcf)", "financial statement analysis", "cost of capital (wacc)", "valuation methods", "time value of money"],
            methodology_skills=["financial modeling", "leveraged buyout (lbo) modeling", "sensitivity analysis", "comparable company analysis", "precedent transactions"],
            tooling_skills=["microsoft excel", "power bi", "sp capital iq", "factset", "think-cell", "tableau"]
        )

        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Corporate Accountant & Tax Consultant",
            core_skills=["financial accounting", "general ledger", "indirect taxation", "direct taxation", "balance sheet reconciliation", "accounting standards (gaap/ifrs)"],
            methodology_skills=["statutory audit", "gst compliance", "tds filing", "bank reconciliation", "internal controls over financial reporting"],
            tooling_skills=["tally prime", "sap fico", "quickbooks", "zoho books", "microsoft excel", "cleartax"]
        )

        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Investment Banking Analyst",
            core_skills=["capital markets", "corporate valuation", "mergers and acquisitions (m&a)", "equity research", "financial statement analysis", "corporate restructuring"],
            methodology_skills=["pitch book preparation", "accretion/dilution analysis", "due diligence", "comparable transactions", "fairness opinions"],
            tooling_skills=["bloomberg terminal", "sp capital iq", "factset", "pitchbook", "think-cell", "microsoft excel"]
        )

        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Risk & Compliance Analyst",
            core_skills=["credit risk", "market risk", "operational risk", "financial regulations", "probability and statistics", "counterparty risk"],
            methodology_skills=["basel iii framework", "aml/kyc compliance", "credit risk modeling", "sox compliance", "stress testing and scenario analysis"],
            tooling_skills=["sas", "sql", "nice actimize", "oracle mantas", "microsoft excel", "power bi"]
        )

        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Quantitative Finance Analyst",
            core_skills=["stochastic calculus", "time series analysis", "derivatives pricing", "econometrics", "probability theory", "linear algebra"],
            methodology_skills=["backtesting", "monte carlo simulation", "risk parity", "factor modeling", "algorithmic execution strategies"],
            tooling_skills=["python", "r", "sql", "matlab", "pandas", "quantlib"]
        )

        JobBenchmark.objects.create(
            sector=finance_sector,
            role_title="Statutory Audit & Accounts Associate",
            core_skills=["auditing standards", "financial reporting", "internal audit", "company law", "gaap/ifrs", "voucher verification"],
            methodology_skills=["substantive testing", "audit sampling", "working paper documentation", "compliance checklist vetting", "materiality assessment"],
            tooling_skills=["tally prime", "sap erp", "microsoft excel", "caseWare", "zoho books"]
        )

        # ==============================================================================
        # 1. PHARMACY & PHARMACEUTICAL SCIENCES (B.Pharm / M.Pharm / Pharm.D)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=pharma_sector,
            role_title="Formulation Development (F&D) Research Scientist",
            core_skills=["pharmaceutics", "pharmacokinetics", "biopharmaceutics", "dosage form design", "physical pharmacy", "preformulation studies"],
            methodology_skills=["good manufacturing practices (gmp)", "stability testing (ich guidelines)", "solubility enhancement", "technology transfer", "in vitro dissolution testing"],
            tooling_skills=["dissolution apparatus", "hplc", "ftir spectrometer", "uv-visible spectrophotometer", "rotary tablet press", "viscometer"]
        )

        JobBenchmark.objects.create(
            sector=pharma_sector,
            role_title="Regulatory Affairs Associate",
            core_skills=["pharmaceutical jurisprudence", "drug discovery pipeline", "clinical trials regulations", "intellectual property rights", "labeling regulations"],
            methodology_skills=["ectd dossier preparation", "ich guidelines compliance", "usfda 21 cfr compliance", "dmf preparation", "post-approval change submissions"],
            tooling_skills=["lorenz docubridge", "mastercontrol", "trackwise", "adobe acrobat pro", "microsoft excel", "documentum"]
        )

        JobBenchmark.objects.create(
            sector=pharma_sector,
            role_title="Pharmacovigilance & Drug Safety Associate",
            core_skills=["pharmacology", "toxicology", "pathophysiology", "medical terminology", "adverse drug reactions", "epidemiology"],
            methodology_skills=["individual case safety reports (icsr)", "signal detection", "meddra coding", "who-art coding", "aggregate safety reporting (pbrer/psur)"],
            tooling_skills=["argus safety", "arxsuite", "who vigibase", "pubmed", "microsoft excel", "meddra browser"]
        )

        JobBenchmark.objects.create(
            sector=pharma_sector,
            role_title="Pharmaceutical Quality Control (QC) Analyst",
            core_skills=["analytical chemistry", "chromatography principles", "chemical assay", "spectroscopy", "microbiology fundamentals", "stoichiometry"],
            methodology_skills=["good laboratory practices (glp)", "analytical method validation", "out of specification (oos) investigation", "pharmacopeial compliance (ip/bp/usp)", "calibration protocols"],
            tooling_skills=["hplc", "gas chromatography (gc)", "karl fischer titrator", "uv-vis spectrophotometer", "empower software", "analytical balance"]
        )

        # ==============================================================================
        # 2. ALLIED HEALTHCARE & NURSING SCIENCES (Nursing, BPT, Optometry, MLT, Radiology)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=healthcare_sector,
            role_title="Clinical Staff Nurse (Critical Care / Inpatient)",
            core_skills=["human anatomy and physiology", "pharmacology for nurses", "pathology", "medical-surgical nursing", "pediatric nursing", "infection control"],
            methodology_skills=["bls and acls protocols", "vital signs monitoring", "wound dressing and aseptic techniques", "iv medication administration", "patient triage"],
            tooling_skills=["multipara patient monitor", "infusion pump", "defibrillator", "pulse oximeter", "ecg machine", "ehr software"]
        )

        JobBenchmark.objects.create(
            sector=healthcare_sector,
            role_title="Consultant Physiotherapist & Rehabilitation Specialist",
            core_skills=["biomechanics", "kinesiology", "musculoskeletal anatomy", "exercise physiology", "neurological rehabilitation", "sports pathology"],
            methodology_skills=["manual therapy techniques", "gait analysis", "post-operative rehabilitation protocol", "ergonomic assessment", "dry needling protocols"],
            tooling_skills=["tens unit", "therapeutic ultrasound", "traction unit", "gonimeter", "interferential therapy (ift)", "rehabilitation balance board"]
        )

        JobBenchmark.objects.create(
            sector=healthcare_sector,
            role_title="Clinical Optometrist",
            core_skills=["ocular anatomy", "visual optics", "binocular vision", "ocular disease", "contact lens science", "pharmacology in eyecare"],
            methodology_skills=["subjective and objective refraction", "slit lamp bio-microscopy", "tonometry", "visual field testing", "orthoptic evaluation"],
            tooling_skills=["phoropter", "slit lamp", "fundus camera", "keratometer", "tonometer", "auto ref-keratometer"]
        )

        JobBenchmark.objects.create(
            sector=healthcare_sector,
            role_title="Medical Laboratory Technologist (MLT)",
            core_skills=["clinical biochemistry", "hematology", "medical microbiology", "histopathology", "immunology", "clinical pathology"],
            methodology_skills=["phlebotomy", "blood banking procedures", "gram staining & culture plating", "elisa protocol", "internal quality control (iqc)"],
            tooling_skills=["automated hematology analyzer", "biochemistry autoanalyzer", "binocular microscope", "centrifuge", "elisa reader", "coagulometer"]
        )

        JobBenchmark.objects.create(
            sector=healthcare_sector,
            role_title="Medical Imaging & Radiology Technologist",
            core_skills=["radiation physics", "radiographic anatomy", "radiation protection", "radiobiology", "imaging protocols", "contrast media"],
            methodology_skills=["patient positioning", "pacs workflow management", "computed tomography (ct) protocoling", "mri safety protocols", "aerb regulations compliance"],
            tooling_skills=["x-ray machine", "ct scanner", "mri system", "ultrasound transducer", "pacs software", "dicom viewer"]
        )

        # ==============================================================================
        # 3. MANAGEMENT, COMMERCE & BUSINESS ADMINISTRATION (BBA / MBA)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=management_sector,
            role_title="Digital Marketing & Performance Growth Manager",
            core_skills=["digital marketing strategy", "consumer behavior", "marketing analytics", "brand management", "content marketing", "media planning"],
            methodology_skills=["search engine optimization (seo)", "conversion rate optimization (cro)", "pay-per-click (ppc) campaign management", "a/b testing", "funnel optimization"],
            tooling_skills=["google analytics 4", "google ads", "meta ads manager", "semrush", "hubspot", "ahrefs"]
        )

        JobBenchmark.objects.create(
            sector=management_sector,
            role_title="Human Resource (HR) Generalist & Talent Specialist",
            core_skills=["organizational behavior", "labor laws & industrial relations", "compensation and benefits", "human resource planning", "performance management systems"],
            methodology_skills=["talent acquisition lifecycle", "employee onboarding", "hr compliance & audits", "grievance handling", "competency mapping"],
            tooling_skills=["workday", "bamboohr", "darwinbox", "keka hr", "linkedin recruiter", "microsoft excel"]
        )

        JobBenchmark.objects.create(
            sector=management_sector,
            role_title="Supply Chain & Logistics Operations Manager",
            core_skills=["operations management", "logistics and distribution", "procurement principles", "inventory management", "quantitative techniques in business"],
            methodology_skills=["demand forecasting", "vendor rating and evaluation", "route optimization", "warehouse space utilization", "just-in-time (jit) implementation"],
            tooling_skills=["sap mm", "oracle scm cloud", "microsoft excel", "tableau", "power bi", "tms software"]
        )

        JobBenchmark.objects.create(
            sector=management_sector,
            role_title="Business Development & Enterprise Sales Executive",
            core_skills=["strategic sales management", "business negotiation", "b2b market dynamics", "pricing strategies", "account management", "contract structuring"],
            methodology_skills=["lead generation", "sales pipeline management", "consultative selling", "competitive benchmarking", "cold outreach strategy"],
            tooling_skills=["salesforce crm", "hubspot crm", "apollo.io", "zoominfo", "linkedin sales navigator", "pandadoc"]
        )

        JobBenchmark.objects.create(
            sector=management_sector,
            role_title="Product Operations Associate",
            core_skills=["product management", "business analysis", "wireframing", "agile methodologies", "user feedback loops", "metrics analysis"],
            methodology_skills=["scrum framework", "user story mapping", "feature prioritization (rice)", "root cause analysis", "cross-functional stakeholder management"],
            tooling_skills=["jira", "confluence", "notion", "figma", "mixpanel", "trello"]
        )

        # ==============================================================================
        # 4. HOSPITALITY & CULINARY ARTS MANAGEMENT (B.Sc Hospitality / Hotel Admin)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=hospitality_sector,
            role_title="Front Office & Guest Experience Manager",
            core_skills=["hospitality operations", "guest relation management", "room division management", "hotel accounting", "revenue management"],
            methodology_skills=["check-in and check-out procedures", "handling guest grievances", "night audit procedures", "yield management strategies", "room allocation management"],
            tooling_skills=["opera pms", "amadeus hospitality", "hotelogix", "ids next", "epos system", "microsoft excel"]
        )

        JobBenchmark.objects.create(
            sector=hospitality_sector,
            role_title="Food & Beverage (F&B) Service Manager",
            core_skills=["food and beverage service", "menu engineering", "food science & nutrition", "bar & beverage operations", "cost control fundamentals"],
            methodology_skills=["fssai compliance", "banquet event order (beo) planning", "dining service etiquette", "f&b inventory control", "table turnover optimization"],
            tooling_skills=["micros pos", "posist", "touchbistro", "toast pos", "microsoft excel", "torqus"]
        )

        JobBenchmark.objects.create(
            sector=hospitality_sector,
            role_title="Executive Sous Chef / Culinary Operations Specialist",
            core_skills=["food production principles", "culinary arts", "bakery and confectionery", "sensory evaluation", "international cuisines", "kitchen hygiene"],
            methodology_skills=["recipe standardization", "haccp protocols", "food cost calculation", "kitchen workflow management", "plating and presentation techniques"],
            tooling_skills=["combi oven", "blast chiller", "sous-vide circulator", "industrial food processor", "kitchen display systems (kds)", "menu planning software"]
        )

        # ==============================================================================
        # 5. DESIGN, UI/UX, ANIMATION & GAME DESIGN (B.Des / B.Sc Animation / Game Dev)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=design_sector,
            role_title="UI/UX & Product Designer",
            core_skills=["user research", "information architecture", "interaction design", "visual design", "typography", "color theory"],
            methodology_skills=["wireframing & prototyping", "usability testing", "design system creation", "heuristic evaluation", "user journey mapping"],
            tooling_skills=["figma", "adobe xd", "miro", "protopie", "maze", "framer"]
        )

        JobBenchmark.objects.create(
            sector=design_sector,
            role_title="Graphic & Brand Identity Designer",
            core_skills=["visual communication", "typography", "branding principles", "editorial design", "layout theory", "print production basics"],
            methodology_skills=["brand guideline creation", "packaging design", "vector illustration", "color separation for print", "social media creative design"],
            tooling_skills=["adobe illustrator", "adobe photoshop", "adobe indesign", "canva", "figma", "coreldraw"]
        )

        JobBenchmark.objects.create(
            sector=design_sector,
            role_title="3D Animator & Visual Effects (VFX) Artist",
            core_skills=["3d modeling principles", "12 principles of animation", "anatomy for artists", "cinematography", "lighting and rendering", "texturing"],
            methodology_skills=["character rigging", "keyframe animation", "uv unwrapping", "rotoscoping", "compositing pipeline"],
            tooling_skills=["autodesk maya", "blender", "zbrush", "foundry nuke", "substance painter", "adobe after effects"]
        )

        JobBenchmark.objects.create(
            sector=design_sector,
            role_title="Game Designer & Level Architect",
            core_skills=["game mechanics design", "level design", "gameplay balancing", "interactive narrative design", "3d spatial reasoning"],
            methodology_skills=["game prototyping", "blockout creation", "player experience testing", "game economy design", "shader graph creation"],
            tooling_skills=["unreal engine", "unity 3d", "blender", "visual studio", "perforce", "c#"]
        )

        # ==============================================================================
        # 6. ARCHITECTURE & INTERIOR DESIGN (B.Arch / B.Des Interior Design)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=architecture_sector,
            role_title="Architectural Project Designer",
            core_skills=["architectural design", "building materials and construction", "history of architecture", "structural systems", "climatology in architecture", "building services"],
            methodology_skills=["national building code (nbc) compliance", "working drawing preparation", "bim modeling", "space programming", "sustainable architectural design"],
            tooling_skills=["autodesk revit", "autocad", "sketchup", "enscape", "lumion", "rhino 3d"]
        )

        JobBenchmark.objects.create(
            sector=architecture_sector,
            role_title="Interior & Spatial Designer",
            core_skills=["interior ergonomics", "materials and finishes", "lighting design", "furniture design", "color psychology", "spatial planning"],
            methodology_skills=["mood board development", "joinery detailing", "bill of quantities (boq) estimation", "vendor site supervision", "false ceiling & electrical layout"],
            tooling_skills=["autocad", "sketchup", "3ds max", "v-ray", "photoshop", "ms excel"]
        )

        # ==============================================================================
        # 7. MEDIA, JOURNALISM & MASS COMMUNICATION (BA / MA Journalism)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=media_sector,
            role_title="Public Relations (PR) & Corporate Communications Specialist",
            core_skills=["media relations", "mass communication theory", "corporate storytelling", "crisis communication", "stakeholder management"],
            methodology_skills=["press release drafting", "media pitching", "press conference coordination", "reputation management", "internal communications strategy"],
            tooling_skills=["cision", "meltwater", "canva", "microsoft powerpoint", "mailchimp", "google alerts"]
        )

        JobBenchmark.objects.create(
            sector=media_sector,
            role_title="Digital Content Journalist & Broadcast Producer",
            core_skills=["investigative journalism", "news writing & reporting", "media ethics & laws", "video production", "photojournalism"],
            methodology_skills=["fact-checking and verification", "video editing for digital news", "scriptwriting", "on-camera reporting", "digital news curation"],
            tooling_skills=["adobe premiere pro", "audacity", "wordpress cms", "canva", "dslr cameras", "obs studio"]
        )

        # ==============================================================================
        # 8. LAW & LEGAL STUDIES (BA LLB / BBA LLB / LLM)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=law_sector,
            role_title="Corporate Legal Associate & Contract Specialist",
            core_skills=["law of contracts", "company law", "commercial jurisprudence", "banking law", "mergers and acquisitions law", "arbitration and conciliation"],
            methodology_skills=["contract drafting and vetting", "legal due diligence", "statutory corporate compliance", "dispute resolution management", "legal risk mitigation"],
            tooling_skills=["manupatra", "scc online", "lexisnexis", "westlaw", "microsoft word", "docusign"]
        )

        JobBenchmark.objects.create(
            sector=law_sector,
            role_title="Intellectual Property (IPR) & Patent Associate",
            core_skills=["patent law", "trademark law", "copyright law", "design protection law", "ip valuation", "indian patent act"],
            methodology_skills=["patent prior art search", "patent claim drafting", "trademark opposition filing", "fer response drafting", "infringement analysis"],
            tooling_skills=["google patents", "espacenet", "ipindia portal", "wipo patentscope", "orbit intelligence", "microsoft excel"]
        )

        # ==============================================================================
        # 9. BIOTECHNOLOGY & FOOD TECHNOLOGY (B.Sc / B.Tech / M.Sc)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=biotech_sector,
            role_title="Industrial Bioprocess & Fermentation Scientist",
            core_skills=["molecular biology", "microbial genetics", "bioprocess engineering", "cell culture techniques", "downstream processing", "biochemistry"],
            methodology_skills=["bioreactor operation & scale-up", "cell line maintenance", "chromatographic purification", "sterilization validations", "aseptic culturing"],
            tooling_skills=["bioreactor / fermenter", "hplc", "centrifuge", "laminar air flow cabinet", "autoclave", "spectrophotometer"]
        )

        JobBenchmark.objects.create(
            sector=biotech_sector,
            role_title="Food Safety & Quality Assurance Officer",
            core_skills=["food chemistry", "food microbiology", "food preservation techniques", "food packaging science", "sensory analysis"],
            methodology_skills=["fssai compliance standards", "haccp plan implementation", "iso 22000 audits", "shelf-life testing", "adulteration testing"],
            tooling_skills=["moisture analyzer", "refractometer", "ph meter", "texture analyzer", "viscometer", "microbial incubator"]
        )

        # ==============================================================================
        # 10. EDUCATION, PEDAGOGY & INSTRUCTIONAL DESIGN (B.Ed / M.Ed)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=education_sector,
            role_title="Curriculum Architect & Instructional Designer",
            core_skills=["educational psychology", "curriculum design", "pedagogical frameworks", "bloom's taxonomy", "formative and summative assessment"],
            methodology_skills=["addie model implementation", "storyboard creation", "learning outcome mapping", "gamification in learning", "rubric development"],
            tooling_skills=["articulate storyline 360", "adobe captivate", "moodle lms", "canvas lms", "canva", "h5p"]
        )

        JobBenchmark.objects.create(
            sector=education_sector,
            role_title="EdTech Content Developer & Academic Coordinator",
            core_skills=["subject matter expertise", "pedagogical content knowledge", "content scripting", "educational technology", "student engagement analytics"],
            methodology_skills=["microlearning design", "video lecture storyboarding", "assessment question tagging", "curriculum pacing", "doubt resolution management"],
            tooling_skills=["notion", "google classroom", "loom", "obs studio", "canvas lms", "camtasia"]
        )

        # ==============================================================================
        # 1. AGRICULTURE, AGRITECH & HORTICULTURE (B.Sc / M.Sc Agriculture / Horticulture)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=agri_sector,
            role_title="Agronomist & Crop Production Specialist",
            core_skills=["soil science", "crop physiology", "plant pathology", "entomology", "plant breeding", "weed science"],
            methodology_skills=["integrated pest management (ipm)", "soil nutrient management", "crop rotation planning", "yield forecasting", "drip irrigation management"],
            tooling_skills=["soil testing kit", "spad chlorophyll meter", "qgis", "ndvi sensors", "drone deploy", "agriapp"]
        )

        JobBenchmark.objects.create(
            sector=agri_sector,
            role_title="Precision Agriculture & Farm Automation Engineer",
            core_skills=["remote sensing", "gis mapping", "agronomy fundamentals", "sensor technology", "crop canopy analytics"],
            methodology_skills=["variable rate application (vra)", "ndvi mapping", "smart irrigation scheduling", "precision spray management", "farm telemetry monitoring"],
            tooling_skills=["qgis", "arcgis pro", "pix4dfields", "dji agras", "climate fieldview", "sentinel hub"]
        )

        # ==============================================================================
        # 2. FASHION DESIGN, TEXTILE TECHNOLOGY & MERCHANDISING (NIFT / B.Des / B.Tech)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=fashion_sector,
            role_title="Fashion Apparel Designer & Technical Developer",
            core_skills=["garment construction", "textile science", "pattern making", "fashion illustration", "draping", "history of costume"],
            methodology_skills=["tech pack creation", "trend forecasting", "fit analysis", "spec sheet creation", "apparel costing"],
            tooling_skills=["clo 3d", "adobe illustrator", "optitex", "gerber accumark", "wgsn", "adobe photoshop"]
        )

        JobBenchmark.objects.create(
            sector=fashion_sector,
            role_title="Apparel Merchandiser & Garment Sourcing Executive",
            core_skills=["textile manufacturing", "garment costing", "fabric yarn count", "international trade", "apparel logistics"],
            methodology_skills=["sample tracking and approvals", "time and action (t&a) calendar", "vendor management", "fabric consumption estimation", "aql inspection standards"],
            tooling_skills=["fastreact", "sap apparel", "microsoft excel", "gerber plm", "bluecherry erp"]
        )

        # ==============================================================================
        # 3. AVIATION, FLIGHT OPERATIONS & AIRPORT MANAGEMENT (B.Sc Aviation / BBA Aviation)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=aviation_sector,
            role_title="Flight Operations & Dispatch Specialist",
            core_skills=["aviation meteorology", "aerodynamics", "air navigation", "flight planning", "aircraft systems", "air traffic management"],
            methodology_skills=["flight plan filing", "fuel calculation", "notam analysis", "weight and balance calculation", "etops compliance", "dgca/faa regulations"],
            tooling_skills=["jeppesen flitestar", "sabre dispatch", "navblue", "sita telex", "arinc 633", "skyvector"]
        )

        JobBenchmark.objects.create(
            sector=aviation_sector,
            role_title="Airport Ground Handling & Terminal Operations Executive",
            core_skills=["airport operations", "aviation safety regulations", "ramp management", "baggage handling systems", "passenger handling services"],
            methodology_skills=["turnaround coordination", "icao/iata safety standards", "terminal crowd management", "emergency response planning", "on-time performance (otp) tracking"],
            tooling_skills=["amadeus airport common use service", "sita airport management", "sabre airvision", "vamsys", "microsoft excel"]
        )

        # ==============================================================================
        # 4. PSYCHOLOGY, BEHAVIORAL SCIENCES & COUNSELING (BA / B.Sc / MA / M.Sc Psychology)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=psych_sector,
            role_title="Clinical Psychologist & Mental Health Counselor",
            core_skills=["abnormal psychology", "psychopathology", "psychological assessment", "developmental psychology", "neuropsychology", "cognitive behavioral theory"],
            methodology_skills=["cognitive behavioral therapy (cbt)", "case formulation", "mental status examination (mse)", "psychometric evaluation", "crisis intervention"],
            tooling_skills=["spss", "wisc test battery", "rorschach inkblot test", "beck depression inventory (bdi)", "dsm-5/icd-11", "qualtrics"]
        )

        JobBenchmark.objects.create(
            sector=psych_sector,
            role_title="Industrial-Organizational (I/O) Psychologist & People Scientist",
            core_skills=["organizational psychology", "psychometrics", "workplace ergonomics", "behavioral statistics", "human performance modeling"],
            methodology_skills=["job analysis", "360-degree assessment design", "employee engagement diagnosis", "leadership competency modeling", "assessment center methodology"],
            tooling_skills=["spss", "r", "qualtrics", "hogan assessment system", "mbti platform", "tableau"]
        )

        # ==============================================================================
        # 5. PUBLIC POLICY, SUSTAINABILITY & ESG (MPP / MSW / Sustainability Degrees)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=policy_sector,
            role_title="ESG & Corporate Social Responsibility (CSR) Specialist",
            core_skills=["environmental social governance (esg)", "sustainable development goals (sdgs)", "carbon accounting", "social impact assessment", "corporate governance"],
            methodology_skills=["gri standards reporting", "brsr framework compliance", "stakeholder materiality assessment", "carbon footprint calculation", "impact monitoring and evaluation (m&e)"],
            tooling_skills=["ecovadis", "enablon", "microsoft excel", "sp global esg", "power bi", "qualtrics"]
        )

        JobBenchmark.objects.create(
            sector=policy_sector,
            role_title="Public Policy Analyst & Governance Associate",
            core_skills=["public economics", "policy evaluation", "political science", "econometrics", "administrative jurisprudence", "public finance"],
            methodology_skills=["policy brief drafting", "cost-benefit analysis (cba)", "stakeholder consultation", "randomized controlled trial (rct) evaluation", "regulatory impact analysis"],
            tooling_skills=["stata", "r", "tableau", "spss", "python", "overleaf/latex"]
        )

        # ==============================================================================
        # 6. SPORTS SCIENCE, KINESIOLOGY & SPORTS MANAGEMENT (B.P.Ed / M.P.Ed / BSM)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=sports_sector,
            role_title="Sports Performance Coach & Exercise Physiologist",
            core_skills=["exercise physiology", "sports biomechanics", "kinesiology", "sports nutrition", "muscle anatomy", "neuromuscular conditioning"],
            methodology_skills=["periodization planning", "lactate threshold testing", "vo2 max assessment", "functional movement screening (fms)", "injury risk mitigation"],
            tooling_skills=["catapult gps", "force plate systems", "metabolic cart", "polar heart rate monitor", "hudl technique", "dartfish"]
        )

        JobBenchmark.objects.create(
            sector=sports_sector,
            role_title="Sports Operations & League Management Executive",
            core_skills=["sports marketing", "sports law & ethics", "facility management", "sponsorship valuation", "event ticketing economics"],
            methodology_skills=["match-day operations management", "anti-doping compliance (wada/nada)", "broadcast logistics coordination", "athlete contract management", "crowd safety management"],
            tooling_skills=["genius sports", "sportradar", "ticketmaster backend", "microsoft excel", "canva", "monday.com"]
        )

        # ==============================================================================
        # 7. EVENT MANAGEMENT & EXPERIENTIAL MARKETING
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=events_sector,
            role_title="Experiential Event Producer & Live Operations Manager",
            core_skills=["event budgeting", "stage lighting & acoustic physics", "crowd psychology", "production economics", "vendor logistics"],
            methodology_skills=["run of show (ros) design", "technical rider vetting", "crowd risk assessment", "crisis management", "stage rigging planning"],
            tooling_skills=["vectorworks spotlight", "autocad", "sketchup", "monday.com", "slack", "cvent"]
        )

        # ==============================================================================
        # 8. NAUTICAL SCIENCE & MARITIME OPERATIONS (B.Sc Nautical Science)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=nautical_sector,
            role_title="Deck Navigation Officer (Nautical Science)",
            core_skills=["terrestrial navigation", "celestial navigation", "meteorology at sea", "ship stability", "colregs (collision regulations)", "cargo work"],
            methodology_skills=["passage planning", "bridge resource management (brm)", "marpol compliance", "solas protocol execution", "radar plotting"],
            tooling_skills=["ecdis (electronic chart display)", "arpa radar", "gyro compass", "ais transponder", "sextant", "gmdss console"]
        )

        # ==============================================================================
        # 9. APPLIED GEOLOGY, MINING & EARTH SCIENCES (B.Sc / M.Sc Applied Geology)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=geosciences_sector,
            role_title="Exploration Geologist & Mineralogist",
            core_skills=["structural geology", "mineralogy", "petrology", "stratigraphy", "geochemistry", "economic geology"],
            methodology_skills=["core logging", "geochemical sampling", "lithological mapping", "mineral resource estimation", "subsurface cross-section profiling"],
            tooling_skills=["leapfrog geo", "micromine", "arcgis", "qgis", "petrel", "petrographic microscope"]
        )

        # ==============================================================================
        # 10. ACTUARIAL SCIENCE & INSURANCE ANALYTICS (B.Sc Actuarial / IFOA / IAI)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=actuarial_sector,
            role_title="Actuarial Analyst & Insurance Pricing Associate",
            core_skills=["actuarial mathematics", "life contingencies", "loss models", "probability & mathematical statistics", "financial economics", "survival models"],
            methodology_skills=["claims reserving (chain ladder)", "experience rating", "glms for insurance pricing", "ifrs 17 compliance", "capital modeling"],
            tooling_skills=["prophet", "python", "r", "microsoft excel / vba", "sas", "sql"]
        )

        # ==============================================================================
        # 11. DENTAL SURGERY & ORAL HEALTHCARE (BDS / MDS)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=dental_sector,
            role_title="Clinical Dental Surgeon & Practice Associate",
            core_skills=["oral anatomy and histology", "oral pathology", "prosthodontics", "conservative dentistry & endodontics", "periodontology", "oral surgery"],
            methodology_skills=["root canal treatment (rct) protocol", "crown and bridge preparation", "dental prophylaxis", "local anesthesia administration", "dental radiography interpretation"],
            tooling_skills=["dental air turbine handpiece", "rvg digital x-ray", "apex locator", "ultrasonic scaler", "autoclave sterilizer", "practo ray"]
        )

        # ==============================================================================
        # 12. VETERINARY MEDICINE & ANIMAL HUSBANDRY (B.V.Sc & AH / M.V.Sc)
        # ==============================================================================

        JobBenchmark.objects.create(
            sector=veterinary_sector,
            role_title="Veterinary Clinician & Livestock Health Officer",
            core_skills=["veterinary anatomy & physiology", "veterinary pharmacology", "veterinary pathology", "animal nutrition", "veterinary microbiology", "zoonotic epidemiology"],
            methodology_skills=["clinical diagnosis in animals", "vaccination scheduling", "veterinary surgical asepsis", "herd health monitoring", "necropsy examination"],
            tooling_skills=["veterinary ultrasound scanner", "veterinary anesthesia machine", "cbc vet analyzer", "centrifuge", "compound microscope", "surgical autoclave"]
        )

                # ==============================================================================
        # 1. FORENSIC SCIENCE & CRIMINOLOGY (B.Sc / M.Sc Forensic Science)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=forensic_sector,
            role_title="Forensic Scientist & Crime Scene Investigator",
            core_skills=["forensic serology", "forensic toxicology", "fingerprint science", "forensic ballistics", "criminalistics", "dna profiling"],
            methodology_skills=["chain of custody maintenance", "crime scene reconstruction", "bloodstain pattern analysis", "forensic photography", "expert witness testimony"],
            tooling_skills=["comparison microscope", "gas chromatography-mass spectrometry (gc-ms)", "ftir spectrometer", "alternate light source (als)", "uv transilluminator", "luminol reagent kit"]
        )
    
        # ==============================================================================
        # 2. BIOINFORMATICS & COMPUTATIONAL BIOLOGY (B.Tech / M.Sc Bioinformatics)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=bioinfo_sector,
            role_title="Bioinformatics Scientist & Computational Biologist",
            core_skills=["genomics", "proteomics", "molecular biology", "next-generation sequencing (ngs)", "structural biology", "python"],
            methodology_skills=["sequence alignment", "molecular docking", "variant calling pipelines", "phylogenetic analysis", "rna-seq differential expression analysis"],
            tooling_skills=["bioconductor", "blast", "pymol", "autodock vina", "samtools", "gatk"]
        )
    
        # ==============================================================================
        # 3. AUDIOLOGY & SPEECH-LANGUAGE PATHOLOGY (BASLP / MASLP)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=audiology_sector,
            role_title="Clinical Audiologist & Speech-Language Pathologist",
            core_skills=["psychoacoustics", "auditory anatomy and physiology", "speech acoustics", "neurogenic communication disorders", "phonetics", "vestibular science"],
            methodology_skills=["pure tone audiometry", "tympanometry", "otoacoustic emissions (oae) testing", "auditory brainstem response (abr)", "speech rehabilitation therapy"],
            tooling_skills=["clinical audiometer", "tympanometer", "noah software", "videonystagmography (vng)", "praat", "hearing aid programmer"]
        )
    
        # ==============================================================================
        # 4. AYURVEDIC MEDICINE & TRADITIONAL SYSTEMS (BAMS / MD Ayurveda)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=ayush_sector,
            role_title="Ayurvedic Medical Officer & Clinical Researcher",
            core_skills=["dravyaguna (pharmacology)", "kayachikitsa (internal medicine)", "panchakarma principles", "rasashastra", "ayurvedic pathophysiology", "charaka samhita"],
            methodology_skills=["nadi pariksha (pulse diagnosis)", "panchakarma therapy protocol", "ayurvedic formulation compounding", "clinical trial documentation", "dietary lifestyle counseling (pathya-apathya)"],
            tooling_skills=["shirodhara apparatus", "panchakarma therapy tables", "electronic medical records (emr)", "optical microscope", "analytical balance", "herb grinder"]
        )
    
        # ==============================================================================
        # 5. COSMETIC TECHNOLOGY & FORMULATION SCIENCE (B.Tech / M.Sc Cosmetics)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=cosmetic_sector,
            role_title="Cosmetic Formulation & R&D Chemist",
            core_skills=["colloid and surface chemistry", "dermatology fundamentals", "rheology", "surfactant science", "skin histology", "emulsion theory"],
            methodology_skills=["cosmetic stability testing", "preservative efficacy testing (pet)", "formula scale-up", "sensory panel evaluation", "claim substantiation"],
            tooling_skills=["brookfield viscometer", "homogenizer", "ph meter", "stability chambers", "texture analyzer", "chromameter"]
        )
    
        # ==============================================================================
        # 6. DAIRY TECHNOLOGY & DAIRY ENGINEERING (B.Tech Dairy Technology)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=dairy_sector,
            role_title="Dairy Processing & Quality Assurance Engineer",
            core_skills=["dairy chemistry", "dairy microbiology", "thermal milk processing", "pasteurization kinetics", "cheese technology", "dairy refrigeration"],
            methodology_skills=["clean-in-place (cip) validation", "htst pasteurization protocol", "milk fat standardization", "sensory profiling of dairy", "fssai dairy compliance"],
            tooling_skills=["milko-tester", "homogenizer", "gerber centrifuge", "htst pasteurizer", "moisture analyzer", "microbial incubator"]
        )
    
        # ==============================================================================
        # 7. FISHERIES SCIENCE & AQUACULTURE (B.F.Sc / M.F.Sc)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=fisheries_sector,
            role_title="Aquaculture Farm Manager & Hatchery Specialist",
            core_skills=["aquaculture engineering", "fish nutrition", "fish pathology", "limnology", "aquatic ecology", "fish breeding genetics"],
            methodology_skills=["water quality monitoring", "induced breeding techniques", "biofloc system management", "fish disease diagnostics", "feed conversion ratio (fcr) optimization"],
            tooling_skills=["dissolved oxygen (do) meter", "salinometer", "water quality test kit", "compound microscope", "paddlewheel aerators", "refractometer"]
        )
    
        # ==============================================================================
        # 8. PACKAGING TECHNOLOGY & SUSTAINABLE MATERIALS (IIP / B.Tech Packaging)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=packaging_sector,
            role_title="Packaging Development & Sustainable Materials Engineer",
            core_skills=["polymer science", "paperboard technology", "corrugation mechanics", "barrier properties", "material degradation kinetics"],
            methodology_skills=["drop and vibration testing", "transit hazard simulation", "water vapor transmission rate (wvtr) testing", "shelf-life packaging design", "astm/is testing standards"],
            tooling_skills=["box compression tester", "bursting strength tester", "drop tester", "universal testing machine (instron)", "artioscad", "cape pack"]
        )
    
        # ==============================================================================
        # 9. GEOINFORMATICS, CARTOGRAPHY & LIDAR (M.Sc / M.Tech Geoinformatics)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=geoinformatics_sector,
            role_title="Geoinformatics & LiDAR Photogrammetry Specialist",
            core_skills=["photogrammetry", "satellite geodesy", "spatial databases", "point cloud processing", "cartography", "python"],
            methodology_skills=["orthomosaic generation", "digital elevation model (dem) creation", "spatial network analysis", "lidar point cloud classification", "supervised satellite classification"],
            tooling_skills=["arcgis pro", "qgis", "agisoft metashape", "pix4dmapper", "postgis", "google earth engine"]
        )
    
        # ==============================================================================
        # 10. SOUND ENGINEERING & MUSIC PRODUCTION (B.Sc Sound Engineering)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=audio_sector,
            role_title="Audio Recording Engineer & Sound Designer",
            core_skills=["acoustics", "psychoacoustics", "signal routing", "audio frequency spectrum", "microphone polar patterns", "digital audio theory"],
            methodology_skills=["multitrack audio recording", "audio mixing and mastering", "foley and sound design", "surround sound mixing (dolby atmos)", "acoustic measurement"],
            tooling_skills=["pro tools", "logic pro", "ableton live", "izotope ozone", "fabfilter bundle", "digital mixing consoles"]
        )
    
        # ==============================================================================
        # 11. MEDICAL PHYSICS & RADIATION SAFETY (M.Sc Medical Physics / BARC/AERB)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=nuclear_sector,
            role_title="Medical Radiation Physicist & Radiological Safety Officer",
            core_skills=["radiation physics", "nuclear radiation dosimetry", "radiobiology", "radiation shielding", "monte carlo radiation transport", "medical linear accelerators"],
            methodology_skills=["radiotherapy treatment planning", "linear accelerator quality assurance", "aerb radiation compliance", "brachytherapy dosimetry", "radiation survey calibration"],
            tooling_skills=["linear accelerator (linac)", "radiation survey meter", "geiger-muller counter", "treatment planning system (eclipse)", "geant4", "ptw 3d water phantom"]
        )
    
        # ==============================================================================
        # 12. DISASTER RISK REDUCTION & HUMANITARIAN RELIEF (M.Sc / MA Disaster Mgmt)
        # ==============================================================================
    
        JobBenchmark.objects.create(
            sector=disaster_sector,
            role_title="Disaster Risk Reduction & Emergency Response Officer",
            core_skills=["hazard vulnerability risk assessment (hvra)", "geological hazards", "disaster sociology", "public health in emergencies", "climate adaptation"],
            methodology_skills=["emergency operations center (eoc) management", "post-disaster needs assessment (pdna)", "incident command system (ics)", "humanitarian logistics planning", "community evacuation routing"],
            tooling_skills=["qgis", "kobo toolbox", "arcgis survey123", "satellite disaster maps", "sphere handbook standards portal", "vhf radio comms"]
        )
        self.stdout.write(self.style.SUCCESS("Successfully seeded multi-department job benchmarks!"))
