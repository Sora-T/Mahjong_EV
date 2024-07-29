from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_break_even_position(prizes, entry_fee, chip):
    prizes_with_chip = [prize + chip for prize in prizes]
    prizes_with_fee_and_chip = [prize - entry_fee for prize in prizes_with_chip]
    prizes_with_fee_and_chip[0] -= entry_fee * (len(prizes) - 1)
    
    break_even_position = None
    for i in range(len(prizes_with_fee_and_chip)):
        if prizes_with_fee_and_chip[i] >= 0:
            break_even_position = i + 1
            break
    
    return break_even_position if break_even_position is not None else "収支±0になる順位はありません"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prizes = [
            int(request.form['prize1']),
            int(request.form['prize2']),
            int(request.form['prize3']),
            int(request.form['prize4'])
        ]
        entry_fee = int(request.form['entry_fee'])
        chip = int(request.form['chip'])
        
        result = calculate_break_even_position(prizes, entry_fee, chip)
        return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)