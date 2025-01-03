from django.core.files import File
from api.models import *
from django.http import HttpResponse
from datetime import date
from django.utils import timezone
from django.db import connection
import time
from api.serializer import *
import pandas as pd

# knust programs = [
#     {'name': "BSc. Agriculture", 'cut-off': 22},
#     {'name': "BSc. Agricultural Biotechnology", 'cut-off': 18},
#     {'name': "BSc. Agribusiness Management", 'cut-off': 17},
#     {'name': "BSc. Landscape Design and Management", 'cut-off': 19},
#     {'name': "BSc. Natural Resources Management", 'cut-off': 18},
#     {'name': "BSc. Forest Resources Technology", 'cut-off': 23},
#     {'name': "BSc. Aquaculture and Water Resources Management", 'cut-off': 22},
#     {'name': "BSc. Packaging Technology", 'cut-off': 16},
#     {'name': "BSc. Architecture", 'cut-off': 9},
#     {'name': "BSc. Construction Technology and Management", 'cut-off': 12},
#     {'name': "BSc. Quantity Surveying and Construction Economics", 'cut-off': 11},
#     {'name': "BSc. Development Planning", 'cut-off': 10},
#     {'name': "BSc. Human Settlement Planning", 'cut-off': 12},
#     {'name': "BSc. Land Economy", 'cut-off': 9},
#     {'name': "BSc. Real Estate", 'cut-off': 10},
#     {'name': "BFA. Painting and Sculpture", 'cut-off': 15},
#     {'name': "BA. Communication Design (Graphic Design)", 'cut-off': 13},
#     {'name': "BA. Integrated Rural Art and Industry", 'cut-off': 15},
#     {'name': "BA. Publishing Studies", 'cut-off': 15},
#     {'name': "BSc. Metal Product Design Technology", 'cut-off': 17},
#     {'name': "BSc. Textile Design and Technology", 'cut-off': 13},
#     {'name': "BSc. Fashion Design", 'cut-off': 12},
#     {'name': "BSc. Ceramics Design Technology", 'cut-off': 24},
#     {'name': "BEd. Junior High School Specialism", 'cut-off': 18},
#     {'name': "BSc. Aerospace Engineering", 'cut-off': 10},
#     {'name': "BSc. Agricultural Engineering", 'cut-off': 16},
#     {'name': "BSc. Automobile Engineering", 'cut-off': 13},
#     {'name': "BSc. Biomedical Engineering", 'cut-off': 7},
#     {'name': "BSc. Chemical Engineering", 'cut-off': 10},
#     {'name': "BSc. Civil Engineering", 'cut-off': 10},
#     {'name': "BSc. Computer Engineering", 'cut-off': 9},
#     {'name': "BSc. Electrical/Electronic Engineering", 'cut-off': 8},
#     {'name': "BSc. Geological Engineering", 'cut-off': 12},
#     {'name': "BSc. Geomatic (Geodetic) Engineering", 'cut-off': 13},
#     {'name': "BSc. Industrial Engineering", 'cut-off': 13},
#     {'name': "BSc. Marine Engineering", 'cut-off': 11},
#     {'name': "BSc. Materials Engineering", 'cut-off': 13},
#     {'name': "BSc. Mechanical Engineering", 'cut-off': 10},
#     {'name': "BSc. Metallurgical Engineering", 'cut-off': 14},
#     {'name': "BSc. Petrochemical Engineering", 'cut-off': 9},
#     {'name': "BSc. Petroleum Engineering", 'cut-off': 8},
#     {'name': "BSc. Telecommunication Engineering", 'cut-off': 12},
#     {'name': "Bachelor of Dental Surgery (BDS)", 'cut-off': 6},
#     {'name': "Doctor of Veterinary Medicine (DVM)", 'cut-off': 13},
#     {'name': "BSc. Disability and Rehabilitation Studies", 'cut-off': 14},
#     {'name': "Bachelor of Herbal Medicine (BHM)", 'cut-off': 15},
#     {'name': "BSc. Human Biology (Medicine)", 'cut-off': 6},
#     {'name': "BSc. Medical Laboratory Sciences", 'cut-off': 7},
#     {'name': "BSc. Medical Imaging", 'cut-off': 9},
#     {'name': "BSc. Midwifery", 'cut-off': 9},
#     {'name': "BSc. Nursing", 'cut-off': 8},
#     {'name': "BSc. Physiotherapy and Sports Science", 'cut-off': 12},
#     {'name': "Pharm D (Doctor of Pharmacy)", 'cut-off': 7},
#     {'name': "BA. Akan Language and Culture", 'cut-off': 20},
#     {'name': "BA. Economics", 'cut-off': 13},
#     {'name': "BA. English", 'cut-off': 16},
#     {'name': "BA. French and Francophone Studies", 'cut-off': 14},
#     {'name': "BA. Geography and Rural Development", 'cut-off': 12},
#     {'name': "BA. History", 'cut-off': 16},
#     {'name': "BA. Linguistics", 'cut-off': 15},
#     {'name': "BA. Media and Communication Studies", 'cut-off': 10},
#     {'name': "BA. Political Studies", 'cut-off': 10},
#     {'name': "BA. Religious Studies", 'cut-off': 18},
#     {'name': "BA. Sociology", 'cut-off': 11},
#     {'name': "BA. Social Work", 'cut-off': 12},
#     {'name': "BSc. Business Administration (Human Resource Mgt./Management)", 'cut-off': 9},
#     {'name': "BSc. Business Administration (Marketing/International Business)", 'cut-off': 10},
#     {'name': "BSc. Business Administration (Accounting/Banking and Finance)", 'cut-off': 7},
#     {'name': "BSc. Business Adm. (Logistics and Supply Chain Mgt/Bus. Info. Tech.)", 'cut-off': 9},
#     {'name': "BSc. Hospitality and Tourism Management", 'cut-off': 10},
#     {'name': "LLB", 'cut-off': 7},
#     {'name': "BSc. Biochemistry", 'cut-off': 12},
#     {'name': "BSc. Food Science and Technology", 'cut-off': 13},
#     {'name': "BSc. Biological Science", 'cut-off': 12},
#     {'name': "BSc. Environmental Sciences", 'cut-off': 15},
#     {'name': "BSc. Chemistry", 'cut-off': 16},
#     {'name': "BSc. Computer Science", 'cut-off': 11},
#     {'name': "BSc. Mathematics", 'cut-off': 17},
#     {'name': "BSc. Actuarial Science", 'cut-off': 11},
#     {'name': "BSc. Statistics", 'cut-off': 12},
#     {'name': "BSc. Physics", 'cut-off': 18},
#     {'name': "BSc. Meteorology and Climate Science", 'cut-off': 19},
#     {'name': "Doctor of Optometry", 'cut-off': 9},
#     {'name': "BSc. Civil Engineering (Obuasi Campus)", 'cut-off': 14},
#     {'name': "BSc. Electrical/Electronic Engineering (Obuasi Campus)", 'cut-off': 13},
#     {'name': "BSc. Geological Engineering (Obuasi Campus)", 'cut-off': 16},
#     {'name': "BSc. Geomatic (Geodetic) Engineering (Obuasi Campus)", 'cut-off': 17},
#     {'name': "BSc. Materials Engineering (Obuasi Campus)", 'cut-off': 18},
#     {'name': "BSc. Mechanical Engineering (Obuasi Campus)", 'cut-off': 14},
#     {'name': "BSc. Metallurgical Engineering (Obuasi Campus)", 'cut-off': 19},
#     {'name': "BSc. Medical Laboratory Sciences (Obuasi Campus)", 'cut-off': 10},
#     {'name': "BSc. Midwifery (Obuasi Campus)", 'cut-off': 12},
#     {'name': "BSc. Nursing (Obuasi Campus)", 'cut-off': 11},
#     {'name': "BBA (HRM/Management) (Obuasi Campus)", 'cut-off': 16},
#     {'name': "BBA (Marketing/International Business) (Obuasi Campus)", 'cut-off': 17},
#     {'name': "BBA (Accounting/Banking and Finance) (Obuasi Campus)", 'cut-off': 13},
#     {'name': "BBA (Logistics & Supply Chain Mgt/Bus. Info. Tech.) (Obuasi Campus)", 'cut-off': 15},
#     {'name': "BSc. Environmental Sciences (Obuasi Campus)", 'cut-off': 18}
# ]

