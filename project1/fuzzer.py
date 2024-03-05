# from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
# from fuzzingbook.Fuzzer import RandomFuzzer
import grammar
import random
import os
# import shutil

class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
    
    def setup_fuzzer(self):
        # This function may be changed.
        # self.fuzzer = EvenFasterGrammarFuzzer(self.grammar)
        # self.random_fuzz = RandomFuzzer(max_length=15,char_start=ord('a'), char_range=26)
        self.nums = [i for i in range(500)]
        self.fuzzer = ProbabilisticGrammarFuzzer(self.grammar)
        self.tables = {"t1":[['a1'],['a2']],"t2":[['a1'],['a2']]} #table as key. List of columns as value [[col1, type], [col2, type],..]
        self.views = {"v1":[['a1'],['a2']],"v2":[['a1'],['a2']]}
        self.indexes = {"t3":["i1","i2"]} #key is table name. Value is list
        self.db = {"abc":''}
        self.triggers = {"trig1":""}
        self.savepoints = {"save1":""}
        if os.path.exists("db/") == False:
            # shutil.rmtree("db/")
            os.mkdir("db/")
        # if os.path.exists("db/"):
        #     shutil.rmtree("db/")
        # os.mkdir("db/")
        # with open("input.txt", 'w') as file:
        #     pass

    def process_input(self,input):
        # if "/*" in input or "--" in input:
        input = input.strip()
        if input.startswith(("/*","--")):
            return input
        # elif "create trigger" in input or "create TEMP trigger" in input or "create TEMPORARY trigger" in input:
        elif input.startswith(("create trigger", "create TEMP trigger", "create TEMPORARY trigger")):
            # if len(self.tables) != 0:
            table_name = ""
            trigger_name = ""
            input_list = input.split(" ")
            for i in range(len(input_list)):
                if "triggername" in input_list[i]:
                    if random.random() < 0.1:
                        trigger_name = random.choice(list(self.triggers.keys()))
                    else:
                        # index_name = random.choice(list(self.indexes.keys()))[0]
                        input_list[i] = input_list[i].replace("triggername","")
                        trigger_name = input_list[i]
                elif "tablename" in input_list[i]:
                    table_name = random.choice(list(self.tables.keys()))
                    input_list[i] = input_list[i].replace(input_list[i],table_name)
            self.triggers[trigger_name] = ''
            input = " ".join(input_list)
            begin_split = input.split("BEGIN ")
            begin_query = begin_split[1].split(";")[0]+";"
            begin_query = self.process_input(begin_query)
            if begin_query[-1] != ";":
                begin_query += ";"
            input = begin_split[0] + "BEGIN " + begin_query + " END;"

        elif input.startswith("update"):
            # input_list = input.split(" ")
            # table_name = random.choice(list(self.tables.keys()))
            # input_list[1] = table_name
            # col1 = random.choice(self.tables[table_name])[0]
            # col2 = random.choice(self.tables[table_name])[0]
            # if random.random() < 0.1:
            #     table_name = random.choice(list(self.tables.keys()))

            # input_list[3] = col1
            # input_list[5] = col2
            # if "RETURNING" not in input_list[-1]:
            #     input_list[-1] = table_name+";"
            # else:
            #     input_list[-2] = table_name

            input_list = input.split(" ")
            tablename = random.choice(list(self.tables.keys()))
            for i in range(len(input_list)):
                if input_list[i].startswith("tablename"):
                    if random.random() < 0.1:
                        input_list[i] = input_list[i].replace(input_list[i],random.choice(list(self.tables.keys())))
                    else:
                        input_list[i] = input_list[i].replace(input_list[i],tablename)
                elif input_list[i].startswith("tablename2"):
                    input_list[i] = input_list[i].replace(input_list[i],random.choice(list(self.tables.keys())))
                elif input_list[i].startswith("col"):
                    col = random.choice(self.tables[tablename])[0]
                    input_list[i] = input_list[i].replace(input_list[i],col)
            input = " ".join(input_list)
            select = input.split("(",1)
            if len(select) > 1:
                select[1] = self.process_input(select[-1][:-2]) + ");"
            input = "(".join(select)

        # elif "drop trigger" in input:
        elif input.startswith("drop trigger"):
            # if len(self.triggers) != 0:
            trigger_name = random.choice(list(self.triggers.keys()))
            input_list = input.split(" ")
            for i in range(len(input_list)):
                if "triggername" in input_list[i]:
                    input_list[i] = input_list[i].replace(input_list[i],trigger_name)
            input = " ".join(input_list)
        # elif "create table" in input or "create TEMP table" in input or "create TEMPORARY table" in input:
        elif input.startswith(("create table", "create TEMP table", "create TEMPORARY table")):
            try:
                cols = input.split("(")[1].split(")")[0].split(",")
                cols = list(map(lambda x: x.split(" "),cols))
                table_name = ""
                input_list = input.split(" ")
                for i in range(len(input_list)):
                    if "tablename" in input_list[i]:
                        if random.random() < 0.1: #20% chance of choosing same table name
                            input_list[i] = random.choice(list(self.tables.keys()))
                            break
                        input_list[i] = input_list[i].replace("tablename","")
                        table_name = input_list[i]
                        break
                self.tables[table_name] = cols
                input = " ".join(input_list)
            except:
                pass

        elif input.startswith(("select","WITH")) and "from" in input:
            # print(input)
            # WITH  recursive zC as NOT MATERIALIZED (select ALL * from tablenameGtR INDEXED BY indexnameHq order by ordercol) select DISTINCT * from tablenamej  ;
            # WITH  p zC as NOT MATERIALIZED (select ALL * from CJX INDEXED BY i1 order by p select DISTINCT * from CJX  ;

            select_split = input.split(" union ")
            if len(select_split) > 1:
                # select_split = input.split(" union ")
                for i in range(len(select_split)):
                    select_split[i] = self.process_input(select_split[i])
                input = " union ".join(select_split)
            # elif len(self.tables) != 0:
            else:
                input_list = input.split(" ")
                # table_name = random.choice(list(self.tables.keys())+list(self.views.keys()))
                table_view_dict = {**self.tables, **self.views}
                table_name = random.choice(list(table_view_dict.keys()))
                for i in range(len(input_list)):
                    if "tablename" in input_list[i]:
                        if random.random() < 0.1:
                            input_list[i] = input_list[i].replace(input_list[i],random.choice(list(table_view_dict.keys())))
                        else:
                            input_list[i] = input_list[i].replace(input_list[i],table_name)
                    elif "indexname" in input_list[i] and len(self.indexes) != 0:
                        index_table = random.choice(list(self.indexes.keys()))
                        index_name = random.choice(self.indexes[index_table])
                        if random.random() < 0.1:
                            index_name += index_name[-1]
                        input_list[i] = input_list[i].replace(input_list[i],index_name)
                            
                    elif "ordercol" in input_list[i]:
                        input_list[i] = ""
                        for col in table_view_dict[table_name]:
                            input_list[i] += col[0] + ","
                        input_list[i] = input_list[i][:-1]
                    elif i == 2 and input_list[i] != "*":
                        if "par" in input:
                            while "par" in input:
                                input = input.replace("par",random.choice(table_view_dict[table_name])[0],1)   
                        else:
                            input_list[i] = ""
                            for col in table_view_dict[table_name]:
                                input_list[i] += col[0] + ","
                            input_list[i] = input_list[i][:-1]
                    elif "wherecol" in input_list[i]:
                        input_list[i] = random.choice(table_view_dict[table_name])[0]
                        
                input = " ".join(input_list)
        
        # elif "insert into" in input:
        # elif input.startswith("insert") or input.startswith("replace"):
        elif input.startswith(("insert", "replace")):
            # if len(self.tables) != 0:
            # print(input)
            table_name = random.choice(list(self.tables.keys()))
            input_list = input.split(" ")
            for i in range(len(input_list)):
                if input_list[i].startswith("tablename"):
                    # print("hii")
                    if random.random() < 0.1:
                        input_list[i] = input_list[i].replace(input_list[i],random.choice(list(self.tables.keys())))
                    else:
                        input_list[i] = input_list[i].replace(input_list[i],table_name)
                    break
                elif input_list[i].startswith("col"):
                    col = random.choice(self.tables[table_name])[0]
                    input_list[i] = input_list[i].replace(input_list[i],col)
            input = " ".join(input_list)
            # input_body_split = input.split("values")
            if len(input.split("values")) == 1: #select statement
                select_split = input.split("select",1)
                # print("select" + select_split[1])
                input = select_split[0] +" " +self.process_input("select" + select_split[1])
            # print(input)
        # elif "delete" in input:
        elif input.startswith("delete"):
            # if len(self.tables) != 0:
            table_name = random.choice(list(self.tables.keys()))
            # input = f"delete from {table_name};"
            input_list = input.split(" ")
            input_list[2] = table_name
            input = " ".join(input_list)
        # elif "create view" in input:
        elif input.startswith(("create view", "create TEMP view", "create TEMPORARY view")):
            # if len(self.tables) != 0:
                # view_name = self.random_fuzz.fuzz()
                # self.views[view_name] = ''
                # table_name = random.choice(list(self.tables.keys()))
                # input = f"create view {view_name} as (select * from {table_name});" #7:52
