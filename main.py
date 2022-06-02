import json
from take_rasp_body import RaspBodyParser


TABLE_PATH = 'full_result.json'
g_params_path = 'g_param_table.json'

with open(g_params_path, encoding='utf8') as file:
    g_params: list = json.load(file)

answer = []

print(len(g_params))
for group in g_params:
    g = group['value']
    ref = f'https://rasp.guap.ru/?g={g}'
    print(g)
    rasp = RaspBodyParser(ref)
    answer.append(rasp.crt_dict())

with open(TABLE_PATH, 'w', encoding='utf8') as file:
    json.dump(answer, file, indent=2, ensure_ascii=False)
