from appJar import gui
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
import pdfplumber

# Define all the functions needed to process the files

def split_pages(input_file, out_file):
    pdf_file = open(input_file, "rb")
    pdf_reader = PdfFileReader(pdf_file)
    plumb = pdfplumber.open(input_file)
    name_ords = app.getEntry("Filename_Coords")
    pageNumbers = pdf_reader.getNumPages()
    coord_array = name_ords.split(', ')
    if len(name_ords) == 0:
        x0 = 50.500
        top = 142.333
        x1 = 300.000
        bottom = 160.677
    else:
        x0 = float(coord_array[0])
        top = float(coord_array[1])
        x1 = float(coord_array[2])
        bottom = float(coord_array[3])
    bounding_box = (x0, top, x1, bottom)

    for i in range (pageNumbers):
        page = plumb.pages[i]
        words = page.extract_words()
        pcrop = plumb.pages[i]
        pcrop = pcrop.within_bbox(bounding_box)
        name = pcrop.extract_text()
        name = name.strip()
        
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(i))
        output_file = open(str(out_file) + "\\" + name + ".pdf", "wb")
        pdf_writer.write(output_file)
        output_file.close()

    pdf_file.close()

def validate_inputs(input_file, output_dir):
    """ Verify that the input values provided by the user are valid

    Args:
        input_file: The source PDF file
        output_dir: Directory to store the completed file
        range: File A string containing a range of pages to copy: 1-3,4
        file_name: Output name for the resulting PDF

    Returns:
        True if error and False otherwise
        List of error messages
    """
    errors = False
    error_msgs = []

    # Make sure a PDF is selected
    if Path(input_file).suffix.upper() != ".PDF":
        errors = True
        error_msgs.append("Please select a PDF input file")

    # Check for a valid directory
    if not(Path(output_dir)).exists():
        errors = True
        error_msgs.append("Please Select a valid output directory")

    return(errors, error_msgs)

def press(button):
    """ Process a button press

    Args:
        button: The name of the button. Either Process of Quit
    """
    if button == "Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        errors, error_msg = validate_inputs(src_file, dest_dir)
        if errors:
            app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
            split_pages(src_file, Path(dest_dir))
    else:
        app.stop()


# Create the GUI Window
app = gui("PDF Split & Rename", useTtk=True)
app.setTtkTheme("default")
# Uncomment below to see all available themes
# print(app.getTtkThemes())
app.setSize(500, 200)

# Add the interactive components
app.addLabel("Choose Source PDF File")
app.addFileEntry("Input_File")

app.addLabel("Select Output Directory")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Input target filename co-ordinates - eg. 50, 142, 300, 161 (x0, top, x1, bottom)")
app.addEntry("Filename_Coords")

# link the buttons to the function called press
app.addButtons(["Process", "Quit"], press)

# start the GUI
app.go()