# legonprograms = [
#     {'name': "BSc. Biological Sciences", 'choice_1': '16(18)', 'choice_2': '8(9)', 'subject_requirements': 'C6 in Chemistry'},
#     {'name': "BSc. Agriculture", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': 'C6 in Chemistry'},
#     {'name': "BSc. Earth Sciences", 'choice_1': 24, 'choice_2': '12(14)', 'subject_requirements': 'C6 in Chemistry, C6 in Physics'},
#     {'name': "BSc. Agricultural Engineering", 'choice_1': 22, 'choice_2': 22, 'subject_requirements': 'B3 in Elective Maths'},
#     {'name': "BSc. Biomedical Engineering", 'choice_1': '10(11)', 'choice_2': 10, 'subject_requirements': 'B3 in Elective Maths'},
#     {'name': "BSc. Computer Engineering", 'choice_1': '8(10)', 'choice_2': 8, 'subject_requirements': 'B3 in Elective Maths'},
#     {'name': "BSc. Food Process Engineering", 'choice_1': 18, 'choice_2': 13, 'subject_requirements': 'B3 in Elective Maths'},
#     {'name': "BSc. Materials Science & Engineering", 'choice_1': '18(19)', 'choice_2': 13, 'subject_requirements': 'B3 in Elective Maths'},
#     {'name': "BSc. Family & Child Studies", 'choice_1': 16, 'choice_2': 16, 'subject_requirements': 'C6 in Management in Living'},
#     {'name': "BSc. Food & Clothing", 'choice_1': 20, 'choice_2': 20, 'subject_requirements': 'C6 in Chemistry'},
#     {'name': "BSc. Information Technology", 'choice_1': '9(11)', 'choice_2': 9, 'subject_requirements': 'B2 in Core Maths'},
#     {'name': "BSc. Mathematical Sciences", 'choice_1': '12(15)', 'choice_2': 7, 'subject_requirements': 'B3 in Elective Maths'},
#     {'name': "BSc. Physical Sciences", 'choice_1': 24, 'choice_2': '21(24)', 'subject_requirements': 'C6 in Chemistry, C6 in Physics'},
#     {'name': "Doctor of Veterinary Medicine", 'choice_1': 14, 'choice_2': 14, 'subject_requirements': None},
#     {'name': "BSc. Psychology", 'choice_1': 22, 'choice_2': 22, 'subject_requirements': None},
#     {'name': "Bachelor of Medicine and Bachelor of Surgery", 'choice_1': 7, 'choice_2': 7, 'subject_requirements': None},
#     {'name': "Doctor of Pharmacy", 'choice_1': 8, 'choice_2': 8, 'subject_requirements': None},
#     {'name': "BSc. Nursing", 'choice_1': '8/12', 'choice_2': '8/12', 'subject_requirements': '08 for Non Science / 12 for Science Background'},
#     {'name': "BSc. Midwifery", 'choice_1': '8/12', 'choice_2': '8/12', 'subject_requirements': '08 for Non Science / 12 for Science Background'},
#     {'name': "Bachelor of Dental Surgery", 'choice_1': 9, 'choice_2': 9, 'subject_requirements': None},
#     {'name': "BSc. Medical Laboratory Sciences", 'choice_1': 11, 'choice_2': 10, 'subject_requirements': None},
#     {'name': "BSc. Physiotherapy", 'choice_1': 14, 'choice_2': 13, 'subject_requirements': None},
#     {'name': "BSc. Dietetics", 'choice_1': 14, 'choice_2': 12, 'subject_requirements': None},
#     {'name': "BSc. Diagnostic Radiography", 'choice_1': 12, 'choice_2': 10, 'subject_requirements': None},
#     {'name': "BSc. Occupational Therapy", 'choice_1': 16, 'choice_2': 14, 'subject_requirements': None},
#     {'name': "BSc. Respiratory Therapy", 'choice_1': 14, 'choice_2': 12, 'subject_requirements': None},
#     {'name': "Bachelor of Public Health", 'choice_1': 16, 'choice_2': 16, 'subject_requirements': None},
#     {'name': "BSc. Education", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "BA. Education", 'choice_1': 21, 'choice_2': 21, 'subject_requirements': None},
#     {'name': "B.Ed. (JHS Specialism)", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "Bachelor of Education (Early Grade Specialism)", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "Bachelor of Education (Upper Grade Specialism)", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "BA. Education (English)", 'choice_1': 20, 'choice_2': 20, 'subject_requirements': None},
#     {'name': "BA. Sports and Physical Culture", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "BSc. Information Technology - Distance Education", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "BSc. Administration - Distance Education", 'choice_1': 30, 'choice_2': 30, 'subject_requirements': None},
#     {'name': "Bachelor of Arts - Distance Education", 'choice_1': 30, 'choice_2': 30, 'subject_requirements': None},
#     {'name': "BSc. Administration - Kumasi City Campus", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "BSc. Administration - Takoradi City Campus", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "Bachelor of Laws", 'choice_1': 6, 'choice_2': 6, 'subject_requirements': None},
#     {'name': "BSc. Administration - Legon Campus", 'choice_1': 7, 'choice_2': 7, 'subject_requirements': None},
#     {'name': "BSc. Administration - Legon Campus (Full-Fee Paying)", 'choice_1': 14, 'choice_2': 14, 'subject_requirements': None},
#     {'name': "BSc. Administration - City Campus", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "Bachelor of Arts (General Arts Background)", 'choice_1': '15(16)', 'choice_2': '15(16)', 'subject_requirements': None},
#     {'name': "Bachelor of Arts Full-Fee Paying", 'choice_1': 22, 'choice_2': 22, 'subject_requirements': None},
#     {'name': "Bachelor of Arts , Administration", 'choice_1': 10, 'choice_2': 10, 'subject_requirements': None},
#     {'name': "Bachelor of Arts , Administration (Full-Fee Paying)", 'choice_1': 18, 'choice_2': 18, 'subject_requirements': None},
#     {'name': "Bachelor of Arts (Business/Science/ Vocational Background)", 'choice_1': 12, 'choice_2': 12, 'subject_requirements': None},
#     {'name': "Bachelor of Arts - City Campus", 'choice_1': 24, 'choice_2': 24, 'subject_requirements': None},
#     {'name': "Bachelor of Fine Arts", 'choice_1': 22, 'choice_2': 22, 'subject_requirements': None},
# ]

