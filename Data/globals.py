from Data.data_structures import Session,Settings,Table_Specs
import copy
from fpdf import FPDF
current_session = Session()
current_session_buffer = copy.deepcopy(current_session)
home_dir = []
table_specs = Table_Specs()
companies = []
passed_students = []
main_page = []
pdf_students = FPDF()
pdf_companies = FPDF()
pdf_global_plan = FPDF()