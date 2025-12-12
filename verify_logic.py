import time
import os
from recorder import Recorder
from document_generator import DocumentGenerator

def test_logic():
    print("Initializing Recorder...")
    rec = Recorder()
    
    print("Starting recording...")
    rec.start()
    
    print("Waiting for 12 seconds to ensure at least one capture interval passes...")
    time.sleep(12)
    
    # Simulate a screen change if possible, or just rely on time passing and natural screen updates (clock etc)
    # or just the initial capture.
    
    print("Stopping recording...")
    rec.stop()
    
    data = rec.get_data()
    print(f"Captured {len(data)} frames.")
    
    if len(data) > 0:
        print("Verifying data integrity...")
        first_item = data[0]
        if "timestamp" in first_item and "image_path" in first_item:
            print("Data structure looks correct.")
        else:
            print("Data structure invalid.")
            
        print("Testing Document Generation (DOCX)...")
        gen = DocumentGenerator()
        try:
            gen.generate_docx(data, "test_report.docx")
            print("DOCX generation successful.")
        except Exception as e:
            print(f"DOCX generation failed: {e}")

        print("Testing Document Generation (PDF)...")
        try:
            gen.generate_pdf(data, "test_report.pdf")
            print("PDF generation successful.")
        except Exception as e:
            print(f"PDF generation failed: {e}")
            
    else:
        print("No data captured. Check interval logic.")

    rec.clear_temp_files()
    print("Temp files cleared.")

if __name__ == "__main__":
    test_logic()
