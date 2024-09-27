import numpy as np
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Bert-based-uncased model
# qa_mod_name = 'bert-based-uncased'
# mod_save_path = "/models/bert_based_uncased"

# Roberta-base-squad2 model
roberta_mod_name = 'deepset/roberta-base-squad2'
roberta_save_path = f"/PRO/Git_Repository/cassandra/Backend/models/{roberta_mod_name.split('/')[1]}"

# Download the question answering model and tokenizer
roberta_tokenizer = AutoTokenizer.from_pretrained(roberta_save_path)
roberta_mod = AutoModelForQuestionAnswering.from_pretrained(roberta_save_path)

roberta = pipeline("question-answering", model=roberta_mod, tokenizer=roberta_tokenizer)

# # embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def get_program_data():
    program_info = """
    The cut-off point for Computer Science(CS) is 90%. The cut-off point for Electrical Engineering 95%. The cut-off point for Mechanical Engineering is 80%.
    """
    return program_info

context = """
Kwame Nkrumah University of Science and Technology (KNUST) boasts a comprehensive range of undergraduate and postgraduate programs encompassing diverse academic fields.  The College of Humanities and Social Sciences equips students with expertise in disciplines like Economics, Sociology, English, History, Linguistics, and Political Studies. Additionally, KNUST offers parallel programs in these disciplines, allowing students to pursue them alongside the standard offerings. The college further broadens its scope with programs in Culture and Tourism, Communication Studies, Akan Language and Culture, Geography and Rural Development, and French and Francophone Studies. Religious Studies rounds out the college's offerings.
For those seeking a career in business, the School of Business provides a strong foundation. Students can choose from specializations in Accounting/Banking and Finance, Marketing/International, Hospitality and Tourism Management, or Logistic and Supply Chain Management, all within the Business Administration program.
KNUST's Faculty of Art fosters creativity through programs in Fashion Design, Publishing Studies, Painting & Sculpture, Communication Design (Graphic Design), Ceramic Design and Technology, Textile Design and Technology, Integrated Rural Art and Industry, and Metalsmithing and Jewelry Technology.
The College of Art and Built Environment caters to those with a passion for design and construction. It offers programs in Architecture, Real Estate, Land Economy, Development Planning, Quality Surveying and Construction Economics (Building Technology), Construction Technology and Management (Building Technology), and Human Settlement Planning. The college also complements these programs with offerings in Painting and Sculpture (BFA), Communication Design (Graphic Design) (BA), Industrial Art (combining Ceramics, Metal Work, Textiles, and Fashion Design) (BA), Integrated Rural Art and Industry (BA), and Publishing Studies (Book Industry) (BA). Parallel programs are available in Integrated Rural Art and Industry, Publishing Studies, and Communication Design, providing additional options for students.
The College of Science offers a robust curriculum in scientific disciplines. Students can pursue degrees in Biochemistry, Chemistry, Mathematics, Statistics, Physics, Actuarial Science, Environmental Science, Biological Science, and Food and Technology. The college also offers a parallel program in Computer Science and a program in Meteorology and Climate Science. For those seeking a career in optometry, a Doctor of Optometry (OD) program is available, spanning six years.
KNUST's College of Health Sciences caters to those with a passion for healthcare. Programs include Nursing, Midwifery, Herbal Medicine, Emergency Nursing (fee-paying), Medical Laboratory Technology, Doctor of Pharmacy (Pharm D) (six years), Human Biology (leading to a three-year Clinical Programme for an MB ChB Degree), Disability & Rehabilitation Studies, Doctor of Veterinary Medicine (DVM) (six years), and Dental Surgery (a three-year BSc in Human Biology followed by a year of clinical study leading to a BDS Degree) (fee-paying).
For those seeking a degree in Agriculture or related fields, the College of Agriculture and Natural Resources offers programs in Agribusiness Management, Forest Resources Technology, Aquaculture & Water Resources Management, Natural Resources Management, and Post Harvest Technology. Additionally, students can pursue a BSc in Dairy and Meat Science, Landscape Design and Management, Agricultural Biotechnology, or Agriculture.
KNUST's College of Engineering provides a rigorous curriculum for those seeking careers in various engineering disciplines. Programs include Civil Engineering, Materials Engineering, Computer Engineering, Electrical & Electronic Engineering, Mechanical Engineering, Geomatic Engineering (Geodetic Engineering), Aerospace Engineering, Petroleum Engineering, Telecommunication Engineering, Geological Engineering, Biomedical Engineering, Petrochemical Engineering, Metallurgical Engineering, and Chemical Engineering.
Finally, KNUST offers Distance Education/Learning Undergraduate Programs, which are two-year post-diploma programs, in Sociology, Information Technology, Statistics, Agriculture, and Actuarial Science. This program format allows for greater flexibility in pursuing a degree.
By encompassing such a wide range of programs, KNUST empowers students to pursue their academic and professional goals across a multitude of disciplines.
"""
context_table = [
    {'school': 'KNUST', 'programs': ['Petroleum Engineering', 'Mechanical Engineering', 'Physics', 'Medicine']},
    {'school': 'UG', 'programs': ['Law', 'Biological Science', 'Biochemistry', 'Medicine']},
]
    
program_context = get_program_data()
question = "what programs are offered at KNUST in college of engineering"
res = roberta(question=question, context=context)
print(res)



# sample_questions = [
#     "What are the available programs for computer science at MIT?",
#     "Which programs does MIT offer for CS?",
#     "What courses can I take in computer science at MIT?",
#     "programs offered at MIT",
#     "courses available at MIT",
# ]

# sample_questions_embeddings = embedding_model.encode(sample_questions, convert_to_tensor=True)


# def get_program_info(user_query):
#     user_query_embedding = embedding_model.encode(user_query, convert_to_tensor=True)
    
#     similarity = util.pytorch.cos_sim(user_query_embedding, sample_questions_embeddings)
    
#     # Find the closest match
#     match_idx = np.argmax(similarity)
#     matched_question = sample_questions[match_idx]
    
#     # Use the match question to find the program info
#     context = get_program_data()
#     program_info_response = qa_mod(question=matched_question, context=context)

#     return program_info_response

# query = get_program_info("What programs are in MIT")

# print(query)























