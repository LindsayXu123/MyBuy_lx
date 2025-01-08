from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = "my_secret_key"

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@app.route('/')
def index():
    return render_template('index.html', page = 'index')

@app.route('/spending', methods=['GET', 'POST'])
def spending():
    if 'spending_data' not in session:
        session['spending_data'] = {}
        for month in MONTHS:
            session['spending_data'][month] = []

    if request.method == 'POST':
        if request.form.get('reset-spend') == 'true':
            for month in session['spending_data']:
                session['spending_data'][month].clear()
            session.modified = True
        else:
            month = request.form.get('month')
            if month in session['spending_data']:
                if 'amount' in request.form and 'description' in request.form:
                    try:
                        amount = float(request.form['amount'])
                        description = request.form['description']
                        if len(description) <= 50:
                            session['spending_data'][month].append({'amount': amount, 'description': description})
                            session.modified = True
                    except ValueError:
                        pass
                elif 'delete_index' in request.form:
                    try:
                        delete_index = int(request.form['delete_index'])
                        if 0 <= delete_index < len(session['spending_data'][month]):
                            session['spending_data'][month].pop(delete_index)
                            session.modified = True
                    except ValueError:
                        pass

    totals = {}
    for month in MONTHS:
        month_total = 0
        for entry in session['spending_data'][month]:
            month_total += entry['amount']
        totals[month] = month_total
    
    total_all_months = sum(totals.values())

    return render_template(
        'index.html', page='spending', spending_data=session['spending_data'], totals=totals, MONTHS=MONTHS,
        total_all_months=total_all_months
    )

@app.route('/items', methods=['GET', 'POST'])
def items():
    if 'checklist_items' not in session:
        session['checklist_items'] = []

    if request.method == 'POST':
        if 'new_item' in request.form:
            new_item = request.form['new_item']
            if new_item.strip():
                session['checklist_items'].append({'task': new_item, 'done': False})
                session.modified = True
        elif 'toggle' in request.form:
            try:
                toggle = int(request.form['toggle'])
                if 0 <= toggle < len(session['checklist_items']):
                    session['checklist_items'][toggle]['done'] = not session['checklist_items'][toggle]['done']
                    session.modified = True
            except ValueError:
                pass
        elif 'delete_index' in request.form:
            try:
                delete_index = int(request.form['delete_index'])
                if 0 <= delete_index < len(session['checklist_items']):
                    session['checklist_items'].pop(delete_index)
                    session.modified = True
            except ValueError:
                pass

    return render_template(
        'index.html',
        page='items',
        checklist_items=session['checklist_items']
    )

@app.route('/notes', methods = ['GET', 'POST'])
def notes():
    user_input = ''
    if request.method == 'POST':
        user_input = request.form['user_input']
    return render_template('index.html', page = 'notes')

@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'budget_data' not in session:
        session['budget_data'] = {}
        for month in MONTHS:
            session['budget_data'][month] = 0

    if request.method == 'POST':
        if request.form.get('reset-budget') == 'true':
            session['budget_data'] = {}
            for month in MONTHS:
                session['budget_data'][month] = 0
            session.modified = True
        else:
            month = request.form.get('month')
            try:
                budget_amount = float(request.form.get('budget_amount', 0))
                session['budget_data'][month] = budget_amount
                session.modified = True
            except ValueError:
                pass

    total_budget = sum(session['budget_data'].values())

    sorted_budget_data = {}
    for month in MONTHS:
        sorted_budget_data[month] = session['budget_data'][month]

    return render_template('index.html', page = 'budget', budget_data = sorted_budget_data, months = MONTHS, total_budget = total_budget)

@app.route('/summary')
def summary():
    return render_template('index.html', page = 'summary')

if __name__ == "__main__":
    app.run(debug=True)