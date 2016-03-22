"""
json_generator.py
desc: Create a collection of companies according to specific criteria defined in views.py

"""

import os
import json
from views import views


class Progress:
    def __init__(self, view, max_val, step=1):
        self.cur = 0
        self.max = max_val - 1
        self.view = view
        self.step = step

    def update(self):
        percentage = round(self.cur / self.max * 100, 2)
        if percentage < 100.00:
            print(self.view['name'] +' - '+str(percentage), end="% \r")
            self.cur += self.step
        else:
            print(self.view['name'] +' - done', end=" - ")


def test_details(model, view):
    details = view['details']
    for test_field, test in details['conditions'].items():
        if test_field in details['defaults']:
            raise KeyError(view['name']+": Cannot test a field marked as default")

        if test_field == 'default':
            for field in details['defaults']:

                if test(model[field]) == False: return False
        elif not test(model[test_field]):
            return False
    return True


def save_json(src, key, path):
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    new_path = os.path.join(path, str(key) + '.json')
    with open(new_path, 'w') as f:
        json.dump(src, f)

def get_json(json_base):
    with open(json_base, 'r') as json_file:
        return json.loads(json_file.readlines()[0])

def view_menu():
    view_len = len(views)
    view_range = range(0, view_len)
    print("Select views to generate files for")
    for n in view_range:
        print('(%d) %s' % (n, views[n]['name']))
    print('(%d) Run all' % view_len)
    choices = list(map(int, "".join(input("Enter comma separated values: ").split()).split(',')))
    if view_len in choices:
        choices = list(view_range)
    return choices


def main():
    choices = view_menu()
    for n in choices:
        view = views[n]
        json_items = get_json(view['base']).items()
        view_list = []
        p = Progress(view=view, max_val=len(json_items))
        for key, model in json_items:
            p.update()
            if test_details(model, view):
                view_list.append(model)
                save_json(model, key, view['save'])
        print("created %d files at %s" % (len(view_list), view['save']), end="\n")

if __name__ == '__main__':
    main()
