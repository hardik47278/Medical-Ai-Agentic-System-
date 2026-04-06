ANALYSIS_PROMPT = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the patient's medical image and structure your response as follows:

### 1. Image Type & Region
- Specify imaging modality (X-ray/MRI/CT/Ultrasound/etc.)
- Identify the patient's anatomical region and positioning
- Comment on image quality and technical adequacy

### 2. Key Findings
- List primary observations systematically
- Note any abnormalities in the patient's imaging with precise descriptions
- Include measurements and densities where relevant
- Describe location, size, shape, and characteristics
- Rate severity: Normal/Mild/Moderate/Severe

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level
- List differential diagnoses in order of likelihood
- Support each diagnosis with observed evidence from the patient's imaging
- Note any critical or urgent findings

### 4. Patient-Friendly Explanation
- Explain the findings in simple, clear language that the patient can understand
- Avoid medical jargon or provide clear definitions
- Include visual analogies if helpful
- Address common patient concerns related to these findings

### 5. Research Context
- Find recent medical literature about similar cases
- Search for standard treatment protocols
- Research any relevant technological advances
- Include 2-3 key references to support your analysis

Format your response using clear markdown headers and bullet points. Be concise yet thorough.
"""

# System message for image analysis
SYSTEM_MESSAGE = """You are a medical imaging expert. When analyzing medical images, 
be thorough and detailed. If the image is unclear or not a medical image, explain 
this respectfully but still try to extract any relevant information."""

# Literature search prompt template
def get_literature_search_prompt(query):
    return f"""
    For the medical condition/finding: {query}
    
    Please provide:
    
    1. Recent medical literature (2-3 papers) about this condition
    2. Standard treatment protocols
    3. Recent technological advances in diagnosis or treatment
    
    Format as markdown with proper citations and, if available, URLs to medical resources.
    """

# System message for literature search
LITERATURE_SYSTEM_MESSAGE = "You are a medical research assistant with expertise in finding relevant medical literature and resources."

# Fallback response when image analysis fails
FALLBACK_RESPONSE = """
## Medical Image Analysis

I'm unable to fully analyze the provided image. This could be due to several factors:

### Possible Reasons
- The image may not be a standard medical imaging format
- The image quality or resolution may be insufficient for detailed analysis
- The image may be missing technical metadata needed for proper interpretation
- The image may be of a type that requires specialized analysis

### Recommendations for Further Discussion
1. **Image Specifics**: What type of imaging study is this? (X-ray, MRI, CT, Ultrasound)
2. **Anatomical Region**: Which part of the body is being examined?
3. **Clinical Context**: What symptoms or condition prompted this imaging study?
4. **Previous Imaging**: Are there any prior studies available for comparison?
5. **Radiologist's Report**: If you have a professional report for this image, specific questions about terminology or findings in that report can be discussed

### Next Steps
- Consider consulting with a healthcare professional for proper interpretation
- Ensure the image is in a standard medical format (DICOM is preferred)
- Provide additional clinical context for more meaningful discussion

Remember that AI analysis should always be confirmed by qualified medical professionals.
"""

# Fallback references when image analysis fails
FALLBACK_REFERENCES = "For assistance with medical imaging interpretation, consider resources like RadiologyInfo.org, which provides patient-friendly explanations of various imaging studies and findings."

# Error response when an exception occurs
ERROR_RESPONSE = """
## Analysis Error

I encountered an error while analyzing this image. This could be due to:

- Technical issues with the image format or processing
- API communication problems
- Image content that doesn't match expected medical imaging patterns

### Suggestions for Better Results

1. **Try a different image format**: Convert to JPEG or PNG if not already
2. **Check image clarity**: Ensure the image is clear and properly oriented
3. **Verify image type**: Confirm this is a standard medical image (X-ray, MRI, CT, etc.)
4. **Provide context**: If you retry, adding information about what the image shows can help

If you're trying to discuss a specific medical condition or imaging finding instead, please let me know and I can provide information without requiring an image.
"""

# Error references when an exception occurs
ERROR_REFERENCES = "For general medical imaging information, resources like RadiologyInfo.org can be helpful."





