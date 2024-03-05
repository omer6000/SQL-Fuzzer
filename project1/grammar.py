# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.
from fuzzingbook.GeneratorGrammarFuzzer import opts

grammar = {
    "<start>": ["<create_table>;","<with> <select>;","<create_view>;","<delete><returning>;",
                "<create_index>;","<drop_index>;","<drop_table>;","<reindex>;","<pragma>;",
                "<drop_view>;","<insert><returning>;",("<comment>",opts(prob=0.003)),"<transaction>;","select <core_functions>;",("<attach_db>;",opts(prob=0.003)),("<detach_db>;",opts(prob=0.003)),
                "<create_virtual_table>;","<func_query>;","<alter_table>;",("<analyze>;",opts(prob=0.003)),("<explain>",opts(prob=0.003)),("<vacuum>;",opts(prob=0.003)),"<savepoint>;","<create_trigger>;","<drop_trigger>;","<update>;"],
    "<returning>": [(" RETURNING *",opts(prob=0.1)),""],
    "<pragma>": ["PRAGMA <schema_name><pragma_function> = <pragma_val>","PRAGMA <schema_name><pragma_function> (<pragma_val>)",("PRAGMA <pragma_function>",opts(prob=0.7))],
    "<pragma_val>" : ["<pragma_true>","<pragma_false>","'<input_str>'","<integer>"],
    "<pragma_true>": ["1", "yes", "true" ,"on"], 
    "<pragma_false>": ["0" ,"no" ,"false" ,"off"],
    "<reindex>": ["REINDEX <schema_name><name>"],
    # "<update>": ["update <name> set <name> = <name> from <name>"],
    "<update>": ["update<insert_or> tablename<name> set <update_cols> <update_from>"],
    "<update_cols>": ["col<name> = <name>","col<name> = <name> , <update_cols>"],
    "<update_from>": ["from tablename2<name>","from (<select>)",("",opts(prob=0.6))], 
    "<savepoint>": ["SAVEPOINT <string>","ROLLBACK TRANSACTION TO SAVEPOINT <string>","RELEASE SAVEPOINT <string>"],
    "<drop_trigger>": ["drop trigger <if_exists> <schema_name>triggername<name> "],
    "<vacuum>": ["VACUUM","VACUUM into 'db/<string>.sqlite'"],
    "<create_trigger>": ["create<temp>trigger triggername<name><exists><trigger_cond1> <trigger_cond2> <trigger_row>on tablename<name> BEGIN <trigger_body>; END"],
    "<create_view>": ["create<temp>view <schema_name>viewname<name><exists> as ( <with> <select> )"],
    "<create_table>": ["create<temp>table <schema_name>tablename<name><exists>(<table_columns_def>)<table_options>",("create<temp>table <schema_name>tablename<name><exists> AS <with> <select>",opts(prob=0.3))],
    "<alter_table>": ["ALTER TABLE <schema_name><name> RENAME TO <schema_name><name>","ALTER TABLE <schema_name><name> RENAME COLUMN <name> TO <name>",
                      "ALTER TABLE <schema_name><name> ADD COLUMN <name> <data_type> <col_constraint>","ALTER TABLE <schema_name><name> DROP COLUMN <name>"],
    "<exists>": [" IF NOT EXISTS "," "],
    "<temp>": [" TEMP "," TEMPORARY "," "],
    "<table_options>": [" WITHOUT ROWID"," STRICT"," STRICT, WITHOUT ROWID",("",opts(prob=0.4))],
    "<trigger_cond1>": ["AFTER","BEFORE","INSTEAD OF"],
    "<trigger_cond2>": ["DELETE","INSERT","UPDATE"],
    "<trigger_row>": ["FOR EACH ROW ",""],
    "<trigger_body>": ["<delete>","<insert>"],
    "<explain>": ["EXPLAIN <start>","EXPLAIN QUERY PLAN <start>"],
    "<analyze>": ["ANALYZE <name>"],
    "<func_query>": ["select <distinct> <funcs> from <name>"],
    "<funcs>": ["<func>","<func>,<funcs>"],
    "<func>": ["avg(par)","min(par)","max(par)","count(par)","count(*)","sum(par)","total(par)","group_concat(par)","group_concat(par,';')","string_agg(par,';')"],
    "<create_virtual_table>": ["CREATE VIRTUAL TABLE <name> USING fts3(content TEXT)",
                               "CREATE VIRTUAL TABLE <name> USING json1(content TEXT)"],
    "<comment>": ["-- <start>","/* <start> */"],
    "<core_functions>": ["<core_func>","<core_func>,<core_functions>"],
    # "<core_func>": ["abs(<integer>)","char(<int_args>)",
    #                      "coalesce(<coalesce_args>)","length('<string>')"
    #                      ,"lower('<string>')","upper('<string>')","random()","max(<int_args>)"
    #                      ,"round(<pos_integer>.<pos_integer>,<num>)",
    #                      "substr('<string>',<num>,<num>)",
    #                      "unicode('<string>')",
    #                      "zeroblob(<integer>)"
    #                      ,"soundex('<string>')"
    #                      ,"hex('<string>')"
    #                      ,"instr('<string>','<string>')"
    #                      ,"rtrim(' <string>  ')"
    #                      ,"quote('<string>')"
    #                      ,"replace('<string>','<string>','<string>')"
    #                      ,"changes()","total_changes(),<typeof>","unhex('<string>')"
    #                      ,"sqlite_version()","sqlite_source_id()","sign(<integer>)"
    #                      ,"last_insert_rowid()","randomblob(<pos_integer>)","load_extension('<string>.so')"
    #                      ,"likely(<integer>)"
    #                      ,"date('now')"
    #                      ,"datetime('now')"
    #                      ,"time('now')"
    #                      ,"julianday('now')"
    #                      ,"strftime('%Y-%m-%d %H:%M:%S', 'now')"
    #                      ,"unixepoch('now')"
    #                      ,"timediff('now','now')"
    #                      ],
    "<core_func>": ["abs(<column_insert>)","char(<insert_vals>)",
                         "coalesce(<insert_vals>)","length(<column_insert>)"
                         ,"lower(<column_insert>)","upper(<column_insert>)","random()","max(<insert_vals>)"
                         ,"round(<column_insert>,<num>)",
                         "substr(<column_insert>,<num>,<num>)",
                         "unicode(<column_insert>)",
                         "zeroblob(<column_insert>)"
                         ,"soundex(<column_insert>)"
                         ,"hex(<column_insert>)"
                         ,"instr(<column_insert>,<column_insert>)"
                         ,"rtrim(' <ascii_chars>  ')"
                         ,"quote(<column_insert>)"
                         ,"replace(<column_insert>,<column_insert>,<column_insert>)"
                         ,"changes()","total_changes(),<typeof>","unhex(<column_insert>)"
                         ,"sqlite_version()","sqlite_source_id()","sign(<column_insert>)"
                         ,"last_insert_rowid()","randomblob(<column_insert>)","load_extension('<ascii_chars>.so')"
                         ,"likely(<column_insert>)"
                         ,"date('now')"
                         ,"datetime('now')"
                         ,"time('now')"
                         ,"julianday('now')"
                         ,"strftime('%Y-%m-%d %H:%M:%S', 'now')"
                         ,"unixepoch('now')"
                         ,"timediff('now','now')"
                         ],
    "<typeof>" : ["typeof(null)","typeof('<ascii_chars>')","typeof(<pos_integer>.<pos_integer>)"],
    "<attach_db>" : ["ATTACH DATABASE 'db/<ascii_chars>.db' as <ascii_chars>"],
    "<detach_db>": ["DETACH DATABASE <name>"],
    # "<coalesce_args>": ["NULL","'<ascii_chars>'","'<ascii_chars>',<coalesce_args>","NULL,<coalesce_args>"],
    # "<int_args>": ["<integer>","<integer>,<int_args>"],
    "<transaction>" :["BEGIN TRANSACTION","COMMIT","ROLLBACK"],
    "<insert>": ["insert<insert_or> into tablename<name> <insert_cols> <insert_body>","replace into tablename<name> <insert_cols> <insert_body>"],
    "<insert_body>": ["values (<insert_vals>)","default values","<select>"],
    "<insert_cols>": [(" ( <insert_col> ) ",opts(prob=0.7)),""],
    "<insert_col>": ["col<string> , <insert_col>",("col<string>",opts(prob=0.7))],
    "<insert_or>": [" OR<cons_resolution>",""],
    "<drop_table>": ["drop table <if_exists> <schema_name>tablename<name> "],
    "<if_exists>": [("if exists",opts(prob=0.35)),""],
    "<drop_index>": ["drop index <if_exists> <schema_name>indexname<name> "],
    "<drop_view>": ["drop view <if_exists> <schema_name>viewname<name> "],
    "<create_index>": ["create index <name> on <name> (<index_cols>)"],
    "<index_cols>": ["<string>","<string>,<index_cols>"],
    "<delete>" : ["delete from <name>"],
    "<select>" : [("select <distinct> * from tablename<name> <indexed_by> <order_by>",opts(prob=0.5)),"select <distinct> <select_col> from tablename<name> <where> <order_by> <select_limit>",("<select> union <select>",opts(prob=0.2))],
    "<select_limit>":[("limit <column_insert>",opts(prob=0.05)),"limit <pos_integer>",""],
    "<with>": ["WITH <recursive> <with_body>",("",opts(prob=0.9))],
    "<with_body>": ["<name> as <materialized> ( <select> ), <with_body>",("<recursive> <name> as <materialized> ( <select> )",opts(prob=0.8))],
    "<recursive>": ["recursive",("",opts(prob=0.8))],
    "<materialized>": [" NOT MATERIALIZED "," MATERIALIZED ",""],
    "<order_by>" : ["order by ordercol",""],
    "<where>": ["where <where_cond>",("",opts(prob=0.6))],
    "<where_cond>": ["wherecol IS NULL","wherecol IS NOT NULL",("<where_cond> AND <where_cond>",opts(prob=0.1)),("<where_cond> OR <where_cond>",opts(prob=0.1)),"wherecol <where_op> <column_insert>"],
    "<where_op>": [">","=","!=","LIKE","NOT LIKE","<=",">="],
    "<distinct>": ["DISTINCT","ALL",""],
    "<indexed_by>": ["INDEXED BY indexname<name>",""],
    "<schema_name>": [("<name>.",opts(prob=0.1)),""],
    "<name>": ["<string>",("<keyword_str>",opts(prob=0.1))],
    "<insert_vals>": [("<column_insert>",opts(prob=0.7)), "<column_insert>,<insert_vals>"],
    "<table_columns_def>": ["<column> <col_constraint>", "<column> <col_constraint>,<table_columns_def>",("<table_constraint>",opts(prob=0.1)),("<table_constraint>,<table_columns_def>",opts(prob=0.05))],
    "<table_constraint>": ["PRIMARY KEY(<select_col>)<conflict_clause><cons_resolution>","UNIQUE(<select_col>)<conflict_clause><cons_resolution>","FOREIGN KEY(<select_col>) REFERENCES <name> (<select_col>)","DEFAULT <column_insert>"],
    "<select_col>": ["<string>,<select_col>","<string>"],
    "<col_constraint>": [("",opts(prob=0.7)),"<col_cons_primarykey><conflict_clause><cons_resolution>","UNIQUE<conflict_clause><cons_resolution>","NOT NULL<conflict_clause><cons_resolution>"],
    "<conflict_clause>": [" ON CONFLICT",""],
    "<col_cons_primarykey>": ["PRIMARY KEY","PRIMARY KEY ASC","PRIMARY KEY ASC"],
    "<cons_resolution>": [" ROLLBACK"," ABORT"," FAIL"," IGNORE"," REPLACE"],
    "<column>": ["<name> <data_type>"],
    "<data_type>": ["TEXT","INTEGER","REAL","BLOB","NUMERIC",""],
    # "<column_insert>" : ["'<string>'","<integer>","<float>","<string>","NULL"],
    "<column_insert>" : ["'<input_str>'","<integer>","<float>","NULL"],
    "<input_str>": ["<ascii_chars>","<ascii_chars><input_str>"],
    "<ascii_chars>": [chr(i) for i in range(32,127)],
    "<string>": ["<letter>","<letter><string>"],
    "<integer>": ["-<num>","<num>","<integer><num>"], #includes negative numbers
    "<float>": ["-<pos_integer>.<pos_integer>","<pos_integer>.<pos_integer>"],
    "<pos_integer>": ["<num>","<pos_integer><num>"],
    "<num>": [str(i) for i in range(10)],
    "<letter>": [chr(i) for i in range(ord('a'),ord('z')+1)]+[chr(i) for i in range(ord('A'),ord('Z')+1)]+['_']+[str(i) for i in range(10)],
    "<keyword_str>": ['"<keyword>"'],
    "<keyword>" : ["ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ALWAYS", "ANALYZE", "AND", "AS", "ASC", "ATTACH",
    "AUTOINCREMENT", "BEFORE", "BEGIN", "BETWEEN", "BY", "CASCADE", "CASE", "CAST", "CHECK", "COLLATE",
    "COLUMN", "COMMIT", "CONFLICT", "CONSTRAINT", "CREATE", "CROSS", "CURRENT", "CURRENT_DATE",
    "CURRENT_TIME", "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE", "DEFERRED", "DELETE", "DESC",
    "DETACH", "DISTINCT", "DO", "DROP", "EACH", "ELSE", "END", "ESCAPE", "EXCEPT", "EXCLUDE", "EXCLUSIVE",
    "EXISTS", "EXPLAIN", "FAIL", "FILTER", "FIRST", "FOLLOWING", "FOR", "FOREIGN", "FROM", "FULL",
    "GENERATED", "GLOB", "GROUP", "GROUPS", "HAVING", "IF", "IGNORE", "IMMEDIATE", "IN", "INDEX",
    "INDEXED", "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT", "INTO", "IS", "ISNULL", "JOIN",
    "KEY", "LAST", "LEFT", "LIKE", "LIMIT", "MATCH", "MATERIALIZED", "NATURAL", "NO", "NOT", "NOTHING",
    "NULL", "NULLS", "OF", "OFFSET", "ON", "OR", "ORDER", "OTHERS", "OUTER", "OVER", "PARTITION", "PLAN",
    "PRAGMA", "PRECEDING", "PRIMARY", "QUERY", "RAISE", "RANGE", "RECURSIVE", "REFERENCES", "REGEXP",
    "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT", "RETURNING", "RIGHT", "ROLLBACK", "ROW",
    "ROWS", "SAVEPOINT", "SELECT", "SET", "TABLE", "TEMP", "TEMPORARY", "THEN", "TIES", "TO",
    "TRANSACTION", "TRIGGER", "UNBOUNDED", "UNION", "UNIQUE", "UPDATE", "USING", "VACUUM", "VALUES",
    "VIEW", "VIRTUAL", "WHEN", "WHERE", "WINDOW", "WITH", "WITHOUT"],
    "<pragma_function>" : [
    "analysis_limit",
    "application_id",
    "auto_vacuum",
    "automatic_index",
    "busy_timeout",
    "cache_size",
    "cache_spill",
    "case_sensitive_like",
    "cell_size_check",
    "checkpoint_fullsync",
    "collation_list",
    "compile_options",
    "count_changes",
    "data_store_directory",
    "data_version",
    "database_list",
    "default_cache_size",
    "defer_foreign_keys",
    "empty_result_callbacks",
    "encoding",
    "foreign_key_check",
    "foreign_key_list",
    "foreign_keys",
    "freelist_count",
    "full_column_names",
    "fullfsync",
    "function_list",
    "hard_heap_limit",
    "ignore_check_constraints",
    "incremental_vacuum",
    "index_info",
    "index_list",
    "index_xinfo",
    "integrity_check",
    "journal_mode",
    "journal_size_limit",
    "legacy_alter_table",
    "legacy_file_format",
    "locking_mode",
    "max_page_count",
    "mmap_size",
    "module_list",
    "optimize",
    "page_count",
    "page_size",
    "parser_trace",
    "pragma_list",
    "query_only",
    "quick_check",
    "read_uncommitted",
    "recursive_triggers",
    "reverse_unordered_selects",
    "schema_version",
    "secure_delete",
    "shorthand_column_names",
    "soft_heap_limit",
    "stats",
    "synchronous",
    "table_info",
    "table_list",
    "table_xinfo",
    "temp_store",
    "temp_store_directory",
    "threads",
    "trusted_schema",
    "user_version",
    "vdbe_addoptrace",
    "vdbe_debug",
    "vdbe_listing",
    "vdbe_trace",
    "wal_autocheckpoint",
    "wal_checkpoint",
    "writable_schema"]
}