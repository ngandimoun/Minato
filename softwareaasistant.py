
import openai
from openai import OpenAI
import streamlit as st

import os
import shelve


with st.expander("Configuration"):
    # Additional section for Discord and Email
    st.markdown("""
        - [🤑 Get Minato Free Credit](https://discord.gg/pNvPGqWfyX)

    """)
    
    st.markdown("""
<h2>
    <span style="color: #2874A6; font-weight: bold; font-size: 24px;">Please add your Minato Key</span>
</h2>
""", unsafe_allow_html=True)

    api_key = st.text_input("Enter your Minato Key", type="password")
    if api_key:
        st.session_state["api_key"] = api_key
    else:
        st.warning("Please enter your Minato Key.")

st.markdown("""
<h2>
<span style="color: #2874A6; font-weight: bold; font-size: 24px;">Stuck with Software related question?</span>
</h2>
""", unsafe_allow_html=True)



    
USER_AVATAR = "👨🏽‍💻"
BOT_AVATAR = "☯️"


# Define the function to get the OpenAI client
def get_openai_client():
    # Replace 'YOUR_OPENAI_API_KEY' with your actual Minato Key

    openai.api_key = os.getenv('OPENAI_API_KEY')
    return openai



# OpenAI client setup

def get_openai_client():
    """
    Create an OpenAI client using the API key provided by the user.
    """
    api_key = st.session_state.get("api_key")
    if api_key:
        return openai.Client(api_key=api_key)
    else:
        return None
        

client = get_openai_client()


# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])


# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Function to check if the question is related to computer science
def is_computer_science_related(question):
    # List of keywords related to computer science  
    
    cs_keywords = [
    
        # Package Managers and Environments
        "pip", "conda", "anaconda", "virtualenv", "docker-compose", "yarn", "vagrant",

        # Operating Systems and Servers
        "linux", "server administration", "server management", "ubuntu", "debian",
        "centos", "red hat", "fedora", "windows server", "macos server", "apache", "nginx",
        "iis", "load balancing", "cloud services", "virtual machines",

        # Web Development Frameworks and Tools
        "react", "npm", "node.js", "express.js", "vue.js", "angular.js", 
        "bootstrap", "material-ui", "webpack", "babel", "eslint", "sass", "less",

        # DevOps and Continuous Integration/Deployment Tools
        "jenkins", "travis ci", "circleci", "gitlab ci", "aws devops", "azure devops", 
        "kubernetes", "ansible", "puppet", "chef", "terraform", "helm",

        # Database Management Systems and Tools
        "mysql", "postgresql", "sql server", "oracle db", "mongodb", "cassandra", 
        "redis", "elasticsearch", "sqlite", "mariaDB", "dynamoDB",

        # Additional Programming Languages and Technologies
        "groovy", "rust", "kotlin", "scala", "elixir", "erlang", "lua", "r", 
        "haskell", "clojure", "dart", "flutter", "swift", "objective-c",

        # Cloud Platforms and Services
        "aws", "azure", "google cloud platform", "ibm cloud", "oracle cloud", 
        "heroku", "digitalocean", "linode", "cloud"

        # Version Control Systems
        "git", "svn", "mercurial",

        # Frontend Technologies
        "html", "css", "javascript", "typescript", "jquery", "ajax",

        # Basic Topics
        "programming", "algorithm", "data structure", "machine learning", "AI", 
        "database", "networking", "software engineering", "cybersecurity", "data analysis", 
        "cloud computing", "blockchain", "big data", "IoT", "web development", 
        "mobile development", "game development", "virtual reality", "augmented reality", 
        "artificial intelligence", "deep learning", "neural networks", "natural language processing", 
        "computer vision", "operating systems", "distributed systems", "quantum computing", 
        "ethics in technology", "human-computer interaction", "graphics", "UI/UX design", 
        "parallel computing", "cryptography", "computational biology",

        # Programming Languages
        "python", "java", "c++", "c#", "javascript", "ruby", "go", "rust", "swift", 
        "kotlin", "php", "typescript", "scala", "perl", "lua", "matlab", "r",

        # Frameworks
        "django", "flask", "spring", "angular", "react", "vue.js", "node.js", "express.js", 
        "rails", "asp.net", "laravel", "tensorflow", "pytorch", "keras", "pandas", "numpy", 
        "scikit-learn", "unity", "unreal engine",
        # JavaScript Frameworks and Libraries
        "react", "angular", "vue.js", "node.js", "express.js", "next.js", "nuxt.js",
        "ember.js", "meteor.js", "svelte", "backbone.js", "jquery", "rxjs",
        "lodash", "underscore.js", "mobx", "redux", "gatsby.js", "grunt", "gulp",
        "webpack", "babel", "parcel", "typescript", "polymer", "aurelia", "mocha",
        "jasmine", "jest", "enzyme", "chai", "sinon", "cypress", "karma", "protractor",
        "socket.io", "electron", "bootstrap", "material-ui", "tailwind css", "foundation",
        "semantic-ui", "bulma", "sveltekit", "react native", "quasar", "vuetify", "ant design",
        "webpack", "rollup", "snowpack", "esbuild", "graphql", "apollo client", "axios",
        "vuepress", "d3.js", "three.js", "chart.js", "highcharts", "amcharts",
        # C++ Frameworks
        "Qt", "Boost", "SFML", "OpenGL", "Vulkan", "wxWidgets", "MFC", "Unreal Engine",
        "Cinder", "OpenCV", "Poco", "JUCE", "Blink", "ASIO", "OpenFrameworks",
        "Cocos2d-x", "Irrlicht", "Ogre3D", "Armadillo", "Eigen", "GTKmm", "FLTK",
        "TBB", "ACE", "Crypto++", "DirectX", "GLFW", "GLUT", "Libuv", "STL", 
        "Boost.Asio", "libCurl", "SFML", "PCL", "CGAL", "ITK", "VTK", "ROOT",

        # Python Frameworks
        "Django", "Flask", "Pyramid", "FastAPI", "Tornado", "Bottle", "CherryPy",
        "Falcon", "Hug", "web2py", "TurboGears", "Dash", "Sanic", "aiohttp",
        "Twisted", "Ray", "Scrapy", "Selenium", "Tkinter", "PyQt", "Kivy",
        "wxPython", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
        "Plotly", "Bokeh", "TensorFlow", "Keras", "PyTorch", "Scikit-learn",
        "NLTK", "spaCy", "Gensim", "OpenCV-Python", "Pillow", "Streamlit",
        "Jupyter", "IPython", "SymPy", "NetworkX", "Pygame", "PyOpenGL",
        "Pyglet", "Pylons", "Zope", "Plone", "Quart",
        # C# Frameworks
        ".NET Framework", ".NET Core", "ASP.NET", "Entity Framework", "Xamarin",
        "Mono", "Blazor", "Unity", "WPF", "UWP", "WinForms", "NUnit", "XUnit",
        "SignalR", "Hangfire", "Akka.NET", "ServiceStack", "Dapper",

        # C Frameworks
        "GTK", "Glib", "Qt (with C bindings)", "SDL", "Allegro", "Cairo",
        "Pango", "OpenCV (with C bindings)", "FFmpeg", "cURL", "OpenGL (with C bindings)",
        "Pthreads", "Zlib", "Libuv", "WinAPI (for Windows)", "Xlib (for X Window System)",

        # Java Frameworks
        "Spring", "Hibernate", "Apache Struts", "JavaServer Faces (JSF)", "Google Web Toolkit",
        "Vaadin", "Grails", "Play Framework", "Apache Wicket", "Dropwizard",
        "Spark Framework", "Vert.x", "JHipster", "Quarkus", "Micronaut",
        "J2EE", "Eclipse RCP", "Swing", "AWT", "JDBC", "JUnit", "TestNG",
        
        # Cryptocurrencies and Blockchain Technologies
        "Bitcoin", "Ethereum", "Ripple", "Litecoin", "Cardano", "Polkadot",
        "Chainlink", "Binance Coin", "Stellar", "Tether", "Monero", "Dash",
        "Zcash", "Dogecoin", "Shiba Inu",

        # Blockchain Development Languages
        "Solidity", "Vyper", "Rust (for blockchain)", "Go (for blockchain)",
        "JavaScript (for blockchain)", "Python (for blockchain)",

        # Blockchain Frameworks and Tools
        "Truffle", "Hardhat", "Ganache", "Remix", "MetaMask", "Ethers.js",
        "Web3.js", "Brownie (Python)", "OpenZeppelin", "Embark", "Hyperledger Fabric",
        "Corda", "EOSIO", "Tezos", "Algorand", "Chain", "Cosmos SDK", "NEO Blockchain",
        "Avalanche", "Solana",

        # Web3 and NFT Technologies and Frameworks
        "Web3.js", "Ethers.js", "Truffle Suite", "Hardhat", "OpenZeppelin", 
        "Moralis", "Alchemy", "Infura", "MetaMask", "WalletConnect", "Chainlink", 
        "IPFS (InterPlanetary File System)", "Arweave", "Filecoin", "NFT.Storage", 
        "Pinata", "The Graph", "Decentraland SDK", "Ethereum Name Service (ENS)", 
        "Uniswap SDK", "Aave Protocol", "Compound", "MakerDAO", "ERC-721", "ERC-1155",
        "Polygon SDK", "Solana Web3.js", "Flow Blockchain", "Tezos", "WAX Blockchain", 
        "Immutable X", "Rarible SDK", "Nifty Gateway", "OpenSea SDK", "Mintbase", 
        "Zora", "Foundation",

        # Finance Quantitative Frameworks and Libraries
        "QuantLib", "Zipline", "QuantConnect", "Backtrader", "PyAlgoTrade",
        "bt", "ffn - Financial Functions for Python", "QSTrader", "Quantopian",
        "FinRL", "Pandas TA", "TA-Lib", "pyfolio", "Riskfolio-Lib",
        "Alpha Vantage", "Alpaca", "Interactive Brokers API", "MetaTrader 5",
        "OANDA API", "Quantmod", "NinjaTrader", "Thinkorswim", "TradingView",
        "Bloomberg Terminal", "Refinitiv Eikon", "SAS", "MATLAB Financial Toolbox",
        "MQL4", "MQL5", "JQuantLib", "RQuantLib", "TensorFlow Finance",
        "KDB+/q", "Esper", "Rmetrics", "FinPricing", "DERISCOPE",

        # Large Language Models and Frameworks
        "OpenAI LLaMA (Large Language Model API)", "Duet", "GPT-3", "GPT-4", 
        "BERT", "RoBERTa", "T5 (Text-to-Text Transfer Transformer)", "XLNet", 
        "ELECTRA", "ALBERT", "OpenAI Codex", "Jurassic-1", "Transformer models",
        "DeepMind WaveNet", "Fairseq", "Hugging Face Transformers", "spaCy",
        "AllenNLP", "TensorFlow Text", "PyTorch-NLP", "Stanford NLP", "NLTK",
        "ChatGPT", "CTRL", "DALL-E", "CLIP", "MuZero", "DeBERTa", "Megatron-LM",
        "UL2 (Understanding Language through Language Models)", "FLAN (Focused Language model ANnotation)",
        # AI Frameworks
        "TensorFlow", "Keras", "PyTorch", "Scikit-learn", "Caffe", "Apache MXNet",
        "Microsoft Cognitive Toolkit (CNTK)", "Theano", "Fast.ai", "OpenCV AI",
        "PaddlePaddle", "DL4J (DeepLearning4j)", "H2O", "ONNX (Open Neural Network Exchange)", 
        "LightGBM", "XGBoost", "CatBoost", "Accord.NET", "Torch", "Chainer", 
        "Deeplearning4j", "Eclipse Deeplearning4j", "YOLO (You Only Look Once)", 
        "Gensim", "spaCy", "NLTK", "AllenNLP", "Prophet", "Starspace", "Fairseq",
        "Hugging Face Transformers", "JAX", "Ray", "Dask", "RAPIDS", "MLflow",
        "AutoML tools (like AutoKeras, Auto-Sklearn)", "EasyOCR", "Tesseract OCR",

        # Hardware and Hardware Frameworks
        "Arduino", "Raspberry Pi", "BeagleBone", "ESP8266", "ESP32",
        "FPGA (Field-Programmable Gate Array)", "ARM Cortex Microcontrollers",
        "NVIDIA Jetson", "Intel Edison", "STM32", "Micro:bit", "Adafruit",
        "Robot Operating System (ROS)", "OpenCV AI Kit", "Maker Pi", 
        "Xilinx", "Altera", "LabVIEW", "MATLAB Simulink", "Eagle PCB", "KiCad",
        "Altium Designer", "Proteus", "VHDL", "Verilog", "SystemVerilog", 
        "CircuitPython", "PlatformIO", "Simulink", "Vivado Design Suite", 
        "Intel FPGA SDK", "Cadence OrCAD", "Autodesk Fusion 360", "ANSYS",
        "SolidWorks", "PTC Creo", "CATIA", "3D Printing Technologies",
        "IoT Platforms (like AWS IoT, Google Cloud IoT, Microsoft Azure IoT)",
        # Cybersecurity Frameworks
        "NIST Cybersecurity Framework", "ISO/IEC 27001", "CIS Controls", 
        "COBIT (Control Objectives for Information and Related Technologies)",
        "PCI DSS (Payment Card Industry Data Security Standard)", "SOC 2",
        "HITRUST CSF (Health Information Trust Alliance Common Security Framework)",
        "FISMA (Federal Information Security Management Act)", "GDPR (General Data Protection Regulation)",
        "HIPAA (Health Insurance Portability and Accountability Act)", "OWASP (Open Web Application Security Project)",
        "SANS Critical Security Controls", "MITRE ATT&CK Framework", "FAIR (Factor Analysis of Information Risk)",
        "ECSA (EC-Council Certified Security Analyst)", "IETF (Internet Engineering Task Force) Security Guidelines",
        "Cloud Security Alliance (CSA) Framework", "ENISA (European Union Agency for Cybersecurity)",
        "ITIL (Information Technology Infrastructure Library)", "CCPA (California Consumer Privacy Act)",
        "CMMC (Cybersecurity Maturity Model Certification)", "OSSTMM (Open Source Security Testing Methodology Manual)",
        "PTES (Penetration Testing Execution Standard)", "Red Team Framework", "Blue Team Framework",
        "ISO/IEC 15408 (Common Criteria)",  
        # UX/UI Frameworks
        "Bootstrap", "Material-UI", "Ant Design", "Semantic UI", "Tailwind CSS",
        "Foundation", "Figma", "Sketch", "Adobe XD", "InVision Studio",
        "Axure RP", "Balsamiq", "Marvel", "Proto.io", "UXPin",
        "Wireframe.cc", "Mockplus", "Origami Studio", "Framer", "Zeplin",

        # Front-End Frameworks
        "React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js",
        "Ember.js", "Backbone.js", "Polymer", "Aurelia", "Alpine.js",
        "Gatsby", "Gridsome", "Quasar", "Vuetify", "React Native",
        "Flutter Web", "Ionic", "Electron", "Capacitor", "Cordova",
        
        # Backend Frameworks
        "Django", "Flask", "Express.js", "Spring Boot", "Ruby on Rails",
        "Laravel", "ASP.NET Core", "Node.js", "Phoenix (Elixir)", "FastAPI",
        "Koa", "Meteor", "Sinatra", "Play Framework", "Hapi.js",
        "NestJS", "Strapi", "LoopBack", "Moleculer", "AdonisJS",
        "FeathersJS", "Sails.js", "Akka (Scala)", "Vert.x (Java)", "Quarkus (Java)",
        "Micronaut (Java)", "Falcon (Python)", "Bottle (Python)", "CherryPy (Python)",
        "Tornado (Python)", "Sanic (Python)", "Gin (Go)", "Echo (Go)", "Buffalo (Go)",
        "Revel (Go)", "Fiber (Go)", "Helidon (Java)", "Dropwizard (Java)",

        # Serverless Framework and related keywords
        "Serverless Framework", "AWS Lambda", "Azure Functions", "Google Cloud Functions",
        "IBM Cloud Functions", "Firebase Functions", "Netlify Functions", "Vercel Functions",
        "OpenWhisk", "Cloudflare Workers", "Tencent Cloud Functions", "Alibaba Cloud Function Compute",
        "Serverless Framework Offline", "Serverless Framework plugins",

        # AWS Technologies and Services
        "Amazon S3", "Amazon EC2", "Amazon RDS", "Amazon DynamoDB", "Amazon Redshift",
        "Amazon Aurora", "Amazon ECS", "Amazon EKS", "Amazon Elastic Beanstalk", "Amazon SNS",
        "Amazon SQS", "Amazon API Gateway", "Amazon CloudFront", "Amazon Route 53", "Amazon VPC",
        "Amazon Lambda@Edge", "Amazon CloudWatch", "Amazon CloudFormation", "AWS Elastic Load Balancing",
        "AWS Identity and Access Management (IAM)", "AWS Elastic Beanstalk", "AWS Elasticache",
        "AWS Fargate", "AWS Glue", "AWS Kinesis", "AWS Step Functions", "Amazon Polly",
        "Amazon Comprehend", "Amazon Lex", "Amazon Translate", "Amazon Rekognition", "AWS Lambda Layers",
        "AWS App Runner", "AWS App Mesh", "AWS Lambda Container Image Support", "AWS X-Ray",

        # Google Cloud Technologies and Services
        "Google Cloud Storage", "Google Compute Engine", "Google Cloud SQL", "Google Cloud Bigtable",
        "Google Cloud Firestore", "Google Kubernetes Engine (GKE)", "Google App Engine", "Google Cloud Pub/Sub",
        "Google Cloud Functions", "Google Cloud Endpoints", "Google Cloud CDN", "Google Cloud DNS",
        "Google Cloud VPC", "Google Cloud Functions for Firebase", "Google Cloud Run",
        "Google Cloud Dataflow", "Google Cloud Dataprep", "Google Cloud Pub/Sub Lite",
        "Google Cloud Speech-to-Text", "Google Cloud Natural Language API", "Google Cloud Translation",
        "Google Cloud Vision AI", "Google Cloud AI Platform", "Google Cloud Functions Framework",

        # Azure Technologies and Services
        "Azure Blob Storage", "Azure Virtual Machines", "Azure SQL Database", "Azure Cosmos DB",
        "Azure Kubernetes Service (AKS)", "Azure Functions", "Azure App Service", "Azure Logic Apps",
        "Azure Event Grid", "Azure Event Hubs", "Azure API Management", "Azure Content Delivery Network (CDN)",
        "Azure DNS", "Azure Virtual Network (VNet)", "Azure Key Vault", "Azure AI and Machine Learning",
        "Azure Cognitive Services", "Azure Functions Premium Plan", "Azure Service Bus", "Azure IoT Hub",
        "Azure Stream Analytics", "Azure Databricks", "Azure Synapse Analytics", "Azure Data Factory",
        "Azure DevOps", "Azure Functions Proxies", "Azure Logic Apps Standard",

        # NVIDIA Technologies and Products
        "NVIDIA GPU", "NVIDIA CUDA", "NVIDIA Deep Learning AI", "NVIDIA TensorRT",
        "NVIDIA GeForce", "NVIDIA Quadro", "NVIDIA Tesla", "NVIDIA DGX", "NVIDIA Jetson",
        "NVIDIA A100", "NVIDIA RTX", "NVIDIA NVLink", "NVIDIA GPU Cloud (NGC)",
        "NVIDIA CUDA Toolkit", "NVIDIA cuDNN", "NVIDIA G-Sync", "NVIDIA GRID",

        # Backendless Technologies and Frameworks
        "Backendless", "Firebase", "Parse", "Kuzzle", "Kinvey", "Supabase", "DreamFactory",
        "AWS Amplify", "Hasura", "Feathers", "LoopBack (StrongLoop)", "Strapi", "Appwrite",
           
        # Libraries and Modules
        "jquery", "bootstrap", "matplotlib", "seaborn", "scipy", "requests", "beautifulsoup", 
        "pillow", "opencv", "gtk", "wxpython", "flask-restful", "d3.js", "three.js"
        # More Programming Languages
        "erlang", "haskell", "clojure", "elm", "f#", "fortran", "cobol", "lisp",

        # Advanced and Niche Topics
        "reinforcement learning", "generative adversarial networks", "gans", 
        "ethical hacking", "penetration testing", "digital forensics", "nosql", 
        "mongodb", "cassandra",

        # Emerging Technologies
        "edge computing", "serverless architecture", "sustainable computing", 
        "green technology",

        # Additional Frameworks and Libraries
        "flutter", "xamarin", "next.js", "svelte", "electron", "flask-sqlalchemy", 
        "pygame",

        # Development Tools and Environments
        "intellij idea", "pycharm", "eclipse", "git", "github", "gitlab", 
        "docker", "kubernetes",

        # Software Development Methodologies
        "agile", "scrum", "kanban", "devops", "ci/cd", "continuous integration", 
        "continuous deployment",

        # Hardware and Infrastructure
        "hardware basics", "processors", "gpus", "aws", "azure", "google cloud platform",

        # Standards and Protocols
        "tcp/ip", "http/https", "ftp", "json", "xml",

        # Mathematical Foundations
        "discrete mathematics", "statistics", "calculus", "graph algorithms", 
        "dynamic programming",

        # Domain-specific Applications
        "bioinformatics", "geoinformatics", "financial technology", "fintech"
    ]

    
    
    
    
    
    return any(keyword.lower() in question.lower() for keyword in cs_keywords)

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.expander("Chat History"):
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])
  

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface with topic detection
if prompt := st.chat_input("Ask Minato, your Software Questions??"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    if is_computer_science_related(prompt):
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state["messages"],
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            non_cs_response = "Sorry, this is not a computer science related question. Please ask something related to computer science."
            st.markdown(non_cs_response)
            st.session_state.messages.append({"role": "assistant", "content": non_cs_response})


# Save chat history after each interaction
#save_chat_history(st.session_state.messages)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}

            
            

            """
st.markdown(hide_st_style, unsafe_allow_html=True)

