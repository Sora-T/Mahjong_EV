from flask import Flask, render_template, request

app = Flask(__name__)


def calculate_break_even_position(prizes, entry_fee, chip):
    prizes_with_chip = [prize + chip for prize in prizes]
    prizes_with_fee_and_chip = [prize - entry_fee for prize in prizes_with_chip]
    prizes_with_fee_and_chip[0] -= entry_fee * (len(prizes) - 1)
    
    total = sum(prizes_with_fee_and_chip)
    if total >= 0:
        return 1.0
    
    cumulative_sum = 0
    for i in range(len(prizes_with_fee_and_chip)):
        prev_sum = cumulative_sum
        cumulative_sum += prizes_with_fee_and_chip[i]
        if cumulative_sum >= 0:
            if prizes_with_fee_and_chip[i] != 0:
                return i + 1 + (-prev_sum) / prizes_with_fee_and_chip[i]
            else:
                return i + 1
    
    return "収支±0になる順位はありません"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        prizes = [
            int(request.form['prize1']),
            int(request.form['prize2']),
            int(request.form['prize3']),
            int(request.form['prize4'])
        ]
        entry_fee = int(request.form['entry_fee'])
        chip_value = int(request.form['chip_value'])
        
        result = []
        for chip_count in range(1, 11):
            chip = chip_value * chip_count
            position = calculate_break_even_position(prizes, entry_fee, chip)
            if isinstance(position, (int, float)):
                result.append(f"+{chip_count}枚なら平均着順 {position:.2f}位 で±0")
            else:
                result.append(f"+{chip_count}枚なら {position}")
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

'''
'''