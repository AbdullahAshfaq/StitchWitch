import reflex as rx

style1 = {
        "background-color": "#0C0E11",  # Dark background color
        "color": "#FFFFFF",  # White text color for contrast
        "font-family": "sans-serif",  # Default font
        "margin": 0,  # Remove default margin
        "height": "100vh",  # Full viewport height
        # "display": "flex",
        "overflow": "scroll",

    }


color = "#ab8bff"

def about() -> rx.Component:

    # asyncio.run(analyze_video_async("assets/video/eye_surgery.mp4"))

    return rx.vstack(
        rx.hstack(
            rx.link(rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px", position="absolute"),href="../",),
        ),


        rx.vstack(
            rx.heading(
                    "How we made StitchWitch",
                    font_size="60px",
                    # background_image= "linear-gradient(95deg, #D6D6ED 42.14%, #727280 63.21%)",
                    style={
                        "color": "transparent",
                        "background-image": "linear-gradient(95deg, #D6D6ED 42.14%, #727280 63.21%)",
                        "background-clip": "text",
                        "-webkit-background-clip": "text",  # For WebKit browsers
                        "-webkit-text-fill-color": "transparent",  # Necessary for webkit browsers
                        "line-height": "1.2",  # Increased line height
                        "margin-top": "80px",  # Add padding at the top

                    },
                    height="auto",
            ),
            rx.heading(
                "🥲 The Problem",
                margin_top="70px",
                font_size="40px"
            ),
            
            rx.text("Over 56% of surgical errors are due to human error according to a study by James W. Suliburk, et al.", font_size="18px", margin_top="23px"),
            rx.text("This was followed by other errors such as procedural, communication, and rule violations.", font_size="18px",margin_top="-10px"),

            rx.heading(
                "🌟 Societal Effect",
                margin_top="70px",
                font_size="40px"
            ),

            rx.text("Infection; Sepsis; Permanent scarring; Organ perforation; Amputation;", font_size="18px", margin_top="23px"),
            rx.text("Nerve damage; Oxygen deprivation; Brain or organ damage; Hemorrhage; and Paralysis.", font_size="18px",margin_top="-10px"),

            rx.heading(
                "👨‍⚕️ Our Innovative Solution",
                margin_top="70px",
                font_size="40px"
            ),

            rx.text("Human errors can be avoided - with the help of AI", font_size="20px", margin_top="23px"),
            rx.text("We built an AI surgical assistant", font_size="18px"),
            rx.text("The model is designed to be integrated with smart glasses such as the Ray-Ban Meta and used by surgeons during operations", font_size="18px",margin_top="-10px"),
            rx.text("Provides instant real-time feedback to prevent surgical mishaps", font_size="18px",margin_top="-10px"),

            rx.heading(
                "🖥️ What about existing technology and measures?",
                margin_top="70px",
                font_size="40px"
            ),

            rx.text("How are surgical errors minimized today and why does our solution revolutionize the way this is handled?", font_size="20px", margin_top="23px"),
            rx.text("Checklists, labelling, and other standard protocols - still prone to mistakes", font_size="18px"),
            rx.text("Technology assisted surgery - human controlled", font_size="18px",margin_top="-10px"),
            rx.text("Large surgical team - Lack of medical personnel", font_size="18px",margin_top="-10px"),
            rx.text("Our solution uses generative AI for accurate and quick error detection that may be missed by the human eye.", font_size="18px",margin_top="-10px"),

            rx.heading(
                "🧑‍🔧 Tech Stack",
                margin_top="70px",
                font_size="40px"
            ),

            rx.center(
                rx.image(src="/Tech Stack.png", width="400px", height="auto", margin_top="30px"),
            ),



            rx.heading(
                "🧑🏻‍💻 Our Proud Developers",
                margin_top="70px",
                font_size="40px"
            ),
            rx.center(
                rx.image(src="/Group Photo.jpeg", width="400px", height="auto", margin_top="23px"),
            ),

            rx.text("Chanbin Na, James Choi, Abdulla Ashfaq, Akhil Ramshankar", font_size="18px",margin_top="10px"),
            rx.vstack(
                rx.text("Thanks!"),
                rx.text("Thanks!"),
                rx.text("Thanks!"),
                rx.text("Thanks!"),
                height="200px",
                color="transparent"
            ),
            margin_top="5.5vh",  # Center horizontally
            align_items="center",
            width="100%",
            height="100%", 
            margin_bottom="200px",
            
            
        ),
        width="100%",
        height= "100vh",
        overflow="scroll",
        margin_bottom="200px",
        
        
    )


app = rx.App(style=style1)
