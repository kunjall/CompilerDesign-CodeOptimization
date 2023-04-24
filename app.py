from flask import Flask, request, send_file, render_template
# import codeopt

app = Flask(__name__)
# @app.route('/')
# def my_form():
#     return render_template('index.html')

@app.route('/', methods=['POST','GET'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text

def optCode():
    opti =''
    if request.method == 'POST' and 'code' in request.form:
        text_input = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        text_input.append(line)

    # # Join the list of lines into a single string
    # text_input_str = "\n".join(text_input)

    # # Open file in write mode
    # with open("input.txt", "w") as f:
    #     # Write text input to file
    #     f.write(text_input_str)

    # f = open("input.txt","r")
    # fout = open("output.txt","w")


    # list_of_lines = f.readlines()
    list_of_lines = text_input
    dictValues = dict()
    constantFoldedList = []
    constantFoldedExpression = []
    deadCodeElemination = []

    output_string = ""


    print("Quadruple form after Constant Folding")
    print("-------------------------------------")
    for i in list_of_lines:
        i = i.strip("\n")
        op,arg1,arg2,res = i.split()
        if(op in ["+","-","*","/"]):
            if(arg1.isdigit() and arg2.isdigit()):
                result = eval(arg1+op+arg2)
                dictValues[res] = result
                print("=",result,"NULL",res)
                constantFoldedList.append(["=",result,"NULL",res])
            elif(arg1.isdigit()):
                if(arg2 in dictValues):
                    result = eval(arg1+op+dictValues[arg2])
                    dictValues[res] = result
                    print("=",result,"NULL",res)
                    constantFoldedList.append(["=",result,"NULL",res])
                else:
                    print(op,arg1,arg2,res)
                    constantFoldedList.append([op,arg1,arg2,res])
            elif(arg2.isdigit()):
                if(arg1 in dictValues):
                    result = eval(dictValues[arg1]+op+arg2)
                    dictValues[res] = result
                    print("=",result,"NULL",res)
                    constantFoldedList.append(["=",result,"NULL",res])
                else:
                    print(op,arg1,arg2,res)
                    constantFoldedList.append([op,arg1,arg2,res])
            else:
                flag1=0
                flag2=0
                arg1Res = arg1
                if(arg1 in dictValues):
                    arg1Res = str(dictValues[arg1])
                    flag1 = 1
                arg2Res = arg2
                if(arg2 in dictValues):
                    arg2Res = str(dictValues[arg2])
                    flag2 = 1
                if(flag1==1 and flag2==1):
                    result = eval(arg1Res+op+arg2Res)
                    dictValues[res] = result
                    print("=",result,"NULL",res) 
                    constantFoldedList.append(["=",result,"NULL",res])
                else:
                    print(op,arg1Res,arg2Res,res)
                    constantFoldedList.append([op,arg1Res,arg2Res,res])
                
        elif(op=="="):
            if(arg1.isdigit()):
                dictValues[res]=arg1
                print("=",arg1,"NULL",res)
                constantFoldedList.append(["=",arg1,"NULL",res])
            else:
                if(arg1 in dictValues):
                    print("=",dictValues[arg1],"NULL",res)
                    constantFoldedList.append(["=",dictValues[arg1],"NULL",res])
                else:
                    print("=",arg1,"NULL",res)
                    constantFoldedList.append(["=",arg1,"NULL",res])
        
        else:
            print(op,arg1,arg2,res)
            constantFoldedList.append([op,arg1,arg2,res])

    print("\n")
    print("Constant folded expression - ")
    print("--------------------")
    for i in constantFoldedList:
        if(i[0]=="="):
            print(i[3],i[0],i[1])
            constantFoldedExpression.append([i[3], i[0], i[1]])
        elif(i[0] in ["+","-","*","/","==","<=","<",">",">="]):
            print(i[3],"=",i[1],i[0],i[2])
            constantFoldedExpression.append([i[3],"=",i[0], i[2]])
        elif(i[0] in ["if","goto","label","not"]):
            if(i[0]=="if"):
                print(i[0],i[1],"goto",i[3])
                constantFoldedExpression.append([i[0], i[1],"goto",i[3]])
            if(i[0]=="goto"):
                print(i[0],i[3])
                constantFoldedExpression.append([i[0], i[3]])
            if(i[0]=="label"):
                print(i[3],":")
                constantFoldedExpression.append([i[3], ":"])
            if(i[0]=="not"):
                print(i[3],"=",i[0],i[1])
                constantFoldedExpression.append([i[0], i[1]])

    print("\n")
    print("After dead code elimination - ")
    print("------------------------------")
    for i in constantFoldedList:
        if(i[0]=="="):
            pass
        elif(i[0] in ["+","-","*","/","==","<=","<",">",">="]):
            print(i[3],"=",i[1],i[0],i[2])
            deadCodeElemination.append([i[3], "=", i[1], i[0], i[2]])
        elif(i[0] in ["if","goto","label","not"]):
            if(i[0]=="if"):
                print(i[0],i[1],"goto",i[3])
                deadCodeElemination.append([i[0],i[1], "goto"])

            if(i[0]=="goto"):
                print(i[0],i[3])
                deadCodeElemination.append([i[0], "=", i[3]])

            if(i[0]=="label"):
                print(i[3],":")
                deadCodeElemination.append([i[3], ":"])

            if(i[0]=="not"):
                print(i[3],"=",i[0],i[1])
                deadCodeElemination.append([i[3], "=", i[0], i[1]])
    output_string = ""
    output_string += "Quadruple form after Constant Folding\n"
    output_string += "-------------------------------------\n"
    for i in constantFoldedList:
        output_string += str(i) + "\n"

    output_string += "\n"
    output_string += "Constant folded expression - \n"
    output_string += "--------------------\n"
    for i in constantFoldedExpression:
        output_string += str(i) + "\n"

    output_string += "\n"
    output_string += "After dead code elimination \n"
    output_string += "--------------------\n"
    for i in deadCodeElemination:
        output_string += str(i) + "\n"

    return render_template('index.html',opti=output_string)

# @app.route('/', methods=['POST','GET'])
# def my_form_post():
# if request.method == "POST":
#         text = request.form['text']
#         return
#     # processed_text = text.upper()
#     else:
#         return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True,port=5000)
# @app.route('/')
# def home():    
#     return send_file('output.txt', as_attachment=True)