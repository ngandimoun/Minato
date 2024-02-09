import streamlit as st

def load_app(app_name):
    with open(app_name, encoding='utf-8') as app_file:
        exec(app_file.read(), globals())

def show_about_us():
    st.markdown(
        """
        <style>
        .highlight {
            color: #0b5ed7; /* Change this color as needed */
        }
        .important {
            color: #d63384; /* Change this color as needed */
        }
        </style>
        
        ---
        
        🚀 <span class="highlight">**Meet Minato**</span>: Your Ultimate AI Sidekick in Computer Science! 🌐
        
        - [🤑 <span class="highlight">Get Minato Free Credit</span>](https://discord.gg/pNvPGqWfyX)

        - [💬 <span class="highlight">Have Questions About Minato? Ask Here</span>](https://discord.gg/pNvPGqWfyX)      
        ---
        
        **🧠 <span class="important">Empowering Coders, One Line at a Time!</span>**
        
        At Minato, we believe in transforming the way you interact with the world of coding. Whether you're battling through tricky coding questions, delving into complex computer science concepts, or prepping for that all-important technical interview, **Minato's got your back**. With our revolutionary AI-driven approach, we turn every coding challenge into a learning opportunity and every technical interview into a walk in the park.
        
        **💡 <span class="important">A Personal Mentor in Your Pocket</span>**
        
        Minato isn't just another software tool - it's your personal mentor. We're here to guide you through the labyrinth of computer science intricacies, offering accurate solutions and easy-to-understand explanations. **Turning technical interviews into a breeze**, Minato is your secret weapon to becoming a **coding maestro**.
        
        **🌟 <span class="important">Conquer the Coding Universe</span>**
        
        Dive into a world of diverse software challenges with Minato. Our platform is designed to sharpen your skills across various topics and programming languages. **🐍 Python problems?** No worries! We've got the perfect drills to boost your skills and prepare you for those intense technical interviews. With Minato, every coding session is a step towards interview success.
        
        **🌍 <span class="important">Real-World Cases for Real-World Experience</span>**
        
        Get ready to immerse yourself in existing codebases and open-source projects, simulating the challenges faced by major tech giants like Google and Facebook. Minato ensures you're not just coding; you're evolving into a tech ninja, adept at querying, modifying, and enhancing functionalities with finesse.
        
        **🎯 <span class="important">What Sets Minato Apart?</span>**
        
        Minato is not just a tool; it's a companion. Designed by developers for developers, and future coding rockstars, Minato is here to make your coding journey not just informative but **thrilling, engaging, and downright awesome**.
        
        🔥 **<span class="highlight">Minato Boasts Four Key Features:</span>**
        
        1. **🔍 Software Assistant**: Providing answers to a wide array of computer science questions.
        2. **🐍 Python Problems**: Focused on pivotal Python problems, crucial for acing technical interviews and skill enhancement.
        3. **💻 Real-world Cases**: Immerse in real codebases and open-source projects for an authentic experience, priming you for the tech world.
        
        Ready to level up your coding game with Minato? Let's embark on this <span class="highlight">exciting coding adventure</span> together!
        
        ---
        
        **🚀 <span class="highlight">Join Us and Become a Coding Legend with Minato!</span>** 🌟
        
        - [🆘 <span class="highlight">Need Help? Our 24/7 Support Team is Ready to Assist</span>](https://discord.gg/pNvPGqWfyX)
        ---
        """,
        unsafe_allow_html=True
    )


# Custom CSS to inject for styling the sidebar and adding space between radio buttons
sidebar_style = """
    <style>
    .sidebar .sidebar-content {
        background-color: #f1f3f6;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .sidebar .sidebar-content h1 {
        color: #0b5ed7;
    }
    .sidebar .sidebar-content label {
        color: #6c757d;
        font-weight: bold;
    }
    /* Custom CSS for adding space between radio buttons */
    .sidebar .sidebar-content div.row-widget.stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 50px;  /* Adjust the gap size as needed */
    }
    </style>
    """
    

st.set_page_config(layout="wide")

# Injecting the style
st.markdown(sidebar_style, unsafe_allow_html=True)



# Google Tag Manager code
gtm_code = """
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-N4W5J4DN');</script>
<!-- End Google Tag Manager -->

<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-N4W5J4DN"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""

# Injecting Google Tag Manager code into the HTML head
st.markdown(gtm_code, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title('🧭 Navigation')
options = st.sidebar.radio('Go to', ['🏠 Home', '🛠️ Software Assistant', '🐍 Python Problems', '🌐 Real World Case'])

st.sidebar.write("Close the navigation sidebar for a better viewing experience.")


if options == '🏠 Home':
    show_about_us()

elif options == '🛠️ Software Assistant':
    load_app('softwareaasistant.py')

elif options == '🐍 Python Problems':
    load_app('pythonGene.py')

elif options == '🌐 Real World Case':
    load_app('realWordUse.py')



