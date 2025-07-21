import streamlit as st
from fpdf import FPDF
import io
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Delivery Note Generator", 
    layout="centered",
    page_icon="🧾"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #2E86AB;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}
.form-container {fo
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 10px;
    border: 1px solid #e9ecef;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🧾 Delivery Note Generator - Avar Garments</h1>', unsafe_allow_html=True)

# Enhanced form with better layout
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("delivery_note_form"):
        st.markdown("### 📝 Enter Delivery Note Details")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            note_no = st.text_input("📄 Delivery Note No.", value="001", help="Enter unique delivery note number")
            date = st.date_input("📅 Date", value=datetime.today())
            
        with col2:
            to_ms = st.text_input("🏢 To M/s", value="Sunbright Washing", help="Recipient company name")
            gstin = st.text_input("🆔 GSTIN", value="33AZJPL9421C1ZK", help="Recipient GSTIN number")
            quantity = st.text_input("📦 Quantity", value="8 Kg", help="Total quantity with unit")
        
        particulars = st.text_area(
            "📋 Particulars", 
            value="Airtex # Yellow\nCPL + Thumble Dry",
            help="Enter item details (one per line)",
            height=100
        )
        
        # Form submission with better styling
        submitted = st.form_submit_button("🚀 Generate Professional PDF", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

class EnhancedDeliveryPDF(FPDF):
    def __init__(self):
        # FIXED: Proper landscape A4 dimensions (297mm x 210mm)
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=False)
    
    def add_border_frame(self, x, y, width, height):
        """Add a decorative border frame"""
        self.set_line_width(0.5)
        self.rect(x, y, width, height)
        self.set_line_width(0.2)
        self.rect(x + 2, y + 2, width - 4, height - 4)
    
    # def add_company_logo_area(self, x, y):
    #     """Add a placeholder area for company logo"""
    #     self.set_line_width(0.3)
    #     self.rect(x, y, 20, 15)
    #     self.set_font("Arial", 'I', 8)
    #     self.set_xy(x + 2, y + 6)

    #     self.cell(16, 4, "LOGO", align='C')
    
    def delivery_note(self, x_offset, y_offset, note_no, gstin, date, to_ms, particulars, quantity):
        # ADJUSTED: Reduced width to fit two copies properly on landscape A4
        note_width = 135  # Reduced from 130 to ensure proper fit
        note_height = 180
        
        # Main border frame
        self.add_border_frame(x_offset, y_offset, note_width, note_height)
        
        # Header section with logo area
        header_y = y_offset + 8
        # self.add_company_logo_area(x_offset + 8, header_y)
        
        # Company name and details
        self.set_xy(x_offset + 25, header_y)
        self.set_font("Arial", 'B', 18)
        self.set_text_color(0, 50, 100)  # Dark blue
        self.cell(85, 8, txt="AVAR GARMENTS", align='C')
        
        # Company address with better formatting (NO EMOJIS)
        address_y = header_y + 10
        self.set_font("Arial", size=9)
        self.set_text_color(0, 0, 0)  # Black
        
        addresses = [
            "1/709c Siva Sakthi Nagar, Vellaikaradu, ",
            "SIDCO, Mudhalipalayam, TIRUPUR - 641606.",
            "Email: avargarments@gmail.com | Phone: +91-9952134884",
            "GSTIN: 33AZJPL9421C1ZK"
        ]
        
        for i, addr in enumerate(addresses):
            self.set_xy(x_offset + 25, address_y + (i * 4))
            self.cell(85, 4, txt=addr, align='C')
        
        # Delivery Note title with background
        title_y = address_y + 20
        self.set_fill_color(230, 240, 250)  # Light blue background
        self.set_xy(x_offset + 8, title_y)
        self.set_font("Arial", 'B', 14)
        self.set_text_color(0, 50, 100)
        # ADJUSTED: Width to match the reduced note width
        self.cell(note_width - 16, 8, txt="DELIVERY NOTE", align='C', fill=True)
        
        # Note details section
        details_y = title_y + 15
        self.set_fill_color(255, 255, 255)  # White background
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", 'B', 10)
        
        # ADJUSTED: Cell widths to fit the new note width
        cell_width = (note_width - 16) / 2
        
        # Note number and date in a box
        self.set_xy(x_offset + 8, details_y)
        self.cell(cell_width, 8, txt=f"Note No: {note_no}", border=1, align='L')
        self.cell(cell_width, 8, txt=f"Date: {date.strftime('%d/%m/%Y')}", border=1, align='L')

        # To M/s section
        self.set_xy(x_offset + 8, details_y + 12)
        self.cell(cell_width, 8, txt=f"To M/s: {to_ms}", border=1, align='L')
        self.cell(cell_width, 8, txt=f"GSTIN: {gstin}", border=1, align='L')

        # Items table with enhanced styling
        table_y = details_y + 28
        self.set_xy(x_offset + 8, table_y)
        
        # Table headers with background color
        self.set_fill_color(220, 230, 240)
        self.set_font("Arial", 'B', 10)
        
        headers = ["S.No", "Particulars", "Qty."]
        # ADJUSTED: Table widths to fit the new note width
        table_width = note_width - 16
        widths = [20, table_width - 40, 20]  # S.No: 20, Qty: 20, Particulars: remaining
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            self.cell(width, 10, txt=header, border=1, align='C', fill=True)
        self.ln()
        
        # Table content
        self.set_fill_color(255, 255, 255)
        self.set_font("Arial", size=9)
        
        lines = particulars.strip().split("\n")
        row_height = 8
        
        for i, line in enumerate(lines):
            self.set_x(x_offset + 8)
            
            # Serial number
            if i == 0:
                self.cell(widths[0], row_height, txt="1", border=1, align='C')
            else:
                self.cell(widths[0], row_height, txt="", border=1, align='C')
            
            # Particulars
            self.cell(widths[1], row_height, txt=line.strip(), border=1, align='L')
            
            # Quantity
            if i == 0:
                self.cell(widths[2], row_height, txt=quantity, border=1, align='C')
            else:
                self.cell(widths[2], row_height, txt="", border=1, align='C')
            self.ln()
        
        # Add empty rows if needed
        min_rows = 3
        if len(lines) < min_rows:
            for _ in range(min_rows - len(lines)):
                self.set_x(x_offset + 8)
                self.cell(widths[0], row_height, txt="", border=1)
                self.cell(widths[1], row_height, txt="", border=1)
                self.cell(widths[2], row_height, txt="", border=1)
                self.ln()
        
        # Signature section with three boxes: Receiver, Vehicle Number, For Avar Garments
        signature_y = table_y + 40 + (max(len(lines), min_rows) * row_height)

        self.set_xy(x_offset + 8, signature_y)
        self.set_font("Arial", 'B', 9)

        # Three equal-width boxes
        sig_width = (note_width - 16) / 3

        # Receiver's signature box
        self.cell(sig_width, 25, txt="", border=1)
        # Vehicle number box
        self.cell(sig_width, 25, txt="", border=1)
        # For Avar Garments box
        self.cell(sig_width, 25, txt="", border=1)

        # Labels below boxes
        self.set_xy(x_offset + 8, signature_y + 27)
        self.set_font("Arial", size=8)
        self.cell(sig_width, 5, txt="Receiver's Signature & Date", align='C')
        self.cell(sig_width, 5, txt="Vehicle Number", align='C')
        self.cell(sig_width, 5, txt="For Avar Garments", align='C')

        # Footer note
        self.set_xy(x_offset + 8, signature_y + 35)
        self.set_font("Arial", 'I', 7)
        self.set_text_color(100, 100, 100)
        self.cell(note_width - 16, 4, txt="Thank you for your business!", align='C')

        # Reset text color
        self.set_text_color(0, 0, 0)

# Form submission handling
if submitted:
    try:
        # Create PDF with proper landscape A4 formatting
        pdf = EnhancedDeliveryPDF()
        pdf.add_page()
        
        # ADJUSTED: Better positioning for two copies on landscape A4
        # Landscape A4 is 297mm wide x 210mm high
        margin = 10
        copy_width = 135
        spacing = 7  # Space between the two copies
        
        # Left copy
        pdf.delivery_note(
            x_offset=margin, 
            y_offset=15, 
            note_no=note_no, 
            date=date, 
            to_ms=to_ms, 
            gstin=gstin,
            particulars=particulars, 
            quantity=quantity
        )
        
        # Right copy - positioned to fit properly on landscape page
        pdf.delivery_note(
            x_offset=margin + copy_width + spacing, 
            y_offset=15, 
            note_no=note_no, 
            date=date, 
            to_ms=to_ms, 
            gstin=gstin,
            particulars=particulars, 
            quantity=quantity
        )
        
        # Add a subtle watermark/footer
        pdf.set_font("Arial", 'I', 6)
        pdf.set_text_color(150, 150, 150)
        pdf.set_xy(10, 200)
        pdf.cell(277, 5, f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Avar Garments Delivery System", align='C')
        
        # Convert to bytes with proper encoding
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            pdf_bytes = pdf_output.encode('latin-1')
        else:
            pdf_bytes = pdf_output
        pdf_buffer = io.BytesIO(pdf_bytes)
        
        # Success message with metrics
        st.success("✅ **Professional PDF Generated Successfully!**")
        
        # Display summary
        with st.expander("📊 Delivery Note Summary", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Note Number", note_no)
            with col2:
                st.metric("Date", date.strftime('%d/%m/%Y'))
            with col3:
                st.metric("Quantity", quantity)
            
            st.write(f"**Recipient:** {to_ms}")
            st.write(f"**Items:** {len(particulars.strip().split(chr(10)))} line(s)")
        
        # Download button with enhanced styling
        st.download_button(
            label="⬇️ Download Professional PDF (Duplicate Copies)",
            data=pdf_buffer,
            file_name=f"Delivery_Note_{note_no}_{date.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # Additional options
        with st.expander("🔧 Additional Options"):
            st.info("**Features included in this PDF:**")
            st.markdown("""
            - 📋 Professional formatting with borders and colors
            - 🏢 Company branding area (logo placeholder)
            - 📱 Contact information display
            - ✍️ Signature boxes for both parties
            - 📄 Duplicate copies on single landscape A4 page
            - 🎨 Enhanced table styling with headers
            - ⏰ Auto-generated timestamp
            """)
    
    except Exception as e:
        st.error(f"❌ Error generating PDF: {str(e)}")
        st.info("Please check your input data and try again.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
    "🧾 Delivery Note Generator v2.0 | Built with Streamlit & FPDF"
    "</div>", 
    unsafe_allow_html=True
)