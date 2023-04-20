const $form = $('form')
const $htmlTimer = $('#timer')
const $htmlScore = $('#score')
const $htmlHS = $('#high-score')
const $words = $('ul')
const $guess = $('#guess')

class Game{
    constructor(time){
        this.time = time
        this.gameOver = false
        this.totalScore = 0
        this.timer = setInterval(this.countDown.bind(this), 1000)
    }
    async handleGuess(guess){
        if(this.gameOver){
            return alert('The game is over and your guess was denied')
        }
        if(guess !== ''){
            const response = await axios.get('/guess', {params: {guess}})
            const result = response.data.result
            const score = response.data.score
            switch (result) {
                case 'ok':
                    this.totalScore += score
                    $htmlScore.text(`Score: ${this.totalScore}`)
                    const $newWord = $('<li>')
                    $newWord.text(`${guess}`)
                    $words.append($newWord)
                    break;
                case 'not-word':
                    alert('Please input a valid word')
                    break;
                case 'not-on-board':
                    alert('Your guess could not be found on this board')
                    break;
                case 'already-found':
                    alert('This word was already found. Please input another word')
                    break;
                default:
                    break;
            }
        }
    }
    async handleGameOver(){
        this.gameOver = true
        const resp = await axios.post('/game-over', { score: this.totalScore })
        alert(`Game over. this is your final score: ${this.totalScore}`)
    }
    async countDown(){
        this.time --
        $htmlTimer.text(`Time Remaining: ${this.time} Seconds`)
        if(this.time === 0){
            clearInterval(this.timer)
            await this.handleGameOver()
        }
    }
}

boggle = new Game(60)
alert('You will have 60 seconds to find as many words as you can. Longer words are worth more')


$form.on('submit', async function(evt){
    evt.preventDefault()
    guess = $guess.val()
    response = await axios.get('/guess', {params: {guess}})
    await boggle.handleGuess(guess)
    $guess.val('')
})