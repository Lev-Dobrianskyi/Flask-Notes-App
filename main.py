from flask import Flask, render_template, request, redirect, url_for
import Database as database

app = Flask(__name__)
app.json.ensure_ascii = False


@app.route('/')
def index():
    # Сортування приходить з адреси: /?sort=date&order=desc
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    notes = database.get_all_notes(sort_by=sort_by, descending=(order == 'desc'))
    return render_template('index.html', notes=notes, sort=sort_by, order=order)


@app.route('/note/<int:note_id>')
def note_page(note_id):
    note = database.get_note(note_id)
    return render_template('note.html', note=note)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add_note.html', error='', header='', text='')

    header = request.form['header'].strip()
    text = request.form['text'].strip()

    if header == '':
        return render_template('add_note.html', error='Заголовок не може бути порожнім',
                               header=header, text=text)

    note_id = database.add_note(header, text)
    return redirect(url_for('note_page', note_id=note_id))


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = database.get_note(note_id)
    if note is None:
        return render_template('edit_note.html', note=None, error='', header='', text='')

    if request.method == 'GET':
        return render_template('edit_note.html', note=note, error='',
                               header=note['header'], text=note['text'])

    header = request.form['header'].strip()
    text = request.form['text'].strip()

    if header == '':
        return render_template('edit_note.html', note=note, error='Заголовок не може бути порожнім',
                               header=header, text=text)

    database.update_note(note_id, header, text)
    return redirect(url_for('note_page', note_id=note_id))


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    database.delete_note(note_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
