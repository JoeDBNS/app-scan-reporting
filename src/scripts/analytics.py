def BuildAnalytics(results):
    analytics_build = {
        'totals': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'dynamic': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'static': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        },
        'component': {
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
    }

    for row in results:
        analytics_build[row[3]][row[2]] += 1

    analytics_build['totals']['High'] = analytics_build['dynamic']['High'] + analytics_build['static']['High'] + analytics_build['component']['High']
    analytics_build['totals']['Medium'] = analytics_build['dynamic']['Medium'] + analytics_build['static']['Medium'] + analytics_build['component']['Medium']
    analytics_build['totals']['Low'] = analytics_build['dynamic']['Low'] + analytics_build['static']['Low'] + analytics_build['component']['Low']

    analytics = [
        ['Totals'],
        ['', 'High', analytics_build['totals']['High']],
        ['', 'Medium', analytics_build['totals']['Medium']],
        ['', 'Low', analytics_build['totals']['Low']],
        ['Scan Types'],
        ['', 'Dynamic'],
        ['', '', 'High', analytics_build['dynamic']['High']],
        ['', '', 'Medium', analytics_build['dynamic']['Medium']],
        ['', '', 'Low', analytics_build['dynamic']['Low']],
        ['', 'Static'],
        ['', '', 'High', analytics_build['static']['High']],
        ['', '', 'Medium', analytics_build['static']['Medium']],
        ['', '', 'Low', analytics_build['static']['Low']],
        ['', 'Component'],
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

    return ws_content
