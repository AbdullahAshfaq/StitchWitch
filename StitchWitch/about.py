import reflex as rx

style = {
        "background-color": "#0C0E11",  # Dark background color
        "color": "#FFFFFF",  # White text color for contrast
        "font-family": "sans-serif",  # Default font
        "margin": 0,  # Remove default margin
        "height": "100vh",  # Full viewport height
        # "display": "flex",
        "overflow": "hidden",
    }
color = "#ab8bff"

def about() -> rx.Component:

    # asyncio.run(analyze_video_async("assets/video/eye_surgery.mp4"))

    return rx.vstack(
        rx.hstack(
            rx.link(rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px"),href="../",),
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
                        "margin-top": "-50px",  # Add padding at the top
                    },
                    height="auto",
            ),
            rx.heading(
                "💡 Project Idea",
                margin_top="20px",
                font_size="30px"
            ),
            rx.text(
                "According to HSS, 22% of the medical problems are from procedure surgery"
                "and we thought that AI could help to solve this problem.",
                font_size="18px"
            ),
            rx.text(
                "and we thought that AI could help to solve this problem.",
                font_size="18px"
            ),
            rx.heading(
                "Our Proud Developers",
                margin_top="20px",
                font_size="30px"
            ),
            rx.center(
                rx.image(src="/Group Photo.jpeg", width="400px", height="auto", margin_top="23px"),
            ),
            rx.vstack(
                
                 
            ),
            margin_top="5.5vh",  # Center horizontally
            align_items="center",
            width="100%",
            height="100%", 
        ),
        width="100%"
        
        
    )


app = rx.App(style=style)
