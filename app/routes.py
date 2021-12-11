from flask import render_template, flash, redirect, request, url_for
import re
from app import app
from .forms import ConfigForm
from .szolanc_logic import Szolanc

max_word_length = 25
grouped = {}


@app.route('/')
def root():
    return render_template('results.html', title='Home', scores=grouped,
                           letters='letters')


@app.route('/results/<letter_draw>/')
def index(letter_draw):
    return render_template('results.html', title='Home', scores=grouped,
                           letters=letter_draw)


@app.route('/config', methods=['GET', 'POST'])
def config():
    form = ConfigForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            game = Szolanc(form.language.data)
            letter_draw = []
            if form.own_letterset.data:
                form.own_letterset.data = re.sub(r'\W+', '', form.own_letterset.data).lower()
                for character in form.own_letterset.data:
                    letter_draw += [character]
                game.hand.update_hand(letter_draw)
            else:
                letter_draw = game.hand.held_letters
            print('Letters drawn: {}'.format(letter_draw))
            flash('Letters: {}'.format(letter_draw))
            valid_words = game.word_check(letter_draw, max_word_length)
            global grouped
            grouped = {}
            if valid_words != 'NONE':
                scores = game.score_calc(valid_words)
                grouped = game.group_by_score(scores)
            else:
                grouped = {0: 'Number of valid words found'}
            return redirect(url_for('index', letter_draw=''.join(letter_draw)))
    return render_template('config.html', title='Configuration', form=form)
