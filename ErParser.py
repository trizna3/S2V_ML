
'''
Script is for parsing text file containing test data.
Text files are written in custom syntax, expressing an entity-relationship model.

Script extract entity_sets names and their attributes names to new textfiles.

Adam Trizna
'''


model_names = list()

def get_model_names():
    model_names_file = "model_names.txt"
    global model_names
    if not model_names:
        model_names = list()
        with open(model_names_file,'r') as names:
            for row in  names:
                model_names.append(row.strip())
    return model_names

def getPathToExemplarModel(model_name):
    return "input_model_scripts_eng/exemplar_solutions/" + model_name + ".txt"
def getPathToStudent1Model(model_name):
    return "input_model_scripts_eng/students_solutions/" + model_name + "1.txt"
def getPathToStudent2Model(model_name):
    return "input_model_scripts_eng/students_solutions/" + model_name + "2.txt"

def processModel(model_name):
    global model_names
    if model_name not in model_names:
        return
    processSolution(getPathToExemplarModel(model_name),getPathToStudent1Model(model_name),"testing_data_processed/"+model_name+"_student1_processed.txt")
    processSolution(getPathToExemplarModel(model_name), getPathToStudent2Model(model_name), "testing_data_processed/"+model_name+"_student2_processed.txt")

def processSolution(exemplar_model_path, student_model_path, output_file):
    output = open(output_file,'w')

    es_id = 1
    es_name = None
    attributes = list()
    attributes_flag = False
    for file_name in [exemplar_model_path,student_model_path]:
        file = open(file_name,'r')
        row = file.readline()

        while row:
            if 'association' in row or 'generalization' in row: # We care about entity sets only
                break
            row = row.split(" ")
            for i in range(len(row)):

                if row[i] == 'entity' and row[i+1] == 'set':
                    es_name = row[i+2].strip().replace('"','')
                if '{' in row[i]:
                    attributes_flag = True
                if '}' in row[i]:
                    attributes_flag = False
                    output.write(str(es_id) + ":" + es_name + ":" + ",".join(attributes) + "\n")
                    es_id += 1
                    es_name = None
                    attributes = list()
                if attributes_flag and '{' not in row[i] and '}' not in row:
                    attributes.append(" ".join(row).strip().replace('"', ''))
            row = file.readline()
        output.write("=\n")
    output.close()

def parse():
    for model in get_model_names():
        processModel(model)

parse()