import streamlit as st
from models import content_extractor, instruction_generator, reference_extractor
from core.template_manager import TemplateManager
from core.ppt_generator import PPTGenerator
from config import Config

st.title("AI-powered PPT Generator")

uploaded_file = st.file_uploader("Upload your poster PDF", type=["pdf"])
reference_file = st.file_uploader("Upload a reference slide (PPTX) for AI to adapt layouts", type=["pptx"])

if uploaded_file:
    with open("input_poster.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    reference_instruction = None
    if reference_file:
        with open("reference_slide.pptx", "wb") as ref:
            ref.write(reference_file.getbuffer())
        reference_instruction = reference_extractor.extract_reference_structure("reference_slide.pptx")

    st.success("Files uploaded. Generating presentation...")

    try:
        poster_text = content_extractor.extract_text_from_pdf("input_poster.pdf")
        presentation_plan = instruction_generator.generate_presentation_plan(
            poster_text, reference_instruction=reference_instruction
        )
        template_manager = TemplateManager(template_dir=Config.TEMPLATE_DIR)
        ppt_generator = PPTGenerator(template_manager)

        for slide in presentation_plan.slides:
            ppt_generator.populate_slide(slide)
        ppt_generator.save(Config.OUTPUT_PATH)

        with open(Config.OUTPUT_PATH, "rb") as f:
            st.download_button("Download Presentation", f, file_name="generated_ppt.pptx")

    except Exception as e:
        st.error(f"Error: {str(e)}")
