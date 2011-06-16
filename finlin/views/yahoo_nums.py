#negative net income uses ()
def remove_parens(elem):
    if elem.find("(") is not -1:
        elem = elem.strip("()")
        elem = '-%s' % elem
    return elem

def make_usable(x):
    for key in x:
        x[key].reverse()
        if key == 'dates':
            x[key] = [datetime.datetime.strptime(elem, "%b %d, %Y") for elem in x[key]]
        elif key == 'rev':
            x[key] = [locale.atof(elem) for elem in x[key]] 
        elif key =='net':
            x[key] = [locale.atof(remove_parens(elem)) for elem in x[key] ]
    return x 

def percent_change(Vpresent, Vpast):
    percent = (Vpresent-Vpast)/Vpast*100
    percent = round(percent, 2)
    return percent

 
def change_quarterly(x):
    growth = {}
    for key in x:
        if key is not 'dates':
            first  = x[key][0]
            second = x[key][1]
            third  = x[key][2]
            fourth = x[key][3]

            yr_chg = percent_change(fourth, first)
            qtr_chg = percent_change(fourth, third) 
            growth[key] = {'qtr_chg': qtr_chg, 'yr_chg':yr_chg}
    return growth

#@view_config(name='', context='finlin.models.Company', 
#             renderer='finlin:templates/company/homepage.pt' )
def company_homepage(context, request):
    
    context.data['competitive_advantage_summary'] = markdown(context.data['competitive_advantage_summary'])
    context.data['growth_strategy_summary'] = markdown(context.data['growth_strategy_summary'])
    context.data['overview'] = markdown(context.data['overview'])
    #quarterly 
    q = {}
    q['dates'] = ['Dec 31, 2010', 'Sep 30, 2010', 'Jun 30, 2010', 'Mar 31, 2010']
    q['rev'] = ['36,585', '35,782', '36,027', '36,009']
    q['net'] = ['(4,066)', '(4,814)', '(1,646)', '(774)'] 
    #annually
    a = {}
    a['dates'] = ['Jun 30, 2010', 'Jun 30, 2009', 'Jun 30, 2008']
    a['rev'] = ['143,007', '136,827', '115,619']
    a['net'] = ['(3,969)', '(4,461)', '(18,882)']

    q = make_usable(q)

    q['exp'] = [i-j for i,j in zip(q['rev'], q['net'])]

    context.growth = change_quarterly(q)
    q['dates'] =  [datetime.datetime.strftime(elem, "%b %d, %Y") for elem in q['dates']]

    conv = locale.localeconv()  # get map of conventions
    locale.LC_MONETARY
    conv['frac_digits'] = 0
    conv['n_sign_posn'] = 0
    q['rev'] = [ locale.format("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], elem), grouping=True) 
        for elem in q['rev'] ] 
    
    q['net'] = [locale.format("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], elem), grouping=True) 
        for elem in q['net'] ]

    q['exp'] = [locale.format("%s%.*f", (conv['currency_symbol'], conv['frac_digits'], elem), grouping=True) 
        for elem in q['exp'] ]


    context.q = q

    return {
        'main': get_renderer('finlin:templates/master.pt').implementation(),
        'company_layout': get_renderer('finlin:templates/company/master.pt').implementation(),
        }


