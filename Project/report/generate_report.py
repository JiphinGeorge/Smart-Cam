import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_placeholder(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(f"\n[ PLACEHOLDER: {text} ]\n(Please insert your screenshot here)\n")
    run.font.color.rgb = RGBColor(255, 0, 0)
    run.font.bold = True
    run.font.size = Pt(12)

def generate_docx():
    doc = Document()

    title = doc.add_heading('PROJECT REPORT', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph('Title: Smart Cam Image Classifier Using Deep Learning & Flask')
    doc.add_paragraph('Course/Internship: AIML Internship Project')
    doc.add_paragraph('Development Stack: Python 3.12, Flask, tf_keras, TensorFlow, Pillow, NumPy, Vanilla JS, Tailwind CSS')

    doc.add_heading('1. Abstract & Introduction', level=1)
    doc.add_paragraph(
        "This project implements an end-to-end Computer Vision application called the Smart Cam Classifier. "
        "By leveraging artificial intelligence and transfer learning, the application allows users to upload captured digital images "
        "to a web interface and instantly receive automated classification predictions with high-fidelity UI feedback."
    )
    doc.add_paragraph(
        "The core predictive engine uses a deep convolutional neural network (MobileNet architecture) trained on custom visual data formats "
        "via Google Teachable Machine. The application architecture resolves major industry challenges regarding "
        "backward compatibility between modern programming environments (Python 3.12 / TensorFlow 2.16+) and "
        "legacy model formats (.h5) by implementing a dynamic execution pipeline using the tf_keras bridge."
    )

    doc.add_heading('2. System Architecture & Core Preprocessing Pipeline', level=1)
    doc.add_paragraph(
        "Deep learning image classifiers demand absolute mathematical precision regarding input data shapes. "
        "The pipeline below illustrates how the Smart Cam backend handles incoming images to prevent matrix dimension misalignment crashes:"
    )
    p1 = doc.add_paragraph()
    p1.add_run("Spatial Cropping & Resizing: ").bold = True
    p1.add_run("Forces varying camera image sizes into a square aspect ratio of exactly 224x224 pixels, the default input shape expected by the MobileNet base layer.")
    
    p2 = doc.add_paragraph()
    p2.add_run("Channel Restructuring: ").bold = True
    p2.add_run("Automatically identifies and repairs input anomalies. If a user uploads a grayscale image, it stacks the arrays to build a 3-channel RGB image. If a PNG with transparency is uploaded, it strips the 4th alpha channel away, ensuring a strict depth of 3 channels.")

    p3 = doc.add_paragraph()
    p3.add_run("Mathematical Pixel Normalization: ").bold = True
    p3.add_run("Converts raw pixel integers from the standard [0, 255] range down into high-speed floating-point coordinates between [-1.0, 1.0] using the tensor formula:")
    
    doc.add_paragraph("Normalized Array = (Image Array / 127.5) - 1.0", style='Intense Quote')

    p4 = doc.add_paragraph()
    p4.add_run("Batch Expansion: ").bold = True
    p4.add_run("Expands the array shape into a 4D tensor matching the network's input signature: (1, 224, 224, 3).")

    doc.add_heading('3. Step-by-Step Implementation & Interface Milestones', level=1)
    
    doc.add_heading('Stage 1: Terminal Directory Navigation', level=2)
    doc.add_paragraph(
        "Navigating to the project workspace using the command line requires targeting the correct drive partition and directory."
    )
    doc.add_paragraph('cd /d "C:\\Users\\asus\\Downloads\\Project"', style='Intense Quote')
    if os.path.exists('screenshot_1.jpg'):
        doc.add_picture('screenshot_1.jpg', width=Inches(6))
    else:
        add_placeholder(doc, "Screenshot 1: Terminal showing navigation")

    doc.add_heading('Stage 2: Flask Local Network Server Boot Sequence', level=2)
    doc.add_paragraph(
        "Executing the local server command fires up the application engine, mounting the web framework structures, "
        "loading the machine learning model into memory (cached once to prevent reloading latency), and initializing access loops through port 5000."
    )
    doc.add_paragraph('python app.py', style='Intense Quote')
    if os.path.exists('screenshot_2.jpg'):
        doc.add_picture('screenshot_2.jpg', width=Inches(6))
    else:
        add_placeholder(doc, "Screenshot 2: Terminal showing Flask app boot")

    doc.add_heading('Stage 3: Base Interface Initialization', level=2)
    doc.add_paragraph(
        "When an engineer accesses the local server address (localhost:5000), the web interface serves a custom Neo-Brutalist HTML/CSS UI. "
        "This boots up a secure drag-and-drop file uploader restricted to image file buffers."
    )
    if os.path.exists('screenshot_3.jpg'):
        doc.add_picture('screenshot_3.jpg', width=Inches(4.5))
    else:
        add_placeholder(doc, "Screenshot 3: Empty web browser running the application")

    doc.add_heading('Stage 4: User Image Selection & Matrix Ingestion', level=2)
    doc.add_paragraph(
        "Once an image drops into the active uploader asset, the browser displays a localized preview image using the FileReader API "
        "while silently submitting the file data via AJAX POST request to the backend /predict endpoint."
    )
    if os.path.exists('screenshot_4.png'):
        doc.add_picture('screenshot_4.png', width=Inches(4.5))
    else:
        add_placeholder(doc, "Screenshot 4: Apple Image provided in Chat")

    doc.add_heading('Stage 5: Inference Matrix Resolution & Final Class Prediction', level=2)
    doc.add_paragraph(
        "The backend passes the sanitized array data into the tf_keras inference engine. Forward-pass matrix calculations evaluate the vectors "
        "and return a JSON payload detailing the predicted class and confidence thresholds. The JavaScript frontend dynamically parses this payload, "
        "triggering real-time CSS color shifts (Green/Blue/Orange based on confidence) and stretching progress bars for visual telemetry."
    )
    doc.add_paragraph("prediction = model.predict(data)\nclass_confidence = float(prediction[0][pred_index]) * 100", style='Intense Quote')
    if os.path.exists('Screenshot_5.png'):
        doc.add_picture('Screenshot_5.png', width=Inches(4.5))
    else:
        add_placeholder(doc, "Screenshot 5: Banana Image provided in Chat")

    doc.add_heading('4. Detailed Technical Analysis', level=1)
    
    doc.add_heading('Model Architecture Analysis', level=2)
    doc.add_paragraph(
        "The underlying deep learning model relies on transfer learning through a pre-trained MobileNet neural network. By freezing the early "
        "feature-extraction layers (which detect generic shapes, edges, and textures) and retraining the final dense classification layers "
        "on the Apple and Banana datasets, the model converges rapidly with minimal computational overhead. This allows real-time inference on CPU hardware."
    )

    doc.add_heading('Confidence Analysis Logic', level=2)
    doc.add_paragraph(
        "The output layer of the neural network applies a Softmax activation function, squashing raw logits into a normalized probability distribution "
        "summing to 100%. If out-of-distribution data is supplied (e.g., an image of a shoe), the model is mathematically forced to assign it to one of the trained classes. "
        "To mitigate ambiguity, a custom threshold logic engine was deployed in the API:"
    )
    c_logic = doc.add_paragraph()
    c_logic.add_run(">= 90%: ").bold = True
    c_logic.add_run("High Confidence. Card turns green. Generates positive natural language insights.\n")
    c_logic.add_run(">= 70%: ").bold = True
    c_logic.add_run("Moderate Confidence. Card turns blue. Generates cautious natural language insights.\n")
    c_logic.add_run("< 70%: ").bold = True
    c_logic.add_run("Low/Ambiguous Confidence. Card turns orange. Warns user to provide a clearer image.")

    doc.add_heading('5. Engineering Challenges & Troubleshooting Log', level=1)
    doc.add_paragraph(
        "During the implementation phase, several critical runtime exceptions were encountered and systematically debugged:"
    )
    c1 = doc.add_paragraph()
    c1.add_run("Drive Switch Terminal Error: ").bold = True
    c1.add_run("Using a raw cd command without the /d parameter in CMD failed to switch drive partitions. This was solved by utilizing the /d disk command patch (e.g. cd /d).")
    
    c2 = doc.add_paragraph()
    c2.add_run("Keras 3 Layer Deserialization Mismatch: ").bold = True
    c2.add_run("Modern TensorFlow 2.16+ environments reject older model configurations exported by Teachable Machine due to DepthwiseConv2D layer serialization changes. "
               "This was permanently solved by installing and explicitly importing tf_keras to force the software environment to read the .h5 files using stable legacy parsers.")
    
    c3 = doc.add_paragraph()
    c3.add_run("Dynamic Label Parsing: ").bold = True
    c3.add_run("Hardcoding labels scales poorly. An autonomous Python parsing loop was written to strip the '0 ' and '1 ' prefixes from labels.txt, ensuring the UI adapts if the model is retrained on new objects.")

    doc.add_heading('6. Future Scope', level=1)
    doc.add_paragraph(
        "While the current Smart Cam iteration is highly functional, future expansions could include:"
    )
    f_list = doc.add_paragraph()
    f_list.add_run("1. Background/Anomaly Class Training: ").bold = True
    f_list.add_run("Adding an 'Unknown' class in Teachable Machine containing diverse random objects to prevent out-of-distribution forced predictions.\n")
    f_list.add_run("2. History Database: ").bold = True
    f_list.add_run("Connecting the Flask backend to a SQLite database to log past predictions and images.\n")
    f_list.add_run("3. Mobile Application: ").bold = True
    f_list.add_run("Exporting the tf_keras model to TensorFlow Lite (.tflite) for edge-deployment on Android and iOS devices without requiring an active server connection.")

    doc.add_heading('7. Conclusion/Inference', level=1)
    doc.add_paragraph(
        "The Smart Cam Classifier effectively demonstrates the application of deep learning for automated image classification. "
        "By migrating from a rigid Streamlit prototype to a customized Flask backend with a tailored frontend design system, the application achieves "
        "greater control over network architecture, asynchronous DOM manipulation, and backward compatibility. This project successfully bridges the gap between modern deployment environments, robust ML engineering, and premium UX/UI design."
    )

    doc.save('Project_Report_Updated.docx')

if __name__ == "__main__":
    print("Generating docx...")
    generate_docx()
    print("Report generation complete: Project_Report.docx")
