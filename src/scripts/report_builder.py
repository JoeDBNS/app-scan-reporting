import modules.module_console as con



def BuildWorksheetAnalytics(data):
    con.Info('\t\tLOAD:\tBUILD ANALYTICS')
    analytics_build = {
        'totals': {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'dynamic': {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'static': {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'component': {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
    }

    for row in data:
        analytics_build[row['simpleDetectionType']][row['severity']['name']] += 1

    analytics_build['totals']['Critical'] = analytics_build['dynamic']['Critical'] + analytics_build['static']['Critical'] + analytics_build['component']['Critical']
    analytics_build['totals']['High'] = analytics_build['dynamic']['High'] + analytics_build['static']['High'] + analytics_build['component']['High']
    analytics_build['totals']['Medium'] = analytics_build['dynamic']['Medium'] + analytics_build['static']['Medium'] + analytics_build['component']['Medium']
    analytics_build['totals']['Low'] = analytics_build['dynamic']['Low'] + analytics_build['static']['Low'] + analytics_build['component']['Low']

    analytics = [
        ['Totals'],
        ['', 'Critical', analytics_build['totals']['Critical']],
        ['', 'High', analytics_build['totals']['High']],
        ['', 'Medium', analytics_build['totals']['Medium']],
        ['', 'Low', analytics_build['totals']['Low']],
        ['Scan Types'],
        ['', 'Dynamic'],
        ['', '', 'Critical', analytics_build['dynamic']['Critical']],
        ['', '', 'High', analytics_build['dynamic']['High']],
        ['', '', 'Medium', analytics_build['dynamic']['Medium']],
        ['', '', 'Low', analytics_build['dynamic']['Low']],
        ['', 'Static'],
        ['', '', 'Critical', analytics_build['static']['Critical']],
        ['', '', 'High', analytics_build['static']['High']],
        ['', '', 'Medium', analytics_build['static']['Medium']],
        ['', '', 'Low', analytics_build['static']['Low']],
        ['', 'Component'],
        ['', '', 'Critical', analytics_build['component']['Critical']],
        ['', '', 'High', analytics_build['component']['High']],
        ['', '', 'Medium', analytics_build['component']['Medium']],
        ['', '', 'Low', analytics_build['component']['Low']]
    ]

    ws_content = {
        'name': 'Analytics',
        'config': {
            'general': {
                'add_headers': False
            },
            'columns': [],
            'rows': {
                'colors': []
            }
        },
        'data': analytics
    }
    con.Pass('\033[F\t\tDONE\tBUILD ANALYTICS')

    return ws_content


def BuildWorksheetCharts(data):
    con.Info('\t\tLOAD:\tBUILD CHARTS')
    ws_content = {
        'name': 'Charts',
        'config': {
            'general': {
                'add_headers': False
            },
            'columns': [],
            'rows': {
                'colors': []
            }
        },
        'data': []
    }
    con.Pass('\033[F\t\tDONE\tBUILD CHARTS')

    return ws_content


def BuildWorksheetFindingsSimple(data):
    con.Info('\t\tLOAD:\tFORMAT FINDINGS')
    project_findings_flat = []

    for row in data:
        project_findings_flat.append([
            row['id'],
            row['severity']['name'],
            row['simpleDetectionType'],
            row['descriptor']['name'],
            ' - '.join(row['results'][0]['toolHierarchy'][1:3])
        ])
    con.Pass('\033[F\t\tDONE\tFORMAT FINDINGS')

    con.Info('\t\tLOAD:\tBUILD WORKSHEET')
    ws_content = {
        'name': 'Findings',
        'config': {
            'general': {
                'add_headers': True
            },
            'columns': [
                {
                    'label': 'id',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                },
                {
                    'label': 'severity',
                    'size': 0,
                    'filter': True,
                    'is_link': False
                },
                {
                    'label': 'type',
                    'size': 0,
                    'filter': True,
                    'is_link': False
                },
                {
                    'label': 'label',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                },
                {
                    'label': 'desc_path',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                }
            ],
            'rows': {
                'colors': []
            }
        },
        'data': project_findings_flat
    }
    con.Pass('\033[F\t\tDONE\tBUILD WORKSHEET')

    con.Info('\t\tLOAD:\tDEFINE COLORS')

    # Color headers row gray
    ws_content['config']['rows']['colors'].append(
        {
            'row_num': 0,
            'color_hex': 'd4d4d4'
        }
    )
    # Color data row based on severity
    for i, finding in enumerate(ws_content['data'], start = 1):
        set_color = 'ffffff' # white

        severity_field_index = 1

        if (finding[severity_field_index] == 'Critical'):
            set_color = '9c0e1a' # dark red
        elif (finding[severity_field_index] == 'High'):
            set_color = 'f54842' # red
        elif (finding[severity_field_index] == 'Medium'):
            set_color = 'f57842' # orange
        elif (finding[severity_field_index] == 'Low'):
            set_color = 'f5d142' # yellow

        ws_content['config']['rows']['colors'].append(
            {
                'row_num': i,
                'color_hex': set_color
            }
        )

    con.Pass('\033[F\t\tDONE\tDEFINE COLORS')

    return ws_content


def BuildWorksheetFindingsDetailed(config, data):
    con.Info('\t\tLOAD:\tFORMAT FINDINGS')
    project_findings_flat = []

    for row in data:
        project_findings_flat.append([
            config['hosts']['srm'] + '/projects/' + str(row['projectId']) + '/findings/' + str(row['id']),
            row['id'],
            row['severity']['name'],
            row['simpleDetectionType'],
            row['results'][0]['tool'],
            row['descriptor']['name'],
            row['firstSeenOn'],
            ' - '.join(row['results'][0]['toolHierarchy'])
        ])
    con.Pass('\033[F\t\tDONE\tFORMAT FINDINGS')

    con.Info('\t\tLOAD:\tBUILD WORKSHEET')
    ws_content = {
        'name': 'Findings',
        'config': {
            'general': {
                'add_headers': True
            },
            'columns': [
                {
                    'label': 'link',
                    'size': 30,
                    'filter': False,
                    'is_link': True
                },
                {
                    'label': 'id',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                },
                {
                    'label': 'severity',
                    'size': 0,
                    'filter': True,
                    'is_link': False
                },
                {
                    'label': 'type',
                    'size': 0,
                    'filter': True,
                    'is_link': False
                },
                {
                    'label': 'tool',
                    'size': 0,
                    'filter': True,
                    'is_link': False
                },
                {
                    'label': 'label',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                },
                {
                    'label': 'firstSeenOn',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                },
                {
                    'label': 'desc_path',
                    'size': 0,
                    'filter': False,
                    'is_link': False
                }
            ],
            'rows': {
                'colors': []
            }
        },
        'data': project_findings_flat
    }
    con.Pass('\033[F\t\tDONE\tBUILD WORKSHEET')

    con.Info('\t\tLOAD:\tDEFINE COLORS')

    # Color headers row gray
    ws_content['config']['rows']['colors'].append(
        {
            'row_num': 0,
            'color_hex': 'd4d4d4'
        }
    )
    # Color data row based on severity
    for i, finding in enumerate(ws_content['data'], start = 1):
        set_color = 'ffffff' # white

        severity_field_index = 2

        if (finding[severity_field_index] == 'Critical'):
            set_color = '9c0e1a' # dark red
        elif (finding[severity_field_index] == 'High'):
            set_color = 'f54842' # red
        elif (finding[severity_field_index] == 'Medium'):
            set_color = 'f57842' # orange
        elif (finding[severity_field_index] == 'Low'):
            set_color = 'f5d142' # yellow

        ws_content['config']['rows']['colors'].append(
            {
                'row_num': i,
                'color_hex': set_color
            }
        )

    con.Pass('\033[F\t\tDONE\tDEFINE COLORS')

    return ws_content


def BuildReports(config, ws_list_build, project_findings):
    ws_list_completed = []

    if ('charts' in ws_list_build):
        ws_list_completed.append(BuildWorksheetCharts(project_findings))

    if ('analytics' in ws_list_build):
        ws_list_completed.append(BuildWorksheetAnalytics(project_findings))

    if ('findings_simple' in ws_list_build):
        ws_list_completed.append(BuildWorksheetFindingsSimple(project_findings))

    if ('findings_detailed' in ws_list_build):
        ws_list_completed.append(BuildWorksheetFindingsDetailed(config, project_findings))

    return ws_list_completed