# uccprograms = [
#     {'name': "B. A. (African Studies)", 'male': 14, 'female': 15},
#     {'name': "B. A. (Arts)", 'male': 15, 'female': 16},
#     {'name': "B. A. (Chinese)", 'male': 16, 'female': 18},
#     {'name': "B. A. (Communication Studies)", 'male': 15, 'female': 16},
#     {'name': "B. A. (Dance)", 'male': 22, 'female': 23},
#     {'name': "B. A. (Film Studies)", 'male': 21, 'female': 22},
#     {'name': "B. A. (Music)", 'male': 21, 'female': 22},
#     {'name': "B. A. (Theatre Studies)", 'male': 19, 'female': 20},
#     {'name': "B. A. (Anthropology)", 'male': 16, 'female': 17},
#     {'name': "B. A. (Population & Health)", 'male': 11, 'female': 12},
#     {'name': "B. A. (Social Sciences)", 'male': 12, 'female': 14},
#     {'name': "B. Sc. (Geography and Regional Planning)", 'male': 12, 'female': 14},
#     {'name': "B. Sc. (Hospitality Management)", 'male': 15, 'female': 18},
#     {'name': "B. Sc. (Tourism Management)", 'male': 14, 'female': 15},
#     {'name': "Bachelor of Commerce (Accounting)", 'male': 12, 'female': 12},
#     {'name': "Bachelor of Commerce (Finance)", 'male': 15, 'female': 15},
#     {'name': "Bachelor of Commerce (Human Resource Management)", 'male': 20, 'female': 20},
#     {'name': "Bachelor of Commerce (Management)", 'male': 17, 'female': 17},
#     {'name': "Bachelor of Commerce (Marketing)", 'male': 20, 'female': 20},
#     {'name': "Bachelor of Commerce (Procurement & Supply Chain Management)", 'male': 17, 'female': 17},
#     {'name': "Bachelor of Science (Economics)", 'male': 15, 'female': 16},
#     {'name': "Bachelor of Science (Economics with Finance)", 'male': 14, 'female': 15},
#     {'name': "B.Ed (Accounting)", 'male': 13, 'female': 13},
#     {'name': "B.Ed (Arts)", 'male': 18, 'female': 19},
#     {'name': "B.Ed (Management)", 'male': 15, 'female': 16},
#     {'name': "B.Ed (Social Sciences)", 'male': 18, 'female': 19},
#     {'name': "B.Ed (Social Studies)", 'male': 18, 'female': 19},
#     {'name': "B.Ed (Communication Design)", 'male': 18, 'female': 19},
#     {'name': "B.Ed (Construction Technology)", 'male': 19, 'female': 20},
#     {'name': "B.Ed (Health, Physical Education and Recreation)", 'male': 30, 'female': 30},
#     {'name': "B.Ed (Home Economics)", 'male': 30, 'female': 30},
#     {'name': "B.Ed (Mathematics)", 'male': 13, 'female': 14},
#     {'name': "B.Ed (Science)", 'male': 12, 'female': 13},
#     {'name': "B.Ed Fine Art (Painting and Sculpture)", 'male': 19, 'female': 20},
#     {'name': "B.Ed. Information Technology Education", 'male': 15, 'female': 16},
#     {'name': "B.Ed (Early Childhood Education)", 'male': 25, 'female': 25},
#     {'name': "B.Ed (Junior High School Education)", 'male': 25, 'female': 25},
#     {'name': "B.Ed (Primary Education)", 'male': 25, 'female': 25},
#     {'name': "B.Sc (Psychology)", 'male': 20, 'female': 21},
#     {'name': "Bachelor of Medicine and Bachelor of Surgery (MBChB)", 'male': 8, 'female': 9},
#     {'name': "Doctor of Pharmacy – (Pharm D)", 'male': 8, 'female': 8},
#     {'name': "B.Sc. (Midwifery)", 'male': 11, 'female': 12},
#     {'name': "B.Sc. (Nursing)", 'male': 11, 'female': 12},
#     {'name': "B.Sc. (Biomedical Sciences)", 'male': 10, 'female': 11},
#     {'name': "B.Sc. (Diagnostic Imaging Technology)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Diagnostic Medical Sonography)", 'male': 11, 'female': 12},
#     {'name': "B.Sc. (Dietetics)", 'male': 19, 'female': 21},
#     {'name': "B.Sc. (Health Information Management)", 'male': 15, 'female': 16},
#     {'name': "B.Sc. (Medical Laboratory Technology)", 'male': 12, 'female': 15},
#     {'name': "B.Sc. (Nutrition)", 'male': 19, 'female': 20},
#     {'name': "B.Sc. (Physician Assistant Studies)", 'male': 18, 'female': 19},
#     {'name': "B.Sc. (Sport and Exercise Science)", 'male': 19, 'female': 20},
#     {'name': "Doctor of Optometry (OD)", 'male': 8, 'female': 8},
#     {'name': "B.Sc. (Agri-Business)", 'male': 24, 'female': 24},
#     {'name': "B.Sc. (Agricultural Extension & Community Development)", 'male': 25, 'female': 25},
#     {'name': "B.Sc. (Agriculture)", 'male': 24, 'female': 25},
#     {'name': "B.Sc. (Agro-Processing)", 'male': 21, 'female': 22},
#     {'name': "B.Sc. (Horticulture)", 'male': 23, 'female': 24},
#     {'name': "B.Sc. (Biochemistry)", 'male': 15, 'female': 15},
#     {'name': "B.Sc. (Conservation Biology and Entomology)", 'male': 14, 'female': 15},
#     {'name': "B.Sc. (Environmental Science)", 'male': 11, 'female': 12},
#     {'name': "B.Sc. (Fisheries and Aquatic Sciences)", 'male': 14, 'female': 15},
#     {'name': "B.Sc. (Forensic Science)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Molecular Biology and Biotechnology)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Actuarial Science)", 'male': 12, 'female': 13},
#     {'name': "B.Sc. (Chemistry)", 'male': 12, 'female': 13},
#     {'name': "B.Sc. (Computer Science)", 'male': 15, 'female': 16},
#     {'name': "B.Sc. (Engineering Physics)", 'male': 12, 'female': 13},
#     {'name': "B.Sc. (Industrial Chemistry)", 'male': 12, 'female': 14},
#     {'name': "B.Sc. (Information Technology)", 'male': 13, 'female': 14},
#     {'name': "B.Sc. (Laboratory Technology)", 'male': 13, 'female': 14},
#     {'name': "B.Sc. (Mathematics and Statistics)", 'male': 9, 'female': 10},
#     {'name': "B.Sc. (Mathematics with Business)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Mathematics with Economics)", 'male': 10, 'female': 11},
#     {'name': "B.Sc. (Mathematics)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Meteorology and Atmospheric Physics)", 'male': 14, 'female': 15},
#     {'name': "B.Sc. (Physics)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Statistics)", 'male': 11, 'female': 11},
#     {'name': "B.Sc. (Water and Sanitation)", 'male': 11, 'female': 12},
# ]


