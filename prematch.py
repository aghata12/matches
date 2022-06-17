from random import shuffle


def coincidences(a,b):
    if b==[]:
        return True
    if len(set.intersection(set(a),set(b)))>=1:
        return True
    if b=="REMOTO":
        return True
    return False


def fill_skills_and_recruiters_in_students(recruiter_list,student_list):
    for recruiter in recruiter_list:
        for student in student_list:
            rec_locations=recruiter["LOCATIONS"]
            rec_skills=recruiter["SKILLS"]
            stud_locations=student["LOCATIONS"]
            stud_skills=student["SKILLS"]
            if coincidences(stud_locations,rec_locations) and coincidences(stud_skills,rec_skills): #and coincidences(stud_skills,rec_skills) //cambiado lo de skills 
                student["PMATCH"].append(recruiter["EMPRESA"])
    return student_list


#generar en base a los horarios totales
def generate_matrix(recruiter_list,hours):
    matrix=[]    
    for recruiter in recruiter_list:
        for hour in hours:
            matrix.append({"EMPRESA": recruiter['EMPRESA'],"NOMBRE DEL RECRUITER":recruiter["NOMBRE DEL RECRUITER"],"HORARIO":hour})
    return matrix

#Matriz-->[NOMBRE DEL RECRUITER,HOUR]
def fill_recruiter_no_available_spaces(matrix,recruiter_list):
    for recruiter in recruiter_list:
        for slot in matrix:
            company_name=slot["EMPRESA"]
            recruiter_hour=slot["HORARIO"]
            if company_name==recruiter["EMPRESA"]:
                if recruiter_hour not in  recruiter["HOURS_DISP"]:
                    slot["HORARIO"]="NO DISP"
                    
    return matrix


#Matriz-->{"EMPRESA": recruiter['EMPRESA'],"NOMBRE DEL RECRUITER":recruiter["NOMBRE DEL RECRUITER"],"HORARIO":hour}

# forced=['Merkatu','10:10','Perla']
def fill_matrix_with_forced_positions(matrix,forced_positions): #evaluar esto 1
    for row in matrix:
        for pos in forced_positions:
            company_name=pos[0]
            hour=pos[1]
            st_name=pos[2]
            if not "ESTUDIANTE" in row.keys():     #si no tiene estudiante asignado
                if company_name==row["EMPRESA"]:
                    if hour==row["HORARIO"]:
                        row["ESTUDIANTE"]=st_name
    return matrix


# [['Merkatu','10.10','Perla'],['Merkatu','11.00','Ainara'],
#                   ['Ibermatica','11.00','DESCANSO'],['Merkatu','10.20','Ainara']]

#Actualiza los estudiantes con la informacion de las posiciones forzadas
def forced_matches(matches,student_list): #evaluar esto 2
    for position in matches:
        for stud in student_list:
            if position[2]==stud["NOMBRE"]:
                stud["BLOCKEDH"].append(position[1])
                stud["DONE"].append(position[0])
    return student_list


#verifica si el rec si es compatible y el estudiante no ha sido entrevistado por el y 
# si el estudiante tiene horario libre
def check_coincidence(recruiter,student):
    comp_name=recruiter["EMPRESA"]
    hour=recruiter["HORARIO"]
    if comp_name in student["PMATCH"]:
        if not comp_name in student["DONE"]:
            if not hour in student["BLOCKEDH"]:
                return True
    return False


#itera sobre la matriz y va llenando los huecos si hay compatibilidad.
def match_students(matrix,student_list):
    for row in matrix:
        if "ESTUDIANTE" in row.keys():      #tiene estudiante asignado?
                continue
        # shuffle(student_list)
        for student in student_list:
            student_name=student["NOMBRE"]
            if check_coincidence(row,student):
                row["ESTUDIANTE"]=student_name
                recruiter=row["EMPRESA"]
                hour=row["HORARIO"]
                student["DONE"].append(recruiter)
                student["BLOCKEDH"].append(hour)
                break
    return matrix

#rellena vacios en la matriz rellenada donde no hubo matches
def fill_empties(matrix):
    for row in matrix:
        if not "ESTUDIANTE" in row.keys():
            row["ESTUDIANTE"]="-"
    return matrix



def fill_data_to_json(matrix,recruiter_list):
    for recruiter in recruiter_list:
        for slot in matrix:
            if recruiter["NOMBRE DEL RECRUITER"]==slot["NOMBRE DEL RECRUITER"]:
                if slot["HORARIO"] in recruiter.keys():
                    hour=slot["HORARIO"]
                    recruiter[hour]=slot["ESTUDIANTE"]
    return recruiter_list

                



            









        

