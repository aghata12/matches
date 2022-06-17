from lib2to3.pytree import convert
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.lib.utils import object_to_json

from students import get_student_list
from recruiter import get_recruiter_list
from prematch import *
from main import *


hours=['10:10','10:20','10:30','10:40','10:50','11:00',"11:20","11:30","11:40","11:50","12:00","12:10","12:30","12:40","12:50"]


forced_positions=[['BIO-Merkatu (Grupo Teknei)','10:10','Perla'],['Merkatu','11:00','Ainara'],
                  ['Ibermatica','11:00','DESCANSO'],['Merkatu','10:20','Ainara']]

def create_app(repositories):
    app = Flask(__name__)
    CORS(app)

    @app.route("/", methods=["GET"])
    def hello_world():
        return "...magic!"


    @app.route("/api/prematch", methods=["POST"])
    def post_coders():
        body = request.json
        students_orig = body["CODERS"]
        recruiters_orig = body["RECRUITERS"]

        recruiters_copy=recruiters_orig[:]
        students=students_orig[:]
        
        student_list=get_student_list(students)
        recruiter_list=get_recruiter_list(recruiters_copy)

        coincidences_st_rec_st_list=fill_skills_and_recruiters_in_students(recruiter_list,student_list)
        matrix=generate_matrix(recruiter_list,hours)
        matrix_no_available_hours=fill_recruiter_no_available_spaces(matrix,recruiter_list)
        
        # rellena matriz con las posiciones forzadas
        matrix_prefilled=fill_matrix_with_forced_positions(matrix_no_available_hours,forced_positions)

        # en student_list rellena los horarios y empresa con que se vio el estudiante de los forzados
        student_list_blocked_hours=forced_matches(forced_positions,coincidences_st_rec_st_list)
        matrix_filled=match_students(matrix_prefilled,student_list_blocked_hours)
        matrix_final=fill_empties(matrix_filled)
        final_json=fill_data_to_json(matrix_final,recruiters_orig)
        
        return jsonify(final_json), 200

    return app