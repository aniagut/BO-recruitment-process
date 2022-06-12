# skills from https://www.itsyourskills.com/purchase-skills-database/
import pandas as pd
import random
import json
import requests
import uuid

names_url = f'https://parseapi.back4app.com/classes/Listofnames_Complete_List_Names?limit=count&keys=Name'
names_headers = {
    'X-Parse-Application-Id': 'cc1IOZpQFg3X3eZ6C9ubnvNcWZPKGlLzCDZdETd4',
    'X-Parse-REST-API-Key': 'ifpPttK7O9BJinGFPs35k9gdYrN13WfvA5S3iHyD'
}


def get_sample_skillset(k: int):
    data = pd.read_excel(r'../resources/Skills.xlsx')
    skillset = []

    for row in data.values:
        skillset.append(row[0])
    random.shuffle(skillset)

    try:
        random_indexes = random.sample(range(0, len(skillset) - 1), k)
    except ValueError:
        print('Sample size exceeded population size.')
        return []

    solution = []
    for idx in random_indexes:
        solution.append(skillset[idx])
    return solution


def get_sample_candidates_names(m: int):
    complete_url = names_url.replace("count", str(m))
    data = json.loads(requests.get(complete_url, headers=names_headers).content.decode('utf-8'))
    solution = []
    for result in data['results']:
        solution.append(result['Name'])
    return solution


def get_sample_positions_ids(n: int):
    solution = []
    for _ in range(n):
        solution.append(uuid.uuid4().__str__())
    return solution


# k - num of skills, m - num of candidates, n - num of positions
def get_sample_case(k: int, m: int, n: int):
    solution = dict()
    skills = get_sample_skillset(k)
    candidates = get_sample_candidates_names(m)
    positions = get_sample_positions_ids(n)

    candidates_skills = [[] for _ in range(m)]
    for idx in range(m):
        for _ in range(k):
            candidates_skills[idx].append(random.randint(0, 10))

    positions_skills = [[] for _ in range(n)]
    for idx in range(n):
        for _ in range(k):
            positions_skills[idx].append(random.randint(0, 100))

    solution['skills'] = skills
    solution['candidates'] = candidates
    solution['positions'] = positions
    solution['candidates_skills'] = candidates_skills
    solution['position_skills'] = positions_skills

    return solution