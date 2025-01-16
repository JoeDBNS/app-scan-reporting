path_options = [
    'admin',
    'reports'
]

path_choice = input('Do you want to run [admin] or [reports]? ').lower().strip()

while (path_choice not in path_options):
    print('invalid entry')

    path_choice = input('\nDo you want to run [admin] or [reports]? ').lower().strip()

if (path_choice == 'admin'):
    print('admin')
elif (path_choice == 'reports'):
    print('reports')