# create view viewnameW IF NOT EXISTS  as (WITH   u as NOT MATERIALIZED (select ALL * from tablenameS  order by ordercol) select DISTINCT * from tablenameD   union select DISTINCT * from tablenamei  );
            # if "WITH" not in input:
            view_name = ""
            split_view = input.split(" as ",1)
            input_list = split_view[0].split(" ")
            for i in range(len(input_list)):
                if "viewname" in input_list[i]:
                    if random.random() < 0.1:
                        input_list[i] = random.choice(list(self.views.keys()))
                    else:
                        input_list[i] = input_list[i].replace("viewname","")
                    view_name = input_list[i]
                    break
            split_view[0] = " ".join(input_list)
            # print(input)
            # print(split_view[-1][1:-2])
            select = self.process_input(split_view[-1][1:-2]) #process select statement using recursion
            # print(select)
            try:
                cols = [[x] for x in select.split(" ")[2].split(",")]
                self.views[view_name] = cols
                split_view[-1] = f"({select});"
                input =" as ".join(split_view)
            except:
                pass

        # elif "drop table" in input:
        elif input.startswith("drop table"):
            # if len(self.tables) != 0:
            table_name = random.choice(list(self.tables.keys()))
            # del self.tables[table_name]
            input_list = input.split(" ")
            for i in range(len(input_list)):
                if "tablename" in input_list[i]:
                    input_list[i] = input_list[i].replace(input_list[i],table_name)
            input = " ".join(input_list)
                
        # elif "drop view" in input:
        elif input.startswith("drop view"):

            if len(self.views) != 0:
                view_name = random.choice(list(self.views.keys()))
                # del self.views[view_name]
                # input = f"drop view {view_name};"
                input_list = input.split(" ")
                for i in range(len(input_list)):
                    if "viewname" in input_list[i]:
                        input_list[i] = input_list[i].replace(input_list[i],view_name)
                input = " ".join(input_list)
        # elif "create index" in input:
        elif input.startswith("create index"):
            # if len(self.tables) != 0:
            table_name = random.choice(list(self.tables.keys()))
            input = input.split("on ")[0]+f"on {table_name}("
            for col in self.tables[table_name]:
                input += col[0]+","
            input = input[:-1] + ");"
            index_name = None
            if random.random() < 0.1:
                index_name = self.indexes[random.choice(list(self.indexes.keys()))][0]
            else:
                index_name = input.split(" ")[2]
            if table_name in self.indexes:
                self.indexes[table_name].append(index_name)
            else:    
                self.indexes[table_name] = [index_name]
        # elif "drop index" in input:
        elif input.startswith("drop index"):
            # if len(self.indexes) != 0:
            table_name = random.choice(list(self.indexes.keys()))
            # index_name = self.indexes[table_name].pop()
            index_name = random.choice(self.indexes[table_name])
            input_list = input.split(" ")
            for i in range(len(input_list)):
                if "indexname" in input_list[i]:
                    input_list[i] = input_list[i].replace(input_list[i],index_name)
            input = " ".join(input_list)
            # if len(self.indexes[table_name]) == 0:
            #     del self.indexes[table_name]
        # elif "ATTACH DATABASE" in input:
        elif input.startswith("ATTACH DATABASE"):

            db = input.split(" ")
            db_path = db[2].replace("'","")
            db_name = db[-1][:-1]
            self.db[db_name] = db_path
        # elif "DETACH DATABASE" in input:
        elif input.startswith("DETACH DATABASE"):

            # if len(self.db) != 0:
            db_name = random.choice(list(self.db.keys()))
            input = f"DETACH DATABASE {db_name};"
                # del self.db[db_name]
        elif input.startswith("REINDEX"):
            arg_list = list(self.tables.keys())+list(self.indexes.keys())
            # if len(arg_list) != 0:
            input = f"REINDEX {random.choice(arg_list)};"
    
        elif input.startswith("ALTER"):
            # if len(self.tables) != 0:
            table_name = random.choice(list(self.tables.keys()))
            if "RENAME TO" in input:
                input_list = input.split(" ")
                input_list[2] = table_name
                new_tablename = input_list[-1][:-1]
                self.tables[new_tablename] = self.tables[table_name] 
                input = " ".join(input_list)
            elif "RENAME COLUMN" in input:
                input_list = input.split(" ")
                input_list[5] = random.choice(self.tables[table_name])[0]
                input = " ".join(input_list)
            elif "DROP COLUMN" in input:
                input_list = input.split(" ")
                input_list[-1] = random.choice(self.tables[table_name])[0]+";"
                input = " ".join(input_list)
        
        # elif "ANALYZE" in input:
        elif input.startswith("ANALYZE"):
            arg_list = list(self.tables.keys())+list(self.indexes.keys())
            # if len(arg_list) != 0:
            input = f"ANALYZE {random.choice(arg_list)};"
        elif "SAVEPOINT" in input:
            input_list = input.split(" ")
            size = len(input_list)
            # n_savepoint = len(self.savepoints)
            if size == 2:
                savepoint = input_list[-1][:-1]
                self.savepoints[savepoint] = ''
            # elif n_savepoint > 0:
            else:
                if random.random() < 0.1:
                    savepoint ="abcdef"
                else:
                    savepoint = random.choice(list(self.savepoints.keys()))
                input_list[-1] = savepoint+";"
            " ".join(input_list)
        return input
    
    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        input = self.fuzzer.fuzz()
        try:
            input = self.process_input(input)
            # with open("input.txt", 'a+') as file:
            #     file.write(input + '\n')
            return input
        except:
            # raise Exception
            return input