# Other
def query(request):
    # start = time.time()
    # all_class = Classe.objects.select_related('school').all()
    
    # for _class in all_class:
    #     all_assessments = Assessment.objects.select_related('student').filter(school=_class.school)
    #     same_class_assessments = []
    #     for _assessments in all_assessments:
    #         if _class == _assessments.student.st_class:
    #             _assessments.student_class = _class
    #             same_class_assessments.append(_assessments)
    
    #     Assessment.objects.bulk_update(same_class_assessments, ['student_class'])    
        
    # end = time.time()
    # # Student.objects.bulk_update(student, ['level'])    
    # print(f"time taken: {end - start}")
    # grade = [
    #     {"Lower Limit": 80, "Upper Limit": 100, "Letter Grade": "A1", "Interpretation": "EXCELLENT"},
    #     {"Lower Limit": 75, "Upper Limit": 79,  "Letter Grade": "B2", "Interpretation": "VERY GOOD"},
    #     {"Lower Limit": 70, "Upper Limit": 74,  "Letter Grade": "B3", "Interpretation": "GOOD"},
    #     {"Lower Limit": 65, "Upper Limit": 69,  "Letter Grade": "C4", "Interpretation": "CREDIT"},
    #     {"Lower Limit": 60, "Upper Limit": 64,  "Letter Grade": "C5", "Interpretation": "CREDIT"},
    #     {"Lower Limit": 55, "Upper Limit": 59,  "Letter Grade": "C6", "Interpretation": "CREDIT"},
    #     {"Lower Limit": 50, "Upper Limit": 54,  "Letter Grade": "D7", "Interpretation": "PASS"},
    #     {"Lower Limit": 45, "Upper Limit": 49,  "Letter Grade": "E8", "Interpretation": "WEAK PASS"},
    #     {"Lower Limit": 0,  "Upper Limit": 44,  "Letter Grade": "F9", "Interpretation": "FAIL"}
    # ]
    # grades_to_create = []
    # for _grade in grade:
    #     grades_to_create.append(GradingSystem.objects.create(
    #         label=_grade['Letter Grade'],
    #         upper_limit=_grade['Upper Limit'],
    #         lower_limit=_grade['Lower Limit'],
    #         remark=_grade['Interpretation']
    #     ))
    # GradingSystem.objects.bulk_create(grades_to_create)
    return HttpResponse('Operation success')

# table_name = 'api_gradingsystem_schools'
#     def delete_table(table_name):
#         with connection.cursor() as cursor:
#             cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

#     delete_table(table_name)







