import pdfplumber

pdf_path = "overlapping.pdf"

with open("extracted_words.txt", "w") as f:  # Open in write mode
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            f.write(f"\n--- Page {page_number} ---\n")
            words = page.extract_words()

            for word in words:
                text = word.get('text', '[NO TEXT]')
                x = word.get('x', 'N/A')
                y = word.get('top', 'N/A')
                print(f"Text: {text:30} | x: {x} | y: {y}")
                f.write(f"Text: {text:30} | x: {x} | y: {y}\